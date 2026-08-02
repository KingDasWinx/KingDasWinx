import json
import re
import time
from datetime import date, datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "contributions.json"
URL = "https://github.com/users/KingDasWinx/contributions"


class ContributionParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.days: dict[str, dict[str, int | str]] = {}
        self.ids: dict[str, str] = {}
        self.tooltip_for: str | None = None
        self.tooltip_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "td" and "ContributionCalendar-day" in (values.get("class") or ""):
            day = values.get("data-date")
            node_id = values.get("id")
            if day:
                self.days[day] = {"date": day, "level": int(values.get("data-level") or 0), "count": 0}
                if node_id:
                    self.ids[node_id] = day
        elif tag == "tool-tip":
            self.tooltip_for = values.get("for")
            self.tooltip_text = []

    def handle_data(self, data: str) -> None:
        if self.tooltip_for:
            self.tooltip_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "tool-tip" or not self.tooltip_for:
            return
        day = self.ids.get(self.tooltip_for)
        match = re.search(r"([\d,]+) contributions?", " ".join(self.tooltip_text))
        if day and match:
            self.days[day]["count"] = int(match.group(1).replace(",", ""))
        self.tooltip_for = None
        self.tooltip_text = []


def streaks(days: list[dict[str, int | str]]) -> tuple[int, int]:
    counts = {datetime.strptime(str(day["date"]), "%Y-%m-%d").date(): int(day["count"]) for day in days}
    longest = running = 0
    for current in sorted(counts):
        running = running + 1 if counts[current] > 0 else 0
        longest = max(longest, running)

    cursor = min(date.today(), max(counts))
    if counts.get(cursor, 0) == 0:
        cursor -= timedelta(days=1)
    current_streak = 0
    while counts.get(cursor, 0) > 0:
        current_streak += 1
        cursor -= timedelta(days=1)
    return current_streak, longest


def main() -> None:
    request = Request(URL, headers={"User-Agent": "KingDasWinx-profile-readme"})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                html = response.read().decode("utf-8")
            break
        except URLError:
            if attempt == 2:
                raise
            time.sleep(3 * (attempt + 1))

    parser = ContributionParser()
    parser.feed(html)
    days = sorted(parser.days.values(), key=lambda item: str(item["date"]))
    if not days:
        raise RuntimeError("GitHub contribution calendar returned no days")

    current, longest = streaks(days)
    best = max(days, key=lambda item: int(item["count"]))
    payload = {
        "updated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "total": sum(int(day["count"]) for day in days),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best,
        "days": days,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

import json
from datetime import datetime, timedelta
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"
PALETTE = ["#161b22", "#6b2a0b", "#9a3412", "#c2410c", "#ea580c", "#fb923c"]
CELL = 11
GAP = 3
LEFT = 45
TOP = 54


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    days = payload["days"]
    dates = [datetime.strptime(day["date"], "%Y-%m-%d").date() for day in days]
    start = min(dates)
    start -= timedelta(days=(start.weekday() + 1) % 7)

    boxes = []
    labels = []
    seen_months: set[tuple[int, int]] = set()
    for day in days:
        current = datetime.strptime(day["date"], "%Y-%m-%d").date()
        offset = (current - start).days
        week, weekday = divmod(offset, 7)
        x = LEFT + week * (CELL + GAP)
        y = TOP + weekday * (CELL + GAP)
        level = min(5, int(day["level"]))
        delay = 80 + week * 10 + weekday * 16
        boxes.append(
            f'<rect class="day" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{PALETTE[level]}" style="animation-delay:{delay}ms"><title>{escape(str(day["date"]))}: {day["count"]} contributions</title></rect>'
        )
        month = (current.year, current.month)
        if current.day <= 7 and month not in seen_months:
            labels.append(f'<text class="axis" x="{x}" y="42">{current.strftime("%b")}</text>')
            seen_months.add(month)

    total = int(payload["total"])
    footer = f'{total:,} contributions · {payload["longest_streak"]}-day longest streak · updated daily'
    legend = "".join(
        f'<rect x="{685 + index * 18}" y="172" width="11" height="11" rx="2.5" fill="{color}"/>'
        for index, color in enumerate(PALETTE)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="205" viewBox="0 0 860 205" role="img" aria-labelledby="title desc">
  <title id="title">KingDasWinx GitHub contributions</title>
  <desc id="desc">Animated contribution calendar refreshed daily from public GitHub data.</desc>
  <style>
    text {{ font-family:ui-monospace,SFMono-Regular,Consolas,monospace }}
    .heading {{ fill:#e6edf3; font-size:14px; font-weight:700 }}
    .axis,.meta {{ fill:#8b949e; font-size:10px }}
    .day {{ opacity:0; animation:reveal .35s cubic-bezier(.16,1,.3,1) forwards }}
    @keyframes reveal {{ from {{ opacity:0; transform:translateY(7px) }} to {{ opacity:1; transform:none }} }}
    @media (prefers-reduced-motion:reduce) {{ .day {{ animation:none; opacity:1 }} }}
  </style>
  <rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#30363d"/>
  <text class="heading" x="24" y="27">contribution-calendar --live</text>
  {''.join(labels)}
  <text class="axis" x="21" y="77">Mon</text><text class="axis" x="21" y="105">Wed</text><text class="axis" x="21" y="133">Fri</text>
  {''.join(boxes)}
  <text class="meta" x="24" y="181">{escape(footer)}</text>
  <text class="meta" x="655" y="181">Less</text>{legend}<text class="meta" x="803" y="181">More</text>
</svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()

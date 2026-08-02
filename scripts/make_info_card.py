from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "info-card.svg"

LINES = [
    ("role", "Front-end Developer @ IotaHub"),
    ("work", "Angular · NestJS"),
    ("personal", "React · TypeScript · Rust · Python"),
    ("focus", "Web · Desktop · Mobile · Cloud · AI/CV"),
    ("study", "Software Engineering @ PUCPR"),
    ("projects", "28 public · 38 private"),
    ("building", "2+ years · 1,005+ contributions"),
    ("web", "kingdaswinx.com.br"),
]


def main() -> None:
    rows = []
    for index, (key, value) in enumerate(LINES):
        y = 96 + index * 34
        delay = 180 + index * 95
        rows.append(
            f'''<g class="line" style="animation-delay:{delay}ms">
      <text class="key" x="28" y="{y}">{escape(key):<12}</text>
      <text class="value" x="142" y="{y}">{escape(value)}</text>
    </g>'''
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="370" viewBox="0 0 500 370" role="img" aria-labelledby="title desc">
  <title id="title">João Moreira developer profile</title>
  <desc id="desc">A neofetch-inspired summary of work, studies, tools and projects.</desc>
  <style>
    text {{ font-family:ui-monospace,SFMono-Regular,Consolas,monospace }}
    .prompt {{ fill:#f97316; font-size:18px; font-weight:700 }}
    .key {{ fill:#f97316; font-size:14px; font-weight:700 }}
    .value {{ fill:#e6edf3; font-size:14px }}
    .line {{ opacity:0; animation:show .42s cubic-bezier(.16,1,.3,1) forwards }}
    @keyframes show {{ from {{ opacity:0; transform:translateY(7px) }} to {{ opacity:1; transform:none }} }}
    @media (prefers-reduced-motion:reduce) {{ .line {{ animation:none; opacity:1 }} }}
  </style>
  <rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#30363d"/>
  <text class="prompt" x="28" y="48">joao@github</text>
  <text class="value" x="164" y="48">~ $ neofetch</text>
  <path d="M28 66H472" stroke="#30363d"/>
  {''.join(rows)}
</svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()

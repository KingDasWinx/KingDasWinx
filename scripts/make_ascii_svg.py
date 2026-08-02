from html import escape
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "avatar.png"
OUTPUT = ROOT / "ascii-portrait.svg"
RAMP = "@%#*+=-:. "
COLS = 76
FONT_SIZE = 7.2
ROW_HEIGHT = 8.1


def main() -> None:
    image = Image.open(SOURCE).convert("L")
    image = ImageOps.autocontrast(image, cutoff=2)
    image = ImageEnhance.Contrast(image).enhance(1.2)

    mask = Image.new("L", image.size)
    from PIL import ImageDraw

    draw = ImageDraw.Draw(mask)
    width, height = image.size
    draw.ellipse((width * 0.06, -height * 0.04, width * 0.96, height * 1.08), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(width * 0.055))
    image = Image.composite(image, Image.new("L", image.size, 255), mask)

    rows = round(image.height / image.width * COLS * 0.53)
    image = image.resize((COLS, rows))
    pixels = list(image.get_flattened_data())
    lines = [
        "".join(RAMP[pixel * (len(RAMP) - 1) // 255] for pixel in pixels[start:start + COLS])
        for start in range(0, len(pixels), COLS)
    ]

    width_px = 350
    height_px = round(rows * ROW_HEIGHT + 34)
    text = []
    for index, line in enumerate(lines):
        y = 22 + index * ROW_HEIGHT
        delay = index * 38
        text.append(
            f'<text class="row" x="12" y="{y:.1f}" style="animation-delay:{delay}ms">{escape(line)}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width_px}" height="{height_px}" viewBox="0 0 {width_px} {height_px}" role="img" aria-labelledby="title desc">
  <title id="title">ASCII portrait of João Moreira</title>
  <desc id="desc">A monochrome portrait revealed line by line.</desc>
  <style>
    .row {{ fill:#e6edf3; font: {FONT_SIZE}px ui-monospace, SFMono-Regular, Consolas, monospace; white-space:pre; opacity:0; animation:print .45s cubic-bezier(.16,1,.3,1) forwards; }}
    @keyframes print {{ from {{ opacity:0; transform:translateX(-8px) }} to {{ opacity:1; transform:none }} }}
    @media (prefers-reduced-motion:reduce) {{ .row {{ animation:none; opacity:1 }} }}
  </style>
  <rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#30363d"/>
  {''.join(text)}
</svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()

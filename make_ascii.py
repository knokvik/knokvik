#!/usr/bin/env python3
"""Regenerate body-only ASCII portrait (background removed) into both SVGs."""
from pathlib import Path
from xml.sax.saxutils import escape
import re
from PIL import Image, ImageEnhance, ImageOps
from rembg import remove

COLS, ROWS = 42, 25
CHARS = " .:-=+*#%@"


def body_canvas(src_path="photo_full.png"):
    src = Image.open(src_path).convert("RGBA")
    cut = remove(src)
    cut.save("subject_only.png")
    bbox = cut.split()[-1].getbbox()
    if not bbox:
        raise SystemExit("no subject found")
    pad = 30
    x0, y0, x1, y1 = bbox
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(cut.width, x1 + pad), min(cut.height, y1 + pad)
    body = cut.crop((x0, y0, x1, y1))
    canvas = Image.new("RGBA", (420, 500), (0, 0, 0, 0))
    pw, ph = body.size
    scale = min(420 / pw, 500 / ph) * 0.98
    nw, nh = int(pw * scale), int(ph * scale)
    body = body.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(body, ((420 - nw) // 2, (500 - nh) // 2), body)
    canvas.save("subject_canvas.png")
    return canvas


def render(cut_rgba, invert_lum=False):
    im = cut_rgba.resize((COLS, ROWS), Image.Resampling.LANCZOS)
    gray = ImageEnhance.Contrast(
        ImageOps.autocontrast(im.convert("L"), cutoff=1)
    ).enhance(1.8)
    alpha = im.split()[-1]
    gp, ap = list(gray.getdata()), list(alpha.getdata())
    n = len(CHARS) - 1
    lines = []
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            i = y * COLS + x
            if ap[i] < 45:
                row.append(" ")
            else:
                p = 255 - gp[i] if invert_lum else gp[i]
                idx = max(1, int(round(p / 255 * n)))
                row.append(CHARS[idx])
        lines.append("".join(row))
    return lines


def inject(path, lines, fill):
    block_lines = [f'<text x="15" y="30" fill="{fill}" class="ascii">']
    for i, line in enumerate(lines):
        block_lines.append(
            f'<tspan x="15" y="{30 + i * 20}">{escape(line)}</tspan>'
        )
    block_lines.append("</text>")
    new_ascii = "\n".join(block_lines)
    svg = Path(path).read_text()
    svg2, n = re.subn(
        r'<text x="15" y="30"[^>]*class="ascii">.*?</text>',
        new_ascii,
        svg,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit(f"could not replace ascii block in {path}")
    Path(path).write_text(svg2)
    print("updated", path)


def main():
    canvas = body_canvas()
    dark = render(canvas, invert_lum=False)
    light = render(canvas, invert_lum=True)
    print("--- BODY ONLY (dark) ---")
    print("\n".join(dark))
    inject("dark_mode.svg", dark, "#c9d1d9")
    inject("light_mode.svg", light, "#24292f")


if __name__ == "__main__":
    main()

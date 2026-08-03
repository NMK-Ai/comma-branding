#!/usr/bin/env python3
import os
import sys

from PIL import Image

W, H = 1080, 2160
HEADER_SIZE = 0x4000
TRIM_THRESHOLD = 20
TRIM_PAD_PCT = 0.02
FILL_PCT = 0.96


def build_canvas(logo_path):
    logo = Image.open(logo_path)
    if logo.mode in ("RGBA", "LA", "P"):
        logo = logo.convert("RGBA")
        black = Image.new("RGBA", logo.size, (0, 0, 0, 255))
        logo = Image.alpha_composite(black, logo)
    logo = logo.convert("RGB")

    # trim the logo's own black padding, keep a small margin around the artwork
    mask = logo.convert("L").point(lambda p: 255 if p > TRIM_THRESHOLD else 0)
    bbox = mask.getbbox()
    if bbox:
        pad = int(max(logo.size) * TRIM_PAD_PCT)
        left = max(bbox[0] - pad, 0)
        top = max(bbox[1] - pad, 0)
        right = min(bbox[2] + pad, logo.size[0])
        bottom = min(bbox[3] + pad, logo.size[1])
        logo = logo.crop((left, top, right, bottom))
    lw, lh = logo.size

    # scale to fit inside the landscape view without cutting anything
    view_w, view_h = H, W
    scale = FILL_PCT * min(view_w / lw, view_h / lh)
    new_w, new_h = int(lw * scale), int(lh * scale)
    logo = logo.resize((new_w, new_h), Image.LANCZOS)

    canvas = Image.new("RGB", (view_w, view_h), (0, 0, 0))
    x = (view_w - new_w) // 2
    y = (view_h - new_h) // 2
    canvas.paste(logo, (x, y))

    stored = canvas.rotate(-90, expand=True)
    if stored.size != (W, H):
        stored = stored.resize((W, H))
    return stored


def main():
    if len(sys.argv) != 4:
        sys.exit(f"usage: {sys.argv[0]} <logo.png> <header_template.bin> <out.bin>")
    logo_path, header_path, out_path = sys.argv[1:4]

    canvas = build_canvas(logo_path)
    bmp_tmp = out_path + ".bmp.tmp"
    canvas.save(bmp_tmp, "BMP")

    with open(header_path, "rb") as f:
        header = f.read(HEADER_SIZE)
    if len(header) < HEADER_SIZE:
        header += b"\x00" * (HEADER_SIZE - len(header))

    with open(bmp_tmp, "rb") as f:
        bmp = f.read()
    os.remove(bmp_tmp)

    with open(out_path, "wb") as f:
        f.write(header)
        f.write(bmp)


if __name__ == "__main__":
    main()

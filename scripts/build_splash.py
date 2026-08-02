#!/usr/bin/env python3
import os
import sys

from PIL import Image

W, H = 1080, 2160
HEADER_SIZE = 0x4000
CROP_PCT = 0.15
SCALE = 1.6


def build_canvas(logo_path):
    logo = Image.open(logo_path).convert("RGB")
    lw, lh = logo.size
    crop_x = int(lw * CROP_PCT)
    logo = logo.crop((crop_x, 0, lw - crop_x, lh))
    lw, lh = logo.size
    new_w, new_h = int(lw * SCALE), int(lh * SCALE)
    logo = logo.resize((new_w, new_h), Image.LANCZOS)

    view_w, view_h = H, W
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

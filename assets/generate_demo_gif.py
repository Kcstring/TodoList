from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw


def draw_frame(size: int, t: float) -> Image.Image:
    img = Image.new("RGB", (size, size), (18, 19, 23))
    draw = ImageDraw.Draw(img)
    cx, cy = size / 2, size / 2

    core_r = size * 0.18
    glow_r = size * 0.28
    draw.ellipse(
        (cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r),
        fill=(32, 35, 42),
    )
    draw.ellipse((cx - core_r, cy - core_r, cx + core_r, cy + core_r), fill=(43, 47, 56))
    draw.ellipse(
        (cx - size * 0.06, cy - size * 0.06, cx + size * 0.06, cy + size * 0.06),
        fill=(241, 241, 239),
    )

    orbit_r = size * (0.33 + 0.02 * math.sin(t * 4.0))
    ring_box = (cx - orbit_r, cy - orbit_r, cx + orbit_r, cy + orbit_r)
    start = (t * 360.0) % 360
    draw.arc(ring_box, start=start, end=start + 250, fill=(120, 128, 142), width=3)

    for i in range(6):
        a = t * 2.4 * math.pi + i * (2 * math.pi / 6)
        px = cx + math.cos(a) * orbit_r
        py = cy + math.sin(a) * orbit_r
        rr = 3 + (i % 2)
        draw.ellipse((px - rr, py - rr, px + rr, py + rr), fill=(228, 230, 233))

    return img


def main() -> None:
    out = Path(__file__).resolve().parent / "demo.gif"
    size = 360
    frames = [draw_frame(size, i / 34.0) for i in range(34)]
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=45,
        loop=0,
        optimize=True,
    )
    print(f"Demo gif generated: {out}")


if __name__ == "__main__":
    main()

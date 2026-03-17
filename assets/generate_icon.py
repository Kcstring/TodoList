from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


def draw_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (18, 19, 23, 255))
    draw = ImageDraw.Draw(img)

    cx = size // 2
    cy = size // 2

    # Main dark core
    core_r = int(size * 0.26)
    draw.ellipse(
        (cx - core_r, cy - core_r, cx + core_r, cy + core_r),
        fill=(31, 35, 42, 255),
    )

    # Orbit ring
    orbit_r = int(size * 0.34)
    ring_w = max(2, size // 20)
    draw.arc(
        (cx - orbit_r, cy - orbit_r, cx + orbit_r, cy + orbit_r),
        start=24,
        end=332,
        fill=(110, 118, 132, 255),
        width=ring_w,
    )

    # Bright center point
    center_r = max(3, size // 14)
    draw.ellipse(
        (cx - center_r, cy - center_r, cx + center_r, cy + center_r),
        fill=(241, 241, 239, 255),
    )

    # Particles
    particles = [
        (-0.28, -0.16, 0.05, (216, 219, 224, 255)),
        (0.28, -0.21, 0.045, (168, 174, 184, 255)),
        (0.33, 0.10, 0.04, (136, 144, 158, 255)),
        (0.09, 0.30, 0.04, (197, 202, 211, 255)),
        (-0.29, 0.22, 0.035, (116, 124, 138, 255)),
    ]
    for rx, ry, rr, color in particles:
        px = int(cx + size * rx)
        py = int(cy + size * ry)
        pr = max(2, int(size * rr))
        draw.ellipse((px - pr, py - pr, px + pr, py + pr), fill=color)

    return img


def main() -> None:
    assets_dir = Path(__file__).resolve().parent
    icon_path = assets_dir / "todo.ico"

    base = draw_icon(256)
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    base.save(icon_path, format="ICO", sizes=sizes)
    print(f"Icon generated: {icon_path}")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), (14, 15, 19))
    draw = ImageDraw.Draw(img)

    # Background particles
    particles = [
        (140, 100, 6, (90, 98, 112)),
        (240, 160, 4, (120, 128, 142)),
        (1110, 90, 5, (105, 113, 127)),
        (1050, 200, 3, (140, 148, 160)),
        (1120, 640, 5, (90, 98, 112)),
    ]
    for x, y, r, color in particles:
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)

    # App window
    wx0, wy0, wx1, wy1 = 300, 70, 980, 650
    draw.rounded_rectangle((wx0, wy0, wx1, wy1), radius=26, fill=(20, 22, 27), outline=(48, 52, 60), width=2)

    # Header
    draw.rounded_rectangle((wx0 + 24, wy0 + 24, wx1 - 24, wy0 + 220), radius=20, fill=(28, 31, 37), outline=(52, 57, 66), width=2)
    draw.text((wx0 + 46, wy0 + 48), "今日待办", fill=(240, 241, 239), font=_font(42))
    draw.text((wx0 + 48, wy0 + 104), "今天：2026-03-18", fill=(162, 168, 178), font=_font(24))

    # Switch buttons
    draw.rounded_rectangle((wx0 + 44, wy0 + 145, wx0 + 290, wy0 + 198), radius=14, fill=(67, 75, 90))
    draw.rounded_rectangle((wx0 + 302, wy0 + 145, wx0 + 548, wy0 + 198), radius=14, fill=(39, 43, 51))
    draw.text((wx0 + 140, wy0 + 156), "今日", fill=(245, 246, 247), font=_font(24))
    draw.text((wx0 + 395, wy0 + 156), "明日", fill=(196, 201, 209), font=_font(24))

    # Input
    draw.rounded_rectangle((wx0 + 24, wy0 + 240, wx1 - 24, wy0 + 292), radius=14, fill=(28, 31, 37), outline=(48, 52, 60), width=2)
    draw.text((wx0 + 42, wy0 + 254), "输入任务，默认添加到当前标签...", fill=(130, 136, 146), font=_font(20))

    # Task list cards
    items = [
        ("完成产品文档 README", True),
        ("检查应用图标是否一致", False),
        ("录制并替换真实演示 GIF", False),
    ]
    y = wy0 + 315
    for text, done in items:
        draw.rounded_rectangle((wx0 + 30, y, wx1 - 30, y + 68), radius=14, fill=(28, 31, 37), outline=(48, 52, 60), width=2)
        cb = (wx0 + 48, y + 21, wx0 + 75, y + 48)
        draw.rounded_rectangle(cb, radius=5, fill=(112, 120, 133))
        if done:
            draw.line((wx0 + 55, y + 35, wx0 + 62, y + 42), fill=(248, 249, 250), width=3)
            draw.line((wx0 + 62, y + 42, wx0 + 70, y + 29), fill=(248, 249, 250), width=3)
            color = (146, 154, 167)
        else:
            color = (235, 237, 240)
        draw.text((wx0 + 92, y + 20), text, fill=color, font=_font(24))
        y += 82

    # Footer note
    draw.text((52, 660), "Tomorrow Todo - Dark Particle UI Showcase", fill=(146, 154, 167), font=_font(20))

    out = Path(__file__).resolve().parent / "ui-showcase.png"
    img.save(out)
    print(f"UI showcase generated: {out}")


if __name__ == "__main__":
    main()

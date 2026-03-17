from __future__ import annotations

import math
from pathlib import Path
import tkinter as tk
import customtkinter as ctk

from app.splash import SplashAnimation
from app.ui import TodoApp


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    data_file = base_dir / "data" / "tasks.json"

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    _apply_particle_window_icon(root)
    root.attributes("-alpha", 0.0)
    root.withdraw()

    def launch_main_ui() -> None:
        app = TodoApp(root, data_file)
        app.center_window()
        root.deiconify()
        root.after(80, app.center_window)
        root.after(220, app.center_window)
        _fade_in_root(root, start=0.0, end=1.0, duration_ms=260)

    SplashAnimation(root, on_complete=launch_main_ui)
    root.mainloop()


def _fade_in_root(
    root: ctk.CTk, start: float, end: float, duration_ms: int, step_ms: int = 16
) -> None:
    steps = max(1, duration_ms // step_ms)
    delta = (end - start) / steps
    state = {"value": start, "count": 0}

    def tick() -> None:
        state["value"] += delta
        state["count"] += 1
        root.attributes("-alpha", max(0.0, min(1.0, state["value"])))
        if state["count"] < steps:
            root.after(step_ms, tick)
        else:
            root.attributes("-alpha", end)

    tick()

def _apply_particle_window_icon(root: ctk.CTk) -> None:
    """
    生成黑色粒子风图标并应用到窗口，替换默认蓝色风格图标。
    """
    base_dir = Path(__file__).resolve().parent
    icon_path = base_dir / "assets" / "todo.ico"

    # Windows 标题栏左上角优先读取 .ico 文件。
    if icon_path.exists():
        try:
            root.iconbitmap(default=str(icon_path))
            return
        except tk.TclError:
            pass

    # 兜底：使用运行时生成图标（某些环境下不显示在标题栏，但可用于任务栏/窗口图标）。
    size = 64
    img = tk.PhotoImage(width=size, height=size)
    bg = "#121317"
    for x in range(size):
        img.put(bg, to=(x, 0, x + 1, size))

    def draw_circle(cx: int, cy: int, r: int, color: str) -> None:
        for x in range(cx - r, cx + r + 1):
            if x < 0 or x >= size:
                continue
            for y in range(cy - r, cy + r + 1):
                if y < 0 or y >= size:
                    continue
                if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= r * r:
                    img.put(color, (x, y))

    # Outer orbit
    for deg in range(0, 360, 4):
        rad = deg * 3.1415926 / 180
        x = int(32 + 18 * math.cos(rad))
        y = int(32 + 18 * math.sin(rad))
        if 0 <= x < size and 0 <= y < size:
            img.put("#4f5562", (x, y))

    # Core and particles
    draw_circle(32, 32, 11, "#2b2f37")
    draw_circle(32, 32, 6, "#f1f1ef")
    draw_circle(18, 25, 2, "#d7d9dd")
    draw_circle(46, 21, 2, "#9aa2ad")
    draw_circle(50, 39, 2, "#7f8794")
    draw_circle(22, 47, 2, "#b7bcc5")
    draw_circle(14, 36, 1, "#8e95a0")

    root._particle_icon = img  # keep reference
    root.iconphoto(True, img)


if __name__ == "__main__":
    main()

from __future__ import annotations

import math
import time
import tkinter as tk
from typing import Callable

from app.window_utils import center_on_primary_workarea


class SplashAnimation:
    def __init__(self, root: tk.Tk, on_complete: Callable[[], None]) -> None:
        self.root = root
        self.on_complete = on_complete

        self.width = 360
        self.height = 360
        self.cx = self.width / 2
        self.cy = self.height / 2

        self.bg = "#141518"
        self.dot = "#f1f1ef"
        self.muted = "#8b9099"
        self.accent = "#9ca3af"

        self.total_ms = 2400
        self.handoff_ms = 260
        self.handoff_done = False
        self.start_ts = time.perf_counter()

        self.win = tk.Toplevel(root)
        self.win.overrideredirect(True)
        self.win.configure(bg=self.bg)
        self.win.attributes("-topmost", True)
        self.win.attributes("-alpha", 0.0)
        try:
            self.win.attributes("-transparentcolor", self.bg)
        except tk.TclError:
            pass
        self._center_window()

        self.canvas = tk.Canvas(
            self.win,
            width=self.width,
            height=self.height,
            bg=self.bg,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.particles = []
        for i in range(10):
            angle = (math.pi * 2 / 10) * i
            self.particles.append(
                {"angle": angle, "speed": 0.045 + 0.005 * (i % 4), "seed": i % 3}
            )

        self._tick()

    def _center_window(self) -> None:
        center_on_primary_workarea(self.win, self.width, self.height)

    @staticmethod
    def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
        return max(low, min(high, value))

    @staticmethod
    def _ease_out_cubic(x: float) -> float:
        x = SplashAnimation._clamp(x)
        return 1 - pow(1 - x, 3)

    @staticmethod
    def _ease_out_back(x: float) -> float:
        x = SplashAnimation._clamp(x)
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * pow(x - 1, 3) + c1 * pow(x - 1, 2)

    def _draw_core(self, t: float) -> None:
        p = self._ease_out_cubic(t / 560)
        r = 2 + 24 * p
        self.canvas.create_oval(
            self.cx - r * 1.6,
            self.cy - r * 1.6,
            self.cx + r * 1.6,
            self.cy + r * 1.6,
            fill="#1f2228",
            outline="",
        )
        self.canvas.create_oval(
            self.cx - r,
            self.cy - r,
            self.cx + r,
            self.cy + r,
            fill=self.dot,
            outline="",
        )

    def _draw_rotation(self, t: float) -> None:
        p = self._clamp((t - 420) / 1200)
        if p <= 0:
            return

        rot = self._ease_out_cubic(p) * math.tau * 2.15
        ring_r = 44 + 12 * math.sin(10 * p)
        arc_r = ring_r + 24

        self.canvas.create_arc(
            self.cx - arc_r,
            self.cy - arc_r,
            self.cx + arc_r,
            self.cy + arc_r,
            start=math.degrees(rot),
            extent=235,
            style="arc",
            outline=self.accent,
            width=3,
        )

        for i in range(6):
            a = rot + i * (math.tau / 6)
            x = self.cx + math.cos(a) * ring_r
            y = self.cy + math.sin(a) * ring_r
            rr = 4 + (i % 2)
            self.canvas.create_oval(x - rr, y - rr, x + rr, y + rr, fill=self.dot, outline="")

        particle_p = self._clamp((t - 650) / 1200)
        if particle_p > 0:
            for p_item in self.particles:
                d = 22 + particle_p * 120 * p_item["speed"] * 10
                a = rot * 0.7 + p_item["angle"]
                x = self.cx + math.cos(a) * d
                y = self.cy + math.sin(a) * d
                rr = 1.5 + p_item["seed"] * 0.6
                self.canvas.create_oval(
                    x - rr,
                    y - rr,
                    x + rr,
                    y + rr,
                    fill=self.muted,
                    outline="",
                )

    def _draw_zoom(self, t: float) -> None:
        p = self._clamp((t - 1320) / 900)
        if p <= 0:
            return
        z = self._ease_out_back(p)
        rr = 76 + 120 * z
        alpha_like = 1.0 - p * 0.85
        line_w = max(1, int(4 - p * 3))
        color = "#d0d3d8" if alpha_like > 0.5 else "#8b9099"
        self.canvas.create_oval(
            self.cx - rr,
            self.cy - rr,
            self.cx + rr,
            self.cy + rr,
            outline=color,
            width=line_w,
        )
        title_size = 12 + int(8 * self._ease_out_cubic(p))
        self.canvas.create_text(
            self.cx,
            self.cy + 92,
            text="Tomorrow Todo",
            fill=self.dot,
            font=("Segoe UI Semibold", title_size),
        )

    def _update_window_alpha(self, t: float) -> None:
        if t <= 240:
            alpha = t / 240
        elif t >= self.total_ms - 260:
            alpha = max(0.0, (self.total_ms - t) / 260)
        else:
            alpha = 1.0
        self.win.attributes("-alpha", alpha)

    def _tick(self) -> None:
        t = (time.perf_counter() - self.start_ts) * 1000
        if not self.handoff_done and t >= self.total_ms - self.handoff_ms:
            self.handoff_done = True
            self.on_complete()
        if t >= self.total_ms:
            self.win.destroy()
            return

        self.canvas.delete("all")
        self._draw_core(t)
        self._draw_rotation(t)
        self._draw_zoom(t)
        self._update_window_alpha(t)
        self.win.after(16, self._tick)

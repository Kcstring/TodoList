from __future__ import annotations

import ctypes
from ctypes import wintypes
import tkinter as tk


def center_on_primary_workarea(window: tk.Misc, width: int, height: int) -> None:
    """
    Center window on Windows primary work area (taskbar-aware).
    """
    try:
        user32 = ctypes.windll.user32

        class RECT(ctypes.Structure):
            _fields_ = [
                ("left", wintypes.LONG),
                ("top", wintypes.LONG),
                ("right", wintypes.LONG),
                ("bottom", wintypes.LONG),
            ]

        rect = RECT()
        SPI_GETWORKAREA = 0x0030
        if not user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0):
            raise OSError("SystemParametersInfoW failed")

        x = int(rect.left + ((rect.right - rect.left) - width) / 2)
        y = int(rect.top + ((rect.bottom - rect.top) - height) / 2)
    except Exception:
        window.update_idletasks()
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = int((sw - width) / 2)
        y = int((sh - height) / 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

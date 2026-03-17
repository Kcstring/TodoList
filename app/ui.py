from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont

import customtkinter as ctk

from app.storage import load_tasks, save_tasks
from app.window_utils import center_on_primary_workarea


class TodoApp:
    def __init__(self, root: ctk.CTk, data_file: Path) -> None:
        self.root = root
        self.data_file = data_file
        self.all_tasks = load_tasks(self.data_file)
        self.current_view = "today"

        self.root.title("Tomorrow Todo")
        self.root.geometry("500x590")
        self.root.minsize(440, 500)
        self.root.configure(fg_color="#141518")

        self.color_bg = "#141518"
        self.color_card = "#1c1f24"
        self.color_text = "#f1f1ef"
        self.color_muted = "#99a0aa"
        self.color_line = "#2c3138"
        self.color_hover = "#242931"
        self.color_accent = "#707885"

        self.font_family = self._pick_font_family()
        self.title_font = ctk.CTkFont(family=self.font_family, size=22, weight="bold")
        self.sub_font = ctk.CTkFont(family=self.font_family, size=13)
        self.task_font = ctk.CTkFont(family=self.font_family, size=14)
        self.task_font_done = ctk.CTkFont(
            family=self.font_family, size=14, overstrike=True
        )
        self.switch_font = ctk.CTkFont(family=self.font_family, size=16, weight="bold")

        self._build_header()
        self._build_input()
        self._build_task_area()
        self._build_actions()
        self.render_tasks()
        self.center_window()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(
            self.root,
            corner_radius=14,
            fg_color=self.color_card,
            border_width=1,
            border_color=self.color_line,
        )
        header.pack(fill="x", padx=16, pady=(16, 8))

        today = datetime.now().strftime("%Y-%m-%d")
        self.title_label = ctk.CTkLabel(
            header,
            text="今日待办",
            font=self.title_font,
            anchor="w",
            text_color=self.color_text,
        )
        self.title_label.pack(fill="x", padx=14, pady=(12, 2))

        ctk.CTkLabel(
            header,
            text=f"今天：{today}",
            font=self.sub_font,
            text_color=self.color_muted,
            anchor="w",
        ).pack(fill="x", padx=14)

        self.progress_label = ctk.CTkLabel(
            header,
            text="完成进度：0/0",
            font=self.sub_font,
            text_color=self.color_muted,
            anchor="w",
        )
        self.progress_label.pack(fill="x", padx=14, pady=(2, 6))

        divider = ctk.CTkFrame(header, height=1, fg_color=self.color_line, corner_radius=0)
        divider.pack(fill="x", padx=14, pady=(0, 10))
        self._build_day_switch(header)
        self._build_particle_strip(header)

    def _build_day_switch(self, parent: ctk.CTkFrame) -> None:
        switch_row = ctk.CTkFrame(parent, fg_color="transparent")
        switch_row.pack(fill="x", padx=12, pady=(0, 8))

        self.today_btn = ctk.CTkButton(
            switch_row,
            text="今日",
            height=44,
            corner_radius=12,
            font=self.switch_font,
            command=lambda: self.switch_view("today"),
        )
        self.today_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.tomorrow_btn = ctk.CTkButton(
            switch_row,
            text="明日",
            height=44,
            corner_radius=12,
            font=self.switch_font,
            command=lambda: self.switch_view("tomorrow"),
        )
        self.tomorrow_btn.pack(side="right", fill="x", expand=True, padx=(6, 0))
        self._apply_switch_style()

    def _build_particle_strip(self, parent: ctk.CTkFrame) -> None:
        strip = tk.Canvas(
            parent, width=240, height=30, bg=self.color_card, highlightthickness=0, bd=0
        )
        strip.pack(anchor="w", padx=12, pady=(0, 10))

        cx, cy = 56, 15
        strip.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, outline="#727987", width=2)
        strip.create_arc(
            cx - 17,
            cy - 17,
            cx + 17,
            cy + 17,
            start=20,
            extent=220,
            style="arc",
            outline="#4f5562",
            width=2,
        )
        dots = [
            (24, 15, 2.8, "#f1f1ef"),
            (88, 14, 2.2, "#d7d9dd"),
            (109, 13, 1.8, "#8e95a0"),
            (128, 16, 1.6, "#7f8794"),
            (145, 12, 1.4, "#6f7785"),
            (160, 17, 1.2, "#636b78"),
            (176, 15, 1.1, "#59616f"),
        ]
        for x, y, r, color in dots:
            strip.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")

    def _build_input(self) -> None:
        input_row = ctk.CTkFrame(self.root, fg_color="transparent")
        input_row.pack(fill="x", padx=16, pady=(2, 8))

        self.task_entry = ctk.CTkEntry(
            input_row,
            placeholder_text="输入任务，默认添加到当前标签...",
            height=40,
            corner_radius=14,
            fg_color=self.color_card,
            border_color=self.color_line,
            text_color=self.color_text,
            placeholder_text_color=self.color_muted,
        )
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.task_entry.bind("<Return>", self.add_task_by_enter)

        ctk.CTkButton(
            input_row,
            text="添加",
            width=86,
            height=40,
            corner_radius=14,
            fg_color="#2e333b",
            hover_color="#3a404a",
            text_color="#ffffff",
            command=self.add_task,
        ).pack(side="right")

    def _build_task_area(self) -> None:
        self.task_scroll = ctk.CTkScrollableFrame(
            self.root,
            corner_radius=14,
            fg_color=self.color_card,
            border_width=1,
            border_color=self.color_line,
        )
        self.task_scroll.pack(fill="both", expand=True, padx=16, pady=(2, 8))

    def _build_actions(self) -> None:
        action_row = ctk.CTkFrame(self.root, fg_color="transparent")
        action_row.pack(fill="x", padx=16, pady=(0, 14))

        ctk.CTkButton(
            action_row,
            text="删除已完成",
            fg_color=self.color_card,
            hover_color=self.color_hover,
            text_color=self.color_text,
            border_width=1,
            border_color=self.color_line,
            corner_radius=12,
            command=self.remove_completed,
        ).pack(side="left")

        ctk.CTkButton(
            action_row,
            text="全部重置",
            fg_color=self.color_card,
            hover_color=self.color_hover,
            text_color=self.color_text,
            border_width=1,
            border_color=self.color_line,
            corner_radius=12,
            command=self.reset_all_pending,
        ).pack(side="right")

    def _pick_font_family(self) -> str:
        candidates = [
            "Arial Rounded MT Bold",
            "Nunito",
            "Quicksand",
            "Segoe UI",
            "Microsoft YaHei UI",
        ]
        try:
            available = set(tkfont.families())
            for family in candidates:
                if family in available:
                    return family
        except tk.TclError:
            pass
        return "Segoe UI"

    def add_task_by_enter(self, _event) -> None:
        self.add_task()

    def add_task(self) -> None:
        text = self.task_entry.get().strip()
        if not text:
            messagebox.showinfo("提示", "请输入任务内容。")
            return
        self.all_tasks.append(
            {"text": text, "done": False, "plan_date": self._current_plan_date()}
        )
        save_tasks(self.data_file, self.all_tasks)
        self.task_entry.delete(0, "end")
        self.render_tasks()

    def toggle_task(self, index: int, var: tk.BooleanVar) -> None:
        self.all_tasks[index]["done"] = bool(var.get())
        save_tasks(self.data_file, self.all_tasks)
        self.render_tasks()

    def remove_completed(self) -> None:
        selected_date = self._current_plan_date()
        self.all_tasks = [
            task
            for task in self.all_tasks
            if not (task.get("plan_date") == selected_date and task.get("done", False))
        ]
        save_tasks(self.data_file, self.all_tasks)
        self.render_tasks()

    def reset_all_pending(self) -> None:
        selected_date = self._current_plan_date()
        for task in self.all_tasks:
            if task.get("plan_date") == selected_date:
                task["done"] = False
        save_tasks(self.data_file, self.all_tasks)
        self.render_tasks()

    def render_tasks(self) -> None:
        for child in self.task_scroll.winfo_children():
            child.destroy()

        self._apply_switch_style()
        self.title_label.configure(text=("今日待办" if self.current_view == "today" else "明日待办"))

        visible_indices = [
            idx
            for idx, task in enumerate(self.all_tasks)
            if task.get("plan_date") == self._current_plan_date()
        ]
        visible_tasks = [self.all_tasks[idx] for idx in visible_indices]

        total = len(visible_tasks)
        done = sum(1 for task in visible_tasks if task.get("done", False))
        self.progress_label.configure(text=f"完成进度：{done}/{total}")

        if not visible_tasks:
            empty_card = ctk.CTkFrame(
                self.task_scroll,
                corner_radius=12,
                fg_color=self.color_card,
                border_width=1,
                border_color=self.color_line,
            )
            empty_card.pack(fill="x", padx=4, pady=6)
            ctk.CTkLabel(
                empty_card,
                text="当前没有任务，先添加一条吧。",
                text_color=self.color_muted,
                font=self.sub_font,
            ).pack(anchor="w", padx=14, pady=14)
            return

        for visible_idx, task in enumerate(visible_tasks):
            index = visible_indices[visible_idx]
            row = ctk.CTkFrame(
                self.task_scroll,
                corner_radius=14,
                fg_color=self.color_card,
                border_width=1,
                border_color=self.color_line,
            )
            row.pack(fill="x", padx=4, pady=6)

            done_var = tk.BooleanVar(value=task.get("done", False))
            ctk.CTkCheckBox(
                row,
                text=task.get("text", ""),
                variable=done_var,
                onvalue=True,
                offvalue=False,
                font=(self.task_font_done if done_var.get() else self.task_font),
                text_color=(self.color_muted if done_var.get() else self.color_text),
                fg_color=self.color_accent,
                hover_color="#7e8796",
                border_color="#7c8491",
                checkmark_color="#ffffff",
                command=lambda i=index, v=done_var: self.toggle_task(i, v),
            ).pack(fill="x", padx=14, pady=12)

    def switch_view(self, view: str) -> None:
        self.current_view = view
        self.render_tasks()

    def _apply_switch_style(self) -> None:
        if self.current_view == "today":
            self.today_btn.configure(fg_color="#3e4550", hover_color="#4b535f")
            self.tomorrow_btn.configure(fg_color="#2a2f36", hover_color="#343b45")
        else:
            self.today_btn.configure(fg_color="#2a2f36", hover_color="#343b45")
            self.tomorrow_btn.configure(fg_color="#3e4550", hover_color="#4b535f")

    def _current_plan_date(self) -> str:
        today = datetime.now().date()
        if self.current_view == "tomorrow":
            return (today + timedelta(days=1)).isoformat()
        return today.isoformat()

    def center_window(self) -> None:
        self.root.attributes("-fullscreen", False)
        self.root.state("normal")
        center_on_primary_workarea(self.root, width=500, height=590)

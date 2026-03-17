from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any, Dict, List


def ensure_data_file(data_file: Path) -> None:
    data_file.parent.mkdir(parents=True, exist_ok=True)
    if not data_file.exists():
        data_file.write_text(
            json.dumps({"tasks": []}, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def load_tasks(data_file: Path) -> List[Dict[str, Any]]:
    ensure_data_file(data_file)
    try:
        raw = json.loads(data_file.read_text(encoding="utf-8"))
        tasks = raw.get("tasks", [])
        if isinstance(tasks, list):
            return _normalize_tasks(tasks)
    except (json.JSONDecodeError, OSError):
        pass
    return []


def save_tasks(data_file: Path, tasks: List[Dict[str, Any]]) -> None:
    ensure_data_file(data_file)
    data_file.write_text(
        json.dumps({"tasks": tasks}, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _normalize_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    today = date.today().isoformat()
    normalized: List[Dict[str, Any]] = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
        text = str(task.get("text", "")).strip()
        if not text:
            continue
        normalized.append(
            {
                "text": text,
                "done": bool(task.get("done", False)),
                "plan_date": str(task.get("plan_date", today)),
            }
        )
    return normalized

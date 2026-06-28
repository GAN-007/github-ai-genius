from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class StateRecord:
    key: str
    value: dict[str, Any]


class ProjectStateStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load_all(self) -> dict[str, dict[str, Any]]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding='utf-8'))

    def save(self, key: str, value: dict[str, Any]) -> None:
        data = self.load_all()
        data[key] = value
        self.path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding='utf-8')

    def load(self, key: str) -> StateRecord | None:
        data = self.load_all()
        if key not in data:
            return None
        return StateRecord(key=key, value=data[key])

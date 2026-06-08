from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from .models import RepoFile


@dataclass(slots=True)
class SearchHit:
    path: str
    snippet: str
    score: float


class CodeIndex:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _init_schema(self) -> None:
        with self.connect() as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS files (path TEXT PRIMARY KEY, sha TEXT, size INTEGER, language TEXT, content TEXT)')
            conn.execute('CREATE VIRTUAL TABLE IF NOT EXISTS file_search USING fts5(path, content)')
            conn.commit()

    def reset(self) -> None:
        with self.connect() as conn:
            conn.execute('DELETE FROM files')
            conn.execute('DELETE FROM file_search')
            conn.commit()

    def add_files(self, files: list[RepoFile], languages: dict[str, str] | None = None) -> None:
        with self.connect() as conn:
            for file in files:
                if file.content is None:
                    continue
                language = languages.get(file.path, '') if languages else ''
                conn.execute('INSERT OR REPLACE INTO files(path, sha, size, language, content) VALUES (?, ?, ?, ?, ?)', (file.path, file.sha, file.size, language, file.content))
                conn.execute('INSERT INTO file_search(path, content) VALUES (?, ?)', (file.path, file.content))
            conn.commit()

    def search(self, query: str, limit: int = 20) -> list[SearchHit]:
        with self.connect() as conn:
            rows = conn.execute('SELECT path, snippet(file_search, 1, "[", "]", "...", 16), rank FROM file_search WHERE file_search MATCH ? ORDER BY rank LIMIT ?', (query, limit)).fetchall()
        return [SearchHit(path=row[0], snippet=row[1], score=float(row[2])) for row in rows]

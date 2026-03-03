from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

SearchMode = Literal["local", "global", "hybrid", "naive", "mix", "bypass"]


@dataclass(slots=True)
class MemoryItem:
    id: str
    document: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MemoryDeleteResult:
    id: str
    deleted: bool


@dataclass(slots=True)
class SearchResult:
    id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    score: float = 0.0


@dataclass(slots=True)
class SearchResponse:
    query: str
    results: List[SearchResult] = field(default_factory=list)


class RagPlugError(RuntimeError):
    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code

from __future__ import annotations

from typing import Any, Dict, List

from ragplug.types import (
    MemoryDeleteResult,
    MemoryItem,
    RagPlugError,
    SearchResponse,
    SearchResult,
)


class _ResponseParser:
    @staticmethod
    def _ensure_dict(data: Any, endpoint: str) -> Dict[str, Any]:
        if not isinstance(data, dict):
            raise RagPlugError(f"Unexpected {endpoint} response format")
        return data

    @staticmethod
    def version(data: Any) -> str:
        payload = _ResponseParser._ensure_dict(data, "/version")
        version_value = payload.get("version")
        if version_value is None:
            raise RagPlugError("Unexpected /version response format")
        return str(version_value)

    @staticmethod
    def memory_item(data: Any) -> MemoryItem:
        payload = _ResponseParser._ensure_dict(data, "/memory")
        return MemoryItem(
            id=str(payload.get("id", "")),
            document=payload.get("document") if isinstance(payload.get("document"), dict) else {},
        )

    @staticmethod
    def memory_delete(data: Any, item_id: str) -> MemoryDeleteResult:
        payload = _ResponseParser._ensure_dict(data, "/memory/{memory_name}/{item_id}")
        return MemoryDeleteResult(
            id=str(payload.get("id", item_id)),
            deleted=bool(payload.get("deleted", False)),
        )

    @staticmethod
    def search(data: Any) -> SearchResponse:
        payload = _ResponseParser._ensure_dict(data, "/search/{memory_name}")
        raw_results = payload.get("results")
        results: List[SearchResult] = []

        if isinstance(raw_results, list):
            for row in raw_results:
                if not isinstance(row, dict):
                    continue
                results.append(
                    SearchResult(
                        id=str(row.get("id", "")),
                        text=str(row.get("text", "")),
                        metadata=row.get("metadata") if isinstance(row.get("metadata"), dict) else {},
                        score=float(row.get("score", 0.0) or 0.0),
                    )
                )

        return SearchResponse(query=str(payload.get("query", "")), results=results)

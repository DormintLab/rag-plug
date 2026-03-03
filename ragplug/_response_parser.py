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
    def version(data: Dict[str, Any]) -> str:
        version_value = data.get("version")
        if version_value is None:
            raise RagPlugError("Unexpected /version response format")
        return str(version_value)

    @staticmethod
    def memory_item(data: Dict[str, Any]) -> MemoryItem:
        return MemoryItem(
            id=str(data.get("id", "")),
            text=str(data.get("text", "")),
            metadata=data.get("metadata") if isinstance(data.get("metadata"), dict) else {},
        )

    @staticmethod
    def memory_delete(data: Dict[str, Any], item_id: str) -> MemoryDeleteResult:
        return MemoryDeleteResult(
            id=str(data.get("id", item_id)),
            deleted=bool(data.get("deleted", False)),
        )

    @staticmethod
    def search(data: Dict[str, Any]) -> SearchResponse:
        raw_results = data.get("results")
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

        return SearchResponse(query=str(data.get("query", "")), results=results)

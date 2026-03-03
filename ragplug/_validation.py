from __future__ import annotations

from typing import Optional


class _Validator:
    @staticmethod
    def require_non_empty(value: str, name: str) -> str:
        if not value or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")
        return value

    @staticmethod
    def validate_top_k(top_k: int) -> int:
        if top_k < 1 or top_k > 50:
            raise ValueError("top_k must be between 1 and 50")
        return top_k

    @staticmethod
    def resolve_memory_name(memory_name: Optional[str], default_memory_name: Optional[str]) -> str:
        name = memory_name or default_memory_name
        if not name or not name.strip():
            raise ValueError("memory_name is required (or set default_memory_name in RagPlug)")
        return name

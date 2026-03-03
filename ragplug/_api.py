from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ragplug._transport import _HttpTransport


class _RagPlugApi:
    def __init__(self, transport: _HttpTransport) -> None:
        self._transport = transport

    @staticmethod
    def _segment(value: str) -> str:
        return quote(value, safe="")

    def version(self) -> Dict[str, Any]:
        return self._transport.request_json("GET", "/version")

    async def aversion(self) -> Dict[str, Any]:
        return await self._transport.arequest_json("GET", "/version")

    def add_memory(self, memory_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = f"/memory/{self._segment(memory_name)}"
        return self._transport.request_json("POST", path, payload=payload)

    async def aadd_memory(self, memory_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = f"/memory/{self._segment(memory_name)}"
        return await self._transport.arequest_json("POST", path, payload=payload)

    def memory_schema(self, memory_name: str) -> Dict[str, Any]:
        path = f"/memory/{self._segment(memory_name)}/schema"
        return self._transport.request_json("GET", path)

    async def amemory_schema(self, memory_name: str) -> Dict[str, Any]:
        path = f"/memory/{self._segment(memory_name)}/schema"
        return await self._transport.arequest_json("GET", path)

    def delete_memory(self, memory_name: str, item_id: str) -> Dict[str, Any]:
        path = f"/memory/{self._segment(memory_name)}/{self._segment(item_id)}"
        return self._transport.request_json("DELETE", path)

    async def adelete_memory(self, memory_name: str, item_id: str) -> Dict[str, Any]:
        path = f"/memory/{self._segment(memory_name)}/{self._segment(item_id)}"
        return await self._transport.arequest_json("DELETE", path)

    def search_memory(self, memory_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = f"/search/{self._segment(memory_name)}"
        return self._transport.request_json("POST", path, payload=payload)

    async def asearch_memory(self, memory_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = f"/search/{self._segment(memory_name)}"
        return await self._transport.arequest_json("POST", path, payload=payload)

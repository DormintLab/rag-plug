from __future__ import annotations

from typing import Any, Dict, Optional

from ragplug._api import _RagPlugApi
from ragplug._response_parser import _ResponseParser
from ragplug._transport import _HttpTransport
from ragplug._validation import _Validator
from ragplug.types import MemoryDeleteResult, MemoryItem, SearchResponse


class RagPlug:
    endpoint_url = "https://api-ragplug.dormint.io"

    def __init__(
        self,
        api_key: str,
        endpoint_url: Optional[str] = None,
        default_memory_name: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key
        self.endpoint_url = (endpoint_url or self.endpoint_url).rstrip("/")
        self.default_memory_name = default_memory_name
        self.timeout = timeout

        self._transport = _HttpTransport(
            endpoint_url=self.endpoint_url,
            api_key=self.api_key,
            timeout=self.timeout,
        )
        self._api = _RagPlugApi(self._transport)

    def _memory_name(self, memory_name: Optional[str]) -> str:
        return _Validator.resolve_memory_name(memory_name, self.default_memory_name)

    def version(self) -> str:
        data = self._api.version()
        return _ResponseParser.version(data)

    async def aversion(self) -> str:
        data = await self._api.aversion()
        return _ResponseParser.version(data)

    def add(
        self,
        text: str,
        memory_name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        item_id: Optional[str] = None,
    ) -> MemoryItem:
        _Validator.require_non_empty(text, "text")
        resolved_memory_name = self._memory_name(memory_name)

        payload: Dict[str, Any] = {
            "text": text,
            "metadata": metadata or {},
            "id": item_id,
        }
        data = self._api.add_memory(resolved_memory_name, payload)
        return _ResponseParser.memory_item(data)

    async def aadd(
        self,
        text: str,
        memory_name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        item_id: Optional[str] = None,
    ) -> MemoryItem:
        _Validator.require_non_empty(text, "text")
        resolved_memory_name = self._memory_name(memory_name)

        payload: Dict[str, Any] = {
            "text": text,
            "metadata": metadata or {},
            "id": item_id,
        }
        data = await self._api.aadd_memory(resolved_memory_name, payload)
        return _ResponseParser.memory_item(data)

    def delete(self, item_id: str, memory_name: Optional[str] = None) -> MemoryDeleteResult:
        _Validator.require_non_empty(item_id, "item_id")
        resolved_memory_name = self._memory_name(memory_name)

        data = self._api.delete_memory(resolved_memory_name, item_id)
        return _ResponseParser.memory_delete(data, item_id)

    async def adelete(self, item_id: str, memory_name: Optional[str] = None) -> MemoryDeleteResult:
        _Validator.require_non_empty(item_id, "item_id")
        resolved_memory_name = self._memory_name(memory_name)

        data = await self._api.adelete_memory(resolved_memory_name, item_id)
        return _ResponseParser.memory_delete(data, item_id)

    def search(
        self,
        query: str,
        top_k: int = 5,
        memory_name: Optional[str] = None,
    ) -> SearchResponse:
        _Validator.require_non_empty(query, "query")
        _Validator.validate_top_k(top_k)
        resolved_memory_name = self._memory_name(memory_name)

        payload = {"query": query, "top_k": top_k}
        data = self._api.search_memory(resolved_memory_name, payload)
        return _ResponseParser.search(data)

    async def asearch(
        self,
        query: str,
        top_k: int = 5,
        memory_name: Optional[str] = None,
    ) -> SearchResponse:
        _Validator.require_non_empty(query, "query")
        _Validator.validate_top_k(top_k)
        resolved_memory_name = self._memory_name(memory_name)

        payload = {"query": query, "top_k": top_k}
        data = await self._api.asearch_memory(resolved_memory_name, payload)
        return _ResponseParser.search(data)

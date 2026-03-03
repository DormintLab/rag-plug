from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from ragplug._error_handler import _ErrorHandler


class _HttpTransport:
    def __init__(self, endpoint_url: str, api_key: str, timeout: float) -> None:
        self.endpoint_url = endpoint_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _url(self, path: str) -> str:
        return f"{self.endpoint_url}{path}"

    def request_json(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            with httpx.Client(timeout=self.timeout, headers=self.headers) as client:
                response = client.request(method, self._url(path), json=payload)
        except httpx.RequestError as error:
            _ErrorHandler.raise_network_error(error)

        _ErrorHandler.raise_for_http_error(response)
        return _ErrorHandler.parse_json_dict(response)

    async def arequest_json(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
                response = await client.request(method, self._url(path), json=payload)
        except httpx.RequestError as error:
            _ErrorHandler.raise_network_error(error)

        _ErrorHandler.raise_for_http_error(response)
        return _ErrorHandler.parse_json_dict(response)

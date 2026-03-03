from __future__ import annotations

from typing import Any

import httpx

from ragplug.types import RagPlugError


class _ErrorHandler:
    @staticmethod
    def raise_for_http_error(response: httpx.Response) -> None:
        if response.is_success:
            return

        detail = None
        try:
            payload = response.json()
            if isinstance(payload, dict):
                detail = payload.get("detail")
        except ValueError:
            detail = None

        message = str(detail) if detail else response.text.strip() or "Request failed"
        raise RagPlugError(message=message, status_code=response.status_code)

    @staticmethod
    def raise_network_error(error: httpx.RequestError) -> None:
        raise RagPlugError(f"Network error: {error}") from error

    @staticmethod
    def parse_json_response(response: httpx.Response) -> Any:
        try:
            data = response.json()
        except ValueError as error:
            raise RagPlugError(
                "Invalid JSON response",
                status_code=response.status_code,
            ) from error

        return data

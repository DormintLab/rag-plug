from __future__ import annotations

import asyncio
import os

from ragplug import RagPlug


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


async def main() -> None:
    api_key = require_env("API_KEY")
    memory_name = require_env("MEMORY_NAME")

    client = RagPlug(api_key=api_key, default_memory_name=memory_name)

    item = await client.aadd(
        document={
            "text": "Async example memory",
            "source": "examples/async_usage.py",
        },
    )
    print(f"Added: {item.id}")

    response = await client.asearch(
        query="Async example",
        field_name="text",
        top_k=3,
    )
    for row in response.results:
        print(f"{row.id} | score={row.score:.4f} | text={row.text}")

    deleted = await client.adelete(item.id)
    print(f"Deleted: id={deleted.id}, deleted={deleted.deleted}")


if __name__ == "__main__":
    asyncio.run(main())

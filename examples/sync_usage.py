from __future__ import annotations

import os

from ragplug import RagPlug


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    api_key = require_env("API_KEY")
    memory_name = require_env("MEMORY_NAME")

    client = RagPlug(api_key=api_key, default_memory_name=memory_name)

    item = client.add(
        text="Paris is the capital of France",
        metadata={"source": "examples/sync_usage.py"},
    )
    print(f"Added: {item.id}")

    response = client.search(query="capital of France", top_k=3)
    for row in response.results:
        print(f"{row.id} | score={row.score:.4f} | text={row.text}")

    deleted = client.delete(item.id)
    print(f"Deleted: id={deleted.id}, deleted={deleted.deleted}")


if __name__ == "__main__":
    main()

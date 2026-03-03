# rag-plug

Python client for the RAGPlug backend API.
It supports adding memory items, semantic search, and deleting items by ID (sync and async).

## Features
- `RagPlug` client with typed response models.
- API key authentication through `X-API-Key`.
- Operations scoped to a target memory (`memory_name`).
- Ready-to-run Python examples in `examples/`.
- CLI helper scripts for quick add/search flows.

## Requirements
- Python `3.10+`
- [Poetry](https://python-poetry.org/) (recommended)

## Installation
```bash
poetry install
```

For local editable install with pip:
```bash
pip install -e .
```

## Configuration
Create a `.env` file in the project root:

```env
API_KEY=your_api_key
MEMORY_NAME=your_memory_name
```

`.env` is already listed in `.gitignore` and should not be committed.

## Python Usage
```python
from ragplug import RagPlug

client = RagPlug(api_key="YOUR_API_KEY", default_memory_name="main")

item = client.add(
    "Paris is the capital of France",
    metadata={"source": "docs"},
)

response = client.search("capital of France", top_k=3)
client.delete(item.id)
```

Async usage:
```python
import asyncio
from ragplug import RagPlug


async def main() -> None:
    client = RagPlug(api_key="YOUR_API_KEY", default_memory_name="main")
    item = await client.aadd("Async memory text")
    response = await client.asearch("Async memory", top_k=3)
    await client.adelete(item.id)
    print(response.results)


asyncio.run(main())
```

## Examples
The repository includes runnable examples:

- `examples/sync_usage.py`
- `examples/async_usage.py`

Run them with:
```bash
set -a; source .env; set +a

poetry run python examples/sync_usage.py
poetry run python examples/async_usage.py
```

## CLI Scripts
- `scripts/add_memory.py`
- `scripts/search.py`

Example:
```bash
set -a; source .env; set +a

poetry run python scripts/add_memory.py \
  --api-key "$API_KEY" \
  --memory-name "$MEMORY_NAME" \
  --text "Smoke test memory" \
  --metadata '{"source":"scripts"}'

poetry run python scripts/search.py \
  --api-key "$API_KEY" \
  --memory-name "$MEMORY_NAME" \
  --query "Smoke test" \
  --top-k 5
```

## Development Commands
```bash
poetry check
poetry build
poetry run python -m compileall ragplug scripts examples
```

If you use Taskfile:
```bash
task all
```

## Release
CI publishes to PyPI for tags matching `v*`.
The tag must match the package version in `pyproject.toml`.

Example:
```bash
poetry version patch
git tag v$(poetry version -s)
git push origin --tags
```

## Project Structure
- `ragplug/client.py`: public `RagPlug` facade.
- `ragplug/types.py`: response models and `RagPlugError`.
- `ragplug/_api.py`, `_transport.py`, `_error_handler.py`, `_validation.py`, `_response_parser.py`: internal client layers.
- `examples/`: sync/async usage examples.
- `scripts/`: CLI utilities.

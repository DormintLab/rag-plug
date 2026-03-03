from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ragplug import RagPlug, RagPlugError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add a memory item to RAGPlug backend.")
    parser.add_argument("--api-key", required=True, help="API key for backend authentication.")
    parser.add_argument("--memory-name", required=True, help="Memory name from backend path.")
    parser.add_argument(
        "--document",
        required=True,
        help='JSON object with document fields. Example: {"text":"Hello","source":"docs"}',
    )
    parser.add_argument("--item-id", default=None, help="Optional custom item id.")
    parser.add_argument("--endpoint-url", default=None, help="Optional backend URL override.")
    return parser.parse_args()


def parse_document(raw: str) -> Dict[str, Any]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid document JSON: {error}") from error

    if not isinstance(payload, dict):
        raise ValueError("document must be a JSON object")
    return payload


def main() -> int:
    args = parse_args()

    try:
        document = parse_document(args.document)
        client = RagPlug(api_key=args.api_key, endpoint_url=args.endpoint_url)
        item = client.add(
            document=document,
            memory_name=args.memory_name,
            item_id=args.item_id,
        )
    except (RagPlugError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "id": item.id,
                "document": item.document,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

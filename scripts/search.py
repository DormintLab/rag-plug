from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ragplug import RagPlug, RagPlugError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search memory in RAGPlug backend.")
    parser.add_argument("--api-key", required=True, help="API key for backend authentication.")
    parser.add_argument("--memory-name", required=True, help="Memory name from backend path.")
    parser.add_argument("--query", required=True, help="Search query string.")
    parser.add_argument("--field-name", required=True, help="Indexed field name to search.")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results (1..50).")
    parser.add_argument(
        "--mode",
        default="naive",
        choices=["local", "global", "hybrid", "naive", "mix", "bypass"],
        help="Search mode.",
    )
    parser.add_argument(
        "--enable-rerank",
        action="store_true",
        help="Enable reranker in backend search.",
    )
    parser.add_argument("--endpoint-url", default=None, help="Optional backend URL override.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        client = RagPlug(api_key=args.api_key, endpoint_url=args.endpoint_url)
        response = client.search(
            query=args.query,
            field_name=args.field_name,
            top_k=args.top_k,
            mode=args.mode,
            enable_rerank=args.enable_rerank,
            memory_name=args.memory_name,
        )
    except (RagPlugError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    payload = {
        "query": response.query,
        "results": [
            {
                "id": row.id,
                "text": row.text,
                "metadata": row.metadata,
                "score": row.score,
            }
            for row in response.results
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

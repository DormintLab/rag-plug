# rag-plug

Python-клиент для backend RAGPlug API.
Поддерживает добавление памяти, семантический поиск и удаление записей по ID (sync/async).

## Возможности
- `RagPlug` с типизированными моделями ответов.
- Аутентификация через `X-API-Key`.
- Операции в рамках конкретной памяти (`memory_name`).
- Готовые CLI-скрипты для быстрого add/search.

## Требования
- Python `3.10+`
- [Poetry](https://python-poetry.org/) (рекомендуется)

## Установка
```bash
poetry install
```

Или через pip (локальная разработка):
```bash
pip install -e .
```

## Конфигурация
Создайте `.env` в корне проекта:

```env
API_KEY=your_api_key
MEMORY_NAME=your_memory_name
```

`.env` добавлен в `.gitignore` и не должен попадать в репозиторий.

## Использование в Python
```python
from ragplug import RagPlug

client = RagPlug(api_key="YOUR_API_KEY", default_memory_name="main")

item = client.add("Paris is the capital of France", metadata={"source": "docs"})
result = client.search("capital of France", top_k=3)
client.delete(item.id)
```

Async-пример:
```python
import asyncio
from ragplug import RagPlug

async def main():
    client = RagPlug(api_key="YOUR_API_KEY", default_memory_name="main")
    await client.aadd("Async memory text")
    res = await client.asearch("Async memory")
    print(res.results)

asyncio.run(main())
```

## CLI-скрипты
- `scripts/add_memory.py`
- `scripts/search.py`

Пример запуска:
```bash
set -a; source .env; set +a

python scripts/add_memory.py \
  --api-key "$API_KEY" \
  --memory-name "$MEMORY_NAME" \
  --text "Smoke test memory" \
  --metadata '{"source":"scripts"}'

python scripts/search.py \
  --api-key "$API_KEY" \
  --memory-name "$MEMORY_NAME" \
  --query "Smoke test" \
  --top-k 5
```

## Команды разработки
```bash
poetry check        # проверка метаданных пакета
poetry build        # сборка sdist + wheel
python -m compileall ragplug scripts
```

## Релиз
CI публикует пакет в PyPI по тегам `v*`.
Тег должен совпадать с версией в `pyproject.toml`.

Пример:
```bash
poetry version patch
git tag v$(poetry version -s)
git push origin --tags
```

## Структура проекта
- `ragplug/client.py`: публичный фасад `RagPlug`.
- `ragplug/types.py`: модели ответов и `RagPlugError`.
- `ragplug/_api.py`, `_transport.py`, `_error_handler.py`, `_validation.py`, `_response_parser.py`: внутренние слои клиента.
- `scripts/`: CLI-утилиты.

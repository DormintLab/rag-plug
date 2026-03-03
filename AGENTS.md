# Repository Guidelines

## Project Structure & Module Organization
This repository is a small Python package managed with Poetry.

- `ragplug/`: main package code.
- `ragplug/client.py`: core client class (`RagPlug`) and public methods.
- `ragplug/__init__.py`: package exports (currently minimal).
- `.github/workflows/release.yml`: tag-based build and PyPI publish workflow.
- `poetry.toml`, `pyproject.toml`, `poetry.lock`: dependency and build configuration.
- `rag-logo.png`: project asset.

Add new modules under `ragplug/` and keep public API entry points explicit in `__init__.py` when needed.

## Build, Test, and Development Commands
Use Poetry for all local workflows.

- `poetry install`: install dependencies in the virtual environment.
- `poetry check`: validate project metadata (also run in CI).
- `poetry build`: build source and wheel distributions.
- `poetry run python -c "from ragplug.client import RagPlug; print(RagPlug)"`: quick import smoke test.
- `poetry version patch` (or `minor`/`major`): bump package version before tagging a release.

CI publishes only when pushing tags matching `v*` and requires `tag == v$(poetry version -s)`.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation.
- Use type hints for public methods and payload structures.
- Use `snake_case` for functions/variables, `PascalCase` for classes, and clear method names (`search`, `add`, `asearch`, `aadd`).
- Keep methods focused; prefer small, composable helpers over large monolithic functions.

No formatter/linter is configured yet; if you add one, use it consistently and document the command here.

## Testing Guidelines
There is no test suite committed yet. New features should include tests.

- Preferred location: `tests/` mirroring package structure (example: `tests/test_client.py`).
- Preferred framework: `pytest`.
- Run tests with: `poetry run pytest`.
- Cover both sync and async code paths for client behavior.

## Commit & Pull Request Guidelines
Recent history is minimal (`initial commit`, `Add logo`, `update poetry`), so use clear, imperative commit subjects.

- Commit format: short subject (<=72 chars), optional body for context.
- PRs should include: summary, rationale, test evidence (or why tests are not present), and release impact.
- Link related issues and include API usage examples when behavior changes.

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import validate

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "packages" / "contracts" / "schemas"
EXAMPLE_DIR = ROOT / "packages" / "contracts" / "examples"


def main() -> None:
    failures: list[str] = []
    for schema_path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        base = schema_path.name.replace(".schema.json", "")
        example_path = EXAMPLE_DIR / f"{base}.json"
        if not example_path.exists():
            failures.append(f"missing example for schema: {schema_path.name}")
            continue

        with schema_path.open("r", encoding="utf-8") as f:
            schema = json.load(f)
        with example_path.open("r", encoding="utf-8") as f:
            example = json.load(f)

        try:
            validate(instance=example, schema=schema)
        except Exception as exc:
            failures.append(f"{base}: {exc}")

    if failures:
        raise SystemExit("\n".join(failures))

    print("all contract examples validated")


if __name__ == "__main__":
    main()

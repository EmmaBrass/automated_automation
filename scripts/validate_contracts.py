from __future__ import annotations

import json
import re
from pathlib import Path

from jsonschema import validate

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "packages" / "contracts" / "schemas"
EXAMPLE_DIR = ROOT / "packages" / "contracts" / "examples"
CHANGELOG_DIR = ROOT / "packages" / "contracts" / "changelog"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def _collect_contract_bases() -> tuple[set[str], set[str]]:
    schema_bases = {p.name.replace(".schema.json", "") for p in SCHEMA_DIR.glob("*.schema.json")}
    example_bases = {p.name.replace(".json", "") for p in EXAMPLE_DIR.glob("*.json")}
    return schema_bases, example_bases


def _validate_schema_example_parity(failures: list[str]) -> None:
    schema_bases, example_bases = _collect_contract_bases()
    for missing in sorted(schema_bases - example_bases):
        failures.append(f"missing example for schema: {missing}.schema.json")
    for orphan in sorted(example_bases - schema_bases):
        failures.append(f"missing schema for example: {orphan}.json")


def _validate_schema_metadata_and_changelog(schema_path: Path, failures: list[str]) -> None:
    base = schema_path.name.replace(".schema.json", "")
    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    version = schema.get("x-contract-version")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        failures.append(f"{base}: missing/invalid x-contract-version (expected SemVer)")
        return

    changelog_path = CHANGELOG_DIR / f"{base}.md"
    if not changelog_path.exists():
        failures.append(f"{base}: missing changelog file {changelog_path.name}")
        return

    changelog_text = changelog_path.read_text(encoding="utf-8")
    if f"## {version}" not in changelog_text:
        failures.append(f"{base}: changelog missing entry for schema version {version}")


def _validate_examples_against_schemas(failures: list[str]) -> None:
    for schema_path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        base = schema_path.name.replace(".schema.json", "")
        example_path = EXAMPLE_DIR / f"{base}.json"

        with schema_path.open("r", encoding="utf-8") as f:
            schema = json.load(f)
        with example_path.open("r", encoding="utf-8") as f:
            example = json.load(f)

        try:
            validate(instance=example, schema=schema)
        except Exception as exc:
            failures.append(f"{base}: {exc}")


def main() -> None:
    failures: list[str] = []
    _validate_schema_example_parity(failures)
    for schema_path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        _validate_schema_metadata_and_changelog(schema_path, failures)

    if failures:
        raise SystemExit("\n".join(sorted(failures)))

    data_failures: list[str] = []
    _validate_examples_against_schemas(data_failures)
    if data_failures:
        raise SystemExit("\n".join(sorted(data_failures)))

    print("all contract policies and examples validated")


if __name__ == "__main__":
    main()

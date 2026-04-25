from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "packages" / "contracts" / "schemas"
EXAMPLE_DIR = ROOT / "packages" / "contracts" / "examples"
CHANGELOG_DIR = ROOT / "packages" / "contracts" / "changelog"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def test_legacy_cli_agent_contract_name_removed_from_docs_tests_scripts() -> None:
    banned = "_".join(["cli", "agent", "execution", "contract"])
    targets = [ROOT / "docs", ROOT / "tests", ROOT / "scripts"]

    hits: list[str] = []
    for target in targets:
        for path in target.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if banned in text:
                hits.append(str(path.relative_to(ROOT)))

    assert hits == []


def test_schema_example_parity() -> None:
    schema_bases = {p.name.replace(".schema.json", "") for p in SCHEMA_DIR.glob("*.schema.json")}
    example_bases = {p.name.replace(".json", "") for p in EXAMPLE_DIR.glob("*.json")}
    assert schema_bases == example_bases


def test_schema_semver_and_changelog_entry() -> None:
    for schema_path in SCHEMA_DIR.glob("*.schema.json"):
        base = schema_path.name.replace(".schema.json", "")
        text = schema_path.read_text(encoding="utf-8")

        marker = '"x-contract-version": "'
        assert marker in text
        version = text.split(marker, 1)[1].split('"', 1)[0]
        assert SEMVER_RE.fullmatch(version)

        changelog_path = CHANGELOG_DIR / f"{base}.md"
        assert changelog_path.exists()
        changelog = changelog_path.read_text(encoding="utf-8")
        assert f"## {version}" in changelog

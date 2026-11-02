#!/usr/bin/env python3
"""Validate this repository's structure; this is not a model-behavior evaluation."""

import json
from pathlib import Path
import re
import sys
import tomllib
from urllib.parse import unquote, urlsplit

from common import read_document
from render_agents import check

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def validate(root: Path) -> list[str]:
    errors = []
    try:
        manifest = json.loads((root / "harness.json").read_text(encoding="utf-8"))
        if manifest["schema_version"] != 1:
            errors.append("Unsupported manifest schema")
        listed = set(manifest["core"])
        for skills in manifest["profiles"].values():
            listed.update(skills)
        actual = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
        if listed != actual:
            errors.append(f"Manifest/skills mismatch: {sorted(listed ^ actual)}")
        for name in sorted(actual):
            path = root / "skills" / name / "SKILL.md"
            fields, body = read_document(path)
            if fields.keys() != {"name", "description"}:
                errors.append(f"Skill fields must be name and description: {name}")
            if fields.get("name") != name or not NAME.fullmatch(name) or len(name) > 64:
                errors.append(f"Invalid skill name: {name}")
            description = fields.get("description", "")
            if not 1 <= len(description) <= 1024 or "<" in description or ">" in description:
                errors.append(f"Invalid description: {name}")
            if not body.strip() or len(body.splitlines()) > 200 or len(body.encode()) > 12000:
                errors.append(f"Skill body is empty or over the local size budget: {name}")
            metadata = path.parent / "agents/openai.yaml"
            text = metadata.read_text(encoding="utf-8")
            if f"${name}" not in text:
                errors.append(f"Skill UI prompt missing invocation: {name}")
            for key in ("display_name", "short_description", "default_prompt"):
                match = re.search(rf'^  {key}: (".*")$', text, re.MULTILINE)
                if not match:
                    errors.append(f"Missing quoted UI metadata {key}: {name}")
                    continue
                value = json.loads(match.group(1))
                if not value or (key == "short_description" and not 25 <= len(value) <= 64):
                    errors.append(f"Invalid UI metadata {key}: {name}")
        for name in ("AGENTS.md", "templates/AGENTS.md"):
            if (root / name).stat().st_size > 8000:
                errors.append(f"Always-loaded instructions exceed 8 KB: {name}")
        for relative in check(root):
            errors.append(f"Stale agent adapter: {relative}")
        for path in (root / "adapters/codex/agents").glob("*.toml"):
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            if data.keys() != {"name", "description", "developer_instructions"}:
                errors.append(f"Unexpected native agent schema: {path.name}")
        for path in root.rglob("*.md"):
            if ".git" in path.parts:
                continue
            for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                parts = urlsplit(link)
                if parts.scheme or parts.netloc or not parts.path:
                    continue
                target = (path.parent / unquote(parts.path)).resolve()
                if not target.is_relative_to(root.resolve()) or not target.exists():
                    errors.append(f"Broken local link in {path.relative_to(root)}: {link}")
        cases = json.loads((root / "evals/cases.json").read_text(encoding="utf-8"))
        ids = [case["id"] for case in cases]
        if len(ids) != len(set(ids)):
            errors.append("Duplicate evaluation IDs")
        covered = set()
        for case in cases:
            expected = set(case["expected_skills"])
            excluded = set(case["excluded_skills"])
            covered.update(expected)
            if not case["prompt"] or not case["criteria"] or not (expected | excluded) <= actual or expected & excluded:
                errors.append(f"Invalid evaluation case: {case['id']}")
        if covered != actual:
            errors.append(f"Skills without positive evaluation cases: {sorted(actual - covered)}")
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(str(error))
    return errors


def main() -> int:
    errors = validate(ROOT)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print("PASS: skill structure, local links, profiles, native adapters, evaluation schema")
    print("This check does not establish agent behavior or application runtime compatibility.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

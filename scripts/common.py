"""Small authoring format: YAML frontmatter with JSON-quoted string values."""

import json
from pathlib import Path


def read_document(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing frontmatter: {path}")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"Unclosed frontmatter: {path}")
    fields = {}
    for line in parts[1].splitlines():
        key, separator, value = line.partition(":")
        if not separator or key in fields:
            raise ValueError(f"Invalid or duplicate frontmatter field: {path}: {line}")
        try:
            fields[key] = json.loads(value.strip())
        except json.JSONDecodeError as error:
            raise ValueError(f"Use JSON-quoted YAML string values in {path}") from error
        if not isinstance(fields[key], str) or not fields[key].strip():
            raise ValueError(f"Expected a nonempty string for {key}: {path}")
    return fields, parts[2].strip() + "\n"

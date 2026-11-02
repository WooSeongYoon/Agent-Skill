#!/usr/bin/env python3
"""Preview or install repository-scoped agent instructions without overwriting files."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL_PATHS = {"codex": ".agents/skills", "claude": ".claude/skills"}


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if not relative or path.is_absolute() or any(
        part in {".", ".."} or ":" in part or "\\" in part for part in relative.split("/")
    ):
        raise ValueError(f"Unsafe relative path: {relative}")
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink() or (current.exists() and current.resolve() != current.absolute()):
            raise ValueError(f"Linked path is not supported: {current}")
    return current


def read_source(root: Path, relative: str) -> bytes:
    path = safe_path(root, relative)
    if not path.is_file():
        raise ValueError(f"Source file missing: {relative}")
    return path.read_bytes()


def build_plan(root: Path, profiles: list[str], tools: list[str],
               with_agents: bool = False, skip_instructions: bool = False) -> dict[str, bytes]:
    config = json.loads(read_source(root, "harness.json"))
    if config["schema_version"] != 1:
        raise ValueError("Unsupported harness schema")
    if not profiles or not tools:
        raise ValueError("Choose at least one profile and tool")
    unknown = set(profiles) - config["profiles"].keys()
    if unknown:
        raise ValueError(f"Unknown profiles: {', '.join(sorted(unknown))}")
    if set(tools) - SKILL_PATHS.keys():
        raise ValueError("Supported tools are codex and claude")
    skills = set(config["core"])
    for profile in profiles:
        skills.update(config["profiles"][profile])
    plan = {}
    for name in sorted(skills):
        folder = safe_path(root, f"skills/{name}")
        read_source(root, f"skills/{name}/SKILL.md")
        for source in sorted(folder.rglob("*")):
            if source.is_symlink():
                raise ValueError(f"Linked source is not supported: {source}")
            if not source.is_file():
                continue
            if "__pycache__" in source.parts or source.suffix == ".pyc":
                continue
            content = read_source(root, source.relative_to(root).as_posix())
            for tool in sorted(set(tools)):
                relative = source.relative_to(folder).as_posix()
                plan[f"{SKILL_PATHS[tool]}/{name}/{relative}"] = content
    instructions = read_source(root, "templates/AGENTS.md")
    plan[".harness/instructions.md"] = instructions
    if not skip_instructions:
        plan["AGENTS.md"] = instructions
        if "claude" in tools:
            plan["CLAUDE.md"] = read_source(root, "templates/CLAUDE.md")
    if with_agents:
        for name in config["agents"]:
            for tool in sorted(set(tools)):
                extension = "toml" if tool == "codex" else "md"
                relative = f"adapters/{tool}/agents/{name}.{extension}"
                plan[f".{tool}/agents/{name}.{extension}"] = read_source(root, relative)
    plan[".harness/project.json"] = json_bytes({
        "schema_version": 1,
        "profiles": sorted(set(profiles)),
        "facts": {"python_version": None, "qt_binding": None, "web_framework": None,
                  "ml_framework": None, "package_manager": None, "gpu": None},
        "commands": {name: [] for name in ["setup", "lint", "typecheck", "test", "build", "smoke"]},
        "notes": "Discover commands from this project. Empty arrays mean unconfigured, not passing."
    })
    plan[".harness/installed.json"] = json_bytes({
        "schema_version": 1,
        "harness_version": config["version"],
        "profiles": sorted(set(profiles)),
        "tools": sorted(set(tools)),
        "with_agents": with_agents,
        "instructions_installed": not skip_instructions,
        "files": {name: digest(data) for name, data in sorted(plan.items())}
    })
    return plan


def inspect_plan(target: Path, plan: dict[str, bytes]) -> list[tuple[str, str]]:
    if target.resolve() != target or target.is_symlink():
        raise ValueError(f"Use a real target directory, not a linked path: {target}")
    if target.exists() and not target.is_dir():
        raise ValueError(f"Target is not a directory: {target}")
    statuses = []
    for relative, content in sorted(plan.items()):
        path = safe_path(target, relative)
        for parent in path.parents:
            if parent == target:
                break
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Parent is not a directory: {parent}")
        if not path.exists():
            statuses.append(("CREATE", relative))
        elif path.is_file() and path.read_bytes() == content:
            statuses.append(("SAME", relative))
        else:
            statuses.append(("CONFLICT", relative))
    return statuses


def apply_plan(target: Path, plan: dict[str, bytes]) -> int:
    statuses = inspect_plan(target, plan)
    conflicts = [name for state, name in statuses if state == "CONFLICT"]
    if conflicts:
        raise ValueError(f"Existing files differ; nothing written: {', '.join(conflicts)}")
    created: list[tuple[Path, bytes]] = []
    try:
        for state, relative in statuses:
            if state == "SAME":
                continue
            path = safe_path(target, relative)
            path.parent.mkdir(parents=True, exist_ok=True)
            # Exclusive creation also refuses files created after the preview.
            with path.open("xb") as stream:
                created.append((path, plan[relative]))
                stream.write(plan[relative])
    except (OSError, ValueError):
        # Keep concurrently changed files; remove only complete files written here.
        for path, content in reversed(created):
            if not path.is_symlink() and path.is_file() and path.read_bytes() == content:
                path.unlink()
        raise
    return len(created)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--profiles", nargs="+", required=True,
                        help="python qt docker web ml full")
    parser.add_argument("--tools", nargs="+", choices=sorted(SKILL_PATHS), default=["codex", "claude"])
    parser.add_argument("--with-agents", action="store_true", help="Install optional role definitions")
    parser.add_argument("--skip-instructions", action="store_true",
                        help="Preserve root instructions; manually merge .harness/instructions.md")
    parser.add_argument("--apply", action="store_true", help="Write files; default is preview only")
    args = parser.parse_args()
    target = Path(os.path.abspath(args.target.expanduser()))
    try:
        if target == ROOT or target.is_relative_to(ROOT):
            raise ValueError("Choose a project outside the harness source checkout")
        plan = build_plan(ROOT, args.profiles, args.tools, args.with_agents, args.skip_instructions)
        statuses = inspect_plan(target, plan)
        for state, name in statuses:
            print(f"{state:8} {name}")
        if any(state == "CONFLICT" for state, _ in statuses):
            raise ValueError("Resolve conflicts manually, or stage in an empty directory. No files written.")
        if args.apply:
            print(f"Installed {apply_plan(target, plan)} new files into {target}")
        else:
            print("Preview only. Re-run with --apply to install these files.")
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"Installation stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

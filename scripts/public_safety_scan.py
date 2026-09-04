#!/usr/bin/env python3
"""Fail on obvious private artifacts before a repository is published."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "build",
    "dist",
}
PRIVATE_PATH_PATTERN = re.compile(r"/" + r"Users/[A-Za-z0-9_.-]+/")
PERSONAL_EMAIL_PATTERN = re.compile(
    r"@[A-Za-z0-9_.-]*(?:gmail|outlook|hotmail)\.com", re.IGNORECASE
)
PRIVATE_ARTIFACT_SUFFIXES = {".jpeg", ".jpg", ".pdf", ".png"}


def iter_files(root: Path):
    """Yield source files while skipping generated and VCS directories."""
    for path in root.rglob("*"):
        if not path.is_file() or any(
            part in IGNORED_DIRECTORY_NAMES or part.startswith(".venv")
            for part in path.relative_to(root).parts
        ):
            continue
        yield path


def scan(root: Path) -> list[str]:
    """Return human-readable findings for obvious private material."""
    findings: list[str] = []
    for path in iter_files(root):
        relative = path.relative_to(root)
        if path.suffix.lower() in PRIVATE_ARTIFACT_SUFFIXES:
            findings.append(f"private artifact suffix: {relative}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if PRIVATE_PATH_PATTERN.search(text):
            findings.append(f"private filesystem path: {relative}")
        if PERSONAL_EMAIL_PATTERN.search(text):
            findings.append(f"personal email pattern: {relative}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    findings = scan(args.root.resolve())
    if findings:
        print("Public-safety scan failed:")
        print("\n".join(f"- {finding}" for finding in findings))
        return 1
    print(f"Public-safety scan passed: {args.root.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Structured role-brief helpers.

The core accepts a brief produced by an agent or browser adapter. It does not
silently scrape arbitrary page instructions or guess volatile eligibility facts.
"""

from __future__ import annotations

from typing import Any

from ..io import load_json
from ..models import validate_role


def load_role(path: str) -> dict[str, Any]:
    role = load_json(path)
    validate_role(role)
    return role


def inspect_role(role: dict[str, Any]) -> dict[str, Any]:
    validate_role(role)
    requirements = role["requirements"]
    return {
        "company": role["company"],
        "title": role["title"],
        "source_url": role["source_url"],
        "location": role.get("location"),
        "employment_type": role.get("employment_type"),
        "required": list(requirements.get("required", [])),
        "nice_to_have": list(requirements.get("nice_to_have", [])),
        "documents": role.get("documents", {"required": ["cv"], "optional": []}),
        "form_questions": list(role.get("form_questions", [])),
        "unknowns": list(role.get("unknowns", [])),
    }

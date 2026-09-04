"""Shared constants and lightweight validation for the public contracts."""

from __future__ import annotations

from typing import Any

APPLICATION_STATES = (
    "draft",
    "researched",
    "tailored",
    "PDF-QA-passed",
    "form-reviewed",
    "submitted-pending-confirmation",
    "confirmed",
)

TRANSITIONS = {
    "draft": {"researched", "blocked"},
    "researched": {"tailored", "blocked"},
    "tailored": {"PDF-QA-passed", "blocked"},
    "PDF-QA-passed": {"form-reviewed", "blocked"},
    "form-reviewed": {"submitted-pending-confirmation", "blocked"},
    "submitted-pending-confirmation": {"confirmed", "blocked"},
    "confirmed": set(),
}


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def validate_candidate(candidate: dict[str, Any]) -> None:
    require_object(candidate, "candidate")
    for key in ("schema_version", "identity", "experience", "projects", "links"):
        if key not in candidate:
            raise ValueError(f"candidate is missing `{key}`")
    if not isinstance(candidate["identity"], dict):
        raise ValueError("candidate.identity must be an object")
    for key in ("experience", "projects", "links"):
        if not isinstance(candidate[key], list):
            raise ValueError(f"candidate.{key} must be an array")


def validate_role(role: dict[str, Any]) -> None:
    require_object(role, "role")
    for key in ("schema_version", "company", "title", "source_url", "requirements"):
        if key not in role:
            raise ValueError(f"role is missing `{key}`")
    if not isinstance(role["requirements"], dict):
        raise ValueError("role.requirements must be an object")

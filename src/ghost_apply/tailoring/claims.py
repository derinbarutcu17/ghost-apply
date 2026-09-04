"""Build and validate a claim ledger without inventing candidate evidence."""

from __future__ import annotations

from typing import Any

from ..models import validate_candidate, validate_role


def _entry(claim: str, wording: str, evidence: str, claim_type: str = "historical") -> dict[str, Any]:
    return {
        "claim": claim,
        "approved_wording": wording,
        "evidence": evidence,
        "allowed_verbs": ["designed", "built", "created", "led", "worked", "supported"],
        "claim_type": claim_type,
        "freshness_rule": "revalidate volatile facts on the live listing",
        "last_verified": None,
    }


def build_claim_ledger(candidate: dict[str, Any], role: dict[str, Any]) -> dict[str, Any]:
    validate_candidate(candidate)
    validate_role(role)
    claims: list[dict[str, Any]] = []
    for index, item in enumerate(candidate["experience"]):
        if not isinstance(item, dict):
            continue
        label = item.get("title") or item.get("role") or "experience"
        wording = item.get("summary") or item.get("description") or label
        claims.append(_entry(label, wording, f"candidate.experience[{index}]"))
    for index, item in enumerate(candidate["projects"]):
        if not isinstance(item, dict):
            continue
        label = item.get("name") or "project"
        wording = item.get("description") or label
        claims.append(_entry(label, wording, f"candidate.projects[{index}]", "current"))
    return {
        "schema_version": 1,
        "role": {"company": role["company"], "title": role["title"], "source_url": role["source_url"]},
        "claims": claims,
        "eligibility": {
            "work_authorization": {"value": "unknown", "source": None},
            "visa_sponsorship": {"value": "unknown", "source": None},
        },
    }


def validate_claim_ledger(ledger: dict[str, Any]) -> None:
    if not isinstance(ledger.get("claims"), list):
        raise ValueError("claim ledger claims must be an array")
    required = ("claim", "approved_wording", "evidence", "allowed_verbs", "claim_type", "freshness_rule")
    for index, claim in enumerate(ledger["claims"]):
        if not isinstance(claim, dict):
            raise ValueError(f"claim {index} must be an object")
        for key in required:
            if not claim.get(key):
                raise ValueError(f"claim {index} is missing `{key}`")

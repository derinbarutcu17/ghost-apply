"""Receipt creation and integrity auditing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..io import load_json, sha256_file, write_json
from ..state_machine import StateMachine


def create_receipt(role: dict[str, Any], output: str | Path, manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    receipt = {
        "schema_version": 1,
        "state": "draft",
        "company": role["company"],
        "role": role["title"],
        "source_url": role["source_url"],
        "application_url": role.get("application_url"),
        "retrieved_at": role.get("retrieved_at"),
        "requirements": role.get("requirements", {}),
        "form_questions": role.get("form_questions", []),
        "claim_ledger": [],
        "eligibility": {
            "work_authorization": {"value": "unknown", "source": None},
            "visa_sponsorship": {"value": "unknown", "source": None},
        },
        "artifacts": list((manifest or {}).get("artifacts", [])),
        "form_payload": [],
        "submission": {"submitted_at": None, "confirmation_url": None, "confirmation_text": None},
        "events": [],
    }
    write_json(output, receipt)
    return receipt


def transition_receipt(receipt: dict[str, Any], target: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    machine = StateMachine(receipt.get("state", "draft"), receipt.get("events", []))
    machine.transition(target, evidence)
    receipt["state"] = machine.state
    receipt["events"] = machine.events
    return receipt


def audit_receipt(path: str | Path) -> dict[str, Any]:
    receipt = load_json(path)
    findings: list[str] = []
    for artifact in receipt.get("artifacts", []):
        artifact_path = Path(artifact.get("path", ""))
        if not artifact_path.is_file():
            findings.append(f"missing artifact: {artifact_path}")
            continue
        if artifact.get("sha256") != sha256_file(artifact_path):
            findings.append(f"artifact hash mismatch: {artifact_path}")
    if receipt.get("state") == "confirmed":
        submission = receipt.get("submission", {})
        if not (submission.get("confirmation_text") or submission.get("confirmation_url")):
            findings.append("confirmed receipt lacks visible confirmation evidence")
    return {"receipt": str(path), "pass": not findings, "findings": findings, "state": receipt.get("state")}

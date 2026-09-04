"""Guarded, auditable application state transitions."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .models import TRANSITIONS


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class StateMachine:
    def __init__(self, state: str = "draft", events: list[dict[str, Any]] | None = None):
        if state not in TRANSITIONS and state != "blocked":
            raise ValueError(f"Unknown application state: {state}")
        self.state = state
        self.events = list(events or [])

    def transition(self, target: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
        evidence = dict(evidence or {})
        if self.state == "blocked":
            raise ValueError("Blocked applications must be resumed explicitly before transitioning")
        if target not in TRANSITIONS.get(self.state, set()):
            raise ValueError(f"Invalid transition: {self.state} -> {target}")
        if target == "confirmed" and not (evidence.get("confirmation_text") or evidence.get("confirmation_url")):
            raise ValueError("confirmed requires visible confirmation_text or confirmation_url evidence")
        event = {"from": self.state, "to": target, "at": now_iso(), "evidence": evidence}
        self.events.append(event)
        self.state = target
        return event

    def block(self, reason: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
        if not reason.strip():
            raise ValueError("A blocked state needs a precise reason")
        event = {"from": self.state, "to": "blocked", "at": now_iso(), "reason": reason, "evidence": dict(evidence or {})}
        self.events.append(event)
        self.state = "blocked"
        return event

    def resume(self, state: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
        if self.state != "blocked":
            raise ValueError("Only blocked applications can be resumed")
        if state not in TRANSITIONS:
            raise ValueError(f"Unknown resume state: {state}")
        event = {"from": "blocked", "to": state, "at": now_iso(), "evidence": dict(evidence or {})}
        self.events.append(event)
        self.state = state
        return event

    def as_dict(self) -> dict[str, Any]:
        return {"state": self.state, "events": self.events}

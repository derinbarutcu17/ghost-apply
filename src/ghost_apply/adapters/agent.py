"""Vendor-neutral request and response contracts for tool-using agents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

RunMode = Literal["dry-run", "review", "live-submit"]


@dataclass(frozen=True)
class AgentRequest:
    role_url: str
    candidate_path: Path
    mode: RunMode = "dry-run"

    def validate(self) -> None:
        if not self.role_url.startswith(("https://", "http://")):
            raise ValueError("role_url must be an HTTP(S) URL")
        if not self.candidate_path.is_file():
            raise ValueError(f"candidate pack not found: {self.candidate_path}")
        if self.mode not in ("dry-run", "review", "live-submit"):
            raise ValueError(f"unsupported run mode: {self.mode}")


def result_contract(*, state: str, receipt_path: str, next_action: str) -> dict[str, str]:
    """Return a stable, JSON-friendly handoff for any agent host."""
    return {"state": state, "receipt": receipt_path, "next_action": next_action}

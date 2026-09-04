"""Explicit user paths; the engine never assumes a personal filesystem layout."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    profile: Path
    runs: Path

    @classmethod
    def from_profile(cls, profile: str | Path, runs: str | Path | None = None) -> Paths:
        profile_path = Path(profile).expanduser()
        return cls(profile=profile_path, runs=Path(runs).expanduser() if runs else profile_path / "runs")

    def create(self) -> None:
        self.profile.mkdir(parents=True, exist_ok=True)
        self.runs.mkdir(parents=True, exist_ok=True)

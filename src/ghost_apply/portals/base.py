"""Driver-neutral portal adapter protocol.

This module intentionally contains no browser implementation. A browser
adapter must report visible state and may not use hidden setters or API uploads.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class PortalFingerprint:
    name: str
    host: str
    login_gated: bool = False


class PortalAdapter(Protocol):
    def identify(self, page: Any) -> PortalFingerprint: ...
    def inspect(self, page: Any) -> dict[str, Any]: ...
    def fill(self, field: str, value: str) -> dict[str, Any]: ...
    def upload(self, control: str, staged_file: str) -> dict[str, Any]: ...
    def review(self, page: Any) -> dict[str, Any]: ...
    def submit(self, page: Any) -> dict[str, Any]: ...
    def confirm(self, page: Any) -> dict[str, Any]: ...

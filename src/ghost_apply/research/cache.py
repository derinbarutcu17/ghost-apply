"""TTL-aware role-cache helpers; volatile fields must still be revalidated."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def _parse(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def is_fresh(entry: dict[str, Any], now: datetime | None = None) -> bool:
    retrieved = _parse(entry.get("retrieved_at"))
    if retrieved is None:
        return False
    now = now or datetime.now(UTC)
    ttl_hours = float(entry.get("ttl_hours", 24))
    return (now - retrieved).total_seconds() < ttl_hours * 3600


def put(cache: dict[str, Any], role: dict[str, Any], retrieved_at: str, ttl_hours: int = 24) -> dict[str, Any]:
    roles = [item for item in cache.get("roles", []) if item.get("source_url") != role.get("source_url")]
    roles.append({**role, "retrieved_at": retrieved_at, "ttl_hours": ttl_hours})
    return {"schema_version": 1, "roles": roles}

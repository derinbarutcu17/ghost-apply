from pathlib import Path

from ghost_apply.io import load_json
from ghost_apply.models import validate_candidate, validate_role
from ghost_apply.research.brief import inspect_role
from ghost_apply.research.cache import is_fresh, put
from ghost_apply.tailoring.claims import build_claim_ledger, validate_claim_ledger

ROOT = Path(__file__).parents[2]
EXAMPLE_CANDIDATE = ROOT / "examples/candidate-context.example.json"
EXAMPLE_ROLE = ROOT / "examples/role-brief.example.json"


def test_examples_are_valid_and_inspectable():
    candidate = load_json(EXAMPLE_CANDIDATE)
    role = load_json(EXAMPLE_ROLE)
    validate_candidate(candidate)
    validate_role(role)
    result = inspect_role(role)
    assert result["company"] == "Example Labs"
    assert "Product design" in result["required"]


def test_claim_ledger_is_grounded_in_input_indexes():
    ledger = build_claim_ledger(load_json(EXAMPLE_CANDIDATE), load_json(EXAMPLE_ROLE))
    validate_claim_ledger(ledger)
    assert ledger["claims"][0]["evidence"].startswith("candidate.")
    assert ledger["eligibility"]["work_authorization"]["value"] == "unknown"


def test_role_cache_is_ttl_aware_and_replaces_same_source():
    role = load_json(EXAMPLE_ROLE)
    cache = put({"schema_version": 1, "roles": []}, role, "2026-01-01T00:00:00Z", ttl_hours=24)
    assert len(cache["roles"]) == 1
    assert is_fresh(cache["roles"][0], __import__("datetime").datetime.fromisoformat("2026-01-01T01:00:00+00:00"))
    assert len(put(cache, role, "2026-01-02T00:00:00Z")["roles"]) == 1

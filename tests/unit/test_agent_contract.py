from pathlib import Path

import pytest

from ghost_apply.adapters.agent import AgentRequest, result_contract


def test_agent_request_validates_explicit_profile_and_mode(tmp_path):
    candidate = tmp_path / "candidate.json"
    candidate.write_text("{}", encoding="utf-8")
    request = AgentRequest("https://example.test/job", candidate, "dry-run")
    request.validate()
    assert result_contract(state="tailored", receipt_path="receipt.json", next_action="qa")["next_action"] == "qa"


def test_agent_request_rejects_missing_candidate(tmp_path):
    with pytest.raises(ValueError, match="not found"):
        AgentRequest("https://example.test/job", Path(tmp_path / "missing.json")).validate()

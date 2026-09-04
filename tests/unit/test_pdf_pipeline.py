from pathlib import Path

from ghost_apply.documents.pdf import generate_package
from ghost_apply.io import load_json
from ghost_apply.qa.pdf import qa_manifest

ROOT = Path(__file__).parents[2]


def test_generate_and_qa_example_package(tmp_path):
    candidate = load_json(ROOT / "examples/candidate-context.example.json")
    role = load_json(ROOT / "examples/role-brief.example.json")
    manifest = generate_package(candidate, role, tmp_path / "package")
    report = qa_manifest(manifest["manifest_path"], tmp_path / "qa")
    assert report["pass_machine"] is True
    assert len(report["artifacts"]) == 2

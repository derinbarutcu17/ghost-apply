import hashlib
import shutil
from pathlib import Path

from ghost_apply.documents.pdf import generate_package
from ghost_apply.io import load_json

ROOT = Path(__file__).parents[2]


def test_staged_bytes_match_source_manifest(tmp_path):
    candidate = load_json(ROOT / "examples/candidate-context.example.json")
    role = load_json(ROOT / "examples/role-brief.example.json")
    manifest = generate_package(candidate, role, tmp_path / "package")
    stage = tmp_path / "stage"
    stage.mkdir()
    for artifact in manifest["artifacts"]:
        source = Path(artifact["path"])
        destination = stage / artifact["filename"]
        shutil.copy2(source, destination)
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
        assert digest == artifact["sha256"]

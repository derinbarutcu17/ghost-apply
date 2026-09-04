from pathlib import Path

from scripts.public_safety_scan import scan


def test_public_safety_scan_accepts_public_source(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("Public documentation.\n", encoding="utf-8")

    assert scan(tmp_path) == []


def test_public_safety_scan_rejects_private_canaries(tmp_path: Path) -> None:
    private_file = "/" + "Users/alice/Documents/CV.pdf"
    personal_email = "alice@" + "gmail.com"
    (tmp_path / "notes.txt").write_text(
        f"Local file: {private_file}\ncontact: {personal_email}\n",
        encoding="utf-8",
    )
    (tmp_path / "screenshot.png").write_bytes(b"not a real image")

    findings = scan(tmp_path)

    assert any("private filesystem path" in finding for finding in findings)
    assert any("personal email pattern" in finding for finding in findings)
    assert any("private artifact suffix" in finding for finding in findings)

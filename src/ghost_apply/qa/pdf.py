"""Deterministic PDF checks using standard command-line PDF tools when available."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from ..io import load_json, sha256_file, write_json


def _command_output(command: list[str]) -> str:
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    return result.stdout + result.stderr


def check_pdf(path: str | Path, render_dir: str | Path | None = None) -> dict[str, Any]:
    pdf = Path(path)
    checks: dict[str, Any] = {"path": str(pdf), "exists": pdf.is_file(), "readable": False, "a4": False, "text_layer": False, "replacement_glyphs": False, "rendered": False}
    if not pdf.is_file() or pdf.stat().st_size == 0:
        checks["pass"] = False
        return checks
    if shutil.which("pdfinfo"):
        info = _command_output(["pdfinfo", str(pdf)])
        checks["readable"] = "Pages:" in info and "Page size:" in info
        match = re.search(r"Page size:\s*([0-9.]+) x ([0-9.]+)", info)
        if match:
            width, height = float(match.group(1)), float(match.group(2))
            checks["a4"] = abs(width - 595.276) <= 1.0 and abs(height - 841.89) <= 1.0
            pages = re.search(r"Pages:\s*(\d+)", info)
            checks["pages"] = int(pages.group(1)) if pages else None
    if shutil.which("pdftotext"):
        text = _command_output(["pdftotext", str(pdf), "-"])
        checks["text_layer"] = len(text.strip()) > 20
        checks["replacement_glyphs"] = "�" not in text and "\ufffd" not in text
        checks["text_chars"] = len(text.strip())
    if render_dir and shutil.which("pdftoppm"):
        target = Path(render_dir)
        target.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(["pdftoppm", "-png", "-r", "100", "-singlefile", str(pdf), str(target / pdf.stem)], check=False, capture_output=True)
        checks["rendered"] = result.returncode == 0 and (target / f"{pdf.stem}.png").is_file()
    else:
        checks["rendered"] = None
    checks["one_page"] = checks.get("pages") == 1
    checks["sha256"] = sha256_file(pdf)
    checks["pass"] = all(checks[key] for key in ("exists", "readable", "a4", "one_page", "text_layer", "replacement_glyphs")) and checks.get("rendered") is not False
    return checks


def qa_manifest(manifest_path: str | Path, out_dir: str | Path) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)
    results = []
    for artifact in manifest.get("artifacts", []):
        result = check_pdf(artifact["path"], output / "renders")
        result["expected_sha256"] = artifact.get("sha256")
        result["hash_matches_manifest"] = result.get("sha256") == artifact.get("sha256")
        result["pass"] = result["pass"] and result["hash_matches_manifest"]
        results.append(result)
    report = {"schema_version": 1, "manifest": str(manifest_path), "submission_allowed": False, "artifacts": results, "pass_machine": bool(results) and all(item["pass"] for item in results), "visual_review": "pending"}
    write_json(output / "report.json", report)
    return report

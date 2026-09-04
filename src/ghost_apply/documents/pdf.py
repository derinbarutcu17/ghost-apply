"""Small, deterministic A4 CV and cover-letter renderer for the public core."""

from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from ..io import canonical_json_hash, sha256_file, write_json
from ..models import validate_candidate, validate_role

INK = colors.HexColor("#20262B")
TEAL = colors.HexColor("#0B6E82")
MUTED = colors.HexColor("#5E6B73")


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "role"


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()["Normal"]
    return {
        "name": ParagraphStyle("name", parent=base, fontName="Helvetica-Bold", fontSize=22, leading=24, textColor=INK, spaceAfter=2),
        "headline": ParagraphStyle("headline", parent=base, fontName="Helvetica-Bold", fontSize=11, leading=13, textColor=TEAL, spaceAfter=4),
        "contact": ParagraphStyle("contact", parent=base, fontName="Helvetica", fontSize=8.5, leading=10, textColor=MUTED),
        "section": ParagraphStyle("section", parent=base, fontName="Helvetica-Bold", fontSize=10.5, leading=12, textColor=TEAL, spaceBefore=8, spaceAfter=3),
        "body": ParagraphStyle("body", parent=base, fontName="Helvetica", fontSize=9, leading=11.2, textColor=INK, spaceAfter=3),
        "role": ParagraphStyle("role", parent=base, fontName="Helvetica-Bold", fontSize=9.3, leading=11, textColor=INK, spaceBefore=2),
        "meta": ParagraphStyle("meta", parent=base, fontName="Helvetica", fontSize=8.2, leading=9.5, textColor=MUTED, spaceAfter=1),
        "bullet": ParagraphStyle("bullet", parent=base, fontName="Helvetica", fontSize=8.55, leading=10.3, textColor=INK, leftIndent=9, firstLineIndent=-6, spaceAfter=1),
        "letter_body": ParagraphStyle("letter_body", parent=base, fontName="Helvetica", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=12),
    }


def _link_line(links: list[dict[str, Any]]) -> str:
    parts = []
    for link in links:
        if isinstance(link, dict) and link.get("url") and link.get("label"):
            parts.append(f'<a href="{_esc(link["url"])}" color="#0B6E82"><u>{_esc(link["label"])}</u></a>')
    return " | ".join(parts)


def _build_cv(path: Path, candidate: dict[str, Any], role: dict[str, Any]) -> None:
    styles = _styles()
    identity = candidate["identity"]
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm, title=f"CV - {role['company']} - {role['title']}", author=str(identity.get("name", "Candidate")))
    story: list[Any] = [
        Paragraph(_esc(identity.get("name", "Candidate")), styles["name"]),
        Paragraph(_esc(candidate.get("headline", role["title"])), styles["headline"]),
        Paragraph(" | ".join(_esc(identity.get(key, "")) for key in ("location", "email", "phone") if identity.get(key)), styles["contact"]),
    ]
    links = _link_line(candidate.get("links", []))
    if links:
        story.append(Paragraph(links, styles["contact"]))
    story.extend([Paragraph("PROFILE", styles["section"]), Paragraph(_esc(candidate.get("summary", "")), styles["body"])])
    story.append(Paragraph("EXPERIENCE", styles["section"]))
    for item in candidate.get("experience", []):
        if not isinstance(item, dict):
            continue
        story.append(Paragraph(_esc(item.get("title", item.get("role", "Experience"))), styles["role"]))
        story.append(Paragraph(_esc(item.get("meta", "")), styles["meta"]))
        for bullet in item.get("bullets", []):
            story.append(Paragraph(f"• {_esc(bullet)}", styles["bullet"]))
    story.append(Paragraph("SELECTED PROJECTS", styles["section"]))
    for item in candidate.get("projects", []):
        if isinstance(item, dict):
            project_link = item.get("url")
            name = _esc(item.get("name", "Project"))
            if project_link:
                name = f'<a href="{_esc(project_link)}" color="#0B6E82"><u>{name}</u></a>'
            story.append(Paragraph(f"{name} - {_esc(item.get('description', ''))}", styles["body"]))
    story.append(Paragraph("SKILLS", styles["section"]))
    for skill in candidate.get("skills", []):
        story.append(Paragraph(f"• {_esc(skill)}", styles["bullet"]))
    doc.build(story)


def _build_letter(path: Path, candidate: dict[str, Any], role: dict[str, Any]) -> None:
    styles = _styles()
    identity = candidate["identity"]
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=25 * mm, leftMargin=25 * mm, topMargin=22 * mm, bottomMargin=22 * mm, title=f"Cover Letter - {role['company']} - {role['title']}", author=str(identity.get("name", "Candidate")))
    story: list[Any] = [
        Paragraph(_esc(identity.get("name", "Candidate")), styles["name"]),
        Paragraph(" | ".join(_esc(identity.get(key, "")) for key in ("location", "email", "phone") if identity.get(key)), styles["contact"]),
        Spacer(1, 15 * mm),
        Paragraph(f"Re: {_esc(role['title'])}", styles["role"]),
        Spacer(1, 8 * mm),
    ]
    first = candidate.get("cover_letter_opening") or f"I am applying for the {role['title']} position at {role['company']}."
    summary = candidate.get("summary", "")
    project = candidate.get("projects", [{}])[0] if candidate.get("projects") else {}
    project_name = project.get("name", "a recent project") if isinstance(project, dict) else "a recent project"
    story.extend([
        Paragraph(_esc(first), styles["letter_body"]),
        Paragraph(_esc(f"My background combines visual design, product thinking, and hands-on prototyping. {summary}"), styles["letter_body"]),
        Paragraph(_esc(f"A relevant example is {project_name}: {project.get('description', '') if isinstance(project, dict) else ''}"), styles["letter_body"]),
        Paragraph(_esc("I would welcome the opportunity to contribute thoughtfully, learn quickly, and add value to the team."), styles["letter_body"]),
        Paragraph("Best,<br/>" + _esc(identity.get("name", "Candidate")), styles["body"]),
    ])
    doc.build(story)


def generate_package(candidate: dict[str, Any], role: dict[str, Any], output_dir: str | Path) -> dict[str, Any]:
    validate_candidate(candidate)
    validate_role(role)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    stem = f"{_slug(role['company'])}-{_slug(role['title'])}"
    cv_path = output / f"{stem}-cv.pdf"
    letter_path = output / f"{stem}-cover-letter.pdf"
    _build_cv(cv_path, candidate, role)
    _build_letter(letter_path, candidate, role)
    source_hash = canonical_json_hash({"candidate": candidate, "role": role})
    artifacts = []
    for path in (cv_path, letter_path):
        artifacts.append({"path": str(path), "filename": path.name, "sha256": sha256_file(path), "bytes": path.stat().st_size, "pages": 1})
    manifest = {
        "schema_version": 1,
        "bundle_id": stem,
        "policy": {"submission_allowed": False, "visual_review": "required"},
        "source": {"role": role["source_url"], "source_hash": source_hash},
        "role": {"company": role["company"], "title": role["title"], "location": role.get("location")},
        "artifacts": artifacts,
    }
    manifest_path = output / "application-package-manifest.json"
    write_json(manifest_path, manifest)
    manifest["manifest_path"] = str(manifest_path)
    return manifest

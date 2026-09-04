"""Command-line entry point for portable, dry-run-first workflows."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from .documents.pdf import generate_package
from .io import load_json, sha256_file, write_json
from .qa.pdf import qa_manifest
from .receipts.receipt import audit_receipt, create_receipt
from .research.brief import inspect_role, load_role
from .tailoring.claims import build_claim_ledger


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ghost-apply", description="Evidence-first job application automation")
    subs = parser.add_subparsers(dest="command", required=True)

    init = subs.add_parser("init", help="create a private profile skeleton")
    init.add_argument("--dest", required=True, type=Path)

    inspect = subs.add_parser("inspect-role", help="inspect an agent-produced role brief")
    inspect.add_argument("--role-file", required=True, type=Path)

    claims = subs.add_parser("build-claims", help="build a claim ledger from JSON inputs")
    claims.add_argument("--candidate", required=True, type=Path)
    claims.add_argument("--role", required=True, type=Path)
    claims.add_argument("--out", required=True, type=Path)

    generate = subs.add_parser("generate", help="generate a CV, letter, and manifest")
    generate.add_argument("--candidate", required=True, type=Path)
    generate.add_argument("--role", required=True, type=Path)
    generate.add_argument("--out", required=True, type=Path)

    qa = subs.add_parser("qa", help="run machine PDF QA")
    qa.add_argument("--manifest", required=True, type=Path)
    qa.add_argument("--out", required=True, type=Path)

    stage = subs.add_parser("stage", help="copy exact artifacts and record hashes; never uploads")
    stage.add_argument("--manifest", required=True, type=Path)
    stage.add_argument("--out", required=True, type=Path)

    receipt = subs.add_parser("receipt", help="create a new application receipt")
    receipt.add_argument("--role", required=True, type=Path)
    receipt.add_argument("--out", required=True, type=Path)
    receipt.add_argument("--manifest", type=Path, help="optional generated package manifest")

    audit = subs.add_parser("audit", help="audit a receipt and artifact hashes")
    audit.add_argument("--receipt", required=True, type=Path)

    run = subs.add_parser("run", help="run the safe local pipeline; live browser work is an adapter concern")
    run.add_argument("--candidate", required=True, type=Path)
    run.add_argument("--role", required=True, type=Path)
    run.add_argument("--out", required=True, type=Path)
    run.add_argument("--mode", choices=("dry-run", "review"), default="dry-run")

    visual = subs.add_parser("visual-review", help="record explicit page-level visual review")
    visual.add_argument("--report", required=True, type=Path)
    visual.add_argument("--out", required=True, type=Path)
    visual.add_argument("--status", choices=("pass", "fail"), required=True)
    visual.add_argument("--reviewer", default="local-user")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "init":
        args.dest.mkdir(parents=True, exist_ok=True)
        write_json(args.dest / "candidate.json", {"schema_version": 1, "identity": {}, "experience": [], "education": [], "languages": [], "projects": [], "links": [], "privacy": {"classification": "private"}})
        write_json(args.dest / "role-cache.json", {"schema_version": 1, "roles": []})
        print(args.dest)
        return 0
    if args.command == "inspect-role":
        print(json.dumps(inspect_role(load_role(str(args.role_file))), indent=2, ensure_ascii=False))
        return 0
    if args.command == "build-claims":
        ledger = build_claim_ledger(load_json(args.candidate), load_role(str(args.role)))
        write_json(args.out, ledger)
        print(args.out)
        return 0
    if args.command == "generate":
        manifest = generate_package(load_json(args.candidate), load_role(str(args.role)), args.out)
        print(manifest["manifest_path"])
        return 0
    if args.command == "qa":
        report = qa_manifest(args.manifest, args.out)
        print("PASS_MACHINE" if report["pass_machine"] else "FAIL_MACHINE")
        return 0 if report["pass_machine"] else 1
    if args.command == "stage":
        manifest = load_json(args.manifest)
        args.out.mkdir(parents=True, exist_ok=True)
        staged = []
        for artifact in manifest.get("artifacts", []):
            source = Path(artifact["path"])
            destination = args.out / artifact["filename"]
            shutil.copy2(source, destination)
            staged.append({"filename": destination.name, "path": str(destination), "sha256": sha256_file(destination), "bytes": destination.stat().st_size})
        write_json(args.out / "staging-manifest.json", {"submission_allowed": False, "artifacts": staged})
        print(args.out / "staging-manifest.json")
        return 0
    if args.command == "receipt":
        receipt_manifest = load_json(args.manifest) if args.manifest else None
        create_receipt(load_role(str(args.role)), args.out, receipt_manifest)
        print(args.out)
        return 0
    if args.command == "audit":
        result = audit_receipt(args.receipt)
        print("PASS" if result["pass"] else "FAIL")
        if result["findings"]:
            print(json.dumps(result["findings"], indent=2))
        return 0 if result["pass"] else 1
    if args.command == "run":
        manifest = generate_package(load_json(args.candidate), load_role(str(args.role)), args.out)
        report = qa_manifest(manifest["manifest_path"], Path(args.out) / "qa")
        receipt_path = Path(args.out) / "receipt.json"
        create_receipt(load_role(str(args.role)), receipt_path, manifest)
        print(json.dumps({"mode": args.mode, "manifest": manifest["manifest_path"], "qa": str(Path(args.out) / "qa/report.json"), "receipt": str(receipt_path), "pass_machine": report["pass_machine"], "next": "visual-review"}, indent=2))
        return 0 if report["pass_machine"] else 1
    if args.command == "visual-review":
        report = load_json(args.report)
        pages = []
        for artifact in report.get("artifacts", []):
            pages.append({"path": artifact["path"], "page": 1, "status": args.status, "reviewer": args.reviewer})
        pass_final = args.status == "pass" and bool(report.get("pass_machine")) and all(page["status"] == "pass" for page in pages)
        review = {"schema_version": 1, "report": str(args.report), "reviewer": args.reviewer, "pages": pages, "status": args.status, "pass_final": pass_final}
        write_json(args.out, review)
        print("PASS_FINAL" if pass_final else "FAIL_VISUAL")
        return 0 if pass_final else 1
    return 2

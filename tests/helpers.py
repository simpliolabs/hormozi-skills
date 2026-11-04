"""Builds a minimal, internally consistent READY run in a temp workspace.

Tests mutate the result to prove each failure predicate fires on the actual
bytes/records, not on prompt wording.
"""
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import check_outputs  # noqa: E402

RUN_ID = "run1"
PRICE_TEXT = "$2,500 one-time"
GUARANTEE_TEXT = "Refund within 30 days if you complete every module and show no result"
PITCH_BODY = (
    "# Pitch\n\nThe program costs $2,500 one-time.\n\n"
    "Guarantee: Refund within 30 days if you complete every module and show no result.\n"
    "Customers get a clear plan for their first client.\n"
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_run(workspace: Path, body: str = PITCH_BODY):
    """Return (run_dir, workspace) for a valid ready run."""
    out = workspace / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "PITCH.md").write_text(body, encoding="utf-8")
    run_dir = out / "runs" / RUN_ID
    src = workspace / "input" / "offer.md"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text("original weak offer", encoding="utf-8")

    brief = {
        "schema_version": 1, "run_id": RUN_ID, "offer_id": "offer1", "task": "write pitch",
        "stage": "C", "maturity": "live_offer", "goal": "pitch", "requested_artifacts": ["PITCH.md"],
        "customer": "coaches", "offer_state": "authorized",
        "facts": [{"id": "f1", "text": "price is 2500", "source_type": "supplied"}],
        "unknowns": ["CAC"], "constraints": [],
        "sources": [{"path": "input/offer.md", "sha256": sha(src.read_bytes())}],
        "workspace_root": ".",
    }
    decisions = {
        "schema_version": 1, "offer_id": "offer1", "version": 3, "parent_hash": None,
        "fields": {
            "price": {"kind": "money", "value": {"amount_minor": 250000, "currency": "USD", "cadence": "one_time"},
                      "display": PRICE_TEXT, "status": "approved", "owner": "owner", "updated": "2026-11-03T00:00:00Z",
                      "authorization_ref": "chat:go-1"},
            "guarantee": {"kind": "guarantee", "value": "30-day conditional refund", "display": GUARANTEE_TEXT,
                          "status": "approved", "owner": "owner", "updated": "2026-11-03T00:00:00Z",
                          "authorization_ref": "chat:go-1", "conditions": ["complete every module"]},
            "cac": {"kind": "money", "value": None, "status": "unknown", "owner": "root", "updated": "2026-11-03T00:00:00Z"},
        },
    }
    claims = {"schema_version": 1, "claims": [
        {"id": "c1", "wording": "Customers get a clear plan for their first client", "source_type": "supplied",
         "status": "verified", "sources": ["input/offer.md"], "scope": "pitch", "qualifications": [],
         "checked_at": "2026-11-03T00:00:00Z", "owner": "root"},
    ]}
    write_json(run_dir / "BRIEF.json", brief)
    write_json(run_dir / "OFFER_DECISIONS.json", decisions)
    write_json(run_dir / "CLAIMS.json", claims)
    art_sha = sha((out / "PITCH.md").read_bytes())
    state = {
        "schema_version": 1, "run_id": RUN_ID, "phase": "READY",
        "tasks": [
            {"id": "t_offer", "role": "sub-offer", "status": "not_applicable", "depends_on": [], "inputs": [], "write_set": []},
            {"id": "t_sales", "role": "sub-sales", "status": "done", "depends_on": ["t_offer"],
             "inputs": [{"path": "input/offer.md", "sha256": sha(src.read_bytes())}], "write_set": ["output/PITCH.md"]},
        ],
        "decision_version": 3, "decision_hash": check_outputs.canonical_hash(run_dir / "OFFER_DECISIONS.json"),
        "artifacts": [{
            "path": "output/PITCH.md", "sha256": art_sha, "decision_version": 3, "task": "t_sales", "ready": True,
            "claim_ids": ["c1"], "uses_fields": ["price", "guarantee"],
            "bindings": [{"field": "price", "rendered_text": PRICE_TEXT}, {"field": "guarantee", "rendered_text": GUARANTEE_TEXT}],
        }],
        "reviews": [{"artifact": "output/PITCH.md", "artifact_sha256": art_sha, "decision_version": 3,
                     "reviewer": "root", "context": "same", "result": "pass"}],
        "blockers": [], "qa_result": "not_run",
    }
    write_json(run_dir / "RUN_STATE.json", state)
    return run_dir, workspace


def codes(findings):
    return {f.code for f in findings}


def refresh_artifact_hash(run_dir: Path, workspace: Path, *, review=True):
    """Re-sync manifest (and optionally the review receipt) with current artifact bytes."""
    st = read_json(run_dir / "RUN_STATE.json")
    new = sha((workspace / "output" / "PITCH.md").read_bytes())
    st["artifacts"][0]["sha256"] = new
    if review:
        st["reviews"][0]["artifact_sha256"] = new
    write_json(run_dir / "RUN_STATE.json", st)


VALID_SUMMARY = (
    "# Owner Summary\n\n"
    "## Offer\n\nA done-with-you pitch program for coaches, priced as approved.\n\n"
    "## Key Decisions\n\n- Price approved by the owner.\n- CAC is unknown and held until measured.\n\n"
    "## Best Hook\n\n> Stop guessing what to say to your first client.\n\n"
    "## Next Actions\n\n1. Confirm the approved price with the owner.\n2. Measure CAC on the first ten leads.\n"
    "3. Send the pitch to the first five prospects.\n"
)


def add_summary(run_dir: Path, workspace: Path, *, body=VALID_SUMMARY, file_path="output/SUMMARY.md",
                manifest_path="output/SUMMARY.md", write_set=None, write_file=True, manifest=True,
                review=True, ready=True, task_id="t_summary"):
    """Declare (and by default write) a root-owned summary with fresh hash, task write set and passing review.

    Each switch removes one thing a complete summary needs, so a test can break exactly one of them."""
    st = read_json(run_dir / "RUN_STATE.json")
    out = workspace / file_path
    if write_file:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(body.encode("utf-8") if isinstance(body, str) else body)
    st["tasks"] = [t for t in st["tasks"] if t["id"] != task_id]
    st["tasks"].append({"id": task_id, "role": "root", "status": "done", "depends_on": [], "inputs": [],
                        "write_set": [manifest_path] if write_set is None else write_set})
    if manifest:
        h = sha(out.read_bytes()) if out.exists() else sha(b"")
        st["artifacts"] = [a for a in st["artifacts"] if a["path"] != manifest_path]
        st["artifacts"].append({"path": manifest_path, "sha256": h, "decision_version": st["decision_version"],
                                "task": task_id, "ready": ready})
        st["reviews"] = [r for r in st["reviews"] if r["artifact"] != manifest_path]
        if review:
            st["reviews"].append({"artifact": manifest_path, "artifact_sha256": h, "decision_version": st["decision_version"],
                                  "reviewer": "root", "context": "same", "result": "pass"})
    write_json(run_dir / "RUN_STATE.json", st)

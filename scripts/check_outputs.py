#!/usr/bin/env python3
"""Local structural/consistency checks for Hormozi offer runs.

Never calls models, the network, publishers or schedulers. Deterministic checks
find absent IDs/bindings/stale reviews; they cannot prove evidence sufficiency
or the absence of unregistered claims -- that needs a semantic review whose
receipt is bound to the artifact hash and decision version.

Exit codes: 0 pass for the requested mode, 1 held/invalid, 2 tool/config failure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

EXIT_PASS, EXIT_HELD, EXIT_TOOL_FAILURE = 0, 1, 2

try:
    from jsonschema import Draft202012Validator
    import yaml
except ImportError as exc:  # fail visibly; never silently skip checks
    Draft202012Validator = None
    yaml = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

CONTROL = {
    "BRIEF.json": "brief",
    "OFFER_DECISIONS.json": "offer-decisions",
    "CLAIMS.json": "claims",
    "RUN_STATE.json": "run-state",
}
OPTIONAL_CONTROL = {"CLAIMS.json"}
PLACEHOLDER = re.compile(r"\[(?:INSERT|TODO|TBD|PLACEHOLDER)[^\]]*\]|\{\{[^}]*\}\}|\bTODO\b|\bTBD\b|lorem ipsum", re.I)
CACHE_SEGMENTS = (".claude/plugins", ".codex/plugins", "plugins/cache")
BLOCKING_CLAIMS = {"unsupported", "prohibited"}
FROZEN_FILES = ("LICENSE", "skills/create-plugin/SKILL.md")


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    artifact: str
    reason: str

    def as_dict(self):
        return asdict(self)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash(path: Path) -> str:
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    return sha256_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def protected_text_hash(data: bytes) -> str:
    """Hash against the canonical LF Git blob; Git's CRLF checkout conversion is accepted, any content change is not."""
    return sha256_bytes(data.replace(b"\r\n", b"\n"))


def _contracts_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "contracts"


def _load_schema(name: str, base: Optional[Path] = None) -> dict:
    return json.loads(((base or _contracts_dir()) / f"{name}.schema.json").read_text(encoding="utf-8"))


def _schema_findings(doc, name: str, artifact: str) -> list[Finding]:
    validator = Draft202012Validator(_load_schema(name))
    return [Finding("SCHEMA_INVALID", "error", artifact, f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}")
            for e in sorted(validator.iter_errors(doc), key=lambda e: list(map(str, e.absolute_path)))]


# ----------------------------------------------------------------- path safety
def _resolve_inside(workspace: Path, rel: str) -> tuple[Optional[Path], Optional[Finding]]:
    """Resolve rel under workspace, rejecting absolute, traversal, symlink escape and plugin-cache paths."""
    norm = rel.replace("\\", "/")
    if any(seg in norm for seg in CACHE_SEGMENTS):
        return None, Finding("PATH_PLUGIN_CACHE", "error", rel, "output must live in the user workspace, not a plugin cache")
    root = workspace.resolve()
    candidate = Path(norm)  # backslashes are separators on every OS, before resolving or comparing ownership
    if re.match(r"^[A-Za-z]:", norm) and not candidate.is_absolute():
        return None, Finding("PATH_ESCAPE", "error", rel, "foreign-drive path is outside the declared workspace")
    if candidate.is_absolute():
        full = candidate
    else:
        full = root / candidate
    try:
        resolved = full.resolve()
        resolved.relative_to(root)
    except (ValueError, OSError):
        return None, Finding("PATH_ESCAPE", "error", rel, "path resolves outside the declared workspace")
    return resolved, None


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


# ------------------------------------------------------------------- run checks
def validate_run(run_dir: Path, workspace_root: Path, mode: str = "ready") -> list[Finding]:
    if mode not in ("draft", "ready"):
        raise ValueError("mode must be draft|ready")
    run_dir, workspace = Path(run_dir), Path(workspace_root)
    findings: list[Finding] = []
    docs: dict[str, object] = {}

    for fname, schema_name in CONTROL.items():
        p = run_dir / fname
        if not p.exists():
            if fname not in OPTIONAL_CONTROL:
                findings.append(Finding("CONTROL_FILE_MISSING", "error", fname, "required control record is absent"))
            continue
        try:
            doc = _read_json(p)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            findings.append(Finding("SCHEMA_INVALID", "error", fname, f"not valid JSON: {exc}"))
            continue
        bad = _schema_findings(doc, schema_name, fname)
        findings += bad
        if not bad:
            docs[fname] = doc

    brief, decisions = docs.get("BRIEF.json"), docs.get("OFFER_DECISIONS.json")
    claims, state = docs.get("CLAIMS.json"), docs.get("RUN_STATE.json")

    if brief:
        for src in brief["sources"]:
            full, err = _resolve_inside(workspace, src["path"])
            if err:
                findings.append(err)
            elif not full.exists() or sha256_bytes(full.read_bytes()) != src["sha256"]:
                findings.append(Finding("SOURCE_HASH_MISMATCH", "error", src["path"], "source changed or missing since the brief was frozen"))

    if claims:
        findings += [Finding("CLAIM_ID_DUPLICATE", "error", d, f"claim id {d} appears more than once in CLAIMS.json; a later entry would shadow the earlier one")
                     for d in _duplicates(c["id"] for c in claims["claims"])]
    findings += _check_identity(brief, decisions, state)
    if decisions and state:
        findings += _check_decisions_vs_state(run_dir, decisions, state)

    if state:
        findings += _check_tasks(state, workspace)
        if mode == "ready":
            findings += _check_ready_state(state)
        findings += _check_inputs(state, brief)
        findings += _check_routes(state, brief, mode)
        findings += _check_receipts(state, workspace)
        findings += _check_routing(state)
        findings += _check_artifacts(state, decisions, claims, brief, workspace, mode)
        findings += _check_summary(state, brief, workspace, mode)
    return findings


def _check_identity(brief, decisions, state) -> list[Finding]:
    """BRIEF, OFFER_DECISIONS and RUN_STATE must describe the same run and offer."""
    out = []
    if brief and state and brief["run_id"] != state["run_id"]:
        out.append(Finding("RUN_IDENTITY_MISMATCH", "error", "RUN_STATE.json", f"run_id {state['run_id']!r} differs from BRIEF run_id {brief['run_id']!r}"))
    if brief and decisions and brief["offer_id"] != decisions["offer_id"]:
        out.append(Finding("RUN_IDENTITY_MISMATCH", "error", "OFFER_DECISIONS.json", f"offer_id {decisions['offer_id']!r} differs from BRIEF offer_id {brief['offer_id']!r}"))
    return out


def _check_ready_state(state) -> list[Finding]:
    """Ready means nothing is open: no blockers and every declared task finished or explicitly not run."""
    out = [Finding("BLOCKER_OPEN", "error", "RUN_STATE.json", f"unresolved blocker: {b}") for b in state["blockers"]]
    for t in state["tasks"]:
        if t["status"] not in ("done", "not_requested", "not_applicable"):
            out.append(Finding("TASK_INCOMPLETE_IN_READY", "error", t["id"], f"task is {t['status']}; ready needs every task done or explicitly not run"))
    return out


def _check_decisions_vs_state(run_dir, decisions, state) -> list[Finding]:
    out = []
    if decisions["version"] != state["decision_version"]:
        out.append(Finding("DECISION_VERSION_MISMATCH", "error", "RUN_STATE.json", "run decision_version differs from OFFER_DECISIONS version"))
    if canonical_hash(run_dir / "OFFER_DECISIONS.json") != state["decision_hash"]:
        out.append(Finding("DECISION_HASH_MISMATCH", "error", "OFFER_DECISIONS.json", "decision record changed without the run state being updated"))
    return out


def _duplicates(ids) -> list[str]:
    """Ids that occur more than once. JSON Schema uniqueItems compares whole objects, not one property, so
    property uniqueness is enforced here, before any lookup dict can silently keep only the last entry."""
    seen, dup = set(), []
    for i in ids:
        if i in seen and i not in dup:
            dup.append(i)
        seen.add(i)
    return dup


def _check_tasks(state, workspace) -> list[Finding]:
    out = [Finding("TASK_ID_DUPLICATE", "error", d, f"task id {d} is declared more than once; ownership would collapse onto the last entry")
           for d in _duplicates(t["id"] for t in state["tasks"])]
    tasks = {t["id"]: t for t in state["tasks"]}
    satisfied = {"done", "not_requested", "not_applicable"}
    for t in state["tasks"]:
        for dep in t["depends_on"]:
            if dep not in tasks:
                out.append(Finding("DEPENDENCY_UNKNOWN", "error", t["id"], f"depends on undeclared task {dep}"))
            elif t["status"] in ("done", "running") and tasks[dep]["status"] not in satisfied:
                out.append(Finding("DEPENDENCY_INCOMPLETE", "error", t["id"], f"started/finished before dependency {dep} was complete"))
        for inp in t["inputs"]:
            full, err = _resolve_inside(workspace, inp["path"])
            if err:
                out.append(err)
            elif not full.exists() or sha256_bytes(full.read_bytes()) != inp["sha256"]:
                out.append(Finding("TASK_INPUT_HASH_MISMATCH", "error", t["id"], f"input {inp['path']} differs from the frozen hash"))
    # cycles
    visiting, done = set(), set()

    def dfs(n):
        if n in done or n not in tasks:
            return False
        if n in visiting:
            return True
        visiting.add(n)
        cyc = any(dfs(d) for d in tasks[n]["depends_on"])
        visiting.discard(n)
        done.add(n)
        return cyc

    if any(dfs(n) for n in tasks):
        out.append(Finding("DEPENDENCY_CYCLE", "error", "RUN_STATE.json", "task dependencies contain a cycle"))
    # disjoint write sets
    owner: dict[str, str] = {}
    for t in state["tasks"]:
        for w in t["write_set"]:
            key, err = _path_key(workspace, w)
            if err:
                out.append(err)
                continue
            if key in owner and owner[key] != t["id"]:
                out.append(Finding("WRITE_SET_OVERLAP", "error", w, f"assigned to both {owner[key]} and {t['id']}"))
            owner[key] = t["id"]
    return out


def _path_key(workspace: Path, rel: str) -> tuple[Optional[str], Optional[Finding]]:
    """Ownership key: the resolved workspace path, case-folded on case-insensitive filesystems (normcase)."""
    full, err = _resolve_inside(workspace, rel)
    return (None, err) if err else (os.path.normcase(str(full)), None)


# ------------------------------------------------------- declared A-E routes
_NOT_RUN = {"not_requested", "not_applicable"}
# Each rule: (role, mode) must be an ancestor of (role, mode) whenever both exist in the run.
ROUTES = {
    "A": {"required": [("sub-offer", "proposal"), ("sub-pricing", "final_feasibility")],
          "order": [(("sub-offer", "proposal"), ("sub-value", "audit")),
                    (("sub-offer", "proposal"), ("sub-pricing", "final_feasibility")),
                    (("sub-value", "audit"), ("sub-pricing", "final_feasibility"))]},
    "B": {"required": [("sub-value", "diagnostic"), ("sub-offer", "revision"),
                       ("sub-value", "revised_check"), ("sub-pricing", "final_feasibility")],
          "order": [(("sub-value", "diagnostic"), ("sub-offer", "revision")),
                    (("sub-offer", "revision"), ("sub-value", "revised_check")),
                    (("sub-offer", "revision"), ("sub-pricing", "final_feasibility")),
                    (("sub-value", "revised_check"), ("sub-pricing", "final_feasibility"))]},
    "D": {"required": [("sub-offer", "revision"), ("sub-pricing", "final_feasibility")],
          "order": [(("sub-pricing", "packaging_exploration"), ("sub-offer", "revision")),
                    (("sub-offer", "revision"), ("sub-value", "revised_check")),
                    (("sub-offer", "revision"), ("sub-pricing", "final_feasibility")),
                    (("sub-value", "revised_check"), ("sub-pricing", "final_feasibility"))]},
    "C": {"required": [], "order": []},
    "E": {"required": [], "order": []},
}
PRICED_STAGES = ("A", "B", "D")


def _norm_path(p: str) -> str:
    return p.replace("\\", "/")


def _ancestors(tasks: dict, tid: str) -> set:
    seen, stack = set(), list(tasks[tid]["depends_on"])
    while stack:
        n = stack.pop()
        if n in seen or n not in tasks:
            continue
        seen.add(n)
        stack.extend(tasks[n]["depends_on"])
    return seen


def _check_inputs(state, brief) -> list[Finding]:
    """A task reads only brief sources and the frozen outputs of its declared dependencies."""
    out, tasks = [], {t["id"]: t for t in state["tasks"]}
    sources = {_norm_path(s["path"]) for s in brief["sources"]} if brief else set()
    for t in state["tasks"]:
        if t["status"] not in ("done", "running"):
            continue
        have = {_norm_path(i["path"]) for i in t["inputs"]}
        for dep in t["depends_on"]:
            d = tasks.get(dep)
            if d is None or d["status"] != "done":
                continue
            for w in d["write_set"]:
                if _norm_path(w) not in have:
                    out.append(Finding("INPUT_UNBOUND", "error", t["id"], f"output {w} of dependency {dep} is not frozen as a hashed input"))
        allowed = set(sources)
        for a in _ancestors(tasks, t["id"]):
            allowed |= {_norm_path(w) for w in tasks[a]["write_set"]}
        for path in sorted(have - allowed):
            if brief:
                out.append(Finding("INPUT_UNDECLARED", "error", t["id"], f"input {path} is neither a brief source nor the output of a declared dependency"))
    return out


def _matching(state, role, mode):
    return [t for t in state["tasks"] if t["role"] == role and t.get("mode") == mode and t["status"] not in _NOT_RUN]


def _check_routes(state, brief, mode) -> list[Finding]:
    if not brief:
        return []
    stage = brief["stage"]
    route, out = ROUTES[stage], []
    tasks = {t["id"]: t for t in state["tasks"]}
    for before, after in route["order"]:
        for a in _matching(state, *after):
            for b in _matching(state, *before):
                if b["id"] not in _ancestors(tasks, a["id"]):
                    out.append(Finding("ROUTE_ORDER_VIOLATION", "error", a["id"], f"stage {stage}: {before[1]} ({b['id']}) must be a declared dependency of {after[1]}"))
    if stage in PRICED_STAGES:
        for sales in (t for t in state["tasks"] if t["role"] == "sub-sales" and t["status"] not in _NOT_RUN):
            for p in _matching(state, "sub-pricing", "final_feasibility"):
                if p["id"] not in _ancestors(tasks, sales["id"]):
                    out.append(Finding("ROUTE_ORDER_VIOLATION", "error", sales["id"], f"stage {stage}: copy must follow final pricing {p['id']}"))
    if stage == "C":
        for t in state["tasks"]:
            if t["role"] in ("sub-market", "sub-offer", "sub-pricing") and t["status"] not in _NOT_RUN:
                out.append(Finding("ROUTE_COPY_ONLY_REWORKS_TERMS", "error", t["id"], "stage C is copy-only; terms, pricing and market work stay as authorized"))
    if stage == "B":
        frozen = {(_norm_path(s["path"]), s["sha256"]) for s in brief["sources"]}
        for t in _matching(state, "sub-value", "diagnostic"):
            if t["status"] == "done" and not any((_norm_path(i["path"]), i["sha256"]) in frozen for i in t["inputs"]):
                out.append(Finding("ORIGINAL_SNAPSHOT_NOT_AUDITED", "error", t["id"], "the diagnostic must read the frozen original offer, not a later or pre-existing file"))
    if mode == "ready":
        if stage == "C" and not any(t["role"] == "sub-sales" and t["status"] == "done" for t in state["tasks"]):
            out.append(Finding("ROUTE_TASK_MISSING", "error", "RUN_STATE.json", "stage C needs a completed sub-sales task"))
        for role, md in route["required"]:
            if not any(t["role"] == role and t.get("mode") == md and t["status"] == "done" for t in state["tasks"]):
                out.append(Finding("ROUTE_TASK_MISSING", "error", "RUN_STATE.json", f"stage {stage} requires a completed {role} task in mode '{md}'"))
    return out


def _check_receipts(state, workspace) -> list[Finding]:
    """Checkpoint and QA receipts are bound to file bytes and the decision version."""
    out = []
    for key, code in (("checkpoint", "CHECKPOINT_STALE"), ("qa_receipt", "QA_RECEIPT_STALE")):
        rec = state.get(key)
        if not rec:
            continue
        full, err = _resolve_inside(workspace, rec["path"])
        if err:
            out.append(err)
        elif not full.exists() or sha256_bytes(full.read_bytes()) != rec["sha256"]:
            out.append(Finding(code, "error", rec["path"], "file is missing or its bytes changed since the receipt was bound"))
        elif rec["decision_version"] != state["decision_version"]:
            out.append(Finding(code, "error", rec["path"], "receipt was bound to a different decision version"))
    if state["qa_result"] == "pass" and not state.get("qa_receipt"):
        out.append(Finding("QA_RECEIPT_MISSING", "error", "RUN_STATE.json", "qa_result 'pass' needs a hash-bound QA receipt"))
    return out


def _check_routing(state) -> list[Finding]:
    out = []
    for r in state.get("routing", []):
        if not r["observed_model"].strip() or not r["observed_effort"].strip():
            out.append(Finding("ROUTING_OBSERVATION_EMPTY", "error", r["task"], "use 'unknown' when the runtime supplies no observation; never blank or copy the request"))
    return out


def _check_artifacts(state, decisions, claims, brief, workspace, mode) -> list[Finding]:
    out: list[Finding] = []
    tasks = {t["id"]: t for t in state["tasks"]}
    fields = decisions["fields"] if decisions else {}
    ledger = {c["id"]: c for c in claims["claims"]} if claims else {}
    manifest_paths = set()

    for art in state["artifacts"]:
        path = art["path"]
        manifest_paths.add(_norm_path(path))
        full, err = _resolve_inside(workspace, path)
        if err:
            out.append(err)
            continue
        if not full.exists():
            out.append(Finding("ARTIFACT_MISSING", "error", path, "manifest lists a file that does not exist"))
            continue
        data = full.read_bytes()
        text = data.decode("utf-8", errors="replace")
        if sha256_bytes(data) != art["sha256"]:
            out.append(Finding("ARTIFACT_HASH_MISMATCH", "error", path, "bytes differ from the manifest hash; acceptance invalidated"))
        if art["decision_version"] != state["decision_version"]:
            out.append(Finding("ARTIFACT_DECISION_STALE", "error", path, "built against an older decision version"))
        task = tasks.get(art["task"])
        if task is not None and mode == "ready" and task["status"] != "done":
            out.append(Finding("ARTIFACT_PRODUCER_INCOMPLETE", "error", path, f"producing task {art['task']} is {task['status']}, not done"))
        if task is None:
            out.append(Finding("ARTIFACT_TASK_UNKNOWN", "error", path, f"task {art['task']} is not declared"))
        elif os.path.normcase(str(full)) not in {k for k, _ in (_path_key(workspace, w) for w in task["write_set"]) if k}:
            # an empty write_set means "writes nothing", so it can never own an artifact
            out.append(Finding("ARTIFACT_OUTSIDE_WRITE_SET", "error", path, "artifact is outside the producing task's write set"))

        # ready mode checks every manifest artifact; draft mode only those declared ready
        if mode == "draft" and not art.get("ready", False):
            continue
        if PLACEHOLDER.search(text):
            out.append(Finding("PLACEHOLDER_IN_READY", "error", path, "ready asset still contains placeholder text"))
        out += _check_bindings(art, fields, text, path)
        out += _check_claims(art, ledger, text, path)
        if mode == "ready":
            out += _check_review(art, state, path)

    if brief:
        for req in brief["requested_artifacts"]:
            # exact path: a bare name means output/<name>; never match on basename alone
            wanted = _norm_path(req)
            wanted = wanted[2:] if wanted.startswith("./") else wanted
            if mode == "ready" and wanted not in manifest_paths and f"output/{wanted}" not in manifest_paths:
                out.append(Finding("REQUESTED_ARTIFACT_MISSING", "error", req, "requested artifact is not in the output manifest"))
    return out


# ------------------------------------------------------ canonical owner summary
# A full run ends with output/SUMMARY.md, declared in the manifest like any other artifact (hash, decision version and
# review are the ordinary artifact checks). Only structure is checked here: whether the chosen hook is the right one and
# the three actions are good stays with the semantic review. An honest "unknown" or "held" is valid text.
SUMMARY_PATH = "output/SUMMARY.md"
SUMMARY_SECTIONS = ("offer", "key decisions", "best hook", "next actions")
_SPECIALIST_ROLES = {"sub-market", "sub-offer", "sub-value", "sub-pricing", "sub-sales"}
_SUMMARY_REQUESTS = {"output/summary.md", "output/owner_summary.md"}
# Known bookkeeping only: the JSON controls, the fixed checkpoint/QA/review file names and the receipt paths the run declares.
# Any other name, review- or receipt-flavoured or not, is a business output and counts.
_BOOKKEEPING_NAMES = {n.casefold() for n in CONTROL} | {"checkpoint.md", "qa_report.md", "review.md"}
_HOOK_LABEL_WORDS = {"see", "refer", "reference", "per", "in", "from", "at", "to", "for", "source", "link", "file", "chosen",
                     "selected", "best", "final", "winning", "hook", "hooks", "the", "our", "is", "are", "above", "below", "also"}
_HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*$")
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_REFERENCE = re.compile(r"!?\[[^\]]*\]\([^)]*\)|https?://\S+|(?:[\w.~-]+[/\\])*[\w.-]+\.(?:md|markdown|txt|json|docx?|pdf|html?)\b", re.I)
_ORDERED_ITEM = re.compile(r"^( {0,3})(\d{1,9})[.)](?:[ \t]+(.*))?$")


def _request_key(req: str) -> str:
    """Equivalent spellings of one workspace output (bare, output/, ./, backslashes) share one key."""
    p = _norm_path(req).strip()
    while p.startswith("./"):
        p = p[2:]
    p = p if "/" in p else f"output/{p}"
    return os.path.normcase(p).replace("\\", "/")  # identity follows the platform, as artifact paths do


def _is_bookkeeping(key: str, declared: set) -> bool:
    return key.startswith("output/runs/") or key in declared or key.rsplit("/", 1)[-1].casefold() in _BOOKKEEPING_NAMES


def _summary_required(state, brief) -> bool:
    keys = {_request_key(r) for r in brief["requested_artifacts"]} if brief else set()
    if {k.casefold() for k in keys} & _SUMMARY_REQUESTS or (brief and brief["stage"] in PRICED_STAGES):
        return True
    if sum(1 for t in state["tasks"] if t["role"] in _SPECIALIST_ROLES and t["status"] not in _NOT_RUN) >= 2:
        return True
    declared = {_request_key(state[k]["path"]) for k in ("checkpoint", "qa_receipt") if state.get(k)}
    business = {k for k in keys if not _is_bookkeeping(k, declared)}
    return len(business) > 1


def _visible_lines(text: str) -> list[str]:
    """Lines outside HTML comments and fenced code blocks, with inline comments removed."""
    out, fence, in_comment = [], None, False
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if in_comment:
            if "-->" not in line:
                continue
            line, in_comment = line.split("-->", 1)[1], False
        if fence:
            if re.match(rf"^ {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*$", line):
                fence = None
            continue
        m = _FENCE.match(line)
        if m:
            fence = m.group(1)
            continue
        line = re.sub(r"<!--.*?-->", "", line)
        if "<!--" in line:
            line, in_comment = line.split("<!--", 1)[0], True
        out.append(line)
    return out


def _sections(text: str) -> dict[str, list[list[str]]]:
    """Level-two sections by lower-cased heading; a section ends at the next level-one or level-two heading."""
    found: dict[str, list[list[str]]] = {}
    current = None
    for line in _visible_lines(text):
        m = _HEADING.match(line)
        if m and len(m.group(1)) <= 2:
            name = re.sub(r"(?:^|[ \t]+)#+[ \t]*$", "", m.group(2) or "").strip().casefold()
            current = None
            if len(m.group(1)) == 2 and name in SUMMARY_SECTIONS:
                current = []
                found.setdefault(name, []).append(current)
            continue
        if current is not None:
            current.append(line)
    return found


def _summary_content_findings(text: str) -> list[Finding]:
    out, found = [], _sections(text)

    def bad(code, why):
        out.append(Finding(code, "error", SUMMARY_PATH, why))

    for name in SUMMARY_SECTIONS:
        n = len(found.get(name, []))
        if n == 0:
            bad("SUMMARY_SECTION_MISSING", f"missing level-two '## {name.title()}' section outside comments and code fences")
        elif n > 1:
            bad("SUMMARY_SECTION_DUPLICATE", f"'## {name.title()}' appears {n} times; exactly one is required")
        elif not any(l.strip() for l in found[name][0]):
            bad("SUMMARY_SECTION_EMPTY", f"'## {name.title()}' has no visible content")
    hook = found.get("best hook", [])
    if len(hook) == 1 and any(l.strip() for l in hook[0]):
        paras, cur = [], []
        for l in hook[0] + [""]:
            l = re.sub(r"^\s*(?:>\s?)*", "", l)
            if l.strip():
                cur.append(l)
            elif cur:
                paras.append(" ".join(cur))
                cur = []

        def states_a_hook(para):
            stripped = _REFERENCE.sub(" ", para)
            if stripped != para:  # a paragraph that only labels a file or link is not hook text
                return any(w not in _HOOK_LABEL_WORDS for w in re.findall(r"\w+", stripped.casefold()))
            return bool(re.search(r"\w", para))
        if not any(states_a_hook(p) for p in paras):
            bad("SUMMARY_HOOK_UNSTATED", "Best Hook must state the chosen hook text, not only point at a file or link")
    actions = found.get("next actions", [])
    if len(actions) == 1 and any(l.strip() for l in actions[0]):
        # top-level items share the first marker's 0..3-space indent; deeper markers and every other line are wrapped or
        # nested explanation and never fill an item, so the action text must sit on its own marker line
        items: list[list[str]] = []
        base = None
        for line in actions[0]:
            m = _ORDERED_ITEM.match(line)
            if m and base in (None, len(m.group(1))):
                base = len(m.group(1))
                items.append([m.group(2), m.group(3) or ""])
        if [i[0] for i in items] != ["1", "2", "3"] or not all(re.search(r"\w", i[1]) for i in items):
            bad("SUMMARY_ACTIONS_INVALID", "Next Actions needs exactly three substantive top-level ordered items numbered 1, 2, 3")
    return out


def _check_summary(state, brief, workspace, mode) -> list[Finding]:
    """The canonical output/SUMMARY.md must be a real file, declared in the manifest, and well-formed."""
    want, _ = _path_key(workspace, SUMMARY_PATH)
    full, _ = _resolve_inside(workspace, SUMMARY_PATH)
    entries = [a for a in state["artifacts"] if _path_key(workspace, a["path"])[0] == want]
    exists = full is not None and full.is_file()
    out: list[Finding] = []
    if mode == "ready" and _summary_required(state, brief):
        if not exists:
            out.append(Finding("SUMMARY_MISSING", "error", SUMMARY_PATH, "a full run needs the canonical output/SUMMARY.md; aliases and nested files do not count"))
        elif not entries:
            out.append(Finding("SUMMARY_NOT_IN_MANIFEST", "error", SUMMARY_PATH, "output/SUMMARY.md exists but no manifest artifact declares it"))
    # content is judged whenever the manifest declares the file; ready mode does not let artifact.ready=false skip it
    if exists and any(mode == "ready" or a.get("ready", False) for a in entries):
        out += _summary_content_findings(full.read_text(encoding="utf-8", errors="replace"))
    return out


def _check_bindings(art, fields, text, path) -> list[Finding]:
    out = [Finding("BINDING_FIELD_DUPLICATE", "error", path, f"field '{d}' is bound more than once; only one registered rendering per field is allowed")
           for d in _duplicates(b["field"] for b in art.get("bindings", []))]
    bound = {b["field"]: b for b in art.get("bindings", [])}
    for name in art.get("uses_fields", []):
        field = fields.get(name)
        if field is None or field["status"] != "approved":
            out.append(Finding("FIELD_NOT_APPROVED", "error", path, f"field '{name}' is {'absent' if field is None else field['status']}; unknown is not zero and unapproved terms cannot ship"))
            continue
        if not field.get("authorization_ref"):
            out.append(Finding("APPROVAL_REF_MISSING", "error", path, f"approved field '{name}' has no authorization_ref"))
        b = bound.get(name)
        if b is None:
            out.append(Finding("BINDING_MISSING", "error", path, f"uses '{name}' without binding it to rendered text"))
            continue
        display = field.get("display")
        if field.get("kind") == "money" and isinstance(field.get("value"), dict):
            for label, rendered in (("display", display), ("binding", b["rendered_text"])):
                if rendered is not None:
                    out += [Finding("MONEY_RENDER_MISMATCH", "error", path, f"'{name}' {label}: {why}") for why in _money_problems(field["value"], rendered)]
        for cond in field.get("conditions", []):
            if _norm(cond) not in _norm(b["rendered_text"]):
                out.append(Finding("GUARANTEE_CONDITION_MISSING", "error", path, f"rendered terms for '{name}' omit required condition: {cond}"))
        # Authoritative wording: explicit display, else a scalar string value. Money with a structured value is
        # checked deterministically above; anything else with neither has no canonical rendering to compare to.
        canon = display
        if canon is None and isinstance(field.get("value"), str) and field["value"].strip():
            canon = field["value"]
        if canon is None and not (field.get("kind") == "money" and isinstance(field.get("value"), dict)):
            out.append(Finding("CANONICAL_RENDERING_MISSING", "error", path, f"approved field '{name}' has no display and no scalar value to derive its canonical wording from"))
        if canon is not None and b["rendered_text"] != canon:
            out.append(Finding("BINDING_DISPLAY_MISMATCH", "error", path, f"binding for '{name}' differs from the canonical wording"))
        if b["rendered_text"] not in text:
            out.append(Finding("BINDING_TEXT_MISSING", "error", path, f"canonical wording for '{name}' does not appear in the artifact"))
    for name, b in bound.items():
        if name not in art.get("uses_fields", []):
            out.append(Finding("BINDING_MISSING", "error", path, f"binding for '{name}' is not declared in uses_fields"))
    return out


# Minor-unit exponent per supported currency (ISO 4217: JPY has 0 minor-unit digits, per the SIX maintenance agency
# and Adyen's currency-code docs). Only these are supported; a canonical currency absent here fails closed rather
# than being assumed to have two decimals. This is a small explicit table, not a currency engine: the schema may
# admit more codes than this checker can verify, and those hold (known limitation).
_CCY_EXPONENT = {c: 2 for c in ("USD", "EUR", "GBP", "CAD", "AUD", "NZD", "MXN", "SGD", "HKD", "CHF", "INR", "BRL", "SEK", "NOK", "DKK", "ZAR", "AED")}
_CCY_EXPONENT["JPY"] = 0
_KNOWN_CCY = set(_CCY_EXPONENT)
_SYMBOL_CCY = {"$": {"USD", "CAD", "AUD", "NZD", "MXN", "SGD", "HKD"}, "\u20ac": {"EUR"}, "\u00a3": {"GBP"}}
# A trailing code is a lookahead and only belongs to this amount when it is not itself the prefix of the next one,
# so a code is never consumed away from the following amount; whitespace of any kind/width may separate token and number.
# A sign (ASCII hyphen, minus, figure/en/em dash, small/fullwidth hyphen-minus) may precede the code, symbol or number.
_SG = r"[-\u2212\u2012\u2013\u2014\ufe63\uff0d]"
_AMOUNT = re.compile(
    rf"(?:(?P<s1>{_SG}\s*))?(?:\b(?P<pre>[A-Z]{{3}})\s*)?(?:(?P<s2>{_SG}\s*))?(?:(?P<sym>[$\u20ac\u00a3])\s*)?(?:(?P<s3>{_SG}\s*))?"
    rf"(?P<num>\d[\d,]*(?:\.\d+)?)(?![\d,])(?=(?:\s*\b(?P<post>[A-Z]{{3}})\b(?!\s*{_SG}?\s*[$\u20ac\u00a3]?\s*{_SG}?\s*\d))?)")
_CADENCE_WORDS = {
    "one_time": r"one[- ]time|\bonce\b|single payment|upfront|lump[- ]sum",
    "monthly": r"monthly|per month|a month|/\s?mo\b|each month|every month",
    "quarterly": r"quarterly|per quarter|a quarter|each quarter",
    "yearly": r"yearly|annual|per year|a year|/\s?yr\b|each year|every year",
    "per_unit": r"per (?!month|year|quarter)[a-z]+|each (?!month|year|quarter)[a-z]+|/\s?(?:seat|user|unit)\b",
}


def _money_problems(value: dict, rendered: str) -> list[str]:
    """Deterministic rendering check: every currency-marked amount, its currency and the cadence wording
    in `rendered` must equal the structured money value. Unrelated example amounts live in prose, not in a bound rendering."""
    from decimal import Decimal
    ccy, cadence = value["currency"], value["cadence"]
    if ccy not in _CCY_EXPONENT:
        return [f"currency {ccy} has no supported minor-unit exponent; a rendering of it cannot be verified here"]
    want = Decimal(value["amount_minor"]).scaleb(-_CCY_EXPONENT[ccy])
    amounts, signed = [], []
    for m in _AMOUNT.finditer(rendered):
        pre, sym, num, post = m["pre"], m["sym"], m["num"], m["post"]
        codes_ = {c for c in (pre, post) if c in _KNOWN_CCY}
        if not sym and not codes_:
            continue  # bare number or unknown letters: not a currency-marked amount
        # A canonical amount is never negative: any sign attached to the amount, its code or its symbol is held, and so
        # is a spaced sign mid-line (ambiguous). The one exception is a bare ASCII hyphen + blanks opening its line
        # (behind optional blockquote markers): that is a Markdown list bullet, not a minus.
        for g in ("s1", "s2", "s3"):
            sg = m[g]
            if sg is None:
                continue
            if g == "s1" and sg[0] == "-" and sg[1:] != "" and not sg[1:].strip() and "\n" not in sg \
                    and not rendered[rendered.rfind("\n", 0, m.start("s1")) + 1:m.start("s1")].strip(" \t>"):
                continue
            signed.append(num)
        amounts.append((codes_, sym, Decimal(num.replace(",", ""))))
    if not amounts:
        return [f"no currency-marked amount; expected {ccy} {want.normalize():,f}"]
    problems = [f"negative or sign-prefixed amount {n}; a canonical amount is non-negative" for n in signed]
    for codes_, sym, amt in amounts:
        if amt != want:
            problems.append(f"amount {amt.normalize():,f} differs from canonical {want.normalize():,f}")
        # an explicit code outranks the bare-symbol assumption; codes and symbol must also agree with each other
        for code in sorted(codes_):
            if code != ccy:
                problems.append(f"currency {code} differs from canonical {ccy}")
            if sym and code not in _SYMBOL_CCY[sym]:
                problems.append(f"currency {code} contradicts symbol {sym}")
        if sym and not codes_ and ccy not in _SYMBOL_CCY[sym]:
            problems.append(f"symbol {sym} does not denote canonical {ccy}")
    found = {k for k, rx in _CADENCE_WORDS.items() if re.search(rx, rendered, re.I)}
    if cadence not in found:
        problems.append(f"cadence '{cadence}' is not stated")
    for other in sorted(found - {cadence}):
        problems.append(f"cadence wording for '{other}' conflicts with canonical '{cadence}'")
    return problems


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower().rstrip(".")


def _check_claims(art, ledger, text, path) -> list[Finding]:
    out, haystack = [], _norm(text)
    for cid in art.get("claim_ids", []):
        c = ledger.get(cid)
        if c is None:
            out.append(Finding("CLAIM_ID_UNKNOWN", "error", path, f"claim {cid} is not in CLAIMS.json"))
            continue
        if c["status"] in BLOCKING_CLAIMS:
            out.append(Finding("CLAIM_UNSUPPORTED_IN_READY", "error", path, f"claim {cid} is {c['status']}"))
        if c["status"] == "hypothesis":
            out.append(Finding("CLAIM_HYPOTHESIS_IN_READY", "error", path, f"claim {cid} is only a hypothesis"))
        if c["status"] == "qualified":
            missing = [q for q in c["qualifications"] if _norm(q) not in haystack]
            if missing:
                out.append(Finding("CLAIM_QUALIFICATION_REMOVED", "error", path, f"claim {cid} lost qualification(s): {missing}"))
    # ledger entries that are blocked must not appear even when the artifact forgot to list them
    for cid, c in ledger.items():
        if c["status"] in BLOCKING_CLAIMS and _norm(c["wording"]) in haystack:
            out.append(Finding("CLAIM_UNSUPPORTED_IN_READY", "error", path, f"blocked claim {cid} wording appears in the artifact"))
    return out


def _check_review(art, state, path) -> list[Finding]:
    match = [r for r in state["reviews"]
             if r["artifact"].replace("\\", "/") == path.replace("\\", "/")
             and r["artifact_sha256"] == art["sha256"]
             and r["decision_version"] == state["decision_version"]
             and r["result"] == "pass"]
    if not match:
        return [Finding("REVIEW_STALE_OR_MISSING", "error", path, "no passing semantic review bound to this artifact hash and decision version")]
    if art.get("high_risk") and not any(r["context"] == "separate" for r in match):
        return [Finding("HIGH_RISK_NO_INDEPENDENT_REVIEW", "error", path, "high-risk readiness requires a separate-context reviewer; hold otherwise")]
    return []


# ------------------------------------------------------------------ repo checks
def _frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return None
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def validate_repo(repo_root: Path) -> list[Finding]:
    repo = Path(repo_root)
    out: list[Finding] = []
    fixture = repo / "tests" / "fixtures" / "expected_inventory.json"
    expected = json.loads(fixture.read_text(encoding="utf-8")) if fixture.exists() else None

    for sk in sorted((repo / "skills").glob("*/SKILL.md")):
        out += _check_frontmatter(sk, sk.parent.name)
    for ag in sorted((repo / "agents").glob("*.md")):
        out += _check_frontmatter(ag, ag.stem)

    if expected:
        have_s = {p.parent.name for p in (repo / "skills").glob("*/SKILL.md")}
        have_a = {p.stem for p in (repo / "agents").glob("*.md")}
        for s in expected["original_skills"]:
            if s not in have_s:
                out.append(Finding("INVENTORY_MISSING", "error", f"skills/{s}", "original skill entrypoint is missing"))
        for a in expected["original_agents"]:
            if a not in have_a:
                out.append(Finding("INVENTORY_MISSING", "error", f"agents/{a}.md", "original agent is missing"))
        for rel, digest in expected["unchanged_sha256"].items():
            p = repo / rel
            if not p.exists() or protected_text_hash(p.read_bytes()) != digest:
                out.append(Finding("PROTECTED_FILE_CHANGED", "error", rel, "file must stay byte-identical to the upstream baseline"))

    cdir = repo / "contracts"
    for name in CONTROL.values():
        p = cdir / f"{name}.schema.json"
        if not p.exists():
            out.append(Finding("SCHEMA_INVALID", "error", str(p.name), "schema file missing"))
            continue
        try:
            Draft202012Validator.check_schema(json.loads(p.read_text(encoding="utf-8")))
        except Exception as exc:  # SchemaError or JSON error
            out.append(Finding("SCHEMA_INVALID", "error", p.name, str(exc).splitlines()[0]))
    return out


def _check_frontmatter(path: Path, expected_name: str) -> list[Finding]:
    fm = _frontmatter(path)
    rel = f"{path.parent.name}/{path.name}"
    if fm is None or not str(fm.get("description", "")).strip():
        return [Finding("FRONTMATTER_INVALID", "error", rel, "frontmatter missing, unparsable or lacks a description")]
    if fm.get("name") != expected_name:
        return [Finding("FRONTMATTER_NAME_MISMATCH", "error", rel, f"name {fm.get('name')!r} != {expected_name!r}")]
    return []


# -------------------------------------------------------------------------- CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, help="validate repository inventory and contracts")
    ap.add_argument("--run", type=Path, help="validate output/runs/<run_id>")
    ap.add_argument("--workspace", type=Path, default=Path("."))
    ap.add_argument("--mode", choices=["draft", "ready"], default="ready")
    ap.add_argument("--json", action="store_true", help="print findings as JSON")
    args = ap.parse_args(argv)
    if _IMPORT_ERROR is not None:
        print(f"check_outputs: missing dependency ({_IMPORT_ERROR}); pip install -r requirements-qa.txt", file=sys.stderr)
        return EXIT_TOOL_FAILURE
    if not args.repo and not args.run:
        ap.error("give --repo and/or --run")
    try:
        findings: list[Finding] = []
        if args.repo:
            findings += validate_repo(args.repo)
        if args.run:
            if not args.run.is_dir():
                print(f"check_outputs: run directory not found: {args.run}", file=sys.stderr)
                return EXIT_TOOL_FAILURE
            findings += validate_run(args.run, args.workspace, args.mode)
    except (OSError, ValueError) as exc:
        print(f"check_outputs: tool failure: {exc}", file=sys.stderr)
        return EXIT_TOOL_FAILURE
    errors = [f for f in findings if f.severity == "error"]
    if args.json:
        print(json.dumps([f.as_dict() for f in findings], indent=2))
    else:
        for f in findings:
            print(f"[{f.severity}] {f.code} {f.artifact}: {f.reason}")
        print("PASS" if not errors else f"HELD: {len(errors)} finding(s)")
    return EXIT_HELD if errors else EXIT_PASS


if __name__ == "__main__":
    sys.exit(main())

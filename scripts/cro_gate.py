#!/usr/bin/env python3
"""Deterministic, read-only planning helper for the root-owned CRO waterfall.

This chooses *whether* and *at what depth* CRO belongs in an offer run.
It does not create tasks, write state, infer business truth, or clear any hold.
No schema, role, phase or task mode changes are required.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

STAGES = {"A", "B", "C", "D", "E"}
SURFACES = {"live", "planned", "offline", "unknown"}


@dataclass(frozen=True)
class CroGate:
    required: bool
    depth: str
    artifact: str | None
    reason: str


def choose_cro_gate(
    stage: str,
    surface: str = "unknown",
    *,
    focused: bool = False,
    offer_workflow: bool = True,
    digital_destination: bool = False,
) -> CroGate:
    """Return a routing recommendation; it is not a RUN_STATE task mode.

    'surface' must be based on the user's actual brief, not guessed from source
    keywords. An unknown surface gets a readiness preflight, not fake page QA.
    """
    if stage not in STAGES:
        raise ValueError("stage must be one of A, B, C, D, E")
    if surface not in SURFACES:
        raise ValueError("surface must be live, planned, offline or unknown")
    if focused:
        return CroGate(False, "focused_skip", None, "A focused single-skill request does not trigger full CRO QA.")
    eligible = stage in {"A", "B", "D"} or (stage == "E" and offer_workflow) or (stage == "C" and digital_destination)
    if not eligible:
        return CroGate(False, "not_applicable", None, "No full offer workflow or digital conversion destination in scope.")
    if surface == "live":
        return CroGate(True, "full_page", "output/CRO_REVIEW.md", "Review the existing page/funnel using actual supplied evidence.")
    if surface == "planned" or surface == "unknown":
        return CroGate(True, "readiness", "output/CRO_REVIEW.md", "Review offer-to-conversion readiness; page-specific claims are NOT ASSESSED.")
    return CroGate(True, "buyer_handoff", "output/CRO_REVIEW.md", "Offline buyer handoff; website and SEO checks are NOT APPLICABLE.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan the read-only downstream CRO gate for an offer workflow")
    parser.add_argument("--stage", choices=sorted(STAGES), required=True)
    parser.add_argument("--surface", choices=sorted(SURFACES), default="unknown")
    parser.add_argument("--focused", action="store_true")
    parser.add_argument("--no-offer-workflow", action="store_true", help="Stage E is not an offer workflow")
    parser.add_argument("--digital-destination", action="store_true", help="Stage C includes a digital conversion destination")
    args = parser.parse_args(argv)
    gate = choose_cro_gate(
        args.stage, args.surface,
        focused=args.focused,
        offer_workflow=not args.no_offer_workflow,
        digital_destination=args.digital_destination,
    )
    print(json.dumps(asdict(gate), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

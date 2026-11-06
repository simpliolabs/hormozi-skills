## Developer native test drive: requested, not yet run

[DEV execution request posted on this PR](https://github.com/simpliolabs/hormozi-skills/pull/5#issuecomment-6672008001). GitHub Issues are disabled, so the request is tracked in the PR conversation. The candidate includes a [fictional DeskFern Studio fixture](docs/qa/pr5-fictional-business/BUSINESS_FIXTURE.md), [four exact native scenarios](docs/qa/pr5-fictional-business/TEST_DRIVE.md), an [intentionally flawed local page](docs/qa/pr5-fictional-business/demo_landing.html), and a [blank result scorecard](docs/qa/pr5-fictional-business/RESULTS_TEMPLATE.md). None of the native results are prefilled or claimed to have passed.

**[CI at current test-fixture HEAD 6b7a04e](https://github.com/simpliolabs/hormozi-skills/actions/runs/42128049903) passed Ubuntu and Windows.** Native auto-routing, independent specialist dispatch and real token efficiency remain pending actual developer evidence. No merge/publish authority implied.

## Purpose
Add a reusable, evidence-led **CRO Page Optimizer** to Hormozi Skills and put it into the **upstream → sales → downstream CRO → QA** waterfall by default during full offer workflows, **even if the owner never requests CRO by name**.

**Stacked on draft PR #4** (`docs/repo-onboarding-review-2026-11-05`) so the updated README, owner/social sections and visible graphics are preserved. Review and merge PR #4 first; after that, retarget this PR to `main` and re-run tests.

## What changed (19 files)
- New `skills/cro-page-optimizer/SKILL.md` with generalizable six-gate SEO/CRO, mobile UX, Clarity/analytics diagnosis, fix-versus-experiment decisions, and explicit evidence/approval holds.
- New public `CRO_FRAMEWORK.md`, no CEO Creative-specific pricing, brand rules, or private data.
- New `references/cro-waterfall.md` as the root-owned stage policy; instructions added to **both** `hormozi-orchestrator` entrypoints and the shared A-E routing guide.
- New read-only `scripts/cro_gate.py` for deterministic eligibility/depth, plus regression tests.
- A visible `assets/readme/cro-waterfall.svg` and README/first-use updates explaining the automatic gate, direct invocation, and upstream feedback rules.
- Beginner/expert adaptive routing: one-question guided intake or precise focused skill requests, **not** automatic execution of every Hormozi skill.
- Added `references/adaptive-routing.md`, [Start Here](docs/START_HERE.md) and `assets/readme/choose-your-path.svg`, with progressive method loading, frozen briefs and valid-checkpoint reuse.
- Added 7 selective-routing regression tests and extended the legacy output-name integrity test only to include `CRO_REVIEW.md`.
- Updated proposed repository About text to include SEO/CRO.

### Scope and default behavior

| Route | Default CRO behavior |
|---|---|
| Stage A/B/D full offer | Mandatory root-owned CRO readiness, even if unrequested |
| Stage E multi-step offer | Mandatory root-owned CRO readiness |
| Stage C with digital destination | CRO readiness after sales |
| Live page with evidence | Full page/funnel audit |
| New offer with no page | Readiness preflight; no imaginary mobile/Clarity data |
| Offline offer | Minimal buyer-handoff audit, SEO/page checks NOT APPLICABLE |
| One focused skill task | No forced full-run QA |

The root adds `CRO_REVIEW.md` to the brief and its write set, runs the actual CRO skill after accepted pricing/sales work, before SUMMARY and structural checks, and carries source-bound findings into records and owner actions. Any proposed material upstream revision requires approval and downstream revalidation. **Not** a new `sub-cro` role or `mode: cro`.

## Non-regression scope
- No change to `scripts/check_outputs.py`, four schemas, the original 17 skill method bodies or five specialist roles.
- No alteration to the PR #3 seven-obligation acceptance evidence, canonical SUMMARY headings, commercial decision authority, or independent-review hold floor.
- A root CRO check cannot clear or counterfeit a separate-context review or owner approval.
- No live website deployment or customer experiment.

## Validation and remaining acceptance
- **[Final CI PASS](https://github.com/simpliolabs/hormozi-skills/actions/runs/42119634301)** on Windows and Ubuntu at exact HEAD `99d0921c1773d859c4b2f8d5f345ea5d493eb078`: **327 tests per OS** (one platform-specific skip each), including the original integration suite, CRO tests, adaptive routing tests, and repository checks.
- Earlier CRO-only candidate had [320 tests per OS passing](https://github.com/simpliolabs/hormozi-skills/actions/runs/42118820362); the additional seven tests cover guided/focused routing.
- `python scripts/cro_gate.py --stage A --surface planned` is a read-only route demonstration, not a host execution certificate.
- **Still necessary:** independent source/code review and fresh native novice, expert and full multi-step offer acceptance demonstrating *actual* method loading; measure real token use where the host reports it and retain all seven inherited obligation identities.
- Prompt-level budget guidance is **not** a guaranteed token/cost cap. Actual native differentiated specialist and separate-context reviewer execution remains unproven.

**Status: DRAFT.** No PR #4/5 merge, plugin release, publication or commercial deployment authorized.
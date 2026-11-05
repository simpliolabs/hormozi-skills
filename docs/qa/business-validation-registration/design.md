# Approved-scope implementation: explicit business-hold registration

This corrects the rejected provenance predicate in DESIGN.md. Independent DESIGN_REVIEW.md SHA256 0ce59823688d091abac1cde38f4bcf2565ba078d6d93e983bdfdc9b8d013af59 supports the following smaller alternative without another review round. The PO's November 5 authorization covers the bounded registration correction, existing instructions/validator, one fresh attempt and updates to draft PR #3. No new commercial-readiness policy is adopted: applicability remains root's semantic judgment from actual sources.

## Diagnosis and design choice

The immutable failed run acknowledged absent real-business validation in BRIEF.unknowns and prose, but omitted it from RUN_STATE.blockers. Existing instructions only give the review hold an explicit registration rule; the checker verifies authored state blockers but has no declaration-to-registration consistency check for this business hold. This is an authoring/registration omission, not proof of a previously required universal provenance rule or knowledge of the model's psychology.

Options considered: instructions-only leaves declared obligations unchecked; inferring absent validation from synthetic source types is unsound and rejected; explicit declaration plus existing-list consistency is the smallest supported solution. A new schema/ledger or general evidence classifier is excluded. This follows the already authorized bounded correction and existing root-declaration/checker-enforcement architecture.

## Concrete behavior

Canonical declaration/blocker: `Fictional fixture; real business validation absent` (the exact text already used in the older immutable archive).

1. During controlled-run intake, root reads actual sources and explicitly declares this known fictional-fixture/no-real-validation limitation in BRIEF.constraints before freezing/delegating the brief. Register the identical string in RUN_STATE.blockers and identify it as an unresolved business hold in CHECKPOINT and QA_REPORT. Do not infer applicability from the source_type enum alone. General real-business limitations still require honest semantic registration; this exact marker is narrowly for the known limitation it describes.
2. In ready validation, schema-valid BRIEF containing that exact constraint requires the exact state blocker. Missing registration produces one derived canonical BLOCKER_OPEN plus BUSINESS_VALIDATION_BLOCKER_UNREGISTERED. Existing exact state registration reuses its ordinary BLOCKER_OPEN; no extra duplicate. HELD, ready=false, timing/task/review findings and narrative disclaimers cannot substitute. Checker stays read-only.
3. No marker means no derived finding and NO inference of validation or approval. Malformed/missing controls keep existing errors; no crash or inference from invalid data. Draft/standalone behavior stays unchanged. Never clear explicit blockers automatically. A genuine independent review resolves its own copy-review requirement, not this business limitation.
4. Existing instructions must distinguish initial declaration completeness from downstream registration. Missing declaration is a native/semantic acceptance failure even if the new checker has nothing to enforce. This is a known cooperative-contract limitation, not complete automatic detection of business truth.

## Implementation plan

One bounded admitted Claude Sonnet/medium implementer; same branch/PR. Test public validate_run first, save red evidence, then minimal helper/call in existing checker and concise shared root instruction plus root entry-point pointer. No changes to four schemas, 17 method bodies, five specialists, dependencies, existing review matching/floor or SUMMARY behavior. Version stays1.1.1 to preserve original prompt path. Do not update old source labels to make tests green.

Tests: marker+missing state blocker; canonical present dedup; HELD/readyfalse; unrelated blockers don't substitute; valid independent review remains valid while business hold persists; similar narrative without exact marker adds no derived hold; supplied/mixed evidence with explicit marker triggers; synthetic-only without marker does not; malformed/missing controls; draft/standalone; input byte hashes unchanged. Preserve existing tests meaningfully. Full suite/repo QA, then independent exact-artifact code review and Windows/Ubuntu CI.

## Immutable replay and native acceptance

Neither historical BRIEF contains the new declaration. Old registered archive must retain its seven identities unchanged. Latest failed archive must still expose the upstream declaration gap: do NOT claim the new checker retroactively discovers its missing business hold. For a downstream regression, use a separately labeled derived test copy adding only the exact BRIEF constraint; preserve original bytes and disclose that single synthetic test edit. This is not fresh/native acceptance.

After code gates: one additional fresh installed native run, original four input hashes and byte-identical prompt, authorized Sol/medium, verified source pin and all installed tracked bytes. Freeze first completion before external inspection; never modify completed RUN_STATE/CHECKPOINT/QA_REPORT or send a repair prompt. Verify the explicit BRIEF declaration and all seven required identities across state/reports/findings, plus canonical SUMMARY, verbatim chosen hook and exactly three prioritized actions. Genuine extra holds are allowed but cannot replace an identity. Actual successful independent review makes the specified seven-hold scenario INCONCLUSIVE; no fabricated refusal. Failure consumes the sole new attempt and requires reporting the observed cause before any further retry.

Return root-cause report, narrow diff/necessity assessment, independent reviews, tests/CI, original and derived replay distinction, install/source hashes, first archive, checker findings and identity matrix on draft PR #3. No merge/release/deployment/publication/business-system actions.

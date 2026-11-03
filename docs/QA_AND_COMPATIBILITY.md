# QA and compatibility (1.1.0)

Status: **draft for review**, with the evidence and limits below. Synthetic examples do not establish commercial effectiveness. Machine-readable settings, source pins and results: [QA_EVIDENCE.json](QA_EVIDENCE.json).

## Reproduce local checks

```sh
pip install -r requirements-qa.txt
python -m unittest discover -s tests
python scripts/check_outputs.py --repo .
python <plugin_root>/scripts/check_outputs.py --workspace <workspace_root> --run <workspace_root>/output/runs/<id> --mode ready
```

Exit 0 means pass, 1 means held, 2 means tool/configuration failure. Negative-test output containing `HELD` is expected in the unit suite. The checker makes no model or network calls.

## Measured source checks

- 167 unit tests and repository QA passed at `49ba1db`. After the instruction-context-only correction, 35 affected workflow tests and repository QA passed at `28f810b`; unchanged whole-suite results were reused.
- Claude 2.1.311 plugin validation passed with listing/context warnings. No listing or publication was performed.
- Independent design review passed. Code review verified 128 whole-READY currency variants and preservation of the original methods, then passed the final instruction-context correction at `28f810b`.
- Static instruction tests check text presence; they cannot establish actual execution or authenticate review metadata.

## Native skill and workflow observations

All 17 standalone business skills were actually invoked through Claude's native Skill tool; initial automated rubrics passed 17/17. Actual-text review found three refund/exposure errors. Targeted reruns after guardrail corrections scored 3/3. Pricing and business-model outputs retained unknown cancellation costs. One objection output still contained an ambiguous ?only if? refund sentence despite a later unknown-policy qualification: **hold that sentence in semantic review**. Rubric votes and prompt instructions do not guarantee safe future copy.

The first multi-step controller run passed structural QA but had not loaded the selected methods. The corrected native run loaded `audit-offer`, `hormozi-offer`, `value-perception` and `pricing-strategy`, made six internal specialist calls, retained the original input, and persisted original audit, revision, separate revised checks, final economics and all four control records. It reached the 600-second worker wall bound before the final conversational handoff. Root ran ready-mode QA against that same persisted workspace afterward: **PASS, exit 0**. A complete native handoff within the bound remains unproven; no new fixture or whole-workflow retry concealed the timeout.

A separate Claude native specialist probe observed `hormozi-skills:sub-offer` handle `a380c09e40ac2a2e0`. Initial admission was refused; the actual read-only audit was then admitted through the documented research exemption. No local hook/configuration was changed. This is evidence for that route, not universal admission.

## Paired comparison and observer limits

Baseline raw rubrics: **6/6**. Candidate raw rubrics: **5/6**. The sparse-idea last-message grader failed although its actual `OFFER.md` contained all four Value Equation levers and explicit hypotheses/holds. Retain the raw failure; this small exploratory comparison establishes no improvement or conversion claim.

The Windows native evaluator could not provide its required shell sandbox. Supported shell-disallow flags enabled file-tool draft tests; full QA was exercised separately in a normal native controller. Long nested fixture paths also produced pre-generation observer errors; byte-identical short-path cases executed. These observer errors were not counted as business outcomes.

Requested Claude generator: `sonnet`, effort `medium`; observed canonical generator: `claude-sonnet-5-5`. Judge alias: `fable`; exact judge runtime and effort were not exposed. A prior `--max-turns 32` invocation reported `num_turns: 39`; requested settings are not proof of a universal turn/quota cap.

## Codex compatibility

CLI 0.164.0-alpha.11.1 resolves marketplace source paths from the marketplace root. Changing `.agents/plugins/marketplace.json` from `../../` to `./` fixed catalog discovery. In an isolated, unauthenticated profile, native marketplace registration, listing and installation succeeded: 19 skill directories plus references, contracts and checker were present, with no credential copy/global configuration change.

An authenticated native read-only audit read the installed root/audit methods and shared references, and held unsupported credit, reporting and draft-refund claims. Automatic skill activation and exact runtime model/effort were not observed. That cache preceded the final instruction-only corrections, which were not rerun in Codex. Optional project TOML roles were parsed but native project-role execution remains untested; plugin installation does not automatically register those roles.

## Install and review boundaries

Keep `skills/`, `agents/`, `references/`, `contracts/` and `scripts/` together. Packaged methods and role instructions are read-only instruction context, separate from workspace business-data inputs. Consumer artifacts belong in the consumer workspace. READY means checked local drafts for owner review; publishing, evidence truth and legal/commercial approval are separate decisions. Semantic review must inspect the actual prose and underlying sources.

Source contracts: [skills/hormozi-orchestrator/SKILL.md:23](../skills/hormozi-orchestrator/SKILL.md#L23), [references/orchestration.md:65](../references/orchestration.md#L65), [.agents/plugins/marketplace.json:11](../.agents/plugins/marketplace.json#L11). Evidence pins/results: [docs/QA_EVIDENCE.json:203](QA_EVIDENCE.json#L203), [docs/QA_EVIDENCE.json:237](QA_EVIDENCE.json#L237).

# PR1 QA and compatibility acceptance

Status: **keep the PR draft; no merge or publication authorization**. The implementation under independent review is `9cd252a8ed98b637bcc0f81af2699011fc4da0e7`. Later evidence-only commits are distinguished from this source pin. The machine-readable requirement matrix is [QA_EVIDENCE.json](QA_EVIDENCE.json).

## Acceptance matrix

| Review item | Result | Evidence and boundary |
| --- | --- | --- |
| P0-1 Same-fixture benchmark | PASS | [Raw baseline/candidate replies, fixture hashes, prior failure](qa/r1/paired-results.json). New baseline **6/6**, candidate **6/6**; unchanged prompts/rubrics. |
| P0-2 Completed one-chat experience | PASS | [A intake and exact-session resume](qa/r1/native-stage-a.json); [two B passes in one session](qa/r1/native-stage-b.json). Actual final owner responses, not post-hoc QA substitutes. |
| P0-3 Actual Codex invocation | PASS | Explicit root `SKILL.md` invocation; observed runtime **gpt-6.1-sol/medium**. Child admission refused, sequential role fallback disclosed. No fake children or model switches. |
| P0-4 Credit claims contained | PASS for held drafts | [Five actual customer assets and sources](qa/r1/credit-negative/), [30 deliberate mutations](qa/r1/credit-mutation-proof.json), [independent prose review](qa/r1/source-review.json). Unsafe promises absent; publication remains HELD. |
| P1-1 Automatic CI | PASS | [207 tests on each of Ubuntu and Windows, plus repo QA](qa/r1/ci-proof.json); [Actions run](https://github.com/simpliolabs/hormozi-skills/actions/runs/41738996761) at the reviewed source pin. Failures propagate; no secrets/deploy. |
| P1-2 Revision-specific evidence | PASS | [Typed matrix](QA_EVIDENCE.json), exact native argv/prompts, source pins and [raw native files](qa/r1/native-fixtures.zip). Observed, simulated, agent narration and unverified results are separated. |
| P1-3 Original inventory/fidelity | PASS | CI inventory/method checks plus independent Git-blob comparison. **17 business skills + create-plugin + new root = 19** skill directories; original five specialists and Claude entrypoints retained. |
| P1-4 Authority, mutations, B replay | PASS | [Native B proof](qa/r1/native-stage-b.json), [archive/hash observer](qa/r1/stage-b-archive-proof.json), simulated proposal/price/guarantee mutation tests. Unapproved bonus, fee and guarantee remain excluded. |
| P1-5 Mature B2B unknown economics | PASS, tested simulated | EUR4,800 monthly fixture retains unknown CAC, refund exposure, delivery cost and affiliate commission; certification/zeroing/leaks fail. Native credit pricing separately preserves unknown costs. No full native mature-unknown B2B generation is claimed. |
| P1-6 Lean scope and portability | PASS within measured scope | [Full-source and exact-fix review](qa/r1/source-review.json); cross-OS CI, consumer paths and token/cost observations below. No new engine/server/dependency. |
| Automatic Codex activation | NOT TESTED, optional | Supported proof is explicit manual invocation. No automatic-activation promise is made. |
| Native optional project-role adapters | NOT TESTED, optional | Parsing is checked; automatic registration/execution is not claimed. Core sequential fallback is observed. |

## What changed after the independent review

`1ee0c25` requires a substantive final reply with the provisional offer, all four Value Equation levers and validation next steps, rather than a file/status index. It also requires an initial checkpoint before delegation and updates after accepted tasks. That corrected the sparse-idea fixture; the old raw failure is retained in the comparison.

CI exposed Windows-only assumptions. Protected repository text now compares the original LF Git-blob hash while accepting Git CRLF/LF checkout conversion; business/input/artifact/review hashes remain byte-exact. Workspace path separators and containment are tested on Windows and Linux.

Full source review then found dictionary shadowing and monetary-unit/sign defects. The checker now rejects duplicate claim/task/binding identities before lookup construction, uses JPY exponent 0 and the other 17 supported currencies' exponent 2, holds unknown currency exponents, and checks the declared negative-sign grammar while preserving ordinary Markdown bullets. Parenthetical accounting notation is outside that grammar. Semantic review still handles ambiguous or unregistered prose; metadata is not authenticated. Currency minor-unit reference: [Adyen documentation](https://docs.adyen.com/development-resources/currency-codes/).

## Native completion, holds and raw proof

A checkpoint turn completed in **94.17 s**, followed by a **276.99 s** completion in the exact same Codex session. B completed in **318.83 s** and its second pass in **330.14 s**, again in the same session, retaining the original inputs and archiving the first pass. The credit-negative case completed in **382.89 s**. Each produced an actual owner-facing final response within its 600-second turn bound.

These are complete draft workflows, not invented commercial approvals. Final-checker rechecks retain only expected holds: A **2** business/hypothesis holds; B **11** business/independent-review holds; credit **11** admission/operation/economics/independent-review holds. [Recheck findings](qa/r1/native-recheck-final-checker.json). No structural or hash failures appeared. The later independent credit prose review did not alter the original records or authorize publication.

[Download raw synthetic inputs, artifacts, checkpoints and control records](qa/r1/native-fixtures.zip); [archive hash and replay notes](qa/r1/native-fixtures-manifest.json). Raw receipts retain recorded local paths for provenance; package instructions use dynamic plugin/workspace roots. The six unchanged native evaluation fixtures and exact supported command are under [evals/](../evals/README.md). No model-calling product harness was added.

The native test model exception was explicitly approved by the owner after this account rejected gpt-5.5. Global routing, hooks and configuration were not changed. Native child preflight still refused the requested build tier; the root disclosed that refusal and used the existing sequential fallback. Runtime `turn_context` metadata independently confirmed Sol/medium; the agents correctly reported unknown when they did not see it.

## Measurements and limitations

The six-fixture evaluator reported generator cost **USD0.8025 baseline / USD1.8814 candidate** and wall time **225.64 s / 512.88 s**. This sample has more candidate overhead, not token savings. Per-case usage/cache counters and output text are in [paired-results.json](qa/r1/paired-results.json). Reported cost is not independently verified account billing; native Codex dollar billing is unmeasured. One generation per fixture and three judge votes do not establish statistical or commercial superiority.

The Windows evaluator used supported shell-disallow flags for file-tool draft tests; full QA was exercised in ordinary native Codex runs. Earlier pre-generation long-path observer errors were not counted as product results. The new benchmark includes all final instruction corrections; later changes are checker/test-only, with unchanged method hashes and final-checker replay of persisted native files. Earlier 5/6 and timeout evidence remains historical, not silently overwritten.

Unknown real material contents/access, operating costs, reporting acceptance and refund operations remain held. An earlier standalone objection draft's ambiguous refund sentence remains unapproved; it is not a ready asset. A clean ledger or passing checker does not prove all prose true. Actual source/prose review and owner release decisions remain necessary. Optional auto-activation/project-role tests were not substituted for core one-chat acceptance.

## Local checks

```sh
python -m pip install -r requirements-qa.txt
python -m unittest discover -s tests -v
python scripts/check_outputs.py --repo .
python <plugin_root>/scripts/check_outputs.py --workspace <workspace_root> --run <run_directory> --mode ready
```

Exit 0 is pass, 1 is held, 2 is tool/configuration failure. Expected negative-test findings printed during the suite are not repo-check failures. Branch protection and release settings were not modified.

Source contracts: [references/orchestration.md:45](../references/orchestration.md#L45), [references/orchestration.md:75](../references/orchestration.md#L75), [scripts/check_outputs.py:149](../scripts/check_outputs.py#L149), [scripts/check_outputs.py:504](../scripts/check_outputs.py#L504).

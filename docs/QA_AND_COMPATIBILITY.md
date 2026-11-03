# QA and Compatibility (v1.1.0)

## Local checks
```
pip install -r requirements-qa.txt
python -m unittest discover -s tests -v
python scripts/check_outputs.py --repo .
python <plugin_root>/scripts/check_outputs.py --workspace <workspace_root> --run <workspace_root>/output/runs/<id> --mode ready
```
Exit codes: 0 pass, 1 held, 2 tool/configuration failure. The script never calls models or the network.

## Native Codex discovery (measured)
Codex resolves marketplace source paths from the **marketplace root**. The original `.agents/plugins/marketplace.json` used `../../`, which points outside the repository, so the plugin was registered but absent from the catalog. The path is now `./`. A minimal unauthenticated control had already installed, so authentication was not the cause.

Verified with Codex CLI 0.164.0-alpha.11.1 in a fresh isolated `CODEX_HOME` (no auth copy, no global config change): `marketplace add`, `plugin list --available`, `plugin add hormozi-skills@hormozi-skills`, `plugin list`. Version 1.1.0, installed and enabled; the install cache contains `skills/`, `references/`, `contracts/` and `scripts/`.

## Measured gates (provisional; root refreshes native results)
- Unit gate: 166 tests passed on the prior head (37ff5cb); this change adds 1 static test (167 total, all passing locally). `check_outputs.py --repo .` passes. `HELD` / `ARTIFACT_HASH_MISMATCH` lines printed during the test run come from deliberate negative-path tests, not from the repo check.
- Static instruction tests prove only that required text is present. They are not runtime proof that any method was loaded.
- 17 standalone skills, native actual-invocation rubric: 17/17. Semantic review then found three refund/exposure failures. `pricing-strategy` is repaired; `business-model` and `objection-destroyer` are repaired in this change (a conditional refund is not exclusivity or low risk; an unknown refund cost is not zero). A targeted native rerun is **pending**.
- Paired benchmark, baseline vs candidate: baseline 6/6, candidate raw 5/6. The failing case (sparse idea) was failed by a last-message grader although the actual `OFFER.md` contains all four Value Equation levers and holds. The raw failure is retained; no improvement or conversion claim is made.
- Native file-tool evaluator cannot shell out in the Windows sandbox. Supported shell removal enabled draft checks only, not full QA.
- Native controller on 8ab69ec: actual structure, order, path and hash `ready` PASS, but no selected standalone method was loaded and tasks ran in root although `Agent` was available. Structural `ready` PASS is insufficient. The root skill, agent and shared workflow now require loading the method and passing it to workers; the native rerun is **pending**.
- Native Codex: 19 skills plus references, contracts and checker installed; the model read the installed root and audit methods and held harmful credit claims. Automatic skill activation was not observed; exact runtime model and effort are unknown.
- Turn bound: `--max-turns 32` was requested; the prior CLI result reported `num_turns` 39. Requested setting and observed count differ; no universal cap is claimed.

## Not yet measured / untested (run by root)
- Native controller rerun after this change, showing which method was loaded per task and whether native workers were dispatched.
- Targeted native rerun of the three repaired refund/exposure cases.
- Independent exact-fix review: required, **not yet passed**.
- Native project-TOML execution: untested.
- Claude-native acceptance beyond the runs above; native A-E and claim cases; whether a loaded skill resolves `<plugin_root>` inside the plugin cache.
- Final public QA receipt: provisional until root records fresh native results.
These are unmet gates until run, not passes.

## Manifest rules
One version (1.1.0) across `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; plugin name `hormozi-skills` and the original author attribution are preserved; `.codex-plugin/plugin.json` declares `"skills": "./skills/"`. `tests/test_compat.py` enforces these.

## Manual install
Copy `skills/`, `agents/`, `references/`, `contracts/` and `scripts/` together; skills load shared files relative to the plugin root, not the working directory.

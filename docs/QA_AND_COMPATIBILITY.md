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

Verified with Codex CLI 0.164.0-alpha.11.1 in a fresh isolated `CODEX_HOME` (no auth copy, no global config change): `marketplace add`, `plugin list --available`, `plugin add hormozi-skills@hormozi-skills`, `plugin list`. Version 1.1.0, installed and enabled; the install cache contains `skills/`, `references/`, `contracts/` and `scripts/`. Receipt: `NATIVE_CODEX_TASK4_INSTALL_RECEIPT.txt` beside the plan documents.

## Not yet measured (pending, run by root)
- Invoking the root skill or a specialist in an installed Codex plugin and observing worker handles.
- Claude-native acceptance (no Claude executable was found on the build shell's PATH).
- The 17 standalone smoke cases, native A-E and claim cases, and the six paired benchmarks.
- Whether a loaded skill resolves `<plugin_root>` from the host's base path inside the plugin cache.
These are unmet gates until run, not passes.

## Manifest rules
One version (1.1.0) across `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; plugin name `hormozi-skills` and the original author attribution are preserved; `.codex-plugin/plugin.json` declares `"skills": "./skills/"`. `tests/test_compat.py` enforces these.

## Manual install
Copy `skills/`, `agents/`, `references/`, `contracts/` and `scripts/` together; skills load shared files relative to the plugin root, not the working directory.

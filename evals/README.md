# Native paired smoke fixtures

These six synthetic fixtures are the unchanged prompts and rubrics used for the original/fork comparison. IDs: a contradictory sources; b focused hooks; c mature B2B; d sparse idea; e strong proof; f weak existing offer. They are test data, not commercial copy.

With Claude Code 2.1.311, run from the candidate root (shell-disallowed file-tool mode used on Windows):

```sh
claude plugin eval . --eval-dir evals/paired --model sonnet --judge-model fable --runs 1 --concurrency 1 --ablation none --no-publish --no-scaffold --trust-plugin --allow-tools Write Edit --disallow-tools Bash PowerShell --keep-temp --output-dir output/native-eval --json output/native-eval/results.json
```

Set `CLAUDE_CODE_EFFORT_LEVEL=medium` in the process environment. One generation is requested per case; three judge votes do not mean three independent generations. Effective aliases, cache effects and tool availability must be observed rather than assumed. File-tool runs cannot establish full shell QA. Normal native Codex execution is tested separately.

For a controlled baseline comparison, export commit `910545c278d999cff14fd6d543f3df34ec0bbe4d` to a separate temporary content directory (no Git checkout is needed), copy this same fixture directory there, and run the same command/settings. Keep source pins and fixture hashes. Do not change a rubric merely to pass a candidate.

Revision-specific inputs, output text, observed costs and native Codex proof are under `docs/qa/r1/`; the requirement matrix distinguishes observed, simulated and unverified results. These examples establish no conversion benefit or general model superiority.

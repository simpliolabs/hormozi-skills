# PR #5 corrected full-offer token observations

These are host counters from two separate first-completion native Codex runs using the unchanged DeskFern C prompt and fictional fixture. They are cumulative across model turns, not unique input bytes or billed cost.

| Run | Source | Input | Cached input | Noncached input | Output | Reasoning output | Elapsed | Completed shell commands | Command output characters |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Original C | `6b7a04e949e4ed69019591acab9f616107348b7c` | 1,042,544 | 979,584 | 62,960 | 12,634 | 470 | 391.84 s | 18 | 168,207 |
| Corrected C | `7b37ac381c8bf5fb00d87b8e78e95979afed0630` | 1,095,278 | 1,015,552 | 79,726 | 19,087 | 1,744 | 515.62 s | 15 | 227,794 |

The corrected run used 52,734 more input tokens, 16,766 more noncached input tokens, 6,453 more output tokens, and 123.78 more seconds. This does **not** establish a token-efficiency improvement. The host gives no per-skill token or cost attribution.

The original run's largest command outputs were combined method reads: value-perception plus pricing-strategy (45,431 characters), pitch plus hooks (26,679), orchestration plus adaptive routing (24,589), landing-page plus CRO (16,524), and CRO references plus gate (12,902). The corrected run likewise read the selected full-offer methods, not the complete 17-skill library. Its larger shell output and longer authored package are plausible contributors to the higher cumulative count, but the available trace does not assign causality or per-step tokens. Focused original B used only the hooks skill and 56,820 input tokens, which supports the focused route for a precise request; it does not prove an absolute efficiency threshold.

The new commercial checker reads existing structured decisions, adds no new model stage or external service, and leaves the review and business holds intact. Future optimization can target repeated large method reads and command output after preserving the same acceptance gates; no untested optimization was folded into this correction.

Evidence: `evidence/sessions/C/c_receipt.json`, `evidence/sessions/C/c_events.jsonl`, `candidate_native/sessions/C/c_receipt.json`, and `candidate_native/sessions/C/c_events.jsonl`. The full original investigation is `PR5_TOKEN_INVESTIGATION_2026-11-06.md`.

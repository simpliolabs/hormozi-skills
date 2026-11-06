---
schema: make-a-change/project/v1
type: project
id: hormozi-skills
title: hormozi-skills
status: active
created: 2026-04-14
updated: 2026-11-06
description: Hormozi-inspired adaptive offer workflows, CRO optimization and owner-controlled commercial safeguards.
kind: skill
owner: simpliolabs
repo: simpliolabs/hormozi-skills
---

# hormozi-skills

The Simpliolabs-maintained fork of an open-source, Hormozi-inspired skill library for coding agents. Its current merged source has 18 business methods (including CRO), a one-chat orchestrator, focused QUICK routing, guided one-question intake and opt-in DEEP workflows. Eligible full offer workflows call for a downstream CRO readiness or evidence-led page/handoff review, with owner-controlled commercial decisions, independent sales-review holds and structural output checks.

**Upstream:** [alexsmedile/hormozi-skills](https://github.com/alexsmedile/hormozi-skills), created by Alex Smedile; original MIT license and attribution remain intact.

**Merged:** [PR #3](https://github.com/simpliolabs/hormozi-skills/pull/3) established the initial hold floor; [PR #4](https://github.com/simpliolabs/hormozi-skills/pull/4) updated onboarding; and [PR #5](https://github.com/simpliolabs/hormozi-skills/pull/5) merged adaptive routing, CRO and corrected commercial-hold identity checks at [commit `862f3c7`](https://github.com/simpliolabs/hormozi-skills/commit/862f3c770f8264750c7c288506f02aedb0cbdb29).

**Validated (bounded):** PR #5's corrected DeskFern full-offer first-completion acceptance preserved all seven obligation identities without operator repair, with automatic CRO in that test and an expected `HELD` result; the focused hooks run passed and beginner/direct CRO had stated limits. Final PR-head Windows/Ubuntu CI passed 342 tests per OS, one skip each. This is **not** authenticated sales-copy approval, proof of general business reliability, differentiated native specialist execution or a new plugin release. Plugin manifests still declare `1.1.1`.

## Links

- [Status](STATUS.md) · [Tasks](TODO.md)
- [Usage and quick start](README.md) · [Operating guide](docs/OPERATING_GUIDE.md)
- [Current validation status](STATUS.md) · [Native PR #5 evidence](https://github.com/simpliolabs/hormozi-skills/blob/48ee079ad87890d5e2b4641473d21738d1198d97/docs/qa/pr5-fictional-business/native-acceptance-fix-2026-11-06/README.md) · [Historical PR #3 baseline](docs/SEVEN_HOLD_VALIDATION.md)

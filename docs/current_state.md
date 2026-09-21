# Current State

_Last updated: 2026-09-15_

## Solve-for rollout

All 39 routed activities have a [page-by-page evaluation](solve_for_evaluation.md).
Clear existing targets use one declared catalog for browser controls and worksheet
requests; ambiguous targets are [documented without implementation](solve_for_deferred.md).
CI now runs seven guardrail scripts, including `tools/test_solve_for.py`.

## Progress and document follow-up

All 70 generator types and 12 custom types now have explicit progress IDs with
legacy-history migration. Word export supports structured Markdown and native,
editable equations. The progress/formatting suite is included in CI. See the
[follow-up record and human review checklist](implementation_fixes_2026-09-15.md).

## September audit corrections

See [the correction record](implementation_fixes_2026-09-14.md) for the physics,
export, shared payload, scoring, and interaction fixes. CI now discovers all 23
generators and runs the two existing guardrails plus all three interaction/export
test scripts, plus the progress/formatting suite. The older compatibility inspection below is historical. DOCX visual
pagination checks require LibreOffice, which is not installed in the audit environment.

## Purpose
This file is the fastest onboarding reference for new contributors/agents. Read this first before scanning broader docs.

## Cross-layout Compatibility (2026-09-11)

Before reusing a feature in a different page layout, read
[Compatibility limits](compatibility_limits.md) and [Activity flow](activity_flow.md).
These source-verified notes cover unresolved metadata/payload differences,
grading and mixed-input constraints, the separate diagram-matching lifecycle,
generator options, and gaps in automated interaction coverage. They supplement
the older status notes below; they do not claim those gaps have been fixed.

## Current Priorities
1. **Validation Pipeline Repair**: keep `tools/validate_payloads.py` aligned with active generator metadata as modules evolve.
2. **Payload Contract Audit**: enforce consistent payload keys/shape across all generators, including less-used code paths.

## Recently Completed
- Critical correctness fixes (roulette planner rates, Atwood prompt mismatch, invalid doc `solve_for` override).
- Additional correctness fixes found during audit:
  - collision generator medium/hard runtime path initialization
  - relative-motion payload key (`unit` -> `units`)
- Validation script modernization:
  - `tools/validate_payloads.py` now runs directly from repo root and derives problem-type mappings from `stored_metadata()`.
- Correctness guardrail baseline completed:
  - `tools/check_prompt_answer_consistency.py`
  - CI enforcement in `.github/workflows/correctness-guardrails.yml`
- Correctness Regression Guardrail Expansion completed:
  - extended seeded regression coverage across `ForceGenerator`, `ProjectileGenerator`, `CollisionGenerator`, `WaveGenerator`, and `MotionGraphGenerator`
  - added hard-difficulty seed sweeps and synthetic regression tripwires per targeted generator class
  - removed dependency-based skip paths for motion graph and doc organizer checks in guardrail scripts
  - upgraded `tools/validate_payloads.py` to metadata x difficulty x seed validation with clearer failure context
  - documented seeded regression requirements in `docs/generator_conventions.md`

## Required Guardrail Commands
Run both before claiming correctness-related work is complete:

```bash
python tools/validate_payloads.py
python tools/check_prompt_answer_consistency.py
```

## Core Architecture Constraints
- Generator outputs must follow the payload contract:
  - required keys: `question`, `answers`, `units`
  - invariant: `len(answers) == len(units)`
- UI/doc tooling assumes dict payloads (legacy tuple payloads are out of scope).
- `solve_for` overrides must only use values each generator actually supports.

## Known Pitfalls
- Stale hardcoded problem-type mappings in tooling can produce false failures.
- Prompt text can drift from answer/unit intent (especially when adding new solve-for branches).
- Doc question factories (`xtrct_docs/question_organizer.py`) can silently introduce invalid generator arguments.

## Start Here (High Signal Files)
- `docs/project_roadmap.md`
- `docs/problem_payload.md`
- `docs/generator_conventions.md`
- `tools/validate_payloads.py`
- `tools/check_prompt_answer_consistency.py`
- `utils/problem_payload.py`
- `xtrct_docs/question_organizer.py`

## Open Follow-Ups
1. Consider adding `CONTRIBUTING.md` with mandatory pre-merge checklist.

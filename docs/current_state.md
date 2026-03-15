# Current State

_Last updated: 2026-02-17_

## Purpose
This file is the fastest onboarding reference for new contributors/agents. Read this first before scanning broader docs.

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

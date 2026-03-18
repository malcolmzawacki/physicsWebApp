# Project Roadmap & Backlog

_Last updated: 2026-02-17_

## Recently Completed
- **Correctness Regression Guardrail (2026-02-17)**: Added recurring guardrail scripts (`tools/validate_payloads.py`, `tools/check_prompt_answer_consistency.py`), documented maintainer runbook, and CI enforcement via `.github/workflows/correctness-guardrails.yml`.
- **Critical Correctness Bugs (2026-02-17)**: Patched known logic/content bugs in active paths (roulette planner rate calculation, Atwood acceleration prompt mismatch, invalid `solve_for` usage in doc question builders), plus adjacent payload/runtime correctness issues found during audit.
- **Streamlit Navigation**: Router rollout complete; next steps are refining activity groupings and course-level filters (minimum level set to High School; remove Middle School tier; keep Regular High School + Advanced).
- Reorganized navigation: added a "Rotation (Advanced)" main area, moved vectors/displacement into Foundations, and updated advanced-only activity filters.
- Moved kinematics generators into `utils/generators/kinematics/` and updated imports/paths across the app.
- Migrated activity modules to `State`-based session handling and removed legacy multipage/tab scaffolding.
- Introduced a generic diagram-matching layout (`utils/layouts/diagram_match_layout.py`) with auto-advance timing and first-question autoload.
- Extracted motion graph matching into a dedicated payload generator (`utils/generators/kinematics/motion_graph_matching_generator.py`) and wired the motion page to the generic layout.
- Removed legacy tuple payload support and standardized generators on dict payloads.
- `utils/generators/kinematics/projectile_generator.py` now supports explicit `solve_for` overrides while keeping question narratives coherent.
- `xtrct_docs/document_creator.py` has an `include_graphs` parameter to add flexibility when diagrams are helpful but not needed
- Created and then moved additional force tab generators to `forces/` folder for better organization, includes `atwood_generator.py`, `tension_generator.py`, and `incline_generator.py`
- Rotational kinematics generator and Streamlit page are in place (`utils/generators/rotational_motion_generator.py`, `app_pages/1_1.1.2_Rotational_Motion.py`).
- Linear motion generator refactor is complete (centralized phrasing, unified variable selection).
- Center of mass generator wording and diagram tweaks are complete.

## In Progress / Short-Term Targets
- **Correctness Regression Guardrail Expansion**: Extend guardrail coverage with additional generator-specific invariants and regression cases as modules expand.
- **Validation Pipeline Repair**: Make `tools/validate_payloads.py` runnable from the documented command path and align problem-type mappings with current generator metadata.
- **Dependency Baseline Fixes**: Update `requirements.txt` to include runtime packages used by UI/dataframe/doc export modules (e.g., pandas, python-docx) and verify clean-environment startup.
- **Payload Contract Audit**: Enforce strict payload-key consistency (`units`/feature keys), fix unfinished generators that violate the contract, and add smoke checks for contract regressions.
- **UI Runtime Responsiveness**: Replace blocking sleep-based auto-advance loops with rerun-safe timing/state patterns and normalize timer/time-limit handling.
- **Shared Submission Flow Redesign**: Refactor `utils/ui.py` answer submission so custom feedback/stars can coexist with retryable attempts and an explicit `Show Answer` path instead of immediate forced reveal on first miss.
- **Nested Activity Lazy Loading**: Standardize selector-driven nested activities (radio/selectbox plus per-mode lazy imports) as the replacement for eager `st.tabs` rendering so multi-mode pages load only the selected activity with one click.
- **Graph & Image Quality**: Carry the print-friendly theming back into Streamlit views and add regression checks for mixed graph/standard sections.
- **Encoding & Content Cleanup**: Remove garbled Unicode artifacts, standardize symbol formatting strategy (Unicode vs LaTeX), and correct chemistry data inconsistencies.
- **Rotational Dynamics Extension**: Plan torque and moment of inertia extensions for the rotational unit (new page sections and generator updates).

## Backlog

### Testing & Tooling
- Expand payload validation into a lightweight smoke-test suite covering representative generators.
- Add unit tests for core generators, plus Streamlit snapshot tests for UI flows and document creation regression tests.
- Improve setup docs (README) and consider optional pre-commit hooks for linting/formatting.
- Develop validation for qualitative/conceptual problem payloads
- Create test suite for multi-representation translation problems
- Add snapshot tests for explanation evaluation logic

### Problem Generators & Data Model
- Add physics/unit validation: dimensional checks, difficulty monotonicity, and sanity bounds for generated values.
- Add optional reproducible seeding so documents/tests can generate deterministic problem sets.
- Surface generator metadata (equations, tags) through a formal hook that UI pages can consume uniformly.
- Extend `solve_for` support (and related phrasing helpers) to other physics generators for consistent behavior.
- Add qualitative problem variants to existing generators (comparison, ranking, prediction tasks)
- Create error-embedded worked examples for each major concept
- Build estimation problem generators with order-of-magnitude targets
- Design multi-concept synthesis problem templates

### UI Layer & State Management
- State migration complete; keep new code on `State` and audit for regressions.
- Explore author tooling in the UI (e.g., expose solve-for overrides, seeds) for rapid debugging.

### Document Generation Pipeline
- Refactor `xtrct_docs/document_creator.py` to separate data extraction, markdown cleaning, table rendering, and answer-key assembly.
- Modify `xtrct_docs/document_creator.py` and `xtrct_docs/question_generator.py` parameter passing to capture context (`include_graphs=False`, `tables=True`) rather than passing them as separate, whole document arguments.
- Allow generator callbacks used for documents to receive contextual metadata (version index, seed) for reproducibility.
- Replace `os.startfile` with a platform-aware opener and wrap temp image creation in context managers for safer cleanup.
- Enhance `xtrct_docs/document_creator.py` answer type recognition to truncate float vals in answer key.

### Content & UX Polish
- Fix encoding glitches (e.g., garbled `Home.py` title, inconsistent m/sÂ² symbols) and adopt a consistent Unicode/LaTeX strategy.
- Audit wording for direction reversals across all generators; align on shared helpers similar to the new linear-motion implementation.
- Centralize copy for equations, hints, and feedback strings; consider LaTeX helpers for formatting parity across UI and docs.
- Create "reasonableness check" helper prompts for each problem type
- Design diagram annotation interfaces for force arrows, vectors, energy transformations
- Add pre-solve prediction prompts and post-solve reflection questions
- Integrate confidence sliders or self-assessment checkboxes

## Strategic Initiatives (Streamlit-Compatible)
- **Declarative Generator Framework**: Separate physics "engines" from presentation, and allow generators to be described via metadata/schema files that the runtime composes into the existing payload contract.
- **Structured Solutions & Hints**: Extend generators to emit stepwise explanations (concept + equation + substitution + result) so both UI hints and answer keys stay consistent.
- **Context & Scenario Library**: Define reusable context packs (nouns, verbs, realistic value ranges, diagram assets) that generators can pull from for authentic problem statements.
- **Authoring Workspace**: Build an author-mode dashboard inside Streamlit for seed controls, curated problem sets, previewing DOCX exports, and managing context packs.
- **Learning Objectives & Analytics**: Tag problems with objectives/standards, log anonymized attempts to a lightweight datastore, and surface mastery dashboards for teachers.
- **Adaptive Practice Layer**: Use the collected performance data to bias future question selection (difficulty, solve_for, context) for individualized practice sequences.
- **Conceptual Understanding Layer**: Extend generators to emit qualitative reasoning problems alongside calculations, comparison questions ("Which has more energy?"), prediction tasks ("What happens if we double the mass?"), and scenario analysis without numerical computation. Include qualitative button-based responses and short text explanations.
- **Multi-Representation Practice**: Build problem variants that require translating between representations (graph -> equation -> verbal description -> diagram). Extend graph generators to include sketching/prediction modes where students select expected graph shapes before seeing calculations. Add diagram annotation tools for labeling forces, energy flow, or motion paths.
- **Error Analysis & Reasoning Problems**: Create a problem type that presents worked solutions (correct or with deliberate errors) and asks students to identify mistakes, explain reasoning, or verify reasonableness. Include "debugging" mode where students diagnose why a calculation went wrong or why an answer is physically impossible.
- **Estimation & Reasonableness Checks**: Add pre-solve estimation prompts ("Should this be closer to 10 or 1000?") and post-solve verification questions ("Does your answer make sense? Why?"). Integrate order-of-magnitude checking and dimensional analysis as explicit practice types.
- **Multi-Step Synthesis Problems**: Design problem chains that combine multiple concepts (e.g., projectile motion -> collision -> energy conservation) requiring students to plan solution strategies across 3-5 connected steps. Include scaffolded versions with planning prompts and strategy hints.
- **Free-Response & Explanation Engine**: Add text input options for conceptual explanations alongside numerical answers. Implement keyword-based or LLM-assisted evaluation for open-ended responses like "Explain why momentum is conserved" or "Describe what happens to kinetic energy."
- **Partial Credit & Process Tracking**: Extend answer checking to award partial credit for correct approach with calculation errors. Track solution steps for multi-part problems and provide targeted feedback on which stage went wrong (setup vs. algebra vs. units).
- **Metacognitive Scaffolding**: Integrate reflection prompts into the UI flow - strategy selection before solving ("Which approach will you use?"), confidence ratings during submission, and post-problem reflection ("What was challenging? What would you check?"). Log these for future adaptive practice.
- **Accessibility & Localization Upgrades**: Improve contrast/readability, offer dyslexia-friendly modes, and plan for multilingual prompts using a centralized copy system.

## Notes & References
- Legacy `unit1_practice_doc` still returns a fully-evaluated list; refactor to match callable generator usage.
- Home page Unicode issue persists and is tracked above under Content & UX.
- Prior architectural docs (`docs/architecture.md`, `docs/ui.md`) should be refreshed once major UI refactors land.

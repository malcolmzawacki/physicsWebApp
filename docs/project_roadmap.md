# Project Roadmap & Backlog

_Last updated: 2026-02-04_

## Recently Completed

- `projectile_generator.py` now supports explicit `solve_for` overrides while keeping question narratives coherent.
- `xtrct_docs/document_creator.py` has an `include_graphs` parameter to add flexibility when diagrams are helpful but not needed
- Created and then moved additional force tab generators to `forces/` folder for better organization, includes `atwood_generator.py`, `tension_generator.py`, and `incline_generator.py`
- Rotational kinematics generator and Streamlit page are in place (`utils/generators/rotational_motion_generator.py`, `pages/1_1.1.2_Rotational_Motion.py`).
- Linear motion generator refactor is complete (centralized phrasing, unified variable selection).
- Center of mass generator wording and diagram tweaks are complete.

## In Progress / Short-Term Targets

- **Streamlit Navigation**: Evaluate replacing implicit `pages/` discovery with explicit `st.navigation` / `st.pages` declarations for clearer unit/module groupings.
- **Graph & Image Quality**: Carry the print-friendly theming back into Streamlit views and add regression checks for mixed graph/standard sections.
- **Rotational Dynamics Extension**: Plan torque and moment of inertia extensions for the rotational unit (new page sections and generator updates).

## Backlog

### Problem Generators & Data Model

- Extend `solve_for` support (and related phrasing helpers) to other physics generators for consistent behavior.
- Surface generator metadata (equations, tags) through a formal hook that UI pages can consume uniformly.
- Add optional reproducible seeding so documents/tests can generate deterministic problem sets.
- Add physics/unit validation: dimensional checks, difficulty monotonicity, and sanity bounds for generated values.
- Add qualitative problem variants to existing generators (comparison, ranking, prediction tasks)
- Create error-embedded worked examples for each major concept
- Build estimation problem generators with order-of-magnitude targets
- Design multi-concept synthesis problem templates

### UI Layer & State Management

- Continue migrating legacy session-state calls to the `State` helper; audit diagram rendering and answer-checking paths for remaining direct `st.session_state` usage.
- Explore author tooling in the UI (e.g., expose solve-for overrides, seeds) for rapid debugging.

### Document Generation Pipeline

- Refactor `xtrct_docs/document_creator.py` to separate data extraction, markdown cleaning, table rendering, and answer-key assembly.
- Allow generator callbacks used for documents to receive contextual metadata (version index, seed) for reproducibility.
- Replace `os.startfile` with a platform-aware opener and wrap temp image creation in context managers for safer cleanup.
- Modify `xtrct_docs/document_creator.py` and `xtrct_docs/question_generator.py` parameter passing to capture context (`include_graphs=False`, `tables=True`) rather than passing them as separate, whole document arguments.
- Enhance `xtrct_docs/document_creator.py` answer type recognition to truncate float vals in answer key.

### Content & UX Polish

- Fix encoding glitches (e.g., garbled `Home.py` title, inconsistent m/sÂ² symbols) and adopt a consistent Unicode/LaTeX strategy.
- Centralize copy for equations, hints, and feedback strings; consider LaTeX helpers for formatting parity across UI and docs.
- Audit wording for direction reversals across all generators; align on shared helpers similar to the new linear-motion implementation.
- Add pre-solve prediction prompts and post-solve reflection questions
- Integrate confidence sliders or self-assessment checkboxes
- Design diagram annotation interfaces for force arrows, vectors, energy transformations
- Create "reasonableness check" helper prompts for each problem type

### Testing & Tooling

- Expand payload validation into a lightweight smoke-test suite covering representative generators.
- Add unit tests for core generators, plus Streamlit snapshot tests for UI flows and document creation regression tests.
- Improve setup docs (README) and consider optional pre-commit hooks for linting/formatting.
- Develop validation for qualitative/conceptual problem payloads
- Create test suite for multi-representation translation problems
- Add snapshot tests for explanation evaluation logic

## Strategic Initiatives (Streamlit-Compatible)

- **Context & Scenario Library**: Define reusable context packs (nouns, verbs, realistic value ranges, diagram assets) that generators can pull from for authentic problem statements.
- **Declarative Generator Framework**: Separate physics "engines" from presentation, and allow generators to be described via metadata/schema files that the runtime composes into the existing payload contract.
- **Authoring Workspace**: Build an author-mode dashboard inside Streamlit for seed controls, curated problem sets, previewing DOCX exports, and managing context packs.
- **Structured Solutions & Hints**: Extend generators to emit stepwise explanations (concept + equation + substitution + result) so both UI hints and answer keys stay consistent.
- **Learning Objectives & Analytics**: Tag problems with objectives/standards, log anonymized attempts to a lightweight datastore, and surface mastery dashboards for teachers.
- **Adaptive Practice Layer**: Use the collected performance data to bias future question selection (difficulty, solve_for, context) for individualized practice sequences.
- **Accessibility & Localization Upgrades**: Improve contrast/readability, offer dyslexia-friendly modes, and plan for multilingual prompts using a centralized copy system.
- **Conceptual Understanding Layer**: Extend generators to emit qualitative reasoning problems alongside calculations—comparison questions ("Which has more energy?"), prediction tasks ("What happens if we double the mass?"), and scenario analysis without numerical computation. Include qualitative button-based responses and short text explanations.
- **Multi-Representation Practice**: Build problem variants that require translating between representations (graph ? equation ? verbal description ? diagram). Extend graph generators to include sketching/prediction modes where students select expected graph shapes before seeing calculations. Add diagram annotation tools for labeling forces, energy flow, or motion paths.
- **Error Analysis & Reasoning Problems**: Create a problem type that presents worked solutions (correct or with deliberate errors) and asks students to identify mistakes, explain reasoning, or verify reasonableness. Include "debugging" mode where students diagnose why a calculation went wrong or why an answer is physically impossible.
- **Estimation & Reasonableness Checks**: Add pre-solve estimation prompts ("Should this be closer to 10 or 1000?") and post-solve verification questions ("Does your answer make sense? Why?"). Integrate order-of-magnitude checking and dimensional analysis as explicit practice types.
- **Multi-Step Synthesis Problems**: Design problem chains that combine multiple concepts (e.g., projectile motion ? collision ? energy conservation) requiring students to plan solution strategies across 3-5 connected steps. Include scaffolded versions with planning prompts and strategy hints.
- **Metacognitive Scaffolding**: Integrate reflection prompts into the UI flow—strategy selection before solving ("Which approach will you use?"), confidence ratings during submission, and post-problem reflection ("What was challenging? What would you check?"). Log these for future adaptive practice.
- **Free-Response & Explanation Engine**: Add text input options for conceptual explanations alongside numerical answers. Implement keyword-based or LLM-assisted evaluation for open-ended responses like "Explain why momentum is conserved" or "Describe what happens to kinetic energy."
- **Partial Credit & Process Tracking**: Extend answer checking to award partial credit for correct approach with calculation errors. Track solution steps for multi-part problems and provide targeted feedback on which stage went wrong (setup vs. algebra vs. units).

## Notes & References

- Legacy `unit1_practice_doc` still returns a fully-evaluated list; refactor to match callable generator usage.
- Home page Unicode issue persists and is tracked above under Content & UX.
- Prior architectural docs (`docs/architecture.md`, `docs/ui.md`) should be refreshed once major UI refactors land.

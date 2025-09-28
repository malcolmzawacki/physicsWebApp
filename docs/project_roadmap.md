# Project Roadmap & Backlog

_Last updated: 2025-09-27_

## Recently Completed

- Linear motion generator now supports explicit `solve_for` overrides while keeping question narratives coherent.
- Added shared motion-context helpers to reduce repeated text logic without mutating physics outputs.
- Document generator now wraps question blocks to keep prompts, tables, and work space together across page breaks.

## In Progress / Short-Term Targets

- **Streamlit Navigation**: Evaluate replacing implicit `pages/` discovery with explicit `st.navigation` / `st.pages` declarations for clearer unit/module groupings.
- **Image & Graph Quality**: Standardize matplotlib/export styling and file handling so graphs render at consistent DPI in both Streamlit and DOCX exports.

## Backlog

### Problem Generators & Data Model

- Extend `solve_for` support (and related phrasing helpers) to other physics generators for consistent behavior.
- Surface generator metadata (equations, tags) through a formal hook that UI pages can consume uniformly.
- Add optional reproducible seeding so documents/tests can generate deterministic problem sets.
- Add physics/unit validation: dimensional checks, difficulty monotonicity, and sanity bounds for generated values.

### UI Layer & State Management

- Continue migrating legacy session-state calls to the `State` helper; audit diagram rendering and answer-checking paths for remaining direct `st.session_state` usage.
- Explore author tooling in the UI (e.g., expose solve-for overrides, seeds) for rapid debugging.

### Document Generation Pipeline

- Refactor `xtrct_docs/document_creator.py` to separate data extraction, markdown cleaning, table rendering, and answer-key assembly.
- Allow generator callbacks used for documents to receive contextual metadata (version index, seed) for reproducibility.
- Replace `os.startfile` with a platform-aware opener and wrap temp image creation in context managers for safer cleanup.

### Content & UX Polish

- Fix encoding glitches (e.g., garbled `Home.py` title, inconsistent m/sA� symbols) and adopt a consistent Unicode/LaTeX strategy.
- Centralize copy for equations, hints, and feedback strings; consider LaTeX helpers for formatting parity across UI and docs.
- Audit wording for direction reversals across all generators; align on shared helpers similar to the new linear-motion implementation.

### Testing & Tooling

- Expand payload validation into a lightweight smoke-test suite covering representative generators.
- Add unit tests for core generators, plus Streamlit snapshot tests for UI flows and document creation regression tests.
- Improve setup docs (README) and consider optional pre-commit hooks for linting/formatting.

## Strategic Initiatives (Streamlit-Compatible)

- **Context & Scenario Library**: Define reusable context packs (nouns, verbs, realistic value ranges, diagram assets) that generators can pull from for authentic problem statements.
- **Declarative Generator Framework**: Separate physics "engines" from presentation, and allow generators to be described via metadata/schema files that the runtime composes into the existing payload contract.
- **Authoring Workspace**: Build an author-mode dashboard inside Streamlit for seed controls, curated problem sets, previewing DOCX exports, and managing context packs.
- **Structured Solutions & Hints**: Extend generators to emit stepwise explanations (concept �+' equation �+' substitution �+' result) so both UI hints and answer keys stay consistent.
- **Learning Objectives & Analytics**: Tag problems with objectives/standards, log anonymized attempts to a lightweight datastore, and surface mastery dashboards for teachers.
- **Adaptive Practice Layer**: Use the collected performance data to bias future question selection (difficulty, solve_for, context) for individualized practice sequences.
- **Accessibility & Localization Upgrades**: Improve contrast/readability, offer dyslexia-friendly modes, and plan for multilingual prompts using a centralized copy system.

## Notes & References

- Legacy `unit1_practice_doc` still returns a fully-evaluated list; refactor to match callable generator usage.
- Home page Unicode issue persists and is tracked above under Content & UX.
- Prior architectural docs (`docs/architecture.md`, `docs/ui.md`) should be refreshed once major UI refactors land.

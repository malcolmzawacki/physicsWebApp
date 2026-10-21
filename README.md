# physicsWebApp

Interactive Streamlit workspace for generating and practicing physics (and chemistry) problem sets. The project bundles reusable question generators, a shared UI layer, and export tools so instructors can quickly spin up randomized practice or build printable worksheets.

## Where to look

For planning and classroom use, start with the first three documents below.
The rest are reference material to open when working on a particular feature.

| Question | Document | What it does not establish |
|---|---|---|
| Where is the site heading, and what should we work on next? | [Project roadmap](docs/project_roadmap.md) — educational direction, architectural direction, ordered queue, and future candidates | That a proposed feature is implemented |
| What works today, and what are the known limits? | [Current state](docs/current_state.md) — implemented scope and verification limits | Future priorities or a complete implementation reference |
| How do we update a family consistently? | [Site update process](docs/site_update_process.md) — work stages, review criteria, and documentation ownership | That a family has passed those stages |
| Which activities have been reviewed for organizing help? | [Organizing-help inventory](docs/organizing_help_inventory.md) — generated coverage list, linked to the review ledger and family notes | Readiness of every difficulty, target, or random branch |
| How is the app structured? | [Architecture](docs/architecture.md) — high-level code map; [payload contract](docs/problem_payload.md) and [organizing-help architecture](docs/organizing_help_architecture.md) for specific contracts | A replacement for current-state status or source verification |
| How do student worksheets work? | [Student worksheets](docs/student_worksheets.md) — controls, export setup, and verification | Automatic export support for every practice activity |

Other feature guides and family reviews are supporting references reached from
these documents. Dated audits and implementation notes preserve historical
evidence; use **Current state** for the reconciled status instead of interpreting
an old finding as an outstanding bug.

### Keeping documentation manageable

- Update the existing owner of a topic before creating another document. Product
  direction and future work belong in the roadmap; shipped behavior belongs in
  current state; rollout procedure belongs in the site update process.
- Keep detailed contracts in their feature guide and branch evidence in the
  family's review. Link to those details instead of copying them across summaries.
- Create a new guide only for a distinct, durable topic with no suitable home,
  and link it from the relevant entry point. Routine changes do not need a new
  dated report, strategy document, or parallel backlog.
- When a document is superseded, identify its replacement and retain useful
  evidence. Any later archive/consolidation pass should preserve incoming links.

## Quick Start

1. **Install dependencies**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Launch the Streamlit app**
   ```bash
   streamlit run Home.py
   ```
3. Open the provided localhost URL in your browser and choose any page from the sidebar to begin.

## Project Layout

- `Home.py` - single-page router that swaps the sidebar based on the current section/activity.
- `app_pages/` - activity modules referenced by the router (legacy page files, now used as function containers).
- `utils/` - shared infrastructure:
  - `generators/` - problem generators that emit payloads consumed by the UI layer.
  - `ui.py`, `ui_components.py`, `ui_state.py` - Streamlit interface helpers and session-state utilities.
  - `problem_payload.py` - canonical schema for generator outputs (see `docs/problem_payload.md`).
  - `word_lists.py`, `graph_utils.py`, etc. - supporting content helpers.
- `tools/` - developer scripts such as lazy tab loaders and payload validators.
- `xtrct_docs/` - utilities for exporting problems into Word documents.
- Export entry point: `python -m xtrct_docs.doc_face` (edit the selected preset/title there). Diagrams are included by default; see [export and compatibility updates](docs/implementation_fixes_2026-09-14.md).
- Student worksheet pilot: **Kinematics > Create a worksheet**. Students download PDFs, requiring LibreOffice on the server; see [setup and verification](docs/student_worksheets.md). Instructor Word exports remain available through the export entry point.
- `docs/` - architecture notes (e.g., generator payload contract, UI guide).

## Development Workflow

- **Author mode** - set `AUTHOR_MODE=True` in `config.py` to surface rich diagnostics inside the UI during generator development.
- **Testing generators** - run the validation script to ensure each generator returns a valid payload:
  ```bash
  python tools/validate_payloads.py
  ```
- **Correctness guardrail** - run prompt/answer and `solve_for` consistency checks:
  ```bash
  python tools/check_prompt_answer_consistency.py
  ```
- **Static checks** - the project currently relies on manual review; add `pydocstyle`, `flake8`, or similar as needed for your workflow.
- **Interaction and export regressions** — run `python tools/test_activity_flow.py`, `python tools/test_relative_motion_page.py`, `python tools/test_audit_regressions.py`, `python tools/test_progress_and_formatting.py`, and `python tools/test_solve_for.py`. CI also runs student worksheet and organizing-help checks listed in [current state](docs/current_state.md). Payload validation discovers generators automatically.
- **Recognizing Forces pilot** — Dynamics > Recognizing Forces; run `python tools/test_recognizing_forces.py` for conceptual content and routed interaction checks.
- **Force diagram matching pilot** — Dynamics > Match the Free-Body Diagram; run `python tools/test_force_diagram_match.py` for physics, unique choices, artwork, and interaction checks.
- **Diagram builder pilot** — Dynamics > Free-Body Diagram Builder; run `python tools/test_force_diagram_builder.py` for qualitative construction physics and the live editor lifecycle.
- **Force and Motion Matching pilot** — Dynamics > Force and Motion Matching; run `python tools/test_force_motion_match.py` for multiple-answer sets, consistent dot diagrams and routed interaction checks. `node tools/test_graph_cards_frontend.js` checks shared single/multiple card behavior with Node 22 and no extra packages.
- **Change of State pilot** — Dynamics > Change of State; run `python tools/test_force_change.py` for one-force before/after changes, exact-set decisions and page interactions.
- **Ranking pilot** — Dynamics > Net Force and Acceleration Ranking; run `python tools/test_force_ranking.py` for exact tied rankings, controlled masses/modes and routed interactions.
- **Session pacing and review** — the shared sidebar checkbox controls automatic loading after correct answers on all practice activities. My Current Session Progress shows answer checks, submitted/correct answers, explanations where available, and matching graphs. History and preferences live only in Streamlit session memory and reset on browser refresh; no persistent student identifier or storage is added. Run `python tools/test_session_progress.py` for routed pacing, history, navigation, and new-session regressions.
- **Stable progress IDs and Word formatting** — see the [implementation notes and manual review checklist](docs/implementation_fixes_2026-09-15.md).

## Contributing Notes

Solve-for controls and worksheet target requests share an explicit catalog. See
the [page-by-page evaluation and export examples](docs/solve_for_evaluation.md),
[available targets](docs/solve_for_targets.md), and
[deferred decisions](docs/solve_for_deferred.md).

1. Extend or create generators in `utils/generators/` and follow the dict payload contract.
2. Update the existing documentation owner for changed behavior or contracts; use the documentation rules above before adding a file.
3. Keep README steps up to date when setup or testing expectations change.

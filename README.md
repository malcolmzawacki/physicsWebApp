# physicsWebApp

Interactive Streamlit workspace for generating and practicing physics (and chemistry) problem sets. The project bundles reusable question generators, a shared UI layer, and export tools so instructors can quickly spin up randomized practice or build printable worksheets.

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
- `docs/` - architecture notes (e.g., generator payload contract, UI guide).

## Development Workflow

- **Author mode** - set `AUTHOR_MODE=True` in `config.py` to surface rich diagnostics inside the UI during generator development.
- **Testing generators** - run the validation script to ensure each generator returns a valid payload:
  ```bash
  python tools/validate_payloads.py
  ```
- **Static checks** - the project currently relies on manual review; add `pydocstyle`, `flake8`, or similar as needed for your workflow.

## Contributing Notes

1. Extend or create generators in `utils/generators/` and follow the dict payload contract.
2. Add documentation in `docs/` when introducing new interaction patterns or complex flows.
3. Keep README steps up to date when setup or testing expectations change.

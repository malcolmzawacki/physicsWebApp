# Author Mode & Tooling

Author mode unlocks diagnostics that make it easier to develop and troubleshoot generators or UI flows.

## Enabling Author Mode

- Set the environment variable before launching Streamlit:
  ```bash
  set APP_AUTHOR_MODE=1
  streamlit run Home.py
  ```
- Alternatively, toggle `AUTHOR_MODE = True` in `config.py` during local development (avoid committing this change).

When enabled, `utils/ui.Interface` surfaces additional debugging aids:

- Exceptions from `choose_problem_dict` render inside the page instead of generic error banners.
- The `Debug` expander shows the normalized payload, answer metadata, optional features, and any extras returned by the generator.
- Diagram rendering errors are printed so you can inspect failing matplotlib code.

## Helpful Utilities

- `tools/validate_payloads.py` – exercises core generators across problem types and difficulties, ensuring the payload schema stays consistent.
- The router lazy-loads activities via handler strings; keep heavy imports inside activity functions for fast startup.
- `xtrct_docs/` scripts – reuse generators to build printable worksheets and verify that exported artifacts match the interactive experience.

## Recommended Workflow

1. Enable author mode and load the relevant page in Streamlit.
2. Use the debug panel to confirm the generator payload (answers, units, metadata) looks correct.
3. Run `python tools/validate_payloads.py` to catch schema regressions.
4. Update docs (`docs/ui.md`, `docs/generator_conventions.md`, etc.) when behavior or expectations change.

Keep author mode disabled in production deployments to avoid exposing stack traces or developer-only information to end users.

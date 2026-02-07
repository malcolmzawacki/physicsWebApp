# Application Architecture

This project runs as a single-page Streamlit app with a custom router that swaps the sidebar based on where students are in the curriculum. The high-level flow is:

1. `Home.py` renders the custom sidebar (main areas or section-specific activities) and routes to a selected activity.
2. The activity function instantiates `utils.ui.Interface` with a generator and difficulty list.
3. The interface requests a dict payload from the generator and normalizes it through `utils.problem_payload.payload_from_dict`.
4. The UI writes question data, metadata, and optional extras into namespaced Streamlit session state via `utils.ui_state.State`.
5. The interface renders inputs using helpers in `utils.ui_components.py`, validates submissions, and stores performance stats.
6. Optional tools (e.g., export scripts in `xtrct_docs/`) can re-use generators to build printable worksheets or documents.

## Modules at a Glance

- **Home.py** ? root entry point that owns the custom router and context-aware sidebar.
- **app_pages/** ? activity modules referenced by the router via lazy handlers.
- **utils/generators/** ? core business logic for creating randomized physics and chemistry problems. Subpackages (like `energy/`) group related domains.
- **utils/ui.py** ? orchestrates question lifecycle, answer validation, diagrams, hints, and gamification.
- **utils/ui_components.py** ? shared render helpers (headers, tables, hints, debug panel, etc.).
- **utils/ui_state.py** ? wrapper to namespace session-state keys per page/prefix.
- **utils/problem_payload.py** ? dataclass and normalizer for generator outputs.
- **tools/** ? developer utilities such as `validate_payloads.py` for payload smoke tests.
- **xtrct_docs/** ? Word export helpers powered by `python-docx` and `matplotlib`.
- **docs/** ? knowledge base for contributors (`problem_payload.md`, `ui.md`, and the guides in this folder).

## Runtime Flow Details

```
Router (Home.py) -> Activity function -> Interface -> Generator -> problem_payload -> UI components -> Session State -> User feedback
```

- **Router layer** controls which activities appear in the sidebar and which function runs.
- **Activity layer** declares titles, prefixes, and generator combinations (formerly page/tab definitions).
- **Custom activities** that bypass `Interface` should use `utils.ui_state.State` (or a thin proxy) for namespaced session state.
- **Interface** centralizes state initialization, rendering, and response handling.
- **Generator** returns a dict payload describing the question, answers, and optional features (see `docs/problem_payload.md`).
- **UI components** render the question, input widgets, diagrams, hints, and debugging aids.
- **Session state** keeps the current question, metadata, and performance metrics resilient across reruns.

## Export & Automation

- The `xtrct_docs` package can call the same generators to build DOCX worksheets. It uses `utils/graph_utils.py` to embed matplotlib figures.
- Additional automation scripts can be added under `tools/` and follow the same generator contract.

## Future Enhancements

- Stabilize automated linting/testing (consider `pytest`, `pydocstyle`, or `ruff`).
- Expand docs with diagrams or flowcharts once architecture stabilizes.
- Enforce the dict payload contract for all generators to keep UI integration consistent.

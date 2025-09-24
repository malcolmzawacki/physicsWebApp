# Application Architecture

This project is a multipage Streamlit app built around reusable problem generators. The high-level flow is:

1. A Streamlit page in `pages/` instantiates `utils.ui.Interface` with a generator and difficulty list.
2. The interface requests a dict payload from the generator (or falls back to legacy tuples) and normalizes it through `utils.problem_payload.payload_from_dict`.
3. The UI writes question data, metadata, and optional extras into namespaced Streamlit session state via `utils.ui_state.State`.
4. The interface renders inputs using helpers in `utils.ui_components.py`, validates submissions, and stores performance stats.
5. Optional tools (e.g., export scripts in `xtrct_docs/`) can re-use generators to build printable worksheets or documents.

## Modules at a Glance

- **Home.py** – root entry point that sets basic configuration and lets users pick a topic.
- **pages/** – Streamlit implementations for each topic. They typically import one or more generators and call `Interface.unified_smart_layout()`.
- **utils/generators/** – core business logic for creating randomized physics and chemistry problems. Subpackages (like `energy/`) group related domains.
- **utils/ui.py** – orchestrates question lifecycle, answer validation, diagrams, hints, and gamification.
- **utils/ui_components.py** – shared render helpers (headers, tables, hints, debug panel, etc.).
- **utils/ui_state.py** – wrapper to namespace session-state keys per page/prefix.
- **utils/problem_payload.py** – dataclass and normalizer for generator payloads.
- **tools/** – developer utilities such as `loading.lazy_tabs` for deferred imports and `validate_payloads.py` for payload smoke tests.
- **xtrct_docs/** – Word export helpers powered by `python-docx` and `matplotlib`.
- **docs/** – knowledge base for contributors (`problem_payload.md`, `ui.md`, and the guides in this folder).

## Runtime Flow Details

```
Streamlit page -> Interface -> Generator -> problem_payload -> UI components -> Session State -> User feedback
```

- **Page layer** declares tab structure, titles, and generator combinations.
- **Interface** centralizes state initialization, rendering, and response handling.
- **Generator** returns a dict payload describing the question, answers, and optional features (see `docs/problem_payload.md`).
- **UI components** render the question, input widgets, diagrams, hints, and debugging aids.
- **Session state** keeps the current question, metadata, and performance metrics resilient across reruns.

## Legacy vs Modern Generators

- New work should return dict payloads (`question`, `answers`, `units`, etc.) so the interface can enrich the UI with diagrams, hints, button options, and metadata.
- Legacy tuple-based generators are still supported through `Interface._store_legacy_result`. The page detects the format (`generation_format`) and renders a classic layout until the generator is migrated.

## Export & Automation

- The `xtrct_docs` package can call the same generators to build DOCX worksheets. It uses `utils/graph_utils.py` to embed matplotlib figures.
- Additional automation scripts can be added under `tools/` and follow the same generator contract.

## Future Enhancements

- Stabilize automated linting/testing (consider `pytest`, `pydocstyle`, or `ruff`).
- Expand docs with diagrams or flowcharts once architecture stabilizes.
- Gradually migrate remaining legacy generators to the dict payload contract for richer UI integration.

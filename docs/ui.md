## Streamlit UI Overview

The UI layer lives in `utils/ui.py` and wraps Streamlit helpers that power every practice page. It provides a configurable interface class that handles question generation, answer capture, scoring, and feature toggles so individual pages only declare their title, generator, and difficulty mix.

### Primary Entry Point: `Interface`

- Constructed with a namespace prefix, display title, generator instance, and list of difficulties. Optional arguments include explicit problem type metadata and weighting for the star scoring system.
- Resolves problem types either from an explicit dict/list or through `generator.get_problem_types()`; raises if nothing can be inferred so page authors spot misconfigured generators early.
- Namespaces all Streamlit session-state keys with the provided prefix by delegating to `utils.ui_state.State`, preventing cross-tab collisions.
- Exposes convenience methods (`unified_smart_layout`, `question_ui_dict`, etc.) that pages call once per rerun; these helpers orchestrate rendering, submission handling, and follow-up actions like automatic question refresh.

### Session-State Lifecycle

When `unified_smart_layout` runs it calls `initialize_session_state` which:

- Seeds core keys such as `current_question`, `correct_answers`, `difficulty`, `problem_type`, and tracking counters (`question_id`, `stars`).
- Lazily initializes the performance tracking payload via `ui_components.init_performance` so the data frame persists across reruns until the user explicitly resets it.
- Carries forward user-specific toggles like the equation level checkbox (`state.get("level")`).

All mutation flows through the `State` helper which prefixes keys (`{prefix}_{name}`) and guards against missing entries with `ensure`/`ensure_lazy`.

### Question Generation Pipeline

`generate_question_once(problem_type, difficulty)` is the heart of the workflow:

1. Calls `generator.choose_problem_dict` and catches exceptions to surface author-mode diagnostics or generic user errors.
2. Normalizes the response via `utils.problem_payload.payload_from_dict`, ensuring the payload conforms to the required schema.
3. Writes question text, answers, units, and feature metadata back into session state while incrementing the `question_id` counter.
4. Immediately triggers `st.rerun()` so the freshly stored data renders on the next Streamlit pass.

Legacy tuple-based generators can still be supported through `_store_legacy_result`, but new work should adhere to the dict contract documented in `docs/problem_payload.md`.

### Optional UI Features

Generators can opt into richer interactions by populating extra keys in the result dict:

- `diagram_data`: consumed by `add_diagram_smart`, which calls `generator.generate_diagram` if implemented and renders the returned Matplotlib figure inside an expander.
- `button_options`: enables multiple-choice questions via `question_ui_buttons`. When absent, the interface falls back to text inputs rendered by `ui_components.draw_answer_inputs`.
- `hints`: displayed through `render_hints` when present; ordering is respected.
- `show_equations`: allows generators to force the equations expander open even if the page hides equation metadata by default.
- `tags`, `timer`, and any additional extras are preserved in session state for downstream UI or analytics.

### Answer Validation and Feedback

- Text-input answers flow through `question_ui_dict`, which validates numeric fields, enforces tolerance (+/-10% by default), and logs results via `update_performance` before showing success/error toasts.
- Button-based activities route through `question_ui_buttons` and `check_button_answers`, comparing exact string matches before updating performance records.
- The optional loading animation (`loading_q_dict`) presents a timed progress bar between questions unless the user cancels it.

### Performance Tracking & Gamification

- `init_performance`, `record_performance`, and `build_performance_table` (from `ui_components`) maintain an attempts/correct matrix keyed by problem type and difficulty.
- `performance_dropdown` surfaces the tracking table inside an expander so students can review their history without leaving the tab.
- `give_stars` awards points based on difficulty and (optionally) problem-type weighting; stars render in the page header and in specialized activities like the graph-matching game.

### Supporting Modules

- `utils/ui_components.py` bundles reusable fragments (headers, data frames, expander layouts, hint drawers, debug panels). Each helper expects already-prefixed session state data supplied by the `Interface` class.
- `utils/ui_state.py` centralizes prefixed session-state access to avoid hard-coded key strings and improve testability.
- `utils/config.py` exposes the `AUTHOR_MODE` toggle; when enabled the UI surfaces tracebacks in-place and keeps the debug panel available.
- `tools/loading.py` offers `lazy_tabs`, which defers expensive imports until a tab is visited, reducing initial load time for heavy modules like the motion graph generator.

### Author Mode & Debugging

Setting `AUTHOR_MODE` (via config or the `APP_AUTHOR_MODE` environment variable) unlocks inline diagnostics:

- Exceptions during question generation bubble up inside Streamlit expanders instead of generic `st.error` messages.
- `debug_panel` shows the raw payload, feature toggles, and metadata so generator authors can confirm schemas quickly.

### Extending the UI Layer

When building new pages or generators:

1. Create or update the generator to follow the dict payload contract and expose metadata through `stored_metadata` when equations/notes are needed.
2. Instantiate `Interface` inside the Streamlit page, passing a unique prefix (short and descriptive) to keep session state isolated.
3. Use `unified_smart_layout` for the common card-style flow, and pass keyword tweaks such as `side_by_side=True` or `equations=False` to adjust the layout.
4. Provide fallback equation dictionaries or other custom UI behavior through keyword arguments or by extending `Interface` if the page needs bespoke controls.

For unusual layouts (e.g., matching activities), the interface helpers can be mixed with direct Streamlit calls while still relying on the session-state and generator lifecycle managed by `Interface`.

### Related Files

- `utils/ui.py` - core interface implementation.
- `utils/ui_components.py` - reusable render helpers.
- `utils/ui_state.py` - namespaced session-state wrapper.
- `utils/problem_payload.py` - payload normalization and validation.
- `docs/problem_payload.md` - companion schema documentation.
- `tools/loading.py` - lazy tab loader used by multipage layouts.

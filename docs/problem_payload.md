## Problem Payload Schema

Every generator should return a dictionary payload with this structure. The UI normalizes it through `utils.problem_payload.payload_from_dict` which validates required fields.

Keys:

- `question` (str) — required. Render-ready prompt (Markdown/LaTeX allowed).
- `answers` (list[Any]) — required. One or more canonical answers (order aligned to units).
- `units` (list[str]) — required. Unit labels for each answer (use empty string if unitless).
- `problem_type` (str) — optional. Helpful for analytics; UI may override.
- `difficulty` (str) — optional. Helpful for analytics; UI may override.
- `diagram_data` (Any) — optional. Raw data for a diagram/figure helper.
- `button_options` (dict[int, list[str]]) — optional. Multiple-choice options indexed by answer part.
- `hints` (list[str]) — optional. Ordered hints to show in the UI.
- `extras` (dict[str, Any]) — optional. Freeform bag for future features.

Required invariants:

- `len(answers) == len(units)`
- `question` is non-empty
- Numerical answers should match UI comparison/tolerance rules

Normalization rules:

- Unknown top-level keys are placed under `extras` by the normalizer.
- Missing required keys cause a validation error.


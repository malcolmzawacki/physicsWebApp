# Generator Conventions

Generators live in `utils/generators/` and are responsible for returning randomized problems that conform to the `ProblemPayload` contract. Follow these guidelines when creating or updating a generator.

## Payload Basics

- Return a dict with `question`, `answers`, and `units` at minimum; see `docs/problem_payload.md` for the full schema.
- Use plain strings for display-ready prompts (Markdown/LaTeX is fine; Streamlit renders both).
- Provide answer lists in the order the UI should render inputs; units must align one-to-one with answers.
- Include optional metadata when available:
  - `diagram_data` for figures you can generate in `generate_diagram()`.
  - `button_options` when multiple-choice buttons make sense.
  - `hints`, `tags`, `time_limit`, `show_equations`, `extras` for richer UI behavior.

## Modern vs Legacy APIs

- Prefer overriding `choose_problem_dict(problem_type, difficulty)` and returning the dict payload directly.
- The `BaseGenerator` class still offers a legacy tuple interface (`choose_problem`). If you must use it temporarily, ensure the tuple entries map to `(question, answers, units, diagram_data)` so the interface can adapt.
- When migrating legacy generators, implement `choose_problem_dict` first, then delete the tuple method and any unused helpers once parity is achieved.

## Difficulty & Randomization

- Implement a helper like `get_difficulty_range()` to scale random values according to the UI-selected difficulty.
- Ensure each difficulty tier produces distinct cognitive load (not just bigger numbers) so the practice flow feels meaningful.
- Use deterministic patterns where validation matters (e.g., ensuring acceleration values line up with motion equations) and encapsulate math helpers for reuse.

## Metadata & UI Integration

- Provide `stored_metadata()` or `get_problem_metadata()` so the UI can surface equations, conceptual explanations, or notes per problem type.
- Populate `button_options` when the answer set is finite (directions, qualitative states, etc.) to unlock the multiple-choice UI.
- Set `show_equations` to `True` when a question requires the equations expander even if the user has not opted in.

## Testing & Validation

- Run `python tools/validate_payloads.py` after changes to confirm payload shape compliance across all difficulties and problem types.
- Consider lightweight asserts within generators to guard against invalid random draws (e.g., division by zero, negative distances where not allowed).
- When adding new generators, update validation scripts or tests so they are exercised automatically.

## Author Mode Tips

- While developing, set `APP_AUTHOR_MODE=1` to surface stack traces and the `Debug` expander inside the UI.
- The debug panel shows the generator payload, diagram data, hints, and other metadata; use it to confirm new fields are wired correctly.

## Documentation Expectations

- Add or update docs in `docs/` whenever you introduce a new generator pattern, metadata field, or export pathway.
- Keep inline comments sparse but meaningful; prefer docstrings for describing non-obvious math helpers or probability distributions.

By following these conventions, generators will integrate smoothly with the shared interface and remain easy to maintain.

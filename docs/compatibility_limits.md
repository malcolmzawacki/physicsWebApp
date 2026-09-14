# Compatibility limits across activity layouts

_Inspected: 2026-09-11. These are source-verified constraints and open follow-ups,
not a completed repository-wide migration or an exhaustive runtime audit._

Read this alongside [page conventions](page_conventions.md), the
[payload contract](problem_payload.md), and [activity flow](activity_flow.md)
before moving an existing activity into a new layout. The Relative Motion page
works with its current adapters; that does not imply all features are portable.

## 1. Equation metadata has two naming conventions

Evidence: `utils/ui_components.py::show_equations_expander` looks for
`honors_equation` / `conceptual_equation` in `get_problem_metadata()`, but looks
for `honors` / `conceptual` in its fallback dict. `BaseGenerator`'s default
`get_problem_metadata()` simply returns an entry from `stored_metadata()`.
Generators such as Relative Motion use the short names.

Consequence: a generator can provide valid equation metadata yet show no
equations when a layout omits the fallback dict. The renderer expects one LaTeX
string, not a list of equation strings. Relative Motion joins equations into a
`gathered` environment and supplies the fallback.

Future direction: normalize both naming conventions at one boundary, establish
one canonical metadata shape, and test base/expanded views without a fallback.

## 2. Payload acceptance does not guarantee feature rendering

Evidence: `utils/problem_payload.py::payload_from_dict` preserves unknown keys in
`extras`. `utils/ui.py::Interface._store_dict_result` stores the core fields and
an explicit top-level feature allowlist; it does not retain `payload.extras`.
The list includes `explanation`, but `unified_smart_layout` does not render a
worked explanation. Relative Motion renders its own `extras.solution_equations`
and `extras.explanation` from its full saved payload.

Consequence: swapping Relative Motion into the standard layout could retain
the question and answer while losing the canonical case and worked solution.
Likewise, `timer`, `time_limit`, and the layout's `timer` argument are not one
unified behavior: storage or presence in a payload does not activate a timer.
The architecture overview's broad claim about retaining extras should not be
treated as a guarantee of the current Interface implementation.

Also, the normalizer reuses the input `extras` dict when adding unknown fields,
so normalization can mutate the caller's extras. Clone before normalizing if
the same case is being shared across consumers that require immutable input.

Future direction: retain one normalized payload and explicitly document which
features each layout renders. Test feature retention, not just payload validity.

## 3. Answer grading is not yet a shared policy

Evidence:

- `Interface.check_answers_dict` uses 10% of the expected answer as tolerance,
  with exact equality at zero. Its numeric input path accepts Python float
  parsing without a separate finite-value check.
- Relative Motion uses `math.isclose(..., rel_tol=.1, abs_tol=1e-9)` and rejects
  non-finite input before recording a submission.
- The current-electricity circuit and series/parallel pages use
  `max(abs(answer) * .05, .05)` as the tolerance.
- `Interface.check_button_answers` uses exact equality; free-text string
  grading lowercases and trims the student input.

Consequence: moving an exercise between layouts can change accepted answers,
especially near zero, or turn an invalid entry into a counted wrong attempt.
The electrical pages' absolute tolerance is in the answer's current units,
so changing those units also changes the effective precision requirement.

Future direction: share parsing and grading while allowing explicit per-question
tolerances and string/choice policies. Preserve intentional instructional
differences; do not silently impose one tolerance on every activity.

## 4. Mixed answer controls and dropdown semantics are restricted

Evidence: `render_button_options` and `render_dropdown_options` create text
fallbacks when a part has no choices, but do not copy that text into
`user_answers_selected`. `Interface.question_ui_buttons` submits that selection
list, so a mixed numeric/choice payload does not have a complete input path.
It also rejects repeated selected values for every dropdown-mode question,
regardless of whether the problem actually represents a ranking.

Consequence: a payload with speed plus direction cannot assume numeric entry
works just because the choice layout displays a text box. Independent dropdown
answers that legitimately repeat are rejected by the ranking rule.

Future direction: define an input type per answer part, unify answer collection,
and make uniqueness an explicit question constraint rather than a widget-mode
assumption. Add mixed-input and valid-duplicate regression cases before reuse.

## 5. Diagram matching remains a separate lifecycle

Evidence: `utils/layouts/diagram_match_layout.py` consumes `prompt`,
`primary_diagram`, `option_diagrams`, and `correct_index`, rather than the
standard ProblemPayload. Its `_auto_advance` is separate from the new
`utils.activity_flow.next_question_countdown` and uses an activity-level cancel
key, not a per-question key. Its scoring increments stars directly without a
submitted guard or the shared performance-recording helpers.

Consequence: the previous countdown extraction covers Interface and Relative
Motion, not every layout. If a correct matching set remains after cancellation,
checking that same correct set again can award another star. Changing controls
also does not inherently regenerate its saved payload; generation is triggered
by the explicit button, missing payload, or advancement.

Future direction: migrate matching with a new question ID, one-attempt scoring,
explicit control-change policy, and a payload adapter. Do not substitute its
timer alone and assume the remaining lifecycle conventions are satisfied.

## 6. Generator options and progress identity are implicit

Evidence: `BaseGenerator.choose_problem_dict` defines only problem type and
difficulty. Some concrete generators add `solve_for`, with their own supported
values. Interface regenerates when type/difficulty changes, and its stars and
performance records derive from the ordered difficulty/type lists and display
labels. Custom pages must manage their additional selector state themselves.

Consequence: optional generator arguments are not portable without an adapter;
changing an extra selector must invalidate the old question. Renaming labels
can split existing session performance history, and reordering difficulty
options changes star awards. Namespaced State prevents key collisions but does
not migrate data shapes or make statistics persistent across sessions.

Future direction: use explicit generator capabilities/options and stable IDs
separate from display labels, with declared scoring weights and state migration
where needed. Keep callbacks responsible for preserving custom selections.

## 7. CI does not yet cover the new interaction tests

Evidence: `.github/workflows/correctness-guardrails.yml` runs
`tools/validate_payloads.py` and `tools/check_prompt_answer_consistency.py`.
It does not run `tools/test_relative_motion_page.py` or
`tools/test_activity_flow.py`. The payload validator uses an explicit generator
registry; custom layouts/models outside that registry need separate coverage.

Consequence: passing CI currently does not prove that messages, cancellation,
auto-advance, selectors, or stars still work. The new UI tests were run locally
when implementing the shared countdown, but future changes need to run them
explicitly until they are added to CI.

Recommended follow-up order: mixed-input correctness and diagram-match scoring;
shared payload/metadata contracts; explicit grading policies; then broader
generator capability/state conventions. Add UI regression coverage to CI with
those changes. These are recommendations, not changes implemented by this note.

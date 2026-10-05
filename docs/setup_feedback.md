# Organizing-help feedback

Organizing help uses its own Streamlit form with Enter submission enabled and
entries retained after checking. Tab moves between inputs; Enter submits only
the setup form. Edits are buffered in the browser until submission, so existing
feedback is labeled as the last check and remains visible while revising. New
questions reset the workspace. The final-answer form remains independent.

The shared contract is documented in [organizing_help_architecture.md](organizing_help_architecture.md).
Generators now emit validated `extras.setup`; the Accelerated Motion generator also retains a derived compatibility `extras.setup_expected`: numeric givens
(including implied zero), `?` for the requested quantity, and `x` for an absent
quantity. Hidden computed answers are not candidates for matching a given.

`utils/setup_feedback.py` owns pure checking and ordered feedback rules. Each
result has a status, stable code, and student-facing message. Correct and blank
entries are handled first; then the first supported rule wins; otherwise the
`unclassified` fallback gives a neutral next step. `utils/setup_workspace.py`
only renders these results below their corresponding inputs and suppresses stale
feedback after edits. Setup checks do not count as final-answer attempts.

The first rule, `matches_other_given`, matches signed numbers against other
numeric givens. It prompts students to revisit units and wording without claiming
to know their reasoning or naming a unique source when multiple givens share a
number. Velocity fields also mention start/end wording. Sign-only discrepancies
are deliberately left to the fallback to avoid an accidental cross-match.

To extend: add a pure rule with a stable code, specify its precedence, and cover
positive matches plus counterexamples in `tools/test_setup_workspace.py`. Keep
quantity metadata with the generator and display definitions in the planned
shared quantity catalog. No AI service, persistence, email, or event collection
is involved. The codes are local result categories, not telemetry.

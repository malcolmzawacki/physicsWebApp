# Reusing feedback and automatic question advancement

For additional open constraints beyond the countdown, see
[Compatibility limits across activity layouts](compatibility_limits.md).

`utils.word_lists.random_correct_message` and `random_error_message` already
provide layout-independent feedback text. Select the message when an answer is
scored and save it in namespaced State when feedback persists across reruns.
Rendering must not re-award stars or record another attempt.

`utils.activity_flow.next_question_countdown(state, question_id, on_next, seconds=3)`
provides the progress bar and Cancel Next Question control. Call it only after
correct feedback and any worked solution have been rendered. The caller supplies
the question replacement callback, including its selected options and rerun.
No generator, payload schema, scoring rule, or page layout is assumed.

The timer deadline survives reruns. Cancellation is keyed by activity and question,
so it does not carry into another question or another page. If cancellation is
removed after the deadline, advancement is immediate. The callback fires at most
once for a given question ID. A different question must use a new ID.

## Compatibility findings

- The previous `Interface.loading_q_dict` directly invoked
  `generate_question_once(problem_type, difficulty)`. Relative Motion stores a
  canonical payload and also has a solve-for selection; calling that old method
  would bypass the custom page's state and selector. The reusable callback fixes
  this. `loading_q_dict` remains a backward-compatible adapter for standard pages.
- The previous cancellation checkbox had no explicit key. The new component
  namespaces it by page and question to avoid widget collisions and stale pauses.
- Standard Interface feedback/scoring methods still assume Interface-managed
  state and render feedback only in the submit event. Custom pages keep their
  persistent result handling; they should not call those scoring methods a second
  time merely to render feedback. This change does not migrate those methods or
  the other custom electricity pages to a new result schema.
- The countdown retains the existing synchronous Streamlit model: it occupies
  the script run briefly while showing progress. If future layouts need live
  controls during the delay, a fragment-based timer would be a separate change.

Validated with Relative Motion (all selector combinations, custom messages,
automatic advancement preserving solve-for, cancellation, incorrect answers,
single scoring), a standard Constant Motion page, and isolated countdown tests.

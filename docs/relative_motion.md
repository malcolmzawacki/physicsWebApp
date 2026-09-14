# Relative Motion

Available through Advanced > Kinematics > Relative Motion. Both the router and
the page entrypoint check course level, including when switching back to High School.
This uses the app's course selector, not account-based authorization.

All cases use constant signed velocities along a single axis. Every velocity names
its subject and reference frame. Independent motion uses right as positive;
boat scenarios use downstream as positive.

| Type | Easy | Medium | Hard |
| --- | --- | --- | --- |
| Independent motion | Relative velocity | Separation after a known time | Meeting/catch-up time |
| Nested reference frames | Person/boat/shore: 2 links | Person/boat/water/shore: 3 links | Add a moving walkway: 4 links |
| Combined | Two people, 2 links each | Two people, 3 links each | Two people, 4 links each |

Solve for Result, Missing velocity, or Mixed practice. A missing velocity can be
any identifiable link, including a boat's, person's, walkway's, or (in nested
cases) water's velocity. The shared current in combined cases cancels and is
excluded from unknown selection. Medium independent cases avoid crossing;
Hard cases guarantee a positive meeting time.

`build_case` generates canonical physics data once. `render_case` hides a chosen
unknown and provides givens, an answer, a diagram with no unknown direction/value
leak, and worked equations. Pass `result` or a link index to `render_case`; the
generator's compatibility entrypoint also accepts the UI target labels.
Canonical cases and worked solutions live in payload `extras`.

The page reuses Interface's namespaced State, stars, and performance tracking,
with a form and post-submission solution. Correct answers show a message from
`utils.word_lists` and automatically advance after the shared three-second
countdown. Cancel Next Question keeps the solution visible. Incorrect answers
show a custom error message and wait for New Question. Messages are selected
once per submission and remain stable on reruns. One attempt is scored
per question, matching the shared UI. Numeric tolerance follows the existing 10%
convention; non-finite inputs are rejected and zero answers require near-zero input.
Base and More Equations views use LaTeX. The fixed example solves the river
current: person/boat = -1, boat/water = 3, person/shore = 4, so water/shore = 2 m/s.

Validation: `tools/validate_payloads.py`, `tools/check_prompt_answer_consistency.py`,
and `tools/test_relative_motion_page.py`. Future extensions can add 2D vectors,
nonuniform currents, or acceleration without changing this first page's scope.

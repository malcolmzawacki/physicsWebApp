# Circuit Fundamentals

_Updated: 2026-10-12. Previously named Circuit Ohm's Law; the page handler and state namespace are unchanged._

This activity practices one circuit relationship at a time. Series and parallel
circuits are included where they help isolate a relationship; component count is
not the boundary between this page and Series and Parallel Circuits.

## Current scope

| Task | Learning focus | Supplied information |
|---|---|---|
| Single Resistor | Use Ohm's law to find voltage, current, or resistance | Two of V/I/R; all targets and difficulties |
| Series Current and Voltage | Apply shared current to calculate the voltage across R1 and R2 | Shared current, R1, R2 |
| Parallel Current and Voltage | Apply shared voltage to calculate the current through R1 and R2 | Source voltage, R1, R2 |

All three tasks support Easy, Medium, and Hard. Difficulty changes the numbers,
not the learning task. Both paired tasks request two component answers and supply
every resistance in the diagram. There is no separate Givens panel; identifying
the quantities belongs to the student and organizing-help workspace. These are
ideal sources, ideal wires, and ohmic resistors, with curated classroom values.
The parallel source maintains its given voltage regardless of branch resistance.

The network page owns equivalent-resistance practice, Series Total Current,
Series Voltage Drop, and Parallel Branch Current. The duplicate Series Current
selector was removed rather than keeping its difficulty-dependent resistance/current
behavior. Source-only Series Voltage Drop moved to the network page; Fundamentals
supplies current for its Series Current and Voltage task. The former standalone
Shared Current and Branch Voltage tasks are retired; their relationships are
explained within the paired calculations rather than asked as copied givens.

Both pages use shared series/parallel schematic geometry and retain textual
fallbacks when schemdraw is unavailable. Multi-loop analysis, power, additional
component types, and a separate Equivalent … section remain deferred.

## Layout and progression

Diagrams occupy half the main row and scale to the available column width.
The shared series geometry reserves a longer lead for the current annotation,
separating it from resistor labels in both browser and exported diagrams.
New Question (Circuit) and Your Performance share a footer row, matching the
standard activity layout. One footer button handles skipping, continuing after
wrong answers, and advancing after a paused correct answer. Automatic advancement
and its pause checkbox still apply to correct answers only.

## Single Resistor organizing-help scope

The Single Resistor subtype now has shared Battery voltage (V), Current (I), and
Resistance (R) roles. All three targets are reviewed at Easy, Medium, and Hard.
Series Current and Voltage, Parallel Current and Voltage,
and the separate Series and Parallel Circuits page remain outside this organizer rollout. Their inventory reviews remain blank.

For an ideal single-resistor loop, battery voltage equals the potential difference
across the resistor. This profile intentionally has one voltage role; it does not
generalize to source/component voltages in circuit networks. Units are V, A, and
ohms; no conversions, negative values, or zero resistances are generated.

### Reviewed branch matrix

All provided values are explicit in the diagram. The duplicate Givens panel is
removed; internal given-value metadata remains for validation and exports. There are no implied
or absent roles in this three-role profile: two values are given and one is
requested. Only the requested field uses ?. Hidden answers are excluded from
setup metadata. All rows below are implemented with organizer enabled.

| Difficulty | Given roles | Requested role | Answer from displayed givens |
|---|---|---|---|
| Easy | I, R | V | I*R |
| Easy | V, R | I | V/R |
| Easy | V, I | R | V/I |
| Medium | I, R | V | I*R |
| Medium | V, R | I | V/R |
| Medium | V, I | R | V/I |
| Hard | I, R | V | I*R |
| Hard | V, R | I | V/R |
| Hard | V, I | R | V/I |

The existing target IDs and sampling are retained. Mixed selects each of the
three unknowns equally. Difficulty changes the curated resistance/current ranges:
Easy uses integer R=2–12 and I=1–6; Medium uses nine resistance choices and six
current choices (including halves); Hard uses seven choices of each (including
tenths). The regression script enumerates every pair and target: 507 cases.

### Shared metadata and custom-page integration

Quantity names, symbols, and units come from `utils/quantities.py`; Single Resistor
equation metadata resolves through that profile. Internal givens and diagram labels use
the same display values, formatted to at most two decimal places with trailing
zeros removed. Calculations and setup checking use those displayed values.
These curated ranges need no additional precision; broader generation would
require another review.

The case supplies validated setup metadata. Both `circuit_payload` and
`OhmsLawTargets` preserve it as `extras.setup`, alongside the existing case,
diagram, grading, and explanation data. The page retains the normalized payload
and mirrors its existing question number to the shared organizer question ID.
The shared renderer is called independently of the final-answer form and renders
no panel for unsupported circuit subtypes. An existing session without the new
payload state receives a fresh circuit on its next render.

Setup checking requires explicit submission, preserves entries, labels stale
results during revisions, and resets with a target/difficulty/type change or New
Circuit. The generic possible-other-given rule and neutral fallback remain;
coincident correct values do not trigger an error, and there are no velocity-phase
hints. Existing final grading (5% relative or 0.05 absolute tolerance), one-attempt
scoring and worked feedback remain independent. Both circuit pages use custom
correct/incorrect messages selected once per answer. Correct answers offer a
collapsed View calculation expander and advance after five seconds unless Cancel
Next Question is checked. Paused correct answers offer New Question (Circuit). Incorrect
answers display the calculation and expected answer until New Question (Circuit) or a
settings change. New Question (Circuit) is also available before submission. No retry or
scoring policy change is introduced.

### Verification and review checkpoint

`tools/test_single_resistor_setup.py` passed all 507 curated cases against displayed
givens, diagram labels, units, requested/hidden separation, and independently
calculated answers. It also checks all nine target/difficulty requests, every
Mixed target, adapter retention, feedback ambiguity, and DOCX serialization with
a circuit diagram. The routed-page checks cover all three difficulties and targets
plus Mixed, two separate forms with Enter enabled, deliberate checks, stale
results, scoring isolation, invalid final inputs, single scoring, cancellable automatic
progression, selector/new-circuit resets, and unsupported subtype transitions.

Baseline payload validation (4,200 cases), prompt/answer consistency, the
solve-for/export suite (nine tests, 525 target/level combinations), and all earlier
organizer suites passed locally. The audit regression tests passed after
updating final-answer selectors to exclude organizer fields. The circuit feedback
regression checks persistent right/wrong results, optional correct calculations,
cancellation/resumed advancement, stable custom messages, and no repeat scoring on both circuit pages. The Single Resistor regression script is now
configured in CI; remote CI has not run as part of this local rollout.

Teacher/browser review remains: try Electricity > Current Electricity > Circuit
Fundamentals > Single Resistor with each unknown and decimal-valued difficulties;
check diagram/field readability and Tab/Enter behavior in the side-by-side layout.
Automated form checks do not certify narrow-screen or screen-reader usability.
Export payload compatibility is checked; printed organizers and a student circuit
worksheet builder are separate decisions. The circuit task split is implemented; the next implementation package is simple
Newton's Second Law. Further circuit organizers are explicitly deferred.

## Circuit task coherence review — 2026-10-12

The implemented boundary is learning focus, not non-overlapping circuit diagrams.
Fundamentals isolates relationships; Series and Parallel coordinates them in
network calculations. The current tasks are listed above and in
[current_electricity_series_parallel.md](current_electricity_series_parallel.md).
No separate Equivalent … section is needed for this bounded package.

The displayed route is Circuit Fundamentals. Old Circuit Ohm's Law session
navigation maps to that route. Retired starter selectors reset to Single Resistor
and clear their old case/result. Single Resistor's state namespace and permanent
progress ID remain unchanged. Series Voltage Drop retains the old Voltage Drop
progress ID and alias. Historical Series Current records are retained under their
original identity: because their task changed with difficulty, they are not
reclassified as current-only practice or combined with new relationship scores.
The paired tasks have new progress IDs; retired one-answer records remain intact
and are not relabeled as two-answer performance. Existing session performance
stays on its originating page; no cross-page history
merge is attempted.

Regression coverage checks 1,080 sampled paired/multi-step cases against their
displayed givens, all new task/difficulty combinations on the routed pages,
parallel diagram rendering, old navigation/selection recovery, feedback, and
single-attempt scoring. Each paired task has R1/R2 answer fields with independent
correctness feedback. Both must be valid numbers before grading; both must be
correct to advance automatically. The whole circuit counts once, with no partial
score. Submitted fields are locked until a new question. Wrong calculations stay
visible and correct ones remain optional. Two-answer diagram exports are checked.
The existing 507-case Single Resistor organizer suite
remains applicable. Visual teacher review of the new selection/layout is still
needed; automated checks do not establish narrow-screen or assistive usability.

This closes the content-organization package. Additional network organizers,
conceptual choice formats, and full multi-answer circuit analysis remain future
work rather than prerequisites for the forces rollout.

## Component organizer preview

Series Current and Voltage and Parallel Current and Voltage now have compact
organizers beneath the prompt in the right-hand column, with the diagram on the
left in a 50/50 split. The answer form sits beneath the diagram in the left column; the repeated
difficulty caption is removed on both current-electricity pages. Given fields
are grouped as Whole circuit, R1, and R2, matching diagram ownership. Optional
field help connects shared current or source voltage with each resistor's own
current/voltage relationship. These one-step tasks have no intermediate section;
the existing paired final-answer form remains independent. Check organized work
does not score, submit final answers, or advance. Question/type/difficulty changes
reset the organizer. Single Resistor keeps its existing organizer.
Relationship explanations are optional help on the activity heading; paired
final-answer inputs sit side by side. Existing live cases can recover organizer
fields from their displayed givens without replacing the question.
Shared Schemdraw labels use an 11-point font. Sources without a supplied voltage
have no text label; old live diagrams also suppress the former Ideal source label.
Series return wires meet the source's lower terminal at its actual height,
eliminating a misleading dead-end tail beside the source voltage label. Shared
geometry applies to practice and exported diagrams.

Together with Series Voltage Drop, 720 sampled cases and all nine routed
type/difficulty branches pass fact, calculation, feedback, reset, and submission-
isolation checks. The Single Resistor suite remains green. Teacher visual review,
including compact laptop layout and component grouping, is pending. Further
components and alternative representations remain future work.

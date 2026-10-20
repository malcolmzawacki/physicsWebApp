# Current State

_Last reconciled with source: 2026-10-12_

Read this first for implemented behavior. Priorities live in
[project_roadmap.md](project_roadmap.md); the repeatable rollout process lives in
[site_update_process.md](site_update_process.md). Historical audit records remain
useful evidence but are not current completion claims.

## Site scope and tracking

The current route inventory contains **43 activities and 151 problem-type/mode
rows**, including Advanced routes, custom pages, explorers, labs, and two worksheet
builders. The [organizing-help inventory](organizing_help_inventory.md) is generated
from routes and metadata with explicit custom-page adapters. Blank review cells
mean unevaluated. It does not yet enumerate every difficulty, target, and random
scenario combination; those require a per-family coverage matrix during review.

There are **45 recorded organizing-help reviews**, including ten Recognizing
Forces / diagram matching context rows with conceptual scaffolds instead of numerical organizers;
Friction and Distance and Thermal Mixed are the newest teacher-preview packages; per-family records track
other review status and evidence limits. These are counts
of inventory rows rather than page counts. Decisions are recorded in
[organizing_help_reviews.json](organizing_help_reviews.json).

## Organizing help: implemented

### Match the Free-Body Diagram pilot (2026-10-20)

**Dynamics > Match the Free-Body Diagram** is available at both course levels.
Ten original cases extend Recognizing Forces into reading force identity,
direction, and relative sizes. Four shuffled, labeled PNG cards are clickable
buttons using the same component as motion matching. Clicking, tapping, or using
Enter/Space selects a card with a visible border without submitting it. Optional text
descriptions communicate the same arrows and relative lengths. Explicit Check
diagram is the primary action beside the hint. Missing selection is unscored;
incorrect choices allow revision with specific feedback; success awards one star
in the standard upper-right header and starts the five-second cancellable countdown.
The shared automatic-loading preference is respected. Context filters, related
cases, Skip question, Next question, session performance, and reset mirror C4.
Current Session Progress saves checked diagrams and explanations as snapshots.

Case assumptions make direction and balance determinate, including the upward
speeding-up bucket and a spring anchored to the left. Comparisons concern opposing
forces on each axis, not exact ratios or comparisons between axes. Diagram
construction, inclines, two-axis acceleration, numerical answers, and exports
remain excluded. See the [C5 coverage and verification record](newtons_laws_aspirations.md#c5-pilot-implementation-record).
Automated physics, rendering, and routed interaction checks passed, including
the existing motion-card regressions. The live browser confirmed image-click and
Enter-key selection, the selected border, and selection without submission.
Touch, narrow-screen/accessibility, and teacher review remain pending.

### Recognizing Forces conceptual pilot (2026-10-19)

**Dynamics > Recognizing Forces** is available at both course levels. Twelve
original cases cover gravity, normal force, friction, tension, direct applied
force, spring force, drag, and a force-free idealized space probe. Students select
all forces on a named object, explicitly check, revise, request an interaction
hint, and choose a fresh or related case. Context filters select surfaces, ropes,
springs, flight, or all contexts. Assumptions are stated; no case requires guessing
whether an unspecified contact or air force exists.

One star is awarded per completed case, displayed prominently at the upper right
using the same title-and-stars header as Newton's Second Law. Session-local records distinguish first
try without help, correction after feedback, and completion with an explicit hint;
skipped cases remain visible. Identical repeated checks and reruns do not add
attempts or stars. Reset clears this activity's practice records. These are not
durable history or mastery claims. This presence-only activity intentionally uses
interaction hints and discrete answer sets instead of equations, numeric
difficulty levels, or the numerical organizer. Correct answers now advance after
a five-second cancellable countdown; incorrect answers stay available for revision.
The form ends with side-by-side hint and primary Check forces actions, with Check
forces first for Enter submission. Skip question moves past an unfinished case;
Next question advances immediately after success. Try a related case is retained.

See the [C4 coverage and verification record](newtons_laws_aspirations.md#c4-pilot-implementation-record).
Teacher review, actual keyboard behavior, and narrow-screen visual review remain
pending; the local browser preview could not connect during implementation.

Enabled for Accelerated Motion (four omitted-variable types plus Mixed), Constant
Motion's Constant Speed subtype, Momentum, Wave Properties, and Circuit
Fundamentals' Single Resistor subtype, Newton's Second Law on Easy, all four Energy Basics families,
all three Conservation of Energy families, and all three Thermal Energy families. Medium/Hard Forces and the other
current-electricity activities use the grouped given/calculated organizers described below.
Other Constant Motion subtypes, Impulse,
Collisions and additional network tasks do not inherit
support from their neighbors.

Students enter numbers, `?` for the requested quantity, and case-insensitive `x`
for neither provided nor requested. Each panel has an independent form: Tab moves
between inputs, Enter or Check setup submits all entries, and entries remain after
checking. Results appear beneath the matching fields with text, icons, and color.
Previous results describe the last check while revisions are buffered; feedback is
not issued on every keystroke. New questions reset the workspace. Setup submission
does not score or advance the final-answer task.

Shared quantity definitions and role-specific symbols live in `utils/quantities.py`.
Generators emit validated `extras.setup` through `utils/setup_schema.py`, describing
given, implied, requested, and absent information. Only given/implied fields expose
values. The renderer reads roles dynamically. Migrated equation templates and
explicit solve-for role mappings share those definitions. This is incremental:
other generators, answer labels, and custom layouts are not universally migrated.

Feedback is intentionally limited: correctness checks, a possible wrong-quantity
match against another given, and a neutral fallback. A number match does not prove
a student's reasoning. Ordinary velocity does not receive initial/final hints.
Sign-only discrepancies avoid accidental cross-quantity diagnoses. See
[feedback behavior](setup_feedback.md) and [architecture](organizing_help_architecture.md).

No attempt database, email digest, persistent learner history, or external
reporting is implemented. All organizing-help entries remain session-local.

## Wave Properties: eight forms implemented, organizer enabled

All eight reviewed given/target combinations are implemented, including period in
wave-speed and reciprocal problems. Mixed samples forms equally; four explicit
targets each sample two forms. Shared definitions provide the four-role organizer,
equations, and unit labels. Period givens use at most three decimal places and
answers use those displayed values; unstated reciprocal values remain absent.
The page exposes Easy; difficulty does not change the generator. Harmonics and
decibels remain outside this rollout. See the [coverage matrix and verification
limits](wave_properties_review.md). The teacher confirmed the period problems and
Tab/Enter behavior on 2026-10-12; narrow-screen and assistive-technology review
remain broader verification limits.

## Single Resistor: three targets across all difficulties

Circuit Fundamentals now provides organizing help for Single Resistor at Easy, Medium,
and Hard, using battery voltage, current, and resistance roles. Diagram labels supply the same values used for setup checking and
answer calculation. The custom page stores a normalized payload and aligns its
question number with the shared organizer ID. Setup submission is independent of
final-answer scoring, feedback, and progression. Organizers for the new focused
relationship tasks and circuit networks remain explicitly deferred. See the [branch review and verification
limits](current_electricity_ohms_law.md#single-resistor-organizing-help-scope).
Teacher/browser review of this layout is pending.

Circuit Fundamentals offers Single Resistor, Series Current and Voltage, and
Parallel Current and Voltage. The paired tasks request each resistor's voltage
from a shared series current, or each branch's current from a shared voltage.
Both answers are checked together with individual correctness feedback and one
score per circuit. Invalid/blank fields prevent scoring; both answers must be
correct to auto-advance. Submitted answer fields lock until the next question. Series and Parallel Circuits
retains its four existing network tasks and adds the full Series Voltage Drop
calculation. The duplicate Series Current subtype is retired. Difficulty keeps a
stable task meaning; focused series practice supplies current, whereas network
voltage drop requires finding it. Old navigation and retired session selections
recover without displaying old cases under new labels. The bounded circuit
organization package is implemented; simple Newton's Second Law is next.

Both circuit pages omit the duplicate Givens panel: students read values from
the schematic. Internal givens remain for checking/export. Diagrams scale within
half of the main row, with additional space separating current and resistor
labels. New Question (Circuit) shares the footer row with Your Performance and
handles all manual generation/advancement.

Both circuit pages use a five-second correct-answer countdown with Cancel Next
Question. Correct calculations remain optional in a collapsed View calculation
expander; pausing keeps them available. Wrong answers show the calculation and
wait for New Question (Circuit). Custom correct/incorrect messages are selected once per
answer and retained across reruns. One-attempt scoring remains unchanged. Local
regressions cover cancellation, resumed advancement, persistent wrong feedback,
optional correct calculations, stable messages, and no repeat scoring.

## Newton's Second Law: Easy review

Organizing help is enabled under Dynamics > Newton's Second Law > Easy for net
force, mass, acceleration, and Mixed practice. The three columns are Net force
(ΣF, N), Mass (m, kg), and Acceleration (a, m/s²), defined by the shared
`newtons_second_law` profile. Net force is the resultant force; no individual
applied force, friction, weight, or normal-force value is inferred from it.
Easy prompts name net force explicitly. The main equation uses the same shared
symbol definitions. Existing target IDs and the activity's progress ID are stable.

| Branch | Given roles | Requested role | Scope / evidence |
|---|---|---|---|
| Easy acceleration | Net force, mass | Acceleration | All 100 mass/acceleration combinations checked |
| Easy net force | Mass, acceleration | Net force | All 100 combinations checked |
| Easy mass | Net force, acceleration | Mass | All 100 combinations checked |
| Easy Mixed | Same three branches, randomly selected | Actual generated target | All three branches checked; no fixed target assumed |
| Medium/Hard, variant 1 | Applied force, mass, acceleration | Net force, friction coefficient | Organizer excluded pending friction review |
| Medium/Hard, variant 2 | Applied force, mass, friction coefficient | Net force, acceleration | Organizer excluded pending friction review |
| Medium/Hard, variant 3 | Mass, acceleration, friction coefficient | Net force, applied force | Organizer excluded pending friction review |

Easy uses positive integer mass and acceleration from 1 through 10; net force is
their product. Prompts display two decimals, so no hidden rounding affects the
answer. There are no conversions, implied constants, negative/zero acceleration,
axis choices, or multiple objects. Requested fields never contain hidden answers.
The profile has no absent roles in these three branches. Feedback handles missing
entries, requested markers, possible given-value mix-ups, and coincident numbers;
it does not diagnose a physical misconception from a number alone.

Setup and final answers have independent forms. Setup checks do not score or
advance the question. Target/new-question changes clear prior setup checks, and
switching to Medium/Hard hides organizing help; returning to Easy starts clean.
The standard final-answer countdown, cancellation, and scoring remain in use.

`tools/test_force_setup.py` covers all 300 Easy numerical cases against parsed
prompt values, target/Mixed metadata, coincident-number feedback, export payloads,
independent forms, Enter-enabled setup, reset, one-time scoring, advancement, and
unsupported difficulties. Shared schema/workspace checks, baseline payload and
prompt checks also pass. The solve-for/export suite checks normal document
serialization. Teacher confirmed intended behavior on 2026-10-12;
AppTest is not a visual or assistive-technology certification. Printed organizing
help is not enabled by this practice rollout.

Later friction review must make the horizontal-surface model, applied-force
orientation, friction direction/type, and g = 10 m/s² convention explicit. Current
Medium/Hard prompts do not consistently state these assumptions; the calculation
uses normal force = mg and applied force = net force + friction. Their shared
reference equations likewise require those qualifications. Medium and Hard mostly
change the number range (20 versus 50), not the task structure. These branches
remain outside the Easy review. The multi-step prototype below now addresses
their assumptions and provides a separate teacher preview.

## Newton's Second Law multi-step prototype

Medium and Hard now offer a first-pass organizer for all three friction variants.
Version 2 separates **Given information** and **Possible in-between calculations**,
with side-by-side fields and optional heading/field help instead of instructional
paragraphs. Final answers remain in the existing answer form.
Students copy supplied numbers, then calculate normal force and friction; variants
that supply acceleration also include net force as a calculated value, explicitly
identified as a final answer only in optional help. Short relationship hints support each step through help controls.
Check organized work is independent of final submission and scoring. Question and
difficulty changes clear checks; Easy retains its original three-field organizer.

Prompts state level ground and horizontal applied force along the motion.
The g = 10 m/s² convention is available in organizer help; the prompt does not
repeat it or explain the direction of kinetic friction. This is a teacher-preview prototype,
not the final shared intermediate-information schema. Its separate force-plan
metadata avoids labeling calculated quantities as absent or asking students to
search the prompt for them. Classroom feedback should guide the shared design.

## Energy Basics review

Energy / Types of Energy has organizing help for all four existing families.
Easy requests energy or work; Medium and Hard also support the two existing
inverse targets and Mixed. All other profile roles are explicitly supplied.

| Family | Organizer roles | Medium/Hard targets |
|---|---|---|
| Elastic Potential Energy | Elastic potential energy, spring constant, deformation | Energy, deformation, spring constant |
| Kinetic Energy | Kinetic energy, mass, speed | Energy, speed, mass |
| Gravitational Potential Energy | Gravitational potential energy, mass, gravitational acceleration, height above reference | Energy, height, mass |
| Work | Work, applied force, distance along force | Work, distance, force |

Prompts specify an ideal spring and deformation from its relaxed length, use speed
for kinetic energy, state g = 10 m/s² and zero gravitational energy at ground
level, and describe a constant force moving an object across flat ground for work.
Work currently samples positive force and distance only, using W = Fd; signed
force/displacement cases remain a later content extension. Gravitational acceleration is an explicit fourth organizer field.
Existing positive integer sampling and difficulty ranges remain; all displayed
two-decimal givens are exact. No conversion, absent role, or intermediate-value
planning is involved. Existing target IDs remain stable despite clearer labels.

`tools/test_energy_setup.py` checks all 11,820 finite sampled-value combinations,
28 target/level branches, Mixed coverage, displayed facts and independent physics
calculations, feedback with coincident numbers, separate Enter-enabled forms,
resets, one-time scoring, cancellable progression, and export payloads. Baseline
payload validation (4,200 cases), prompt consistency, and solve-for/export checks
also pass. Teacher layout and keyboard review is pending. Conservation of Energy,
thermal activities, friction-distance tasks, and printed organizers are excluded.
The intermediate-values design decision is queued immediately after this preview
in the roadmap; this rollout does not settle that decision.

## Circuit component organizer preview

The circuit component organizer enables the two paired Fundamentals activities
and all five Series and Parallel activities at all three difficulties. Givens are
grouped by Whole circuit/R1/R2 where supplied; equivalent-resistance tasks show
only the two resistor groups. Series Voltage Drop adds equivalent resistance and
circuit current; Series Total Current adds equivalent resistance only.
All 1,680 sampled cases and 21 routed branches pass fact, calculation, independent
checking, feedback, and reset tests. See the two current-electricity documents for
scope and pending teacher review. Single Resistor retains its existing organizer;
all eight current-electricity activities are covered. Broader difficulty variety,
additional components, and printed organizers remain separate future work.

## Conservation of Energy organizer review

A Mixed problem type samples all three conversion families equally, then uses
each family's existing direction/target sampling. The activity remains labeled
Mixed; its optional reference shows general conservation and energy definitions.
No Solve for selector is shown for this mode. This differs from Mixed practice
under Solve for, which varies the requested quantity within a chosen family.
The shared selector row now gives Solve for a smaller share (1.6 versus Problem
Type's 3 and Difficulty's 1.2); optional help explains its purpose.

All three families (Gravitational ↔ Kinetic, Elastic ↔ Kinetic, and Gravitational
↔ Elastic) now support organizing help at Easy, Medium, and Hard, with all existing
targets and Mixed. Givens are grouped by shared properties and starting/ending
states. A possible in-between energy calculation has optional relationship help;
the requested final quantity is excluded from these fields. Setup checks remain
independent of final submission and scoring. g = 10 m/s² and the ideal/no-loss
model are explained in optional heading help. Thermal and friction-distance
activities remain outside this rollout.

Answers now use displayed two-decimal givens, resolving earlier hidden precision
in spring/motion speeds and spring/gravity masses. Supplied spring/gravity masses
have a minimum of 0.01 kg so the displayed problem cannot have zero mass. Total
vertical change in spring/gravity questions includes compression/expansion;
upward kinetic/gravity questions specify launch from ground level. Horizontal
spring/motion questions state frictionless motion. Target IDs and scenario counts
remain stable; speed and spring-constant wording is clarified.

`tools/test_conservation_setup.py` checks 3,600 sampled cases covering all 60
scenario/difficulty branches, displayed facts, independent conservation equations,
intermediate values, explicit/Mixed target and export payloads, page checks,
stale feedback, reset, and final-submission isolation. Baseline validation and
solve-for/export checks pass. Teacher layout/keyboard review remains pending;
printed organizers are not included.
An additional 360 seeded Mixed cases cover all three families in both directions
at every difficulty, plus Mixed exports, selector reset, and final-answer flow.

## Thermal Energy organizer review

All three conversion families, both directions, and every existing target at
Easy/Medium/Hard have optional organizing help. Easy retains thermal-energy
targets only; Medium/Hard retain existing inverse targets. Shared facts (including
supplied thermal energy) and start/end quantities are grouped separately. Two
side-by-side possible calculations cover starting and ending mechanical energy,
with optional formulas or energy-balance hints. Actual requested quantities stay
out of those fields. Checks do not submit final answers, score, or advance.

The page consistently requests positive Thermal energy rather than calling a
positive energy loss signed work by friction. Optional equations state
E_thermal = E_i − E_f and W_f = −E_thermal. Legacy target IDs remain stable;
visible thermal, speed, and spring-constant labels are clarified. Answers and
intermediates use displayed two-decimal facts. Candidates whose rounded givens
imply zero mass, nonpositive thermal loss, or nonpositive residual are resampled
within the same chosen variant. Raw number samplers used by Friction and Distance
remain unchanged; that page is outside this rollout.

Optional heading help gives g = 10 m/s², vertical ramp height, horizontal ideal
springs, and the rest/relaxed endpoint conventions. Ramp-ascent wording now
distinguishes vertical height from distance along a ramp and specifies the stop
where needed. The shared energy renderer supports side-by-side calculations and
page-specific assumptions rather than reusing Conservation's no-loss assumption.

`tools/test_thermal_setup.py` covers 3,480 sampled cases across all 58 reachable
direction/target/level branches, displayed facts, independent energy balance,
intermediates, explicit/Mixed selection, export payloads, independent forms,
stale feedback, reset, and one-time final scoring. Teacher review is pending;
printed organizers remain outside this package. Thermal now also has a Mixed
problem type: equal sampling across three conversion families, followed by each
family's existing direction/target sampling. Easy still asks only for thermal
energy. The general optional equation reference does not identify the conversion;
Solve for is hidden in Mixed mode. Another 360 seeded cases cover all six
directions at every difficulty, with Mixed exports and page checks.

## Friction and Distance organizer review

All three families, six directions, and 90 existing direction/target/level branches
now have optional organizing help. Easy keeps its two requested answers (thermal
energy, then another quantity); Medium/Hard keep their single requested target.
Givens are grouped by shared properties, starting/ending states, and Along the
path. Vertical height and distance along the rough path have separate roles.
Possible in-between calculations include positive thermal energy and starting/
ending mechanical energy, arranged side by side with optional hints. On Easy,
thermal energy also serves as the first final answer; the last requested answer
is excluded from the intermediate fields.

Thermal energy is calculated from displayed friction magnitude × displayed
distance, retaining the product's precision during subsequent calculations.
Force/distance targets instead use the displayed mechanical-energy difference.
Nonpositive rounded facts/residuals and impossible ramp height/path combinations
resample within the same direction/variant. Optional assumptions specify constant
friction magnitude over the stated path, vertical ramp height, horizontal ideal
springs, and smooth horizontal spring sections for ramp cases. Reference equations
distinguish positive thermal energy from negative friction work. Existing target
IDs, branch counts, and scoring/progression behavior remain stable.

`tools/test_friction_setup.py` checks 3,600 displayed-fact cases across all 90
branches, target identities, independent energy balance and Fd calculations,
positive domains and ramp geometry, explicit/Mixed target selection and exports,
isolated checks, stale feedback, resets, and final scoring. Teacher review is
complete for the current scope (teacher accepted 2026-10-13). All four current Energy pages now offer organizing help; cross-family
Mixed is available on Conservation and Thermal. Printed organizers and broader
content/difficulty expansion remain separate work.

## Solve-for and exports

Browser controls and worksheet requests share `utils/solve_for_catalog.json` and
`utils/solve_for.py` for supported existing targets. Coverage is deliberately
partial: see [evaluation](solve_for_evaluation.md), [targets](solve_for_targets.md),
and [deferred decisions](solve_for_deferred.md). The earlier evaluation's route
counts are historical. Uniform inverse generation is not a prerequisite for
organizing help: the generated payload must identify its actual targets even when
the selection was Mixed or the task has fixed outputs.

Kinematics and Dynamics have student worksheet routes, with per-section controls,
PDF conversion and preview; LibreOffice is required for PDF conversion. Their
activity catalogs live in `utils/worksheet_ui.py`. Instructor DOCX export remains
separate. Export scaffolding has not been reviewed just because a practice subtype
supports organizing help. See [worksheet notes](student_worksheets.md).

## Validation and evidence limits

CI currently invokes payload validation, prompt/answer consistency, activity flow,
relative motion, audit regressions, progress/formatting, solve-for, and student
worksheet tests. It installs LibreOffice for the worksheet conversion check.
CI now also invokes the organizing-help scripts and inventory drift check:

- `tools/test_setup_schema.py`
- `tools/test_setup_workspace.py`
- `tools/test_constant_setup.py`
- `tools/test_momentum_setup.py`
- `tools/test_wave_setup.py`
- `tools/test_single_resistor_setup.py`
- `tools/test_force_setup.py`
- `tools/test_energy_setup.py`
- `tools/test_conservation_setup.py`
- `tools/test_thermal_setup.py`
- `tools/test_friction_setup.py`
- `tools/test_circuit_workspace.py`
- `tools/build_organizing_inventory.py --check`

Local rollout checks passed for the previously migrated families on 2026-10-12, together
with payload validation (4,200 cases), prompt/answer consistency, and the solve-for
suite (nine tests, 525 target/level combinations and exports). Single Resistor
coverage adds 507 cases across all curated value pairs and targets. All 14 audit
regression tests passed after adapting final-input selectors for organizer fields. The route-count
assertion now reflects 41 routes, including both worksheet builders. This is not
a fresh full-site interaction/worksheet run or a remote CI result. Payload checks
establish contract validity, not complete content coverage or accessibility.

For physics/generator changes run both baseline guardrails, plus targeted family,
interaction, solve-for, and export checks appropriate to the changed surface:

```text
python tools/validate_payloads.py
python tools/check_prompt_answer_consistency.py
python tools/build_organizing_inventory.py --check
```

## Established foundations and remaining limits

Earlier work established dict payloads, shared State helpers, stable progress IDs
with history migration, equation rendering, diagram matching, and correctness/export
repairs. See the [September follow-up](implementation_fixes_2026-09-15.md) and
[correction record](implementation_fixes_2026-09-14.md). Custom pages still have
separate lifecycles; consult [compatibility limits](compatibility_limits.md) and
[activity flow](activity_flow.md) before sharing UI features.

Current gaps are tracked as work, not assumed solved: content-combination review,
quantity/notation migration, grouped object/axis/component layouts, unit/precision
policies, and narrow-screen and assistive-technology review. Realistic number/unit
generation is a later initiative.

## Projectile organizer first pass

Projectiles retains Type 1/2/3 terminology at the teacher's request. All existing
families, difficulties, directions and solve-for targets now offer optional
organizing help. Speed/angle facts sit above horizontal/vertical columns; time
has a separate row. Given cliff height remains a positive distance, while the
launch-to-ground or launch-to-landing vertical displacement uses up-positive signs.
Maximum height and total vertical change are distinct. Hints carry assumptions,
component relationships, signs, and flight versus peak/crossing time distinctions.
The last requested answer is excluded from the possible intermediate calculations.
Check organized work is independent of final submission and scoring.

Answers and intermediate values use printed givens, including rounded angles.
The elevated-landing sampler previously used vyi = 5(2t1+t2), inconsistent with
its two crossing times and h = 5t1t2. It now uses vyi = 5(t1+t2), with a matching
horizontal velocity and landing vertical velocity. Type 2 explicitly returns to
launch height; elevated landings specify descent; setback launches specify level
ground behind the edge. Equation references use ay = -g and signed displacement.
Existing difficulty/target scope and stable IDs are preserved.

`tools/test_projectile_setup.py` checks 1,860 sampled target cases, displayed facts,
kinematic identities, ascending/descending crossing times, exports, separate forms,
feedback commitment, stale feedback, resets and scoring. Shared solve-for and
payload/prompt checks pass. Teacher layout review is pending: vertical size on
small laptops is an explicit concern, and this first pass remains easy to compact.
Diagrams are deferred to the teacher's separate effort; no descriptive renaming.

Projectile preview iteration: initial and landing vertical velocity now share a
row within the Vertical calculation column. The landing-velocity label uses a
plain f rather than the accidental mathematical script character. Base and More
equations references are distinct again; type-specific derived relations appear
only with More equations. General layout preferences are recorded in
organizing_help_architecture.md. Teacher preview remains pending.

Projectile space refinement: vertical displacement is no longer a separate
organizer input. Supplied cliff height already contains the needed geometric
information; translating its sign does not warrant a second field. Type 2 also
omits a zero-displacement entry. Signed displacement remains part of the solver
and equation reference. Updated 2026-10-13.

# Current State

_Last reconciled with source: 2026-10-12_

Read this first for implemented behavior. Priorities live in
[project_roadmap.md](project_roadmap.md); the repeatable rollout process lives in
[site_update_process.md](site_update_process.md). Historical audit records remain
useful evidence but are not current completion claims.

## Site scope and tracking

Newton's Second Law classroom layout (2026-10-27): Medium/Hard organizing-help
feedback now appears directly under its own input in each given/calculation
column, including correct, incorrect and changed-entry messages. The final Submit
button is primary/red, and New Question lives in the sidebar, away from the final
answer form. These button-layout options are enabled only on Newton's Second Law;
other standard pages retain their existing controls. Organizer checking remains
independent of final scoring. The force-setup regression checks cover feedback
placement, form isolation, reset, scoring and progression across difficulties.

Calculator preview (2026-10-27): a shared lower-right Calculator button opens a
scientific pop-over on every routed view. It supports keyboard expressions,
arithmetic and scientific functions, degrees/radians, the last answer, and ten
history entries. Draft, result, mode and history survive activity navigation in
the current session; browser refresh starts a new calculator session. Calculator
widgets run in a fragment to avoid rerunning the activity. No dependencies were
added. `python tools/test_calculator.py` checks expression restrictions, numeric
results, keypad callbacks and navigation persistence. Desktop browser layout and
calculation were checked locally; deployment load times have not been measured.

Performance follow-up (2026-10-23): routine browser-save acknowledgements now send
record IDs and only answers missing from the server, instead of repeatedly
uploading all earlier diagrams. Browser storage and initial refresh restoration
remain complete; legacy full responses, cross-tab merging, fixed expiry, reset
generations, code retention and storage-failure warnings remain supported. A
30-answer synthetic image test reduced acknowledgement data from 18,718,440 to
10,500 bytes (not total network traffic). The three card-matching pages reconcile
selection before drawing their board, taking one activity execution per edit
instead of two. Scoring, feedback and the countdown animation are unchanged.
Storage and single-execution regression checks now run in CI. See the
[baseline audit and follow-up](force_activity_performance_audit_2026-10-23.md).

Compact force-activity layouts (2026-10-22): secondary instructions, conventions
and modeling notes appear in a small hover-help ? beside the scenario title. The
situation, target object, numeric givens, ranking mode and multiple-selection
instruction remain beside the answer controls. Practice filters live in the
sidebar on the five scenario activities; Ranking retains its visible mode selectors.
Change of State puts initial P/T values with the question. These six activities
own their page title, avoiding a duplicate Dynamics heading. The spatial builder
uses tighter panels with inline length menus for single forces. The design goal
is to keep the essential question and answer interface in the same frame on
roughly 2:1 Chromebook screens; long scenarios, hints and extra forces can still
require scrolling.

Force and Motion Matching keeps Motion display (Written descriptions / Dot
diagrams) visible beside the question, preserving the same case and selections
when switched. Its reference diagram has a slightly wider column and is exempt
from the small reference-image cap so fullscreen can enlarge the original artwork.

The motion-graph prototype adds Position–time, Velocity–time and Mixed graph types
(two of each type, one graph per card). The paired position/velocity view was
removed after teacher review to keep the conceptual task focused on reading the
y-axis and relating one graph to the forces. Existing sessions on that removed
view switch to Mixed graph types without losing the question or selections.
All representations use the same nine motion histories, answer sets and time
interval; switching modes neither regenerates the case nor scores an answer.
Graphs use signed position relative to the starting point rather than cumulative
distance, schematic scales, and consistent axes within each graph type. Graph
cards show their graph type without a verbal motion answer; accessible text gives
sampled values. Existing automated
checks verify graph slopes, all renderings, stable selections across modes,
completion/history, and all seven force cases. Classroom evaluation is pending.

The Free-Body Diagram Builder spatial prototype (2026-10-22) has force menus
above, left, right and below the live diagram. Position determines direction;
adding the same force elsewhere moves it and preserves its chosen length.
Each force uses a Short/Medium/Long dropdown instead of a slider. Check diagram
and Show interaction hint sit together below the editor. Existing grading,
retry feedback, stars and countdown behavior remain in place. Automated builder
checks cover movement, length persistence, navigation and completion snapshots;
teacher/student review of this experimental layout remains pending.

The post-classroom follow-up on 2026-10-22 uses "ignore" in place of "neglect"
and removes rope-elasticity qualifications. Force and Motion Matching defaults to
written motion descriptions, with dot diagrams available through Motion display;
switching views preserves the question, selections and attempts. Multiple-answer
instructions now appear in the main question area. Session progress shows a total
star count across all activity history, plus stars per activity in the daily
summary. Activity resets do not remove earned history; browser refresh restores
the saved history within its fixed 24-hour lifetime.

The 2026-10-22 comparison-layout follow-up puts Match the Free-Body Diagram,
Force and Motion Matching, and Change of State choices in one four-across row,
wrapping to two columns on narrow screens. Motion/change reference diagrams sit
beside their questions above the choices. Readable text below each choice carries
force labels/values or the motion description. Ranking force values are now bold
text below the image; saved diagram images retain larger two-line value labels.

Classroom feedback applied 2026-10-22: Recognizing Forces highlights the question
and retains the corrected checkbox submission while completion/countdown is shown.
All force activities with multiple selections explicitly say to select/check all
that apply. Force and Motion Matching gives missing/extra guidance without naming
answer letters or showing its worked explanation until completion. Diagram matching
uses sharper artwork; comparison boards now use the four-across layout described
above. Ranking selectors and equation text are larger, with clearer
selector borders. Regression checks cover corrected locked selections across reruns
and non-revealing motion feedback; core grading/history behavior is unchanged.

Current Session Progress opens with **Progress for [today's date]** and a compact
table of checks, correct answers, incorrect answers, and stars by activity and
problem type. For example, attempted Projectiles Type 1, Type 2, and Type 3 appear
as separate rows. Difficulty remains in answer review rather than adding rows.
New checks capture the selected problem type; older saved checks without this
field remain grouped as **Unspecified**. Numerical activities use their existing
problem-type labels; custom activities capture their named modes or contexts
where available. Saved browser history accepts the optional field without
invalidating older records. The summary
is intended for a single screenshot of a typical class session; it groups checks
instead of listing every question or diagram. Longer activity lists split into
columns. Review answers shows one selected check at a time with its saved answers,
explanation, and diagrams. Dates use America/New_York; dated checks from earlier
days are excluded from today's view; a date selector appears when retained checks
span dates. The total-star count covers all retained dates. Existing check/retry
scoring and full answer-review snapshots are unchanged; no new performance
measures, daily/weekly compression, accounts, or teacher exports are added.

Browser progress persistence (2026-10-22): existing history, including answer
review diagrams, and a random 16-digit code are saved in this browser profile's
localStorage. A fixed 24-hour window begins when the saved record is first created;
refreshes, visits and new answers do not extend it. Expiry discards the entire
history while preserving the code. Data is removed before restoration on a later visit,
or during polling while the page is open; deletion cannot run while the site is
closed. Dates use New York midnight, independently of the 24-hour expiry window.
Practice preferences, current questions and other activity state remain session-only.

The code is stored under a separate, non-expiring localStorage key and remains
until explicitly deleted through the combined delete control or browser site-data
controls. Existing codes from the initial single-key format are preserved on
migration, even if their progress has already expired. Expiry creates a new history
generation without changing the code; corrupt progress also leaves the separate
code intact. Switching browser profiles/devices does not transfer the code.

The sidebar shows the saving status and expiry in New York time. Its confirmed
delete control removes all saved answers, diagrams, stars and the old code,
starting an empty window with a new code. A generation marker prevents stale tabs
from restoring cleared/expired history. Record IDs deduplicate browser/session
merges, and Web Locks serialize writes across Chromium tabs. Only new records are
sent for saving; polling does not retransmit acknowledged diagrams. Stored JSON
is versioned and validated. Browser storage limits or blocking produce a visible
warning while current-session practice continues; data is not silently truncated.
Clearing site data or switching profiles/devices can lose progress. The code uses
no device information and does not authenticate a student or prevent edited
screenshots. Restored history uses the normal Streamlit connection for display;
there is no new durable server-side history store.

`tools/test_session_progress.py` covers summaries, date selection, review filters,
session isolation without a browser, and existing question progression.
`tools/test_progress_storage.py` and `node tools/test_progress_storage_frontend.js`
cover restoration, merging, fixed expiry with code preservation, code migration,
explicit code deletion/rotation, stale tabs,
serialization, corrupt input, blocked storage and quota failure.

The current route inventory contains **47 activities and 166 problem-type/mode
rows**, including Advanced routes, custom pages, explorers, labs, and two worksheet
builders. The [organizing-help inventory](organizing_help_inventory.md) is generated
from routes and metadata with explicit custom-page adapters. Blank review cells
mean unevaluated. It does not yet enumerate every difficulty, target, and random
scenario combination; those require a per-family coverage matrix during review.

There are **60 recorded organizing-help reviews**, including twenty-five force
identification / matching / construction context rows with conceptual scaffolds instead of numerical organizers;
Friction and Distance and Thermal Mixed are the newest teacher-preview packages; per-family records track
other review status and evidence limits. These are counts
of inventory rows rather than page counts. Decisions are recorded in
[organizing_help_reviews.json](organizing_help_reviews.json).

## Organizing help: implemented

### Net Force and Acceleration Ranking pilot (2026-10-20)

**Dynamics > Net Force and Acceleration Ranking** implements the user-prioritized
C10 pilot. Four distinct cart diagrams display mass and horizontal force values.
Students choose Net force or Acceleration, with an explicit Magnitude (size only)
or Signed horizontal value comparison. Right is positive in signed mode; magnitude
ignores direction and accepts opposite-sign ties. Optional settings choose equal
or different masses and whether fresh boards include tied values. Generation
guarantees each requested condition, with three distinct values when ties are on
and four when off. All diagrams use a common force scale within the board.

Rank 1 means greatest. Shared ranks express ties; gaps after ties are accepted.
Check ranking compares the ordering/ties exactly, using rational acceleration
values from displayed integer givens. Feedback identifies incorrect pairwise
relationships. Incomplete ranks are unscored, unchanged checks do not duplicate
records, and form entries persist after checks/hints and navigation. A related
comparison retains the same physical carts while switching force versus
acceleration; ties may then change regardless of the fresh-board tie preference.

Upper-right stars, hints, optional equations, session history with diagrams,
reset and the shared cancellable progression are retained. Tests cover 1,600
controlled boards, 20,480 rank assignments, signed/magnitude and force/acceleration
counterexamples, 36 rendered cases and all 16 setting combinations in the routed
page. Teacher/layout/accessibility review remains deferred. See the
[C10 implementation record](newtons_laws_aspirations.md#c10-ranking-implementation-record).

### Change of State pilot (2026-10-20)

**Dynamics > Change of State** adds C3 with ten original before/after situations.
A frictionless cart has a rightward hand push and/or leftward winch-rope pull.
The initial diagram sits beside a compact two-by-two grid of four choices.
Four shuffled cards each change exactly one horizontal interaction: add, remove,
increase or reduce it. Students select every change that satisfies the requested
motion. Cases include starting from rest either way, changing from speeding up to
constant velocity or slowing down, and increasing acceleration in either direction.
Force values are explicitly labeled 0/10/20/30 N; 20 N normal force and weight,
mass and vertical equilibrium remain unchanged. Zero means an interaction is absent.

The task concerns the initial motion after the force change; velocity cannot
instantly vanish or reverse. Each accepted set has multiple valid alternatives,
with exact-set checking and missing/extra feedback. Selection/hints are unscored,
wrong sets remain revisable, and unchanged checks do not duplicate records.
The upper-right star, shared auto-load preference, cancellable countdown, context
filters, related/skip/next, reset and session snapshots follow C2.

Automated verification covers all 160 case/state combinations, 4,800 answer
sets, four kinds of force change, all 16 diagrams and the routed page lifecycle.
Teacher and layout/accessibility review remain deferred as requested.
See the [C3 implementation record](newtons_laws_aspirations.md#c3-change-of-state-implementation-record).

### Force and Motion Matching pilot (2026-10-20)

**Dynamics > Force and Motion Matching** adds C2 with seven original constant-force
situations and four selectable motion cards per question, arranged in a compact
two-by-two grid beside the initial force diagram. Students select every
compatible card, rather than a single answer. The cards toggle independently;
Check motions submits the whole set. Missing and extra choices receive feedback,
with revision until complete. The shared cards keep the earlier single-answer
behavior on motion-graph and free-body-diagram matching.

Force diagrams constrain acceleration, while unspecified initial velocity permits
rest/coasting in balanced cases and opposite initial directions in unbalanced
cases. Four numbered equal-time dots and a description come from one motion
definition per card. Nine histories include rest, constant speed either way,
speeding up, slowing without reversal, and starting from rest. All choices are
qualitative; exact magnitudes and inter-card spatial scales are not compared.
Horizontal pushes are frictionless; vertical cable pulls and gravity-only flight
avoid velocity-dependent friction/drag assumptions. Forces stay constant over
the interval and loads stay clear of travel limits.

One star per completed set, explicit checking, optional hint, revision, context
filters, related/skip/next, session history with diagrams, reset and the shared
cancellable automatic progression are retained. Empty selection is unscored;
duplicate checks and stale browser events do not inflate records. Automated
model/interaction tests pass. Teacher and layout/accessibility review are deferred
as requested. See the [C2 implementation record](newtons_laws_aspirations.md#c2-force-and-motion-implementation-record).

### Free-Body Diagram Builder pilot (2026-10-20)

**Dynamics > Free-Body Diagram Builder** is available at both course levels.
It reuses the ten bounded C5 situations, with a multiselect for the seven force
types, cardinal direction selectors, and Short/Medium/Long arrow controls.
A side-by-side live preview updates during editing; no edits score an answer.
The central box represents the named object. Symbols on arrows have an adjacent
legend and a full text description is available. Same-direction arrows have
separate attachment points so all seven force choices remain visible, even in
an incorrect construction.

Check diagram gives separate feedback for presence, direction, and relative
sizes. Size comparisons only concern opposing forces on the same axis; exact
ratios and comparisons between axes are not required. Missing directions do not
score; unchanged checks do not duplicate attempts. Correct diagrams lock and
award one star in the upper-right header, with the shared automatic-loading
preference and five-second cancellable countdown. Optional hints, related cases,
Skip question, session performance and history snapshots, and reset are retained.
Drafts survive navigation. Numerical equations, dragging, inclines, two-axis
acceleration, and exports are excluded from this pilot.

See the [I2 implementation record](newtons_laws_aspirations.md#i2-builder-implementation-record)
for coverage and verification. Teacher and full accessibility review remain pending.

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
activity catalogs live in `utils/worksheet_ui.py`. Dynamics now also exports its six conceptual
activities: force recognition, diagram matching/construction, force-motion
matching (including dot/graph choices), change of state, and force/acceleration
ranking. Their paper adapters reuse authored cases and answer predicates;
required diagrams remain included independently of optional sketches. Instructor DOCX export remains
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

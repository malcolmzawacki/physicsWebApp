# Newton's Laws: activity aspirations and feasibility

_Research and repository review: 2026-10-19. C4 and C5 pilots implemented for teacher preview;
the remaining activities are proposals._

## Purpose and boundary

Build an uncluttered, personalizable Newton's Laws unit with conceptual practice,
diagram construction, numerical reasoning, and experiments. The Physics Classroom
(TPC) supplies reference learning goals and interaction examples; our activities
would use original questions, explanations, artwork, and implementation.

This document assesses every entry found in TPC's Newton's Laws catalogs:
**8 Physics Interactives and 13 Concept Builders**. It proposes educational
equivalents, not exact copies or a promise of matching every original feature.
The C4/C5 implementation records below describe the bounded pilots; the phases do not reorder the
active work in [the project roadmap](project_roadmap.md).

The separate **Forces in Two Dimensions** catalogs are excluded, along with
inclines, angled-force decomposition, vector equilibrium challenges, projectiles,
and circular-motion games. Perpendicular force arrows in an ordinary free-body
diagram remain appropriate: a horizontally moving object still has vertical
forces. Two-axis acceleration in one cataloged Concept Builder is explicitly
deferred below. Atwood's Machine remains included because it is listed in this
Newton's Laws catalog and its idealized motion uses a scalar coordinate.

Minds On Physics, Calculator Pad, videos, and standalone Concept Checkers are
outside the requested inventory. Short original comprehension checks can accompany
our explorers without attempting to reproduce those additional catalogs.

## Evidence and confidence

Catalog membership comes from the accessible [Newton's Laws Interactive index](https://www.physicsclassroom.com/interactive/newtons-laws)
and [Newton's Laws Concept Builder index](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws).
Several older URLs and launch/notes pages returned access errors. Public activity
descriptions, teacher resources, and exercises support the assessments below;
the simulations themselves were not systematically operated in a browser.
Consequently, catalog coverage is established for these retrieved pages, while
exact feature parity and the completeness of their latest live revisions remain
unverified. Recheck the catalogs when implementation begins.

Each linked activity description supports the brief account of TPC's activity.
Suggested controls, implementation choices, difficulty, and release sequence are
our engineering and teaching judgments. In particular, exact Atwood controls and
the inaccessible Solve It! activity page require confirmation before promising
parity. No restricted question banks were needed for this assessment.

## Existing foundations and real gaps

The repository already provides numerical Newton's Second Law practice and
optional organizing help through `ForceGenerator`, `force_plan_workspace`, and
the shared interface. Its reviewed Easy branch is scalar; its current friction
branches assume level ground, horizontal applied force, and g = 10 m/s². These
are starting points, not general dynamic simulation models.

The graph-card component and matching layout provide reusable selection,
submission, stale-event rejection, and feedback patterns. They currently select
one answer; multi-selection, ranking, sorting, and diagram editing need their
own checking and attempt behavior. The existing Atwood generator primarily
implements half-Atwood cases; a two-hanging-mass explorer needs additional physics
and rendering. Existing graph generators can inform representation work, but
independently generated graphs must not be combined as though they describe the
same motion.

Useful source starting points:

- [Newton's Laws activity page](../app_pages/1_2.1_Forces.py)
- [Force generator](../utils/generators/force_generator.py)
- [Atwood generator](../utils/generators/forces/atwood_generator.py)
- [Graph cards](../utils/graph_cards.py) and [matching layout](../utils/layouts/diagram_match_layout.py)
- [Current state](current_state.md), [architecture](architecture.md), and [rollout process](site_update_process.md)

There is no persistent learner-history database. Session-local practice and
teacher-selected settings are sufficient for initial releases. Saved assignments,
cross-visit progress, and automatic personalization based on long-term history
would be separate work.

## Feasibility scale

All entries below are feasible as original educational equivalents within the
Streamlit site. **Small** means mostly ordinary widgets and bounded content;
**Medium** adds substantial diagrams, checking, or a new interaction;
**Large** adds evolving physics, playback, or significant numerical verification.
These are relative work sizes, not elapsed-time estimates. First implementations
include shared-foundation costs; later activities reuse them. Content authoring
and classroom review remain necessary at every size.

## Physics Interactives: all eight entries

| ID / reference activity | Feasibility and proposed first version | Personalization and principal work | Phase |
|---|---|---|---|
| I1 **Force** | **Medium; strong fit.** Adjustable mass, horizontal applied force, and surface conditions; show motion, force arrows, and velocity-time data. A compute-and-inspect version can precede animation. | Choose frictionless or frictional trials, initial motion, visible measurements, and investigation prompts. Build explicit static/kinetic friction behavior rather than extending the current positive-acceleration generator into a simulator. | 4 |
| I2 **Free-Body Diagrams** | **Medium; strong fit.** Construct a diagram with force-type, direction, and relative-size controls. A widget-driven diagram is sufficient initially; dragging is optional. | Select force types and contexts, give presence/direction/size feedback separately, and allow revision. Check the named object and physical force relationships, rather than comparing a screenshot. | 2 |
| I3 **Free-Body Diagrams…The Sequel** | **Small to Medium after I2.** A distinct extension set of diagram-construction situations using the same editor. | Add novel original contexts and more subtle force comparisons. Keep it as a recognizable practice set without building another editor. Review each scenario for unit-boundary issues. | 3 |
| I4 **Rocket Sledder** | **Large for continuous interaction; feasible.** Thrust, friction, and drag controls connected to sled motion, a speed display, and force arrows. | Begin with discrete thrust changes and pause/step; later allow changes while moving. Handle coasting, braking, reversal, and rest correctly. Reuse I1's model where appropriate, with explicit drag behavior. | 5 |
| I5 **Falling Bodies - 1D** | **Large; strong fit as a numerical investigation.** Set initial height/velocity, mass, gravity, drag coefficient, area, and air density; compute tables and graphs. Animation is optional. | Offer realistic presets and controlled comparisons, with an advanced parameter panel. New signed-drag solver, bounded computation, impact detection, units, and time-step convergence are the main work. | 6 |
| I6 **Skydiving** | **Large initially; Medium after I5.** Guided falling-motion explorer with parachute deployment, force arrows, and synchronized speed/acceleration graphs. | Vary mass, deployment conditions, and parachute properties. Reuse the falling-body solver; teach increasing downward speed, terminal descent, and slowing while still descending. Deployment is a declared simplified model. | 6 |
| I7 **Elevator Ride** | **Medium; strong fit.** Step through an elevator trip, relating motion, acceleration, forces, and scale reading. Add animated playback after the stage version works. | Vary mass, acceleration, travel direction, and hidden/revealed representations. Compute normal force from acceleration rather than direction of travel; define contact loss/free-fall limits. | 4 |
| I8 **Atwood's Machine** | **Medium to Large; feasible.** Two hanging masses, ideal rope/pulley, adjustable masses, and predictions of acceleration and tension; optional animation. | Compare equal mass, unequal mass, fixed total mass, and fixed mass difference. Existing half-Atwood practice is useful context but is not this explorer. Confirm TPC's exact variants before expanding beyond the proposed ideal case. | 7 |

Activity evidence: [Force and original FBD descriptions](https://www.physicsclassroom.com/teacher-toolkits/newton-s-second-law/newton-s-second-law-complete-toolkit);
[Sequel announcement](https://www.physicsclassroom.com/Recent-Additions/2023-Additions);
[Rocket Sledder description](https://www.physicsclassroom.com/getattachment/Teacher-Toolkits/Newtons-Second-Law/Newtons-Second-Law-PDF-Version/ForceFBDs.pdf?disposition=inline&ext=.pdf);
[Falling Bodies exercise](https://direct.physicsclassroom.com/getattachment/Physics-Interactives/Newtons-Laws/Falling-Bodies-1D/Falling-Bodies-1D-Exercise/Assignment.pdf?disposition=inline&ext=.pdf&lang=en-US);
[Skydiving reference](https://www.physicsclassroom.com/class/newtlaws/Lesson-3/Free-Fall-and-Air-Resistance);
[Elevator Ride reference](https://www.physicsclassroom.com/class/circles/lesson-4/weightlessness-in-orbit);
[Atwood reference in Newton's Laws teacher notes](https://www.physicsclassroom.com/Lesson-Plans/Honors-Physics/Newtons-Laws/Teacher-Notes).

## Concept Builders: all thirteen entries

The linked titles are source descriptions. These proposed equivalents preserve
their distinct learning decisions even where several activities share a model.

| ID / reference activity | Feasibility and proposed first version | Personalization and principal work | Phase |
|---|---|---|---|
| C1 [Balanced vs. Unbalanced Forces](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws/Balanced-Unbalanced-Forces) | **Small to Medium.** Interpret a motion representation, identify speed change, and classify force balance. | Choose words, data, graphs, or dot diagrams; vary signs and initial motion. Include rest and constant nonzero velocity. Avoid implying that motion itself requires net force. | 1 |
| C2 [Force and Motion](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws/Force-and-Motion) | **Medium.** Given a force diagram, select every compatible motion/dot diagram. | Start with a few options and grow the comparison set. Needs multi-answer checking: force determines acceleration but does not uniquely determine velocity. Explicitly allow opposite initial directions. | 2 |
| C3 [Change of State](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws/Change-of-State) | **Medium.** Choose a changed force diagram consistent with a requested change in motion. | Vary whether forces are added, removed, increased, or reduced. Initial version selects diagrams; later version edits them. Design constraints so every accepted alternative is physically valid. | 3 |
| C4 [Recognizing Forces](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws/Recognizing-Forces) | **Small; best first pilot.** Identify forces present on a specifically named object. | Select contexts and available force types; offer interaction-based hints. Use a scenario library with explicit contact, attachment, and drag assumptions. Distinguish absence from insufficient information. | 1 |
| C5 [Match That Free-Body Diagram](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws/Match-That-FBD) | **Small to Medium.** Select the diagram matching a described situation. | Vary distractors by missing/extra force, direction, or relative magnitude. Reuse the graph-card interaction pattern and force renderer, with exactly one defensible answer in single-choice mode. | 2 |
| C6 [Normal Force Card Sort](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws/Normal-Force) | **Medium.** Classify situations by normal force equal to, greater than, or less than weight, or insufficient information. | Begin with per-card category selectors; add drag sorting later. Include vertical acceleration and additional vertical pushes/pulls with explicit conditions. Keep inclined/angled extensions outside this plan. | 3 |
| C7 [Which One Doesn't Belong? Force and Motion](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws/Which-One-Doesnt-Belong) | **Medium to Large.** Find the inconsistent item among words, FBDs, graphs, dot diagrams, and tables. | Choose representation count and complexity. Generate every representation from one scenario, deliberately alter one, and verify that the intended answer is unique. This is a synthesis activity. | 5 |
| C8 [Mass and Weight](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws/Mass-and-Weight) | **Small.** Distinguish the quantities, identify units, and calculate with W = mg. | Set gravity convention, environment, numeric range, and whether arithmetic is needed. State local g and distinguish gravitational weight from a scale's contact-force reading. | 1 |
| C9 [Newton's Second Law - Equations as Guides to Thinking](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws/Newtons-Second-Law) | **Small.** Predict acceleration changes as net force and/or mass change. | Choose qualitative, ratio, or numerical responses; vary one quantity before both. Use exact ratios and make net force distinct from one applied force. | 1 |
| C10 [Net Force (and Acceleration) Ranking Tasks](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws/Net-Force-Ranking-Tasks) | **Medium.** Rank cases by net force or acceleration. | Adjust case count, mass variation, direction, and whether ties occur. Rank selectors with shared ranks are sufficient initially. Explicitly distinguish magnitude ranking from signed-component ranking. | 3 |
| C11 [Air Resistance and Skydiving](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws/Skydiving) | **Medium; easier after the drag model.** Compare drag factors, connect velocity/force/acceleration diagrams, and interpret stages on a velocity-time graph. | Release all three strands as bounded practice modes. Use the same physical definitions as I5/I6 and clearly state which variables are held fixed in comparisons. | 6 |
| C12 [F net = m•a](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws/FnetEqualsMA) | **Medium; partial scope recommended.** Construct individual forces producing a specified acceleration. Accept multiple valid force combinations. | Include horizontal or vertical acceleration with cardinal force controls and optional balancing perpendicular forces. TPC's highest level includes simultaneous horizontal/vertical net forces: assess as feasible, but defer that two-axis extension to the separate unit. | 3, one-axis scope |
| C13 **Solve It! with Newton's Second Law** ([catalog](https://direct.physicsclassroom.com/Concept-Builders/Newtons-Laws), [supporting description](https://www.physicsclassroom.com/Physics-Video-Tutorial/Newtons-Laws/Force-Of-Friction/Learning-Tools)) | **Small to Medium; strongest numerical reuse.** Solve scalar acceleration problems, progressing to multiple forces and friction. | Build on the current numerical page, with original scenarios, useful retries, and optional organizing help. Review zero/negative acceleration and vertical cases before enabling them. Exact original branch coverage remains unverified. | 4 |

## Implementation approach

Keep Streamlit as the site's application framework. Ordinary forms, selection
controls, generated diagrams, and tables suit most Concept Builders. Browser-side
SVG/canvas interaction is appropriate for diagram manipulation and smooth motion.
[Streamlit's component documentation](https://docs.streamlit.io/develop/concepts/custom-components/overview)
supports integrating such custom interactions. The repository already uses v1
components; evaluate the installed/deployed version before choosing v1 or v2 for
new work. A framework migration is not a prerequisite.

Develop a few shared capabilities as activities need them:

1. **Force scenario and diagram definitions:** named object, interactions, axes,
   gravity convention, forces, motion state, assumptions, and supported answers.
   Generate diagrams, wording, and feedback from consistent data.
2. **Conceptual attempts:** explicit Check, preserved entries, optional help,
   revision, and related retry cases. Keep answer sets, category assignments,
   tied ranks, and open-ended force constructions distinct from scalar grading.
3. **Consistent representations:** one motion definition produces graphs,
   diagrams, text, and tables. This supports C1/C2 and eventually C7.
4. **One-dimensional experiments:** compute reproducible trials, record chosen
   parameters and measurements, compare runs, and support pause/step/playback.
   Transmit submissions and recorded trials to Python rather than every animation
   frame. A precomputed trajectory is sufficient for many experiments; live force
   changes need an explicit event model.

Do not turn the numerical organizer into a mandatory panel for conceptual work.
Existing one-attempt scoring/auto-advance behavior must not silently determine
the new practice design. Proposed conceptual practice allows correction and
separately identifies first-try success, supported correction, and completion.
Retain session-local records initially; these are not claims of durable mastery.

## Proposed implementation sequence

Phases are dependency-based packages, not a fixed calendar or an instruction to
implement everything in one chat. Each should yield a complete, teacher-reviewable
activity before the next package starts.

| Phase | Deliverables | Completion evidence and dependencies |
|---|---|---|
| **1. Conceptual entry points** | C4 Recognizing Forces first; then C8 Mass and Weight, C9 proportional reasoning, and C1 force balance. | Establish original scenario definitions, targeted optional help, explicit checking, and retry behavior. Review representations and misconceptions with the teacher. Each activity can ship independently. |
| **2. Read and construct diagrams** | C5 diagram matching, I2 FBD construction, and C2 force-to-motion matching. | Reuse phase 1 definitions; verify force identity, direction, relative magnitude, and multi-answer logic. Demonstrate keyboard/touch operation and stable state across reruns. |
| **3. Change, sort, and rank** | C3 Change of State, C6 Normal Force, C10 ranking, C12 one-axis force construction, and I3 FBD extension set. | Add typed checkers for categories, ties, and multiple valid constructions. Publish C12's explicit two-axis exclusion. Every original catalog entry remains accounted for. |
| **4. Connect reasoning to measurements** | C13 numerical pathway, I1 Force explorer, and I7 Elevator Ride. | Extend reviewed scalar models; establish signed motion, friction states, gravity consistency, and recorded-trial comparisons. Release step-based versions before animation where useful. |
| **5. Motion control and synthesis** | I4 Rocket Sledder and C7 inconsistent-representation challenge. | Reuse the motion/force foundations. Verify coasting/reversal and representation agreement. Browser playback must survive unrelated Streamlit reruns without duplicating trials. |
| **6. Drag and falling investigations** | I5 Falling Bodies first, then I6 Skydiving and all three C11 practice strands. | Verify the signed-drag solver, terminal behavior, deployment, impact, and numerical convergence. Provide both guided presets and an advanced investigation mode. |
| **7. Coupled systems** | I8 ideal Atwood explorer. | Add the two-hanging-mass model and synchronized diagrams; verify acceleration, tension, equal masses, mass swaps, and travel limits. Review before considering half-Atwood extensions. |

Recommended first implementation chat: **C4 Recognizing Forces only**, with a
small original set covering gravity, normal force, friction, tension, applied
force, spring force, and drag where justified by the scenario. Establish the
learning interaction and feedback quality before scaling the content set. The
next bounded deliverable is C5; the full phase sequence remains the aspiration.

## Personalization and student experience

Separate **physics challenge**, **support**, and **representation**. Offer a small
number of relevant controls per activity rather than one large settings panel.
Teacher choices can bound contexts, quantities, gravity, force types, and task
length. Student choices can expose a hint, switch an available representation,
repeat a related case, or try a fresh context. Larger numbers alone should not
define a harder conceptual task.

Use an uncluttered activity workspace: scenario, representation, response, Check,
feedback, and next action. Keep instructions and calculations available on demand.
Provide non-drag alternatives, text labels for diagrams, visible keyboard focus,
and readable small-laptop layouts. Experiments should connect prediction,
measurement, and explanation; an animation alone is not the finished activity.

## Verification and boundaries for later work

Before enabling each activity, check its declared scenarios and difficulty modes,
including cases with rest, constant speed, slowing down, negative velocity, and
zero net force wherever applicable. Diagrams must identify forces on one object;
third-law partner forces act on different objects and cannot be canceled on that
object's diagram. A force direction alone does not determine motion direction.

For friction, distinguish static adjustment from kinetic friction and avoid
artificial reversal after stopping. For falling motion, drag opposes velocity,
vanishes at rest, and approaches the appropriate terminal behavior; test smaller
time steps and interpolate the ground event. For elevators, scale reading is
normal force, and a negative calculated normal force signals loss of contact
rather than a physical scale reading. For ideal Atwood motion, verify the scalar
acceleration and both masses' tension equations independently.

Check submissions, help, retries, resets, changed settings, navigation, and stale
browser events. Numerical checks should use displayed values and appropriate
rounding policies; diagram/rank/selection checking should use physical or discrete
criteria rather than the numerical answer tolerance. Add model and lifecycle
regressions appropriate to the implemented scope, plus browser review on the
devices students use. Existing tests passing does not establish a new activity's
readiness. Printable variants can follow for suitable question formats; continuous
simulation export is not a prerequisite.

The retrieved catalogs do not list a dedicated Newton's Third Law Concept Builder
or Interactive in this unit. A third-law interaction-pair activity would improve
unit coverage, but is an **additional future candidate**, not one of the twenty-one
inventoried activities. Likewise, accounts, dashboards, persistent progress,
automatic mastery adaptation, and the deferred two-axis extension need separate
scope decisions. Their absence does not block the proposed first release.

## Handoff to the next chat

Read this document with the roadmap and current-state page; inspect the current
source before making reuse assumptions. Start with C4, agree the concrete original
scenarios and feedback, implement the bounded activity, and review it before
expanding. Maintain this document as the unit's aspiration; record shipped scope
in current state and implementation evidence in the existing rollout/review
structure. Do not mark these catalog entries complete solely because a shared
renderer or generator has been created.

## C4 pilot implementation record

Implemented 2026-10-19 as **Dynamics > Recognizing Forces**, available at High School
and Advanced levels. Original content and checker: `utils/recognizing_forces.py`;
workspace: `utils/recognizing_forces_ui.py`. This is a presence-only pilot; direction,
relative size, drawing, multi-axis dynamics, worksheets, and durable history are
excluded. Every scenario states contact/attachment/air/gravity assumptions; none
requires an insufficient-information answer. The other catalog activities remain
aspirations, and this implementation makes no claim of exact TPC feature parity.

| Original case | Context | Forces on the named object |
|---|---|---|
| Book on a desk | Surfaces | Gravity, normal |
| Book held in place by a horizontal hand push | Surfaces | Gravity, normal, applied, static friction |
| Puck coasting after the stick leaves | Surfaces | Gravity, normal; no friction or air resistance in the model |
| Crate sliding after release | Surfaces | Gravity, normal, kinetic friction |
| Hanging lamp | Ropes | Gravity, tension |
| Bucket lifted by a rope | Ropes | Gravity, tension; no direct hand contact |
| Mass hanging on a stretched spring | Springs | Gravity, spring |
| Cart released while attached to a stretched spring | Springs | Gravity, normal, spring |
| Upward ball after release, no air resistance | Flight | Gravity |
| Upward ball with air resistance | Flight | Gravity, drag |
| Skydiver and equipment at constant downward speed | Flight | Gravity, drag; person/equipment treated as one object |
| Coasting probe in idealized empty space | Flight | None; gravity explicitly negligible |

All seven force types remain available as response choices. Context selection
bounds cases, not the answer list. Related cases contrast conditions or transfer
the same interaction model; fresh cases do not repeat within a selected set until
it is exhausted. Check preserves selections and reports missing/extra forces by
interaction. Hint requests preserve selections and do not submit an answer.
Feedback always describes the last explicit check. Success locks the case and
awards one star, then advances after a five-second cancellable countdown. Students
can cancel to inspect feedback, choose Next question immediately, or try a related
case. Incorrect cases stay available for revision or Skip question. Check forces
is the primary button, first in a side-by-side footer with the optional hint so
Enter submits answers. Identical checks do not inflate the
record. Performance separates first try without help, corrections after feedback,
and completion with a requested hint; skipped/in-progress cases and check counts
are visible. Repeating a case is another practice record, not mastery evidence.

Verification: `python tools/test_recognizing_forces.py` checks all 12 expected
sets independently, all 1,536 possible answer sets, and routed forms, completion
locking, duplicate checking, hints, revision, filters, related cases, navigation,
fresh-case coverage, reset, primary submission, cancellation, and automatic
progression without duplicate advancement using Streamlit AppTest. Added to CI; inventory
adapter covers all five context selections. Baseline payload/consistency checks
and route checks passed for integration: 4,320/4,320 existing generator payloads,
prompt/answer consistency, all nine solve-for tests, activity-flow regressions,
and inventory drift checking (42 routes, 146 rows, no unresolved routes).
Tests needing temporary files used a workspace-local TEMP/TMP directory because
the sandbox's default temporary directory denied file creation.
Actual Enter/Tab/touch behavior,
narrow-screen layout, assistive technology, and teacher content review remain
pending. Browser preview attempts failed to connect to the local server in this
environment; AppTest is not visual review. Review this pilot before C5.

## C5 pilot implementation record

Implemented 2026-10-20 as **Dynamics > Match the Free-Body Diagram**, available at
both course levels. Model, checker, and reusable arrow artwork live in
`utils/force_diagram_match.py`; the workspace is `utils/force_diagram_match_ui.py`.
This is a four-option, single-answer reader, not the I2 diagram-construction editor.
All artwork and distractors are original. The presence assumptions and target
objects reuse C4's scenario library with the additional directional/acceleration
facts below. C4's presence-only questions retain their original scope.

| Case / context | Expected forces and relationships | Additional explicit fact |
|---|---|---|
| Book at rest / Surfaces | Weight down = normal up | No horizontal interactions |
| Book pushed but at rest / Surfaces | Weight = normal; applied right = static friction left | Push is to the right |
| Puck coasting / Surfaces | Weight down = normal up | Stick no longer touches; friction/air neglected |
| Crate sliding right / Surfaces | Weight = normal; friction left | Hand released; kinetic friction |
| Hanging lamp / Ropes | Weight down = tension up | Taut cable; at rest |
| Bucket lifting / Ropes | Tension up > weight down | Vertical rope; moving up and speeding up |
| Hanging spring mass / Springs | Spring up = weight down | At rest; spring, not rope |
| Spring cart / Springs | Normal = weight; spring left | Stretched spring anchored to the left |
| Rising ball / Flight | Weight down only | Hand released; no air resistance |
| Skydiver / Flight | Drag up = weight down | Constant downward speed; equipment/person one object |

Each board contains a correct diagram and three wrong alternatives: missing
weight, a reversed force, and a size/balance error (or a spurious upward hand force
for the rising ball). Four choices are shuffled for every fresh case. The checker
compares identities, directions, and ordering of lengths along an axis; it does
not require exact numeric ratios or comparisons across axes. Correct sizes are
qualitative representatives of the stated balance/acceleration. No force labels
or net-force arrows are mistaken for separate interactions. Parallel arrows in
incorrect choices are offset so their directions and labels remain readable.

Four clickable image cards reuse the motion-matching component, with a selected
border and native button keyboard operation; there is no separate radio selector.
The cards are followed by side-by-side primary
Check diagram / optional hint buttons. Choosing or requesting a hint never checks
an answer. Checking with no selection does not score an attempt; wrong choices remain revisable; repeated
unchanged checks do not duplicate records. One star per completed case appears
in the shared upper-right header. Success uses the five-second cancellable
countdown and shared automatic-loading preference. Context filters, related
cases, skip/next, performance, and reset remain available. Checked answers store
their selected and expected diagrams in Current Session Progress. Text diagram
descriptions offer the same force identity, direction, and relative lengths.

Verification: `python tools/test_force_diagram_match.py` independently checks all
ten force/direction sets and their net-force signs, 500 shuffled boards for exactly
one physically valid answer and all answer positions, qualitative size invariance,
and 40 rendered diagrams. Routed AppTest covers blank checks, retries, hint/draft
preservation, navigation, context changes, stars, single history recording,
completion locking, reset, auto-load off, cancellation/resumption, and prevention
of duplicate advancement. The script is included in CI. Diagram contact sheets
were visually inspected. After switching to the shared clickable cards, live
browser checks confirmed mouse and Enter-key selection, the visible selected
border, and no submission on selection. The existing motion-card regressions
also passed. Touch, narrow-screen/assistive-technology behavior and teacher
content review remain pending.
Integration checks also passed: 4,320 existing generator payloads, prompt/answer
consistency, nine solve-for tests, the C4 suite, and the inventory drift check
(43 routes, 151 rows, no unresolved route adapters).

Deliberate exclusions: force-free deep-space and same-direction weight/drag cases,
diagram construction, exact force values/ratios, inclines/angled forces, two-axis
acceleration, printable output, persistent progress, and claims of TPC parity.
Review this pilot before the next phase-2 package (I2 construction or C2
force-to-motion matching); sharing the renderer does not complete those activities.

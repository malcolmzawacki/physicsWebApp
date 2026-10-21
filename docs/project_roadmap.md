# Project Roadmap & Backlog

_Direction and near-term rollout status updated: 2026-10-12_

Implemented behavior belongs in [current_state.md](current_state.md). This roadmap
orders future work; it does not mark an activity ready merely because its neighbor
works. Use the [rollout process](site_update_process.md), [inventory](organizing_help_inventory.md),
and review ledger for execution and evidence.

## Product direction: broader entry points and growing independence

The [Newton's Laws activity aspirations](newtons_laws_aspirations.md) assess the
eight Interactives and thirteen Concept Builders in that reference unit and
propose a phased implementation sequence. This is a scoped future candidate,
excluding the separate Forces in Two Dimensions unit; it does not reorder the
active rollout queue. C4 Recognizing Forces is now implemented as a bounded
teacher-preview pilot (2026-10-19); see current state and the aspiration's C4
implementation record. After the C4 interaction review, C5 Match the Free-Body
Diagram is now enabled for teacher preview (2026-10-20), covering ten original
cases with diagram selection, direction/size feedback, and the same progression.
I2 Free-Body Diagram Builder is now enabled for teacher preview (2026-10-20):
ten shared situations, live widget-driven construction, and separate force,
direction, and relative-size feedback. Review the editor before expanding to
dragging or additional situations. C2 Force and Motion Matching is now enabled
for teacher preview (2026-10-20): seven force cases, six motion cards, exact-set
multi-selection, and explicit unknown initial velocity. Teacher/layout review of
these pilots is deferred until the teacher is home; continue bounded implementation
and automated verification without blocking on small layout decisions. Phase 2's
initial selection/construction activities are implemented for preview; broader
content and classroom readiness remain separate. C3 Change of State is now enabled
for deferred teacher review (2026-10-20): ten before/after cases, add/remove/
increase/reduce options, and exact-set matching to the requested motion change.
Teacher priority changed to C10 Net Force and Acceleration Ranking, now enabled
for deferred review (2026-10-20): four-case boards, separate net force/acceleration
and magnitude/signed modes, controlled masses/ties, and same-case quantity
comparison. C6 Normal Force Card Sort remains a later phase-3 candidate.
Teacher/layout review of the recent pages remains deferred; the rest of the unit
is aspirational.

Help students with a wider range of starting abilities participate meaningfully
in physics and chemistry, then develop greater independence. Practice should
exercise reading, identifying quantities, interpreting representations, choosing
relationships, predicting, and evaluating results as well as algebra and
arithmetic. A student's algebra fluency should not be the only way they can enter
an activity or demonstrate physical understanding.

The intended student journey is: identify a need, find suitable practice, choose
support and a medium, commit to an attempt, use feedback, and decide what to try
next. A coherent release completes that journey for a reviewed scope of content;
the site can continue growing in response to classroom experience. There is no
fixed final feature list.

This is the direction for incremental development, not a separate rewrite
project. The current organizer rollout is the first foundation. Future work
should support these principles:

- **Separate challenge, support, and presentation.** Physics complexity, available
  scaffolds, and browser/paper delivery are independent choices. Easy/Medium/Hard
  labels alone do not describe a student's needs. Avoid adding every possible
  control to the interface; expose choices when they help the learning task.
- **Practice individual decisions and reconnect them.** Allow bounded practice
  of reading givens, identifying a target, selecting a relationship, interpreting
  a graph, or predicting a sign, then return to complete problems. A numerical
  organizer is one scaffold, not the universal activity format.
- **Use support to build independence.** Let students move from a worked example
  or guided attempt to a related problem with less help and then an unfamiliar
  context. Make support available again when needed; do not automatically remove
  it after a correct answer or equate supported success with independent mastery.
- **Preserve student agency.** Keep explicit commitment before feedback, useful
  retries, and clear distinctions between checking a setup, checking an answer,
  and revealing a solution. Feedback should address observable work without
  claiming to know the student's reasoning from a number alone.
- **Connect paper and browser practice.** Reuse the same underlying problems and
  instructional definitions, with layouts and supports suited to each medium.
  Changing presentation should not silently change the question set.

## Architectural direction supporting that journey

Extend existing foundations as reviewed families require them:

1. **Describe the meaning of a problem explicitly.** Build on quantity roles and
   setup metadata to represent givens, implied facts, actual targets, assumptions,
   units, displayed precision, and relevant object/axis/stage context. Prompts,
   diagrams, checking, hints, and exports should consume shared definitions.
   Authored equations and solutions remain appropriate; a universal algebra
   engine is not a prerequisite.
2. **Separate the problem from the attempt and its presentation.** Keep generated
   content distinct from student entries, submitted checks, revealed help,
   scoring/progression, and document layout. Share lifecycle behavior where it
   fits while retaining task-specific interactions for explorers and matching.
3. **Consolidate activity capabilities incrementally.** Build toward stable
   activity descriptions used by navigation, solve-for, and worksheet selection.
   Record supported capabilities separately from reviewed/enabled scope; retain
   the review ledger as evidence rather than treating registration as readiness.
4. **Keep instructional logic reusable outside a particular UI.** Separate
   generation, checking, and document rendering from Streamlit display/state
   handling where those boundaries are touched. No frontend replacement is
   scheduled. Consider one only against concrete interaction requirements.
5. **Verify the student's actual experience.** Coverage matrices and tests should
   check intended branches, displayed givens and precision, feedback, state
   transitions, and applicable representations. A valid payload or one successful
   branch is insufficient evidence for a whole family.

Use a simple numerical family, a grouped-quantity family, and a nonnumeric
activity to test these boundaries during their scheduled work. Extend the model
from those concrete requirements before attempting a universal migration.

## Active initiative: systematic content and scaffolding rollout

Expand organizing help through bounded problem-family work packages. Each package
first evaluates content coverage, then connects shared definitions and metadata,
adds feedback, verifies behavior, and enables only its reviewed scope. Preserve
explicit student commitment before feedback, independent final-answer submission,
and consistent Enter/Tab behavior. Missing content is a separate deliverable and
must not disappear from view when the next family is selected.

The shared foundation is implemented and enabled for Accelerated Motion, Constant
Speed, Momentum, Wave Properties, Single Resistor, Easy Newton's Second Law, and Energy Basics.
Wave Properties' period problems and keyboard behavior are teacher-confirmed;
Easy Newton's Second Law is teacher-confirmed; Energy Basics is the current teacher preview checkpoint. This is
partial site coverage, not completion of a universal schema migration.

## Ordered near-term queue

Teacher checkpoint (2026-10-13): all four Energy pages are accepted for the current organizing-help scope, including Thermal Mixed. Energy content/difficulty expansion and printed organizers remain later work. The next priority is Projectiles, ahead of the generic rollout order, to support first-time physics students in the accelerated ECE UConn course before their upcoming kinematics exam. Review all three existing projectile families for horizontal/vertical roles, shared versus event-specific times, optional component calculations, sign conventions, displayed-value consistency, and explicit launch/landing geometry. Keep givens distinct from inferred or calculated values and keep explanatory help optional.

Circuit organizing help is now enabled for the two paired Fundamentals activities
and all five Series and Parallel activities, completing current-electricity
coverage with Single Resistor. The first component preview is teacher-approved;
the teacher-approved for the current scope. Broader content/difficulty
variety and additional circuit components remain later work.

Current teacher preview: Newton's Second Law Medium/Hard now has a first-pass
multi-step organizer, requested as the concrete experiment for the intermediate-
values decision. It separates copied givens from calculated supporting values and
marks net force when it also serves as a final answer. Easy retains its existing
organizer. Review this prototype before generalizing the pattern to energy or
circuits; the earlier Easy-only review remains evidence for that bounded scope.

| Order | Work package | Current position | Completion evidence |
|---|---|---|---|
| 1 | Establish the rollout process and inventory maintenance | Established; applied to Wave Properties | Existing family review now records eight-form scope, sampling, precision, exclusions, checks, and remaining teacher review; ledger and generated inventory updated |
| 2 | Wave Properties content completion | Implemented; automated checks passed | Eight forms, four targets, displayed-given precision policy, consistent units/equations; 2,376 displayed-value cases passed |
| 3 | Wave Properties organizing help | Completed for reviewed scope; teacher checked | Teacher confirmed new period problems and Tab/Enter behavior on 2026-10-12; automated content/interaction checks passed |
| 4 | Single Resistor review and rollout | Enabled; teacher/browser review pending | All nine target/difficulty branches and 507 curated cases reviewed; shared profile, custom-page lifecycle, diagram/givens agreement, feedback and export checks passed |
| 5 | Circuit task coherence | Accepted as viable baseline; equation reference completed | Circuit Fundamentals provides Single Resistor plus paired series/parallel current-and-voltage practice; standalone copy-the-given tasks retired; both component answers checked once with individual feedback; duplicate Series Current retired, full Series Voltage Drop moved to Series and Parallel; current/voltage support distinguishes learning focus; old-session recovery and regressions checked. Duplicate Givens panels removed, diagrams widened/spaced, footer controls aligned with standard pages. Additional circuit organizers queued separately; see current_electricity_ohms_law.md |
| 6 | Simple Newton's Second Law review | Enabled on Easy; teacher checked | Teacher confirmed intended behavior on 2026-10-12. Net force/mass/acceleration organizer for all three targets and Mixed; 300 combinations and routed forms/scoring/transitions checked. Medium/Hard friction branches explicitly excluded; see current_state.md#newtons-second-law-easy-review |
| 7 | Energy Basics organizing help | Enabled; teacher preview pending | Elastic, kinetic, gravitational energy and work; all 28 available target/level branches, Mixed, 11,820 sampled-value cases, forms, progression, and exports checked. Explicit gravity/reference-height assumptions and flat-ground work prompts; see current_state.md#energy-basics-review |
| 8 | Intermediate-values design decision | Working pattern established through Forces and circuits | Decide how organizing help distinguishes a value that is not supplied but useful to calculate from one that is irrelevant. Clarify quantity identification versus solution planning, the meaning of the x marker, and any separate intermediate-step support before implementing multi-step families. The current pattern separates Given information from Possible in-between calculations, keeps help optional, and excludes the last requested calculation from the intermediate section. Generalize through subsequent family reviews. |
| 9 | Circuit organizing help | Enabled throughout Current Electricity; teacher-approved for the current scope | All eight activities covered. Component grouping and optional help retained; intermediate fields only where needed. Seven-activity component suite checks 1,680 cases and 21 routed branches; Single Resistor has separate 507-case coverage. Initial paired/Voltage Drop preview teacher-approved. See current_electricity_series_parallel.md |
| 10 | Conservation of Energy organizing help | Enabled; teacher preview pending | All three families, both directions, existing targets and all difficulties; additional Mixed problem type samples conversions as well as targets. Stage-grouped givens and optional energy intermediates; 3,600 displayed-value cases across 60 scenario/level branches. Precision and vertical-change wording corrected; see current_state.md#conservation-of-energy-organizer-review |
| 11 | Thermal Energy organizing help | Enabled; teacher preview pending | Three families, six directions, all 58 existing direction/target/level branches. Optional stage givens and mechanical-energy intermediates; positive thermal/sign labels and displayed-fact answers aligned. 3,480 sampled cases and page/export checks passed. Friction and Distance is next after review; see current_state.md#thermal-energy-organizer-review |
| 12 | Friction and Distance plus Thermal Mixed | Enabled; teacher preview pending | All 90 Friction/Distance direction/target/level branches, 3,600 displayed-fact cases, stage/path roles and energy intermediates. Thermal Mixed samples all three families/six directions; 360 seeded cases and exports checked. All four Energy pages now have optional organizing help; see current_state.md#friction-and-distance-organizer-review |
| Later review | Circuit difficulty progression and content variety | Documented; no current expansion | Current levels mainly change curated values/decimal arithmetic, not topology or reasoning. Review varied givens/targets, ratios, conceptual tasks, and configurations separately from organizing help; see current_electricity_series_parallel.md. Teacher accepts the present activities as a viable baseline. |
| Parallel maintenance | Make organizer regressions mandatory | CI configured; local checks passed | Schema, organizer, Constant Speed, Momentum, Waves, Single Resistor, and inventory checks added; route assertion reconciled to 41; remote CI result pending |

A queue position is not an assessment. Complete each family's intended scope or
document an explicit, visible exclusion before enabling it; do not invent inverses
just to make a table symmetric. Wave Properties now supplies the first worked
example of the rollout process. The initial preference for Newton's Second Law
was based on scalar-organizer implementation complexity. The teacher's circuit
review now prioritizes instructional coherence within the current unit: review
the overlapping tasks. That bounded content split is now implemented. Additional
relationship/network organizers have an explicit follow-up package in the queue;
full circuit analysis remains future work. The
Easy Newton's Second Law package is now teacher-confirmed. Energy Basics is enabled
for teacher preview; Forces and circuits now provide a working intermediate-values pattern. Conservation of Energy is now enabled for teacher preview; Thermal Energy is also enabled for teacher preview; Friction and Distance is now also enabled for teacher preview.

The later forces review must distinguish applied and net force in Medium/Hard,
state the horizontal/friction/gravity assumptions used by the solver and equations,
and assess the numeric-only difficulty progression. It is separate from the
completed Easy scalar scope and is not silently enabled by that organizer.

## Subsequent rollout waves

1. **Single-object scalar relations:** energy/work, numerical impulse, rotational
   motion, and simple torque. Define conversions, sign conventions, constants,
   displayed precision, and difficulty-dependent outputs before migration.
2. **Grouped quantities:** average/combined journeys, projectiles, relative motion,
   collisions, and multi-force systems. Build object/axis/stage roles and layouts
   once a reviewed family supplies concrete requirements.
3. **Networks and species:** circuit branches/components and stoichiometry need
   topology/species context and custom-page adapters.
4. **Other representations:** graphs, rankings, compound naming, algebra, and
   explorers require a scaffold suited to their learning task. They remain in the
   inventory; numerical tables are not the default completion criterion.
5. **Worksheet assistance:** decide independently whether/how organizers belong in
   printable worksheets and answer keys. Practice support does not imply export
   support.

## Shared architecture and feedback work

- **Conceptual circuit progression:** later explore building circuits and judging
  whether depicted circuits provide a closed conducting path. Use clear, deliberate
  open terminals and junctions; unintended wire tails must not look like branches.
  Current introductory resistor activities depict complete source/component loops.
  Extend this teaching model explicitly when additional components require it.

- **Dyslexia accessibility:** reduce unnecessary reading and keep labels concise.
  Put optional explanations in accessible help controls; preserve essential
  problem information and review readability and compact layouts on student laptops.

- Extend quantity definitions and role-specific notation incrementally. Preserve
  displacement x and v_i/v_f conventions; distinguish quantity IDs from x markers.
- Connect prompt wording, equation symbols, answer labels, units, and target roles
  to shared definitions. Remove duplicate page equation references during migration.
- Treat prompt-given values as the source for setup checking; hidden calculated
  values remain distinct. Include implied facts and actual targets for Mixed cases.
- Add narrow, testable feedback rules with stable categories and counterexamples.
  Separate unit/quantity mistakes from initial/final, object, sign, and stage errors.
  Keep a useful fallback; never claim to infer reasoning solely from a number.
- Establish displayed precision and per-field unit contracts before reciprocal or
  converted values expand. Future context-sensitive number generation is separate.
- Review tab order, Enter behavior, text/icon cues, narrow-screen layouts, and
  assistive-technology usability on each new layout. Automated tests do not certify
  accessibility.

## Privacy-preserving feedback-gap reporting: deferred

No collection or notification service is active. A later design may capture only
unclassified feedback gaps, aggregate repeated patterns, and notify once per new
pattern. It must use a strict field allowlist, exclude identity/session/device/IP
and raw free text, set retention, and separate immediate storage from scheduled
notification. Personal-email routing, hosting logs, service selection, and applicable
school requirements need an explicit review before implementation. Do not add
learner tracking as an incidental part of the scaffolding rollout.

## Other continuing initiatives

- **Realistic values and contexts:** subject-appropriate ranges, units, and reusable
  scenario packs; consistent conversion and precision policies.
- **Structured solutions and hints:** one source for conceptual steps, substitution,
  and answers across UI and exports. Circuit incorrect answers retain the worked
  calculation until explicit progression. Correct answers offer an optional
  calculation and a five-second cancellable countdown, preserving rapid practice. Next, design staged wrong-answer support
  (physical relationship, equation choice, substitution, calculation) with useful
  opportunities to revise before revealing the full solution; do not infer a
  specific misconception from a numerical answer alone.
- **Final-answer interaction:** retryable attempts and an explicit Show Answer
  pathway; keep separate from organizer feedback and current scoring behavior.
- **Worksheet/export quality:** mixed activity sections, diagrams, physical writing
  space, pagination, PDF preview, and conversion reliability; preserve reusable
  question sets when only layout changes.
- **Correctness and compatibility:** branch-aware physics invariants, unsupported
  argument checks, custom-layout lifecycle coverage, dependency/startup verification,
  and Markdown/equation formatting parity.
- **Performance and maintenance:** rerun-safe timing, lazy nested activity loading,
  document-rendering separation, portable file handling, and encoding cleanup where
  verified by a focused review.

## Longer-term proposals (not current implementation commitments)

The direction above is agreed; these implementations remain candidates rather
than additions to the immediate queue. Promote one bounded pilot at a time after
its prerequisite content and metadata are ready.

| Candidate | Instructional purpose / implementation boundary |
|---|---|
| Focused skill practice | Isolate reading, quantities/units, relationship choice, sign, graph interpretation, or estimation; reconnect the skill to a complete problem. |
| Supported-to-independent practice pilot | In one reviewed family, offer a guided attempt followed by a related problem with less help available by choice. Review whether students can proceed and explain their next step; completion alone is not mastery evidence. Can begin session-locally without learner accounts. |
| Deliberately related problems | Vary one condition, the requested quantity, the context, or the representation intentionally; distinguish numerical repetition from transfer to a new situation. |
| Worked-error analysis and reasonableness | Let students inspect a plausible solution, identify an error, predict a result, or evaluate units and physical bounds before calculating. |
| Paper/browser problem references | Reopen the exact printed problem for support or discussion. Requires a versioned reproducibility strategy; a seed alone is insufficient when generator behavior changes. |
| Teacher-curated practice recipes | Describe a skill focus, problem mix, support options, and length, then reuse the recipe with fresh problems across supported media. |
| Author inspection tools | Preview branches, roles, displayed numbers, and browser/export output together; surface content gaps and reproduce questionable cases. Build on the inventory and author mode. |

The independence pilot does not require completing the site-wide organizer
migration. Select a ready family, define the specific skill and intended support
transition, and use teacher/student review before expanding. Record findings in
that family's existing review rather than introducing a separate strategy file.

Other candidates: reusable context packs, dimensional checks, multi-step problems,
diagram annotation, partial credit, and localization. Mastery analytics, automatic
adaptation, persistent learner history, reflection logging, and free-response
evaluation require separate pedagogical/privacy decisions. They are not implied
by student-selected support or session-local practice sequences.

## Completed foundations / historical references

Shared route navigation, dict payloads, State helpers, supported-target solve-for
catalog, stable progress IDs, correctness guardrails, DOCX equations/Markdown,
student PDF worksheet tooling, and the five-family organizer foundation are in
place. Earlier detailed fix records remain linked from current_state. Claims that
validation still needs its original path repair, solve-for is universally absent,
or all pages share one lifecycle are obsolete; new gaps should be recorded with
specific evidence and scope.

## Precision-aware numerical grading (future iteration; 2026-10-13)

- Record displayed givens and their rounding precision alongside full-precision
  values. Evaluate how those rounded inputs affect each requested answer, rather
  than choosing a tolerance from the answer magnitude alone.
- Build per-answer tolerances from propagated input-rounding uncertainty, with
  an explicit policy for student answer rounding. Retain an absolute tolerance
  near zero, where relative error alone is unsuitable. Keep measurement/rounding
  allowances distinct from any pedagogical allowance for mistakes.
- Begin with an Atwood audit: independently solve every target and prompt variant
  using only the displayed givens; compare with stored answers at the proposed
  three-decimal display precision. Cover near-balanced forces, small acceleration,
  inverse mass calculations, and multipart outputs. If rounding makes a case
  ambiguous or unstable, retain more precision or adjust generation rather than
  silently granting a very large tolerance.
- This is deferred work, not an implemented grading change. Current Atwood givens
  remain at four decimal places until the calculation audit is complete. A full
  variant audit requires explicit mappings of displayed givens and independent
  inverse calculations; do not treat a few random examples as sufficient evidence.

### Projectile preview checkpoint (2026-10-13)

The first organizer pass is enabled across Type 1/2/3 and all current targets and
levels. Preserve these teaching categories; diagrams will provide reminders in a
separate effort. Horizontal/vertical columns, vector givens and a shared time row
are ready for teacher review. Screen height on small laptops is the next explicit
layout decision. Optional hints and distinct given/intermediate values remain the
established pattern. Displayed-fact calculations and elevated-landing crossing
consistency were corrected as part of the rollout; see
[current state](current_state.md#projectile-organizer-first-pass).

# Organizing help: architecture and rollout readiness

For the exhaustive routed activity/problem-type checklist and explicit review
blanks, use the [organizing-help inventory](organizing_help_inventory.md).
The family-level recommendations below are planning guidance, not completed reviews.
Use the [rollout process](site_update_process.md) and [current roadmap](project_roadmap.md)
for execution order; dated rollout notes below are historical findings.

## Implemented contract

Classroom layout principle (2026-10-22): aim to show the essential question,
givens and answer controls together in one frame on roughly 2:1 Chromebook
screens. Put secondary instructions, conventions and modeling explanations in
hover help beside the scenario title. Keep target objects, necessary values,
comparison modes and "check all that apply" visible. This is a practical design
goal, not a reason to shrink important text or omit information.

`utils/quantities.py` separates physical definitions (name, unit, dimension) from
profile-local roles (quantity reference, display name, LaTeX symbol, phase).
Distance and displacement, and speed and velocity, have distinct identities even
when dimensions match. Roles can share a physical definition without sharing a
symbol. Add object/component/axis context explicitly when those profiles migrate;
do not encode physical identity by guessing from a letter or a unit.

`extras.setup` is optional JSON-safe metadata with version 1, a registered profile,
a field for every role, and actual `target_roles` in profile order. Field statuses
are given, implied, requested, or absent. Only given/implied fields contain values;
implied fields also require a wording cue. Requested/absent fields cannot carry
hidden numeric answers. Values use the profile's declared units for this pilot.
Future variable-unit generation needs per-field unit IDs and a conversion policy
before being enabled; this version does not implement conversions.

The normal payload validator checks the contract. `make_setup` builds it from the
same values and target used to write the prompt. `expected_entries` translates
statuses to the student-facing ? and x markers. The compatibility `setup_expected`
map remains on accelerated-motion payloads, derived from the new source.

The workspace reads profile roles dynamically and renders nothing without setup
metadata. Page opt-ins now include Accelerated Motion, Constant Speed, Momentum,
Wave Properties, and Single Resistor. Constant Speed is enabled
within Constant Motion; other Constant Motion branches remain unsupported and
show no organizing-help panel. Explicit checking, independent grading, and session-local
state behavior are unchanged.

Migrated solve-for catalog entries declare `quantity_roles`.
The dispatcher checks that explicit selections agree with the generated target.
Mixed practice uses the family's declared sampling policy; generated setup reports the
actual target even when the request was mixed. Existing target IDs stay unchanged.

Equations use explicit ${role} templates resolved through the same profile symbols.
All Accelerated Motion equation displays and the Constant Speed equation displays
are migrated. These remain authored formulas, not an algebra engine. Other formula
strings and legacy answer labels remain migration work. No runtime LaTeX parsing.

Feedback rules accept role definitions instead of assuming vi/vf always mean
linear velocity. Quantity/role-aware rules can be added independently of rendering.
No persistence, email, event collection, or automatic live grading is introduced.

## Readiness by page / activity family

These are implementation entry points and required work, not claims that all
branches have been migrated or individually audited for prompt correctness.

| Page/activity | Required construction before enabling |
|---|---|
| Accelerated Motion | Migrated; keep schema, prompt, equation, and target checks in regression coverage. |
| Constant Motion | Constant Speed metadata/equations ready; average and combined variants need leg-specific distance/displacement and time roles, and explicit totals. |
| Vectors and Displacement | Separate magnitudes, signed components, directions, and path legs; review which tasks need component tables rather than scalar fields. |
| Relative Motion | Define observer/reference-frame and object roles; distinguish signed component and magnitude conventions. |
| Projectiles | Add axis and event roles; identify shared time and implied components; document sign convention and gravity assumptions. |
| Rotational Motion | Add angular definitions/units and separate profiles; do not reuse linear identities for a/vi/vf. |
| Torque | Define force, lever arm, angle, and sign conventions; qualitative ranking needs its own assistance design. |
| Forces | Separate net/applied/normal/friction/tension/weight; add body and system context. Tension, incline, Atwood, and center-of-mass branches need their own profiles and prompt metadata. |
| Momentum and Impulse | Add object and before/after roles; distinguish impulse, momentum, change in momentum, and contact time. Collision and multipart targets require explicit target lists. |
| Energy | Separate energy type and state, work, power, thermal loss, distance, and height; avoid assuming every internally computed intermediate is given. |
| Waves | Wave Properties' four roles and eight forms are migrated/enabled and teacher checked. Harmonics and sound-level quantities remain unreviewed for organizing help. |
| Static Electricity | Numeric Coulomb/field cases need charge and object roles; friction, conduction, and induction sequence/sign activities need a different organizing interaction. |
| Current Electricity / Circuits | Single Resistor's V/I/R profile is enabled across all difficulties; teacher review pending. Series Current/Voltage Drop and power/charge/time require separate reviews and component/source/total roles. |
| Series/Parallel Circuits | Build component/branch/whole-circuit groups from topology; a flat five-column form is not an appropriate default. |
| Stoichiometry | Add species, amount kind, reaction role, and conversion basis; constants and molar masses need explicit availability rules. Custom page flow needs an adapter to the shared renderer. |
| Compound Names | Formula/name/charge reasoning requires a distinct scaffold, not numeric givens. |
| Math Skills | Arithmetic and rearrangement need expression/step assistance; do not force physical-quantity roles onto them. |
| Graph analysis and matching | Coordinate, slope, area, and representation-specific assistance need separate design. |
| Test Page / explorers | No automatic opt-in; assistance should follow each interactive activity's objective. |

## Migration gate for each family

1. Define quantities and local roles with units, symbols, and context.
2. Emit actual prompt information for every supported difficulty/target branch,
   including implied facts and multiple targets. Use absent for excluded roles.
3. Link applicable solve-for entries and equation templates explicitly.
4. Test prompt/metadata agreement, mixed generation, zeros, signs, coincident
   values, requested/hidden separation, and unsupported branches.
5. Review the layout with realistic field counts and narrow screens, then opt in
   the page. Keep unsupported branches free of organizing-help UI.

Constant Speed, Momentum, Wave Properties, and Single Resistor are enabled. Follow
Single Resistor's teacher review checkpoint, then simple force/mass/acceleration. Build
object/axis/component grouping before enabling collisions or circuit networks.


## Proposed review order after the ready-feature rollout (2026-10-03)

This is an estimate of implementation difficulty, not a readiness assessment.
Unreviewed inventory rows remain blank until their actual branches are inspected.

1. Simple scalar relations: Momentum, Wave Properties, Single Resistor; then
   Newton's Second Law's simplest cases. Review difficulty-dependent branches
   before enabling an entire problem type.
2. More single-object quantities: energy/work, basic impulse, rotational motion
   (unit conversions), and simple torque. Establish unit/sign policies explicitly.
3. Multiple stages, objects, or axes: average/combined motion, projectiles,
   relative motion, collisions, and multi-force systems. Add grouping first.
4. Circuit networks and chemistry: topology/species roles and conversion context.
5. Graphs, rankings, symbolic exercises, and explorers: design a suitable scaffold
   before deciding whether any of the numeric organizer should be reused.

Worksheet builders remain a separate export decision rather than automatically
inheriting the practice page's organizing-help review status.


## Momentum rollout findings (2026-10-03)

The Momentum practice activity now uses the shared organizer for momentum, mass,
and velocity. All three solve-for branches provide two givens and one requested
quantity. The current generator uses positive values and exposes only Easy on its
page; this rollout does not generalize it to signed vectors or collisions.
The existing Ns unit is retained (equivalent to kg m/s); conversion support remains
out of scope. Ordinary velocity has no initial/final phase, so the shared feedback
correctly omits the start/end reminder. No new layout or feedback rule was needed.
All displayed equations use shared profile symbols. The regression test checks
prompt/given agreement, no feedback before Check setup, all targets, value mix-ups,
question resets, and independent final-answer grading.

## Wave Properties rollout findings (2026-10-12)

Wave Properties now covers eight given/target forms with a four-role organizer,
shared equations/units, and four solve-for targets. Displayed period givens drive
answers; derived-but-unstated quantities remain absent. Automated checks passed;
the teacher confirmed period problems and Tab/Enter behavior. See [its coverage review](wave_properties_review.md).
The current queue remains in the roadmap.

## Single Resistor rollout findings (2026-10-12)

The case model emits a V/I/R setup profile; both circuit payload adapters preserve
it. The custom page retains a normalized payload and aligns its existing question
number with the shared organizer ID, allowing shared checking/reset behavior
without replacing circuit scoring. Givens and diagram labels use the same displayed
values. All nine target/difficulty branches and 507 curated cases passed review
checks; teacher/browser layout review is pending. See the [existing circuit guide](current_electricity_ohms_law.md#single-resistor-organizing-help-scope).
Other circuit subtypes and printed organizers remain separate work.

## Layout and equation-reference preferences

Group directional information by axis in consistent rows or columns. Within an
axis, group quantities of the same type together where space allows: initial and
final vertical velocity can share a row. Equation references should similarly
group alternative ways of solving for the same quantity, as Accelerated Motion
does for distance, time, and velocity. Keep given facts separate from supporting
calculations even when the same quantity type appears in both sections. Optional
hints carry extra explanation; compactness should preserve readable labels.

Projectile base references contain the general relations. Type-specific derived
relations (including Type 2 zero net vertical displacement, total flight time,
and maximum height) belong only in More equations, rather than both reference
modes. Type 1/2/3 names remain teaching categories. Updated 2026-10-13.

Avoid duplicate organizer inputs for equivalent geometric information: projectile
cliff height and signed launch-to-landing displacement do not need separate
entries. Do not add a field solely to reinforce a sign convention when optional
help can carry that reminder. Type 2 needs no separate zero-displacement input.

# Organizing help: architecture and rollout readiness

For the exhaustive routed activity/problem-type checklist and explicit review
blanks, use the [organizing-help inventory](organizing_help_inventory.md).
The family-level recommendations below are planning guidance, not completed reviews.

## Implemented contract

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
metadata. Its existing page opt-in remains: Accelerated Motion and Constant Speed show the UI. Constant Speed is enabled
within Constant Motion; other Constant Motion branches remain unsupported and
show no organizing-help panel. Explicit checking, independent grading, and session-local
state behavior are unchanged.

Solve-for catalog entries for both migrated families now declare `quantity_roles`.
The dispatcher checks that explicit selections agree with the generated target.
Mixed practice retains its sampling behavior; the generated setup reports the
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
| Waves | Distinguish frequency, period, speed, wavelength, and sound-level quantities; logarithmic cases need separate validation conventions. |
| Static Electricity | Numeric Coulomb/field cases need charge and object roles; friction, conduction, and induction sequence/sign activities need a different organizing interaction. |
| Current Electricity / Circuits | Define current, potential difference, resistance, power, charge/time where used; bind component and source/total roles to the diagram model. |
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

Constant Speed is now enabled. Next, review a simple momentum or
force/mass/acceleration family to validate cross-unit reuse. Build
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

Next simple-scalar candidate: Wave Properties. Its frequency/period distinctions
and actual generated branches should be reviewed before enabling the organizer.

# Organizing-help activity and problem-type inventory

Generated from the current route catalog and generator/worksheet metadata, with
explicit adapters for custom pages. **47 routes; 166 problem-type/mode rows.**

A blank **Review** or **Findings / next work** cell means **not yet evaluated for
organizing help**. Discovery is not review, migration, or proof of readiness.
Previously passing solve-for and payload tests do not fill these review cells.
Recorded assessments are limited to the migrated families listed below.

Scope: every routed activity, including Advanced routes, custom pages, explorers,
labs, and both worksheet builders. Rows represent selectable problem types or
named modes; custom activities without such a selector use a descriptive task row.
Difficulty/solve-for combinations, randomized scenario branches, and individual
worksheet recipes are future review dimensions, not all separately enumerated here.
Stoichiometry reaction-type rows each include all available difficulties/conversions.
Worksheet rows remain unreviewed even when the underlying practice generator was
migrated: export scaffolding is a separate question.

Maintain decisions in [organizing_help_reviews.json](organizing_help_reviews.json).
Rebuild with `python tools/build_organizing_inventory.py`; verify drift with
`python tools/build_organizing_inventory.py --check`. New unmapped routes receive an
UNRESOLVED placeholder rather than disappearing. Generator type changes are picked
up automatically; custom selector changes require updating the explicit adapter.

See [architecture and migration requirements](organizing_help_architecture.md).


## Foundations / Algebra

Route: `file:app_pages/1_0.1.1_Math_Skills.py::algebra.main` ([page](../app_pages/1_0.1.1_Math_Skills.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Step-by-step equation rearrangement (easy / medium / hard / extra_hard) | [custom mode/task](../app_pages/1_0.1.1_Math_Skills.py) |  |  |

## Foundations / Scientific Notation

Route: `file:app_pages/1_0.1.1_Math_Skills.py::sci_notate.main` ([page](../app_pages/1_0.1.1_Math_Skills.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Scientific-notation expressions (easy / medium / hard) | [custom mode/task](../app_pages/1_0.1.1_Math_Skills.py) |  |  |

## Foundations / Arithmetic

Route: `file:app_pages/1_0.1.1_Math_Skills.py::arithmetic.main` ([page](../app_pages/1_0.1.1_Math_Skills.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Addition | [generator metadata](../utils/generators/arithmetic_generator.py) |  |  |
| Subtraction | [generator metadata](../utils/generators/arithmetic_generator.py) |  |  |
| Multiplication | [generator metadata](../utils/generators/arithmetic_generator.py) |  |  |
| Division | [generator metadata](../utils/generators/arithmetic_generator.py) |  |  |

## Foundations / Vector Practice

Route: `file:app_pages/1_1.1.0_Vectors_and_Displacement.py::vectors.vector_practice` ([page](../app_pages/1_1.1.0_Vectors_and_Displacement.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Find Components | [generator metadata](../utils/generators/vector_generator.py) |  |  |
| Find Resultant | [generator metadata](../utils/generators/vector_generator.py) |  |  |
| Summing Vectors | [generator metadata](../utils/generators/vector_generator.py) |  |  |

## Kinematics / Create a worksheet

Route: `utils.worksheet_ui:render_kinematics_worksheet` ([page](../utils/worksheet_ui.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Accelerated Motion / No Time | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Accelerated Motion / No Distance | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Accelerated Motion / No Acceleration | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Accelerated Motion / No Final Velocity | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Accelerated Motion / Mixed | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Constant Motion / Constant Speed | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Constant Motion / Average Speed | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Constant Motion / Average Velocity | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Constant Motion / Combined Constant Motion | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Distance & Displacement / One Dimensional | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Distance & Displacement / Two Dimensional | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Projectiles / Type 1 | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Projectiles / Type 2 | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Projectiles / Type 3 | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Relative Motion / Independent motion | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Relative Motion / Nested reference frames | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Relative Motion / Combined | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Types of Motion Graphs / Position-Time Graph | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Types of Motion Graphs / Velocity-Time Graph | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Matching Motion Graphs / Position-Time First | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Matching Motion Graphs / Velocity-Time First | [worksheet catalog](../utils/worksheet_ui.py) |  |  |

## Kinematics / Relative Motion

Route: `file:app_pages/1_1.1.4_Relative_Motion.py::relative_motion` ([page](../app_pages/1_1.1.4_Relative_Motion.py)); minimum level: advanced.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Independent motion | [generator metadata](../utils/generators/kinematics/relative_motion_generator.py) |  |  |
| Nested reference frames | [generator metadata](../utils/generators/kinematics/relative_motion_generator.py) |  |  |
| Combined | [generator metadata](../utils/generators/kinematics/relative_motion_generator.py) |  |  |

## Kinematics / Distance & Displacement

Route: `file:app_pages/1_1.1.0_Vectors_and_Displacement.py::dist_disp.distance_displacement` ([page](../app_pages/1_1.1.0_Vectors_and_Displacement.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| One Dimensional | [generator metadata](../utils/generators/kinematics/dist_disp_generator.py) |  |  |
| Two Dimensional | [generator metadata](../utils/generators/kinematics/dist_disp_generator.py) |  |  |

## Kinematics / Constant Motion

Route: `file:app_pages/1_1.1.1_Motion.py::constant_motion` ([page](../app_pages/1_1.1.1_Motion.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Constant Speed | [generator metadata](../utils/generators/kinematics/const_motion_generator.py) | Migrated; enabled | Three-role organizing help enabled for Constant Speed only. Page checks cover explicit targets, submission isolation, feedback, and switching to unsupported problem types. Reviewed 2026-10-03. |
| Average Speed | [generator metadata](../utils/generators/kinematics/const_motion_generator.py) |  |  |
| Average Velocity | [generator metadata](../utils/generators/kinematics/const_motion_generator.py) |  |  |
| Combined Constant Motion | [generator metadata](../utils/generators/kinematics/const_motion_generator.py) |  |  |

## Kinematics / Accelerated Motion

Route: `file:app_pages/1_1.1.1_Motion.py::accelerated_motion` ([page](../app_pages/1_1.1.1_Motion.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| No Time | [generator metadata](../utils/generators/kinematics/linear_motion_generator.py) | Migrated; pilot enabled | Shared quantities, setup schema, equations, and generator metadata implemented; setup/schema tests cover family. Detailed feedback-rule coverage remains limited. Reviewed 2026-10-02. |
| No Distance | [generator metadata](../utils/generators/kinematics/linear_motion_generator.py) | Migrated; pilot enabled | Shared quantities, setup schema, equations, and generator metadata implemented; setup/schema tests cover family. Detailed feedback-rule coverage remains limited. Reviewed 2026-10-02. |
| No Acceleration | [generator metadata](../utils/generators/kinematics/linear_motion_generator.py) | Migrated; pilot enabled | Shared quantities, setup schema, equations, and generator metadata implemented; setup/schema tests cover family. Detailed feedback-rule coverage remains limited. Reviewed 2026-10-02. |
| No Final Velocity | [generator metadata](../utils/generators/kinematics/linear_motion_generator.py) | Migrated; pilot enabled | Shared quantities, setup schema, equations, and generator metadata implemented; setup/schema tests cover family. Detailed feedback-rule coverage remains limited. Reviewed 2026-10-02. |
| Mixed | [generator metadata](../utils/generators/kinematics/linear_motion_generator.py) | Migrated; pilot enabled | Shared quantities, setup schema, equations, and generator metadata implemented; setup/schema tests cover family. Detailed feedback-rule coverage remains limited. Reviewed 2026-10-02. |

## Kinematics / Types of Motion Graphs

Route: `file:app_pages/1_1.1.1_Motion.py::motion_graph_types` ([page](../app_pages/1_1.1.1_Motion.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Position-Time Graph | [generator metadata](../utils/generators/kinematics/motion_graph_generator.py) |  |  |
| Velocity-Time Graph | [generator metadata](../utils/generators/kinematics/motion_graph_generator.py) |  |  |

## Kinematics / Matching Motion Graphs

Route: `file:app_pages/1_1.1.1_Motion.py::motion_graph_matching` ([page](../app_pages/1_1.1.1_Motion.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Position-Time First | [custom mode/task](../app_pages/1_1.1.1_Motion.py) |  |  |
| Velocity-Time First | [custom mode/task](../app_pages/1_1.1.1_Motion.py) |  |  |

## Kinematics / Projectiles

Route: `file:app_pages/1_1.1.1_Motion.py::projectiles` ([page](../app_pages/1_1.1.1_Motion.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Type 1 | [generator metadata](../utils/generators/kinematics/projectile_generator.py) | Enabled; first-pass teacher preview pending | Horizontal/vertical organizer with separate speed/angle givens and time row; optional hints, context-specific vertical displacement, and given versus intermediate separation. Existing names and target IDs retained. Answers follow printed givens. Type 3 elevated-landing crossing formula corrected; descending landing and same-height Type 2 geometry clarified. 1,860 sampled target cases, worksheet exports, independent forms and resets checked. Laptop height/readability review pending; diagrams are a separate teacher-directed effort. See current_state.md#projectile-organizer-first-pass. Updated 2026-10-13. |
| Type 2 | [generator metadata](../utils/generators/kinematics/projectile_generator.py) | Enabled; first-pass teacher preview pending | Horizontal/vertical organizer with separate speed/angle givens and time row; optional hints, context-specific vertical displacement, and given versus intermediate separation. Existing names and target IDs retained. Answers follow printed givens. Type 3 elevated-landing crossing formula corrected; descending landing and same-height Type 2 geometry clarified. 1,860 sampled target cases, worksheet exports, independent forms and resets checked. Laptop height/readability review pending; diagrams are a separate teacher-directed effort. See current_state.md#projectile-organizer-first-pass. Updated 2026-10-13. |
| Type 3 | [generator metadata](../utils/generators/kinematics/projectile_generator.py) | Enabled; first-pass teacher preview pending | Horizontal/vertical organizer with separate speed/angle givens and time row; optional hints, context-specific vertical displacement, and given versus intermediate separation. Existing names and target IDs retained. Answers follow printed givens. Type 3 elevated-landing crossing formula corrected; descending landing and same-height Type 2 geometry clarified. 1,860 sampled target cases, worksheet exports, independent forms and resets checked. Laptop height/readability review pending; diagrams are a separate teacher-directed effort. See current_state.md#projectile-organizer-first-pass. Updated 2026-10-13. |

## Rotation (Advanced) / Rotational Kinematics

Route: `file:app_pages/1_1.1.2_Rotational_Motion.py::rotational_kinematics` ([page](../app_pages/1_1.1.2_Rotational_Motion.py)); minimum level: advanced.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| No Time | [generator metadata](../utils/generators/rotational_motion_generator.py) |  |  |
| No Distance | [generator metadata](../utils/generators/rotational_motion_generator.py) |  |  |
| No Acceleration | [generator metadata](../utils/generators/rotational_motion_generator.py) |  |  |
| No Final Velocity | [generator metadata](../utils/generators/rotational_motion_generator.py) |  |  |
| Mixed | [generator metadata](../utils/generators/rotational_motion_generator.py) |  |  |

## Rotation (Advanced) / Torque

Route: `file:app_pages/1_1.1.3_Torque.py::torque_activity` ([page](../app_pages/1_1.1.3_Torque.py)); minimum level: advanced.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Perpendicular Force | [generator metadata](../utils/generators/torque_generator.py) |  |  |
| Angled Force | [generator metadata](../utils/generators/torque_generator.py) |  |  |
| Net Torque | [generator metadata](../utils/generators/torque_generator.py) |  |  |
| Torque Comparison (More/Less/Same) | [generator metadata](../utils/generators/torque_generator.py) |  |  |
| Torque Ranking (Least to Greatest) | [generator metadata](../utils/generators/torque_generator.py) |  |  |

## Dynamics / Create a worksheet

Route: `utils.worksheet_ui:render_forces_worksheet` ([page](../utils/worksheet_ui.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Newton's Second Law / Newton's Second Law | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Center of Mass / One Dimensional | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Center of Mass / Two Dimensional | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Tension / Suspension | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Atwood Machines / Static Friction Half Atwood | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Atwood Machines / Frictionless Half Atwood | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Atwood Machines / Kinetic Friction Half Atwood | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Inclined Planes / Static Incline | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Inclined Planes / Frictionless Incline | [worksheet catalog](../utils/worksheet_ui.py) |  |  |
| Inclined Planes / Kinetic Friction Incline | [worksheet catalog](../utils/worksheet_ui.py) |  |  |

## Dynamics / Recognizing Forces

Route: `utils.recognizing_forces_ui:render_recognizing_forces` ([page](../utils/recognizing_forces_ui.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| All contexts | [custom mode/task](../utils/recognizing_forces_ui.py) | Enabled; conceptual scaffold; teacher preview pending | Presence-only original C4 pilot with explicit named objects and assumptions, interaction hints, multi-selection checking, revision, related cases, five-second cancellable correct-answer progression, primary Check forces beside the hint, Skip question, and session-local completion records. Numerical organizers/equations and difficulty levels are inapplicable. Twelve cases, 1,536 answer sets and routed AppTest lifecycle checked. Visual/keyboard and teacher review pending. See newtons_laws_aspirations.md#c4-pilot-implementation-record. Updated 2026-10-19. |
| Surfaces | [custom mode/task](../utils/recognizing_forces_ui.py) | Enabled; conceptual scaffold; teacher preview pending | Presence-only original C4 pilot with explicit named objects and assumptions, interaction hints, multi-selection checking, revision, related cases, five-second cancellable correct-answer progression, primary Check forces beside the hint, Skip question, and session-local completion records. Numerical organizers/equations and difficulty levels are inapplicable. Twelve cases, 1,536 answer sets and routed AppTest lifecycle checked. Visual/keyboard and teacher review pending. See newtons_laws_aspirations.md#c4-pilot-implementation-record. Updated 2026-10-19. |
| Ropes | [custom mode/task](../utils/recognizing_forces_ui.py) | Enabled; conceptual scaffold; teacher preview pending | Presence-only original C4 pilot with explicit named objects and assumptions, interaction hints, multi-selection checking, revision, related cases, five-second cancellable correct-answer progression, primary Check forces beside the hint, Skip question, and session-local completion records. Numerical organizers/equations and difficulty levels are inapplicable. Twelve cases, 1,536 answer sets and routed AppTest lifecycle checked. Visual/keyboard and teacher review pending. See newtons_laws_aspirations.md#c4-pilot-implementation-record. Updated 2026-10-19. |
| Springs | [custom mode/task](../utils/recognizing_forces_ui.py) | Enabled; conceptual scaffold; teacher preview pending | Presence-only original C4 pilot with explicit named objects and assumptions, interaction hints, multi-selection checking, revision, related cases, five-second cancellable correct-answer progression, primary Check forces beside the hint, Skip question, and session-local completion records. Numerical organizers/equations and difficulty levels are inapplicable. Twelve cases, 1,536 answer sets and routed AppTest lifecycle checked. Visual/keyboard and teacher review pending. See newtons_laws_aspirations.md#c4-pilot-implementation-record. Updated 2026-10-19. |
| Flight | [custom mode/task](../utils/recognizing_forces_ui.py) | Enabled; conceptual scaffold; teacher preview pending | Presence-only original C4 pilot with explicit named objects and assumptions, interaction hints, multi-selection checking, revision, related cases, five-second cancellable correct-answer progression, primary Check forces beside the hint, Skip question, and session-local completion records. Numerical organizers/equations and difficulty levels are inapplicable. Twelve cases, 1,536 answer sets and routed AppTest lifecycle checked. Visual/keyboard and teacher review pending. See newtons_laws_aspirations.md#c4-pilot-implementation-record. Updated 2026-10-19. |

## Dynamics / Match the Free-Body Diagram

Route: `utils.force_diagram_match_ui:render_force_diagram_match` ([page](../utils/force_diagram_match_ui.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| All contexts | [custom mode/task](../utils/force_diagram_match_ui.py) | Enabled; conceptual scaffold; teacher preview pending | C5: ten original cases, four shuffled diagrams, clickable image selection using the shared motion-card component; single-choice checking by force identity/direction and qualitative size on each axis, hints, revision, upper-right stars, cancellable progression, session history with diagrams. 500 shuffled boards, 40 rendered diagrams and routed lifecycle checked. Numerical organizer, drawing and exports excluded. Live mouse/Enter selection and selected borders checked; no submission on selection. Motion-card regressions pass. Touch/accessibility and teacher review pending. See newtons_laws_aspirations.md#c5-pilot-implementation-record. Updated 2026-10-20. |
| Surfaces | [custom mode/task](../utils/force_diagram_match_ui.py) | Enabled; conceptual scaffold; teacher preview pending | C5: ten original cases, four shuffled diagrams, clickable image selection using the shared motion-card component; single-choice checking by force identity/direction and qualitative size on each axis, hints, revision, upper-right stars, cancellable progression, session history with diagrams. 500 shuffled boards, 40 rendered diagrams and routed lifecycle checked. Numerical organizer, drawing and exports excluded. Live mouse/Enter selection and selected borders checked; no submission on selection. Motion-card regressions pass. Touch/accessibility and teacher review pending. See newtons_laws_aspirations.md#c5-pilot-implementation-record. Updated 2026-10-20. |
| Ropes | [custom mode/task](../utils/force_diagram_match_ui.py) | Enabled; conceptual scaffold; teacher preview pending | C5: ten original cases, four shuffled diagrams, clickable image selection using the shared motion-card component; single-choice checking by force identity/direction and qualitative size on each axis, hints, revision, upper-right stars, cancellable progression, session history with diagrams. 500 shuffled boards, 40 rendered diagrams and routed lifecycle checked. Numerical organizer, drawing and exports excluded. Live mouse/Enter selection and selected borders checked; no submission on selection. Motion-card regressions pass. Touch/accessibility and teacher review pending. See newtons_laws_aspirations.md#c5-pilot-implementation-record. Updated 2026-10-20. |
| Springs | [custom mode/task](../utils/force_diagram_match_ui.py) | Enabled; conceptual scaffold; teacher preview pending | C5: ten original cases, four shuffled diagrams, clickable image selection using the shared motion-card component; single-choice checking by force identity/direction and qualitative size on each axis, hints, revision, upper-right stars, cancellable progression, session history with diagrams. 500 shuffled boards, 40 rendered diagrams and routed lifecycle checked. Numerical organizer, drawing and exports excluded. Live mouse/Enter selection and selected borders checked; no submission on selection. Motion-card regressions pass. Touch/accessibility and teacher review pending. See newtons_laws_aspirations.md#c5-pilot-implementation-record. Updated 2026-10-20. |
| Flight | [custom mode/task](../utils/force_diagram_match_ui.py) | Enabled; conceptual scaffold; teacher preview pending | C5: ten original cases, four shuffled diagrams, clickable image selection using the shared motion-card component; single-choice checking by force identity/direction and qualitative size on each axis, hints, revision, upper-right stars, cancellable progression, session history with diagrams. 500 shuffled boards, 40 rendered diagrams and routed lifecycle checked. Numerical organizer, drawing and exports excluded. Live mouse/Enter selection and selected borders checked; no submission on selection. Motion-card regressions pass. Touch/accessibility and teacher review pending. See newtons_laws_aspirations.md#c5-pilot-implementation-record. Updated 2026-10-20. |

## Dynamics / Free-Body Diagram Builder

Route: `utils.force_diagram_builder_ui:render_force_diagram_builder` ([page](../utils/force_diagram_builder_ui.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| All contexts | [custom mode/task](../utils/force_diagram_builder_ui.py) | Enabled; conceptual scaffold; teacher preview pending | I2: ten shared bounded situations; live force/direction/Short-Medium-Long editor and symbol-labeled preview. Separate presence/direction/size checks accept equivalent constructions. Hints, revisions, upper-right stars, shared cancellable progression, drafts, session snapshots and reset. 25,068 complete constructions, 1,280 force sets, rendering stress and routed lifecycle checked. Dragging, numerical equations, inclines, two-axis acceleration and exports excluded. See newtons_laws_aspirations.md#i2-builder-implementation-record. Updated 2026-10-20. |
| Surfaces | [custom mode/task](../utils/force_diagram_builder_ui.py) | Enabled; conceptual scaffold; teacher preview pending | I2: ten shared bounded situations; live force/direction/Short-Medium-Long editor and symbol-labeled preview. Separate presence/direction/size checks accept equivalent constructions. Hints, revisions, upper-right stars, shared cancellable progression, drafts, session snapshots and reset. 25,068 complete constructions, 1,280 force sets, rendering stress and routed lifecycle checked. Dragging, numerical equations, inclines, two-axis acceleration and exports excluded. See newtons_laws_aspirations.md#i2-builder-implementation-record. Updated 2026-10-20. |
| Ropes | [custom mode/task](../utils/force_diagram_builder_ui.py) | Enabled; conceptual scaffold; teacher preview pending | I2: ten shared bounded situations; live force/direction/Short-Medium-Long editor and symbol-labeled preview. Separate presence/direction/size checks accept equivalent constructions. Hints, revisions, upper-right stars, shared cancellable progression, drafts, session snapshots and reset. 25,068 complete constructions, 1,280 force sets, rendering stress and routed lifecycle checked. Dragging, numerical equations, inclines, two-axis acceleration and exports excluded. See newtons_laws_aspirations.md#i2-builder-implementation-record. Updated 2026-10-20. |
| Springs | [custom mode/task](../utils/force_diagram_builder_ui.py) | Enabled; conceptual scaffold; teacher preview pending | I2: ten shared bounded situations; live force/direction/Short-Medium-Long editor and symbol-labeled preview. Separate presence/direction/size checks accept equivalent constructions. Hints, revisions, upper-right stars, shared cancellable progression, drafts, session snapshots and reset. 25,068 complete constructions, 1,280 force sets, rendering stress and routed lifecycle checked. Dragging, numerical equations, inclines, two-axis acceleration and exports excluded. See newtons_laws_aspirations.md#i2-builder-implementation-record. Updated 2026-10-20. |
| Flight | [custom mode/task](../utils/force_diagram_builder_ui.py) | Enabled; conceptual scaffold; teacher preview pending | I2: ten shared bounded situations; live force/direction/Short-Medium-Long editor and symbol-labeled preview. Separate presence/direction/size checks accept equivalent constructions. Hints, revisions, upper-right stars, shared cancellable progression, drafts, session snapshots and reset. 25,068 complete constructions, 1,280 force sets, rendering stress and routed lifecycle checked. Dragging, numerical equations, inclines, two-axis acceleration and exports excluded. See newtons_laws_aspirations.md#i2-builder-implementation-record. Updated 2026-10-20. |

## Dynamics / Force and Motion Matching

Route: `utils.force_motion_match_ui:render_force_motion_match` ([page](../utils/force_motion_match_ui.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| All situations | [custom mode/task](../utils/force_motion_match_ui.py) | Enabled; conceptual scaffold; teacher/layout review deferred | C2: seven constant-force cases, four multi-select motion cards beside the initial diagram, nine synchronized motion histories. Initial velocity explicitly unknown; balanced forces admit rest and coasting both ways, unbalanced forces admit opposing initial directions. Exact-set missing/extra feedback, revisions, hints, stars, session images and cancellable progression. 2,240 answer sets and routed lifecycle checked. No velocity-dependent friction/drag or two-axis acceleration. Teacher/layout review deferred at user request. See newtons_laws_aspirations.md#c2-force-and-motion-implementation-record. Updated 2026-10-20. |
| Balanced forces | [custom mode/task](../utils/force_motion_match_ui.py) | Enabled; conceptual scaffold; teacher/layout review deferred | C2: seven constant-force cases, four multi-select motion cards beside the initial diagram, nine synchronized motion histories. Initial velocity explicitly unknown; balanced forces admit rest and coasting both ways, unbalanced forces admit opposing initial directions. Exact-set missing/extra feedback, revisions, hints, stars, session images and cancellable progression. 2,240 answer sets and routed lifecycle checked. No velocity-dependent friction/drag or two-axis acceleration. Teacher/layout review deferred at user request. See newtons_laws_aspirations.md#c2-force-and-motion-implementation-record. Updated 2026-10-20. |
| Horizontal net force | [custom mode/task](../utils/force_motion_match_ui.py) | Enabled; conceptual scaffold; teacher/layout review deferred | C2: seven constant-force cases, four multi-select motion cards beside the initial diagram, nine synchronized motion histories. Initial velocity explicitly unknown; balanced forces admit rest and coasting both ways, unbalanced forces admit opposing initial directions. Exact-set missing/extra feedback, revisions, hints, stars, session images and cancellable progression. 2,240 answer sets and routed lifecycle checked. No velocity-dependent friction/drag or two-axis acceleration. Teacher/layout review deferred at user request. See newtons_laws_aspirations.md#c2-force-and-motion-implementation-record. Updated 2026-10-20. |
| Vertical net force | [custom mode/task](../utils/force_motion_match_ui.py) | Enabled; conceptual scaffold; teacher/layout review deferred | C2: seven constant-force cases, four multi-select motion cards beside the initial diagram, nine synchronized motion histories. Initial velocity explicitly unknown; balanced forces admit rest and coasting both ways, unbalanced forces admit opposing initial directions. Exact-set missing/extra feedback, revisions, hints, stars, session images and cancellable progression. 2,240 answer sets and routed lifecycle checked. No velocity-dependent friction/drag or two-axis acceleration. Teacher/layout review deferred at user request. See newtons_laws_aspirations.md#c2-force-and-motion-implementation-record. Updated 2026-10-20. |

## Dynamics / Change of State

Route: `utils.force_change_ui:render_force_change` ([page](../utils/force_change_ui.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| All situations | [custom mode/task](../utils/force_change_ui.py) | Enabled; conceptual scaffold; teacher/layout review deferred | C3: ten before/after cart cases; four one-interaction changes beside the initial diagram, adding/removing/increasing/reducing horizontal pushes and rope pulls. Same mass and vertical equilibrium; explicit force magnitudes. Exact-set checking for requested acceleration/motion, hints/revisions/stars/session snapshots/cancellable progression. All 160 case/state combinations, 4,800 answer sets, 16 diagrams and routed lifecycle checked. Teacher/layout review deferred. See newtons_laws_aspirations.md#c3-change-of-state-implementation-record. Updated 2026-10-20. |
| Start moving | [custom mode/task](../utils/force_change_ui.py) | Enabled; conceptual scaffold; teacher/layout review deferred | C3: ten before/after cart cases; four one-interaction changes beside the initial diagram, adding/removing/increasing/reducing horizontal pushes and rope pulls. Same mass and vertical equilibrium; explicit force magnitudes. Exact-set checking for requested acceleration/motion, hints/revisions/stars/session snapshots/cancellable progression. All 160 case/state combinations, 4,800 answer sets, 16 diagrams and routed lifecycle checked. Teacher/layout review deferred. See newtons_laws_aspirations.md#c3-change-of-state-implementation-record. Updated 2026-10-20. |
| Change speed | [custom mode/task](../utils/force_change_ui.py) | Enabled; conceptual scaffold; teacher/layout review deferred | C3: ten before/after cart cases; four one-interaction changes beside the initial diagram, adding/removing/increasing/reducing horizontal pushes and rope pulls. Same mass and vertical equilibrium; explicit force magnitudes. Exact-set checking for requested acceleration/motion, hints/revisions/stars/session snapshots/cancellable progression. All 160 case/state combinations, 4,800 answer sets, 16 diagrams and routed lifecycle checked. Teacher/layout review deferred. See newtons_laws_aspirations.md#c3-change-of-state-implementation-record. Updated 2026-10-20. |
| Change acceleration | [custom mode/task](../utils/force_change_ui.py) | Enabled; conceptual scaffold; teacher/layout review deferred | C3: ten before/after cart cases; four one-interaction changes beside the initial diagram, adding/removing/increasing/reducing horizontal pushes and rope pulls. Same mass and vertical equilibrium; explicit force magnitudes. Exact-set checking for requested acceleration/motion, hints/revisions/stars/session snapshots/cancellable progression. All 160 case/state combinations, 4,800 answer sets, 16 diagrams and routed lifecycle checked. Teacher/layout review deferred. See newtons_laws_aspirations.md#c3-change-of-state-implementation-record. Updated 2026-10-20. |

## Dynamics / Net Force and Acceleration Ranking

Route: `utils.force_ranking_ui:render_force_ranking` ([page](../utils/force_ranking_ui.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Net force | [custom mode/task](../utils/force_ranking_ui.py) | Enabled; ranking scaffold; teacher/layout review deferred | C10: four-case cart rankings; magnitude or signed horizontal components, equal/different masses, controlled ties. Exact rational values, pairwise ordering/tie checking, rank gaps accepted, explicit form submission, hints/revision/stars/history/shared countdown. Same-case comparison switches force and acceleration. 1,600 boards, 20,480 rank assignments, 36 diagrams and all 16 routed settings checked. Teacher/layout review deferred. See newtons_laws_aspirations.md#c10-ranking-implementation-record. Updated 2026-10-20. |
| Acceleration | [custom mode/task](../utils/force_ranking_ui.py) | Enabled; ranking scaffold; teacher/layout review deferred | C10: four-case cart rankings; magnitude or signed horizontal components, equal/different masses, controlled ties. Exact rational values, pairwise ordering/tie checking, rank gaps accepted, explicit form submission, hints/revision/stars/history/shared countdown. Same-case comparison switches force and acceleration. 1,600 boards, 20,480 rank assignments, 36 diagrams and all 16 routed settings checked. Teacher/layout review deferred. See newtons_laws_aspirations.md#c10-ranking-implementation-record. Updated 2026-10-20. |

## Dynamics / Newton's Second Law

Route: `file:app_pages/1_2.1_Forces.py::newtons_2nd` ([page](../app_pages/1_2.1_Forces.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Newton's Second Law | [generator metadata](../utils/generators/force_generator.py) | Enabled; Easy only; teacher checked | Net force/mass/acceleration organizer enabled for all three Easy targets and Mixed. All 300 integer mass/acceleration/target combinations match displayed facts and answers; target bindings, exports, independent forms, scoring, progression, and Medium/Hard exclusions checked. Friction branches require applied/net-force roles, explicit surface/direction/gravity assumptions, and a separate review. See current_state.md#newtons-second-law-easy-review. Reviewed 2026-10-12. Teacher confirmed intended behavior on 2026-10-12. |

## Dynamics / Center of Mass

Route: `file:app_pages/1_2.1_Forces.py::center_of_mass` ([page](../app_pages/1_2.1_Forces.py)); minimum level: advanced.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| One Dimensional | [generator metadata](../utils/generators/forces/center_of_mass_generator.py) |  |  |
| Two Dimensional | [generator metadata](../utils/generators/forces/center_of_mass_generator.py) |  |  |

## Dynamics / Tension

Route: `file:app_pages/1_2.1_Forces.py::tension` ([page](../app_pages/1_2.1_Forces.py)); minimum level: advanced.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Suspension | [generator metadata](../utils/generators/forces/tension_generator.py) |  |  |

## Dynamics / Atwood Machines

Route: `file:app_pages/1_2.1_Forces.py::atwood` ([page](../app_pages/1_2.1_Forces.py)); minimum level: advanced.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Static Friction Half Atwood | [generator metadata](../utils/generators/forces/atwood_generator.py) |  |  |
| Frictionless Half Atwood | [generator metadata](../utils/generators/forces/atwood_generator.py) |  |  |
| Kinetic Friction Half Atwood | [generator metadata](../utils/generators/forces/atwood_generator.py) |  |  |

## Dynamics / Inclined Planes

Route: `file:app_pages/1_2.1_Forces.py::inclines` ([page](../app_pages/1_2.1_Forces.py)); minimum level: advanced.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Static Incline | [generator metadata](../utils/generators/forces/incline_generator.py) |  |  |
| Frictionless Incline | [generator metadata](../utils/generators/forces/incline_generator.py) |  |  |
| Kinetic Friction Incline | [generator metadata](../utils/generators/forces/incline_generator.py) |  |  |

## Momentum / Momentum

Route: `file:app_pages/1_4.1_Momentum_and_Impulse.py::momentum` ([page](../app_pages/1_4.1_Momentum_and_Impulse.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Momentum | [generator metadata](../utils/generators/momentum_generators/momentum.py) | Migrated; enabled | Momentum, mass, velocity profile and equation symbols connected; all three targets checked against prompt facts and page flow. Existing positive one-object values and Ns notation retained. No initial/final hint for ordinary velocity. Reviewed 2026-10-03. |

## Momentum / Impulse

Route: `file:app_pages/1_4.1_Momentum_and_Impulse.py::impulse` ([page](../app_pages/1_4.1_Momentum_and_Impulse.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Change in Momentum (Multiple Choice) | [generator metadata](../utils/generators/momentum_generators/impulse_generator.py) |  |  |
| Change in Momentum | [generator metadata](../utils/generators/momentum_generators/impulse_generator.py) |  |  |
| Impulse | [generator metadata](../utils/generators/momentum_generators/impulse_generator.py) |  |  |

## Momentum / Collisions

Route: `file:app_pages/1_4.1_Momentum_and_Impulse.py::collisions` ([page](../app_pages/1_4.1_Momentum_and_Impulse.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Inelastic Collision | [generator metadata](../utils/generators/momentum_generators/collision_generator.py) |  |  |
| Elastic Collision | [generator metadata](../utils/generators/momentum_generators/collision_generator.py) |  |  |

## Energy / Types of Energy

Route: `file:app_pages/1_6.1_Energy.py::energy_basics_page` ([page](../app_pages/1_6.1_Energy.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Elastic Potential Energy | [generator metadata](../utils/generators/energy/energy_basics.py) | Enabled; teacher checked for current scope | Shared roles, equations, target bindings, and setup metadata enabled for every existing difficulty/target branch and Mixed. Four-family review covers 11,820 sampled-value cases and 28 target/level branches, explicit assumptions, displayed precision, independent forms, feedback, resets, scoring, progression, and exports. Easy retains energy/work targets only. Intermediate-value planning and other energy activities excluded. See current_state.md#energy-basics-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |
| Kinetic Energy | [generator metadata](../utils/generators/energy/energy_basics.py) | Enabled; teacher checked for current scope | Shared roles, equations, target bindings, and setup metadata enabled for every existing difficulty/target branch and Mixed. Four-family review covers 11,820 sampled-value cases and 28 target/level branches, explicit assumptions, displayed precision, independent forms, feedback, resets, scoring, progression, and exports. Easy retains energy/work targets only. Intermediate-value planning and other energy activities excluded. See current_state.md#energy-basics-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |
| Gravitational Potential Energy | [generator metadata](../utils/generators/energy/energy_basics.py) | Enabled; teacher checked for current scope | Shared roles, equations, target bindings, and setup metadata enabled for every existing difficulty/target branch and Mixed. Four-family review covers 11,820 sampled-value cases and 28 target/level branches, explicit assumptions, displayed precision, independent forms, feedback, resets, scoring, progression, and exports. Easy retains energy/work targets only. Intermediate-value planning and other energy activities excluded. See current_state.md#energy-basics-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |
| Work | [generator metadata](../utils/generators/energy/energy_basics.py) | Enabled; teacher checked for current scope | Shared roles, equations, target bindings, and setup metadata enabled for every existing difficulty/target branch and Mixed. Four-family review covers 11,820 sampled-value cases and 28 target/level branches, explicit assumptions, displayed precision, independent forms, feedback, resets, scoring, progression, and exports. Easy retains energy/work targets only. Intermediate-value planning and other energy activities excluded. See current_state.md#energy-basics-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |

## Energy / Conservation of Energy

Route: `file:app_pages/1_6.1_Energy.py::energy_conserv_page` ([page](../app_pages/1_6.1_Energy.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Mixed | [generator metadata](../utils/generators/energy/energy_conserv.py) | Enabled; teacher checked for current scope | Equal family sampling across all three conservation conversions, followed by existing direction/target sampling. General optional equation reference; no family title or Solve for control in Mixed mode. Stage organizer retained. 360 seeded cases cover six family/direction combinations at every difficulty; exports, selector resets and final submission checked. See current_state.md#conservation-of-energy-organizer-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |
| Elastic <--> Kinetic | [generator metadata](../utils/generators/energy/energy_conserv.py) | Enabled; teacher checked for current scope | Stage-grouped givens and optional intermediate energy calculation for all difficulties, existing targets, Mixed, and both directions. 3,600 displayed-value cases cover all 60 scenario/level branches across the three families, independent physics equations, metadata, exports, checks, feedback, reset, and submission isolation. Answers use displayed facts; total vertical change includes spring compression/expansion. Thermal/friction-distance and printed organizers excluded. See current_state.md#conservation-of-energy-organizer-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |
| Gravitational <--> Kinetic | [generator metadata](../utils/generators/energy/energy_conserv.py) | Enabled; teacher checked for current scope | Stage-grouped givens and optional intermediate energy calculation for all difficulties, existing targets, Mixed, and both directions. 3,600 displayed-value cases cover all 60 scenario/level branches across the three families, independent physics equations, metadata, exports, checks, feedback, reset, and submission isolation. Answers use displayed facts; total vertical change includes spring compression/expansion. Thermal/friction-distance and printed organizers excluded. See current_state.md#conservation-of-energy-organizer-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |
| Gravitational <--> Elastic | [generator metadata](../utils/generators/energy/energy_conserv.py) | Enabled; teacher checked for current scope | Stage-grouped givens and optional intermediate energy calculation for all difficulties, existing targets, Mixed, and both directions. 3,600 displayed-value cases cover all 60 scenario/level branches across the three families, independent physics equations, metadata, exports, checks, feedback, reset, and submission isolation. Answers use displayed facts; total vertical change includes spring compression/expansion. Thermal/friction-distance and printed organizers excluded. See current_state.md#conservation-of-energy-organizer-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |

## Energy / Thermal Energy

Route: `file:app_pages/1_6.1_Energy.py::thermal_energy_page` ([page](../app_pages/1_6.1_Energy.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Mixed | [generator metadata](../utils/generators/energy/thermal_loss.py) | Enabled; teacher checked for current scope | Equal sampling of three families with existing direction/target sampling. Easy retains thermal-only questions. General optional equations; Solve for hidden. Stage organizer retained. 360 seeded cases cover all six directions at each difficulty, with Mixed exports and routed checks. See current_state.md#thermal-energy-organizer-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |
| Elastic <--> Kinetic | [generator metadata](../utils/generators/energy/thermal_loss.py) | Enabled; teacher checked for current scope | Optional stage-grouped givens and starting/ending mechanical-energy calculations; page-specific thermal/sign/model help. Positive thermal-energy labels replace misleading positive friction-work labels; IDs stable. All 58 reachable direction/target/level branches reviewed across the three families; 3,480 displayed-value cases, independent physics, explicit/Mixed target and export payloads, feedback, reset, isolated checking and final scoring passed. Invalid rounded cases resample; shared raw samplers unchanged. Friction/Distance and printed organizers excluded. See current_state.md#thermal-energy-organizer-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |
| Gravitational <--> Kinetic | [generator metadata](../utils/generators/energy/thermal_loss.py) | Enabled; teacher checked for current scope | Optional stage-grouped givens and starting/ending mechanical-energy calculations; page-specific thermal/sign/model help. Positive thermal-energy labels replace misleading positive friction-work labels; IDs stable. All 58 reachable direction/target/level branches reviewed across the three families; 3,480 displayed-value cases, independent physics, explicit/Mixed target and export payloads, feedback, reset, isolated checking and final scoring passed. Invalid rounded cases resample; shared raw samplers unchanged. Friction/Distance and printed organizers excluded. See current_state.md#thermal-energy-organizer-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |
| Gravitational <--> Elastic | [generator metadata](../utils/generators/energy/thermal_loss.py) | Enabled; teacher checked for current scope | Optional stage-grouped givens and starting/ending mechanical-energy calculations; page-specific thermal/sign/model help. Positive thermal-energy labels replace misleading positive friction-work labels; IDs stable. All 58 reachable direction/target/level branches reviewed across the three families; 3,480 displayed-value cases, independent physics, explicit/Mixed target and export payloads, feedback, reset, isolated checking and final scoring passed. Invalid rounded cases resample; shared raw samplers unchanged. Friction/Distance and printed organizers excluded. See current_state.md#thermal-energy-organizer-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |

## Energy / Friction and Distance

Route: `file:app_pages/1_6.1_Energy.py::friction_distance_page` ([page](../app_pages/1_6.1_Energy.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Elastic <--> Kinetic | [generator metadata](../utils/generators/energy/frict_and_dist.py) | Enabled; teacher checked for current scope | Stage/path-grouped givens and optional thermal/starting/ending energy calculations. Easy thermal-plus-target and Medium/Hard single-target branches retained. All 90 direction/target/level branches reviewed across three families; 3,600 displayed-fact cases, independent balances/Fd, positive domains, ramp geometry, exports, isolated checks, feedback, reset, final scoring passed. Rounded invalid candidates resample; calculated thermal precision retained. Printed organizers and wider content expansion excluded. See current_state.md#friction-and-distance-organizer-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |
| Gravitational <--> Kinetic | [generator metadata](../utils/generators/energy/frict_and_dist.py) | Enabled; teacher checked for current scope | Stage/path-grouped givens and optional thermal/starting/ending energy calculations. Easy thermal-plus-target and Medium/Hard single-target branches retained. All 90 direction/target/level branches reviewed across three families; 3,600 displayed-fact cases, independent balances/Fd, positive domains, ramp geometry, exports, isolated checks, feedback, reset, final scoring passed. Rounded invalid candidates resample; calculated thermal precision retained. Printed organizers and wider content expansion excluded. See current_state.md#friction-and-distance-organizer-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |
| Gravitational <--> Elastic | [generator metadata](../utils/generators/energy/frict_and_dist.py) | Enabled; teacher checked for current scope | Stage/path-grouped givens and optional thermal/starting/ending energy calculations. Easy thermal-plus-target and Medium/Hard single-target branches retained. All 90 direction/target/level branches reviewed across three families; 3,600 displayed-fact cases, independent balances/Fd, positive domains, ramp geometry, exports, isolated checks, feedback, reset, final scoring passed. Rounded invalid candidates resample; calculated thermal precision retained. Printed organizers and wider content expansion excluded. See current_state.md#friction-and-distance-organizer-review. Reviewed 2026-10-12. Teacher accepted the completed Energy organizer rollout on 2026-10-13. Broader content, difficulty progression, and printed organizers remain separate work. |

## ⚡Electricity⚡ / Static Electricity / Charging by Friction

Route: `file:app_pages/1_3.1_Static_Electricity.py::charging_by_friction_page` ([page](../app_pages/1_3.1_Static_Electricity.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Explorer | [custom mode/task](../app_pages/1_3.1_Static_Electricity.py) |  |  |
| Comparison Practice | [custom mode/task](../app_pages/1_3.1_Static_Electricity.py) |  |  |
| Ranking Logic Puzzle | [custom mode/task](../app_pages/1_3.1_Static_Electricity.py) |  |  |

## ⚡Electricity⚡ / Static Electricity / Charging by Conduction

Route: `file:app_pages/1_3.2_Static_Electricity_Conduction.py::charging_by_conduction_page` ([page](../app_pages/1_3.2_Static_Electricity_Conduction.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Contact charging (Easy: signs) | [custom mode/task](../app_pages/1_3.2_Static_Electricity_Conduction.py) |  |  |
| Contact charging (Medium: signs and mechanism) | [custom mode/task](../app_pages/1_3.2_Static_Electricity_Conduction.py) |  |  |
| Contact charging (Hard: signs, mechanism, and amounts) | [custom mode/task](../app_pages/1_3.2_Static_Electricity_Conduction.py) |  |  |

## ⚡Electricity⚡ / Static Electricity / Charging by Induction

Route: `file:app_pages/1_3.3_Static_Electricity_Induction.py::charging_by_induction_page` ([page](../app_pages/1_3.3_Static_Electricity_Induction.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Induction (Easy) | [custom mode/task](../app_pages/1_3.3_Static_Electricity_Induction.py) |  |  |
| Induction (Medium) | [custom mode/task](../app_pages/1_3.3_Static_Electricity_Induction.py) |  |  |
| Induction (Hard) | [custom mode/task](../app_pages/1_3.3_Static_Electricity_Induction.py) |  |  |

## ⚡Electricity⚡ / Current Electricity / Circuit Fundamentals

Route: `file:app_pages/1_3.4_Current_Electricity_Circuits.py::current_electricity_circuits_page` ([page](../app_pages/1_3.4_Current_Electricity_Circuits.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Single Resistor | [custom mode/task](../app_pages/1_3.4_Current_Electricity_Circuits.py) | Migrated; enabled; teacher review pending | Voltage/current/resistance targets at all three difficulties reviewed; 507 curated cases match displayed givens, diagram, units, setup, and answers. Shared three-role profile and custom-page payload/question-ID adapter enabled; separate forms, scoring, feedback, resets, cancellable automatic progression, and unsupported subtype checks passed. Custom messages persist across reruns. Correct calculation is optional with a five-second cancellable countdown; wrong calculation stays visible until New Question (Circuit) or settings change. Other focused relationship tasks, circuit networks, and export organizers explicitly deferred. Route renamed Circuit Fundamentals; Single Resistor scope is unchanged. See current_electricity_ohms_law.md. Updated 2026-10-12. |
| Series Current and Voltage | [custom mode/task](../app_pages/1_3.4_Current_Electricity_Circuits.py) | Enabled; teacher checked | Component-owned givens grouped by Whole circuit/R1/R2. Series Voltage Drop adds equivalent resistance and circuit current as possible in-between calculations; paired Fundamentals tasks need no intermediate section. Separate checks, feedback, reset, and final submission isolation passed at all difficulties; 720 sampled cases across the three tasks. Other network activities excluded. See current_electricity_ohms_law.md#component-organizer-preview. Reviewed 2026-10-12. |
| Parallel Current and Voltage | [custom mode/task](../app_pages/1_3.4_Current_Electricity_Circuits.py) | Enabled; teacher checked | Component-owned givens grouped by Whole circuit/R1/R2. Series Voltage Drop adds equivalent resistance and circuit current as possible in-between calculations; paired Fundamentals tasks need no intermediate section. Separate checks, feedback, reset, and final submission isolation passed at all difficulties; 720 sampled cases across the three tasks. Other network activities excluded. See current_electricity_ohms_law.md#component-organizer-preview. Reviewed 2026-10-12. |

## ⚡Electricity⚡ / Current Electricity / Series and Parallel Circuits

Route: `file:app_pages/1_3.5_Current_Electricity_Series_Parallel.py::current_electricity_series_parallel_page` ([page](../app_pages/1_3.5_Current_Electricity_Series_Parallel.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Series Equivalent Resistance | [custom mode/task](../app_pages/1_3.5_Current_Electricity_Series_Parallel.py) | Enabled; teacher review pending | Component-grouped givens and optional help at all three difficulties. Series Total Current offers equivalent resistance as an intermediate; equivalent-resistance and branch-current tasks have no unnecessary intermediate section. Seven-activity suite passes 1,680 sampled cases, 21 routed branches, independent checks, feedback, resets, and live-session recovery. Single Resistor covered separately. Broader difficulty variety and components deferred. See current_electricity_series_parallel.md. Reviewed 2026-10-12. |
| Series Total Current | [custom mode/task](../app_pages/1_3.5_Current_Electricity_Series_Parallel.py) | Enabled; teacher review pending | Component-grouped givens and optional help at all three difficulties. Series Total Current offers equivalent resistance as an intermediate; equivalent-resistance and branch-current tasks have no unnecessary intermediate section. Seven-activity suite passes 1,680 sampled cases, 21 routed branches, independent checks, feedback, resets, and live-session recovery. Single Resistor covered separately. Broader difficulty variety and components deferred. See current_electricity_series_parallel.md. Reviewed 2026-10-12. |
| Series Voltage Drop | [custom mode/task](../app_pages/1_3.5_Current_Electricity_Series_Parallel.py) | Enabled; teacher checked | Component-owned givens grouped by Whole circuit/R1/R2. Series Voltage Drop adds equivalent resistance and circuit current as possible in-between calculations; paired Fundamentals tasks need no intermediate section. Separate checks, feedback, reset, and final submission isolation passed at all difficulties; 720 sampled cases across the three tasks. Other network activities excluded. See current_electricity_ohms_law.md#component-organizer-preview. Reviewed 2026-10-12. |
| Parallel Equivalent Resistance | [custom mode/task](../app_pages/1_3.5_Current_Electricity_Series_Parallel.py) | Enabled; teacher review pending | Component-grouped givens and optional help at all three difficulties. Series Total Current offers equivalent resistance as an intermediate; equivalent-resistance and branch-current tasks have no unnecessary intermediate section. Seven-activity suite passes 1,680 sampled cases, 21 routed branches, independent checks, feedback, resets, and live-session recovery. Single Resistor covered separately. Broader difficulty variety and components deferred. See current_electricity_series_parallel.md. Reviewed 2026-10-12. |
| Parallel Branch Current | [custom mode/task](../app_pages/1_3.5_Current_Electricity_Series_Parallel.py) | Enabled; teacher review pending | Component-grouped givens and optional help at all three difficulties. Series Total Current offers equivalent resistance as an intermediate; equivalent-resistance and branch-current tasks have no unnecessary intermediate section. Seven-activity suite passes 1,680 sampled cases, 21 routed branches, independent checks, feedback, resets, and live-session recovery. Single Resistor covered separately. Broader difficulty variety and components deferred. See current_electricity_series_parallel.md. Reviewed 2026-10-12. |

## Waves / Wave Properties

Route: `file:app_pages/1_7.1_Waves.py::wave_properties` ([page](../app_pages/1_7.1_Waves.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Wave Properties | [generator metadata](../utils/generators/waves_generator.py) | Migrated; enabled; teacher checked | Eight given/target forms and four solve-for targets cover speed, wavelength, frequency, and period. Three-decimal displayed period givens drive answers; shared roles, units, equations, and setup metadata connected. 2,376 displayed-value cases and routed form/feedback/reset checks passed. Teacher confirmed new period problems and Tab/Enter work on 2026-10-12. Easy page only; harmonics/decibels and export organizers excluded. See wave_properties_review.md. |

## Waves / Harmonics

Route: `file:app_pages/1_7.1_Waves.py::Harmonics` ([page](../app_pages/1_7.1_Waves.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| String Harmonics | [generator metadata](../utils/generators/waves_generator.py) |  |  |
| Open Ended Column Harmonics | [generator metadata](../utils/generators/waves_generator.py) |  |  |
| Closed End Column Harmonics | [generator metadata](../utils/generators/waves_generator.py) |  |  |

## Waves / deciBel Scale

Route: `file:app_pages/1_7.1_Waves.py::deciBel_practice` ([page](../app_pages/1_7.1_Waves.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| deciBel Scale | [generator metadata](../utils/generators/waves_generator.py) |  |  |

## Chemistry / Compound Names Practice

Route: `file:app_pages/1_Chem-_Compound_Names.py::practice_quiz_page` ([page](../app_pages/1_Chem-_Compound_Names.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Ionic naming | [custom mode/task](../app_pages/1_Chem-_Compound_Names.py) |  |  |
| Covalent naming | [custom mode/task](../app_pages/1_Chem-_Compound_Names.py) |  |  |
| Polyatomic naming (optional) | [custom mode/task](../app_pages/1_Chem-_Compound_Names.py) |  |  |

## Chemistry / Compound Formula Explorer

Route: `file:app_pages/1_Chem-_Compound_Names.py::create_exploration_page` ([page](../app_pages/1_Chem-_Compound_Names.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Covalent Compound | [custom mode/task](../app_pages/1_Chem-_Compound_Names.py) |  |  |
| Ionic Compound (Monatomic) | [custom mode/task](../app_pages/1_Chem-_Compound_Names.py) |  |  |
| Ionic Compound (with Polyatomic Ion) | [custom mode/task](../app_pages/1_Chem-_Compound_Names.py) |  |  |

## Chemistry / Stoichiometry Practice

Route: `file:app_pages/1_Chem-_Stoichiometry.py::stoichiometry_practice_page` ([page](../app_pages/1_Chem-_Stoichiometry.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Random | [custom mode/task](../app_pages/1_Chem-_Stoichiometry.py) |  |  |
| Combustion | [custom mode/task](../app_pages/1_Chem-_Stoichiometry.py) |  |  |
| Decomposition | [custom mode/task](../app_pages/1_Chem-_Stoichiometry.py) |  |  |
| Synthesis | [custom mode/task](../app_pages/1_Chem-_Stoichiometry.py) |  |  |
| Single Replacement | [custom mode/task](../app_pages/1_Chem-_Stoichiometry.py) |  |  |
| Double Replacement | [custom mode/task](../app_pages/1_Chem-_Stoichiometry.py) |  |  |

## Chemistry / Stoichiometry Explorer

Route: `file:app_pages/1_Chem-_Stoichiometry.py::stoichiometry_explorer_page` ([page](../app_pages/1_Chem-_Stoichiometry.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Molar Mass Calculator | [custom mode/task](../app_pages/1_Chem-_Stoichiometry.py) |  |  |
| Balancing Equations | [custom mode/task](../app_pages/1_Chem-_Stoichiometry.py) |  |  |
| Limiting Reagent | [custom mode/task](../app_pages/1_Chem-_Stoichiometry.py) |  |  |

## Labs / Roulette

Route: `file:app_pages/1_0.0_Test_Page.py::roulette` ([page](../app_pages/1_0.0_Test_Page.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Simulation (no problem-type selector) | [custom mode/task](../app_pages/1_0.0_Test_Page.py) |  |  |

## Labs / Reverse Engineering

Route: `file:app_pages/1_0.0_Test_Page.py::planner_tab` ([page](../app_pages/1_0.0_Test_Page.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Planner (no problem-type selector) | [custom mode/task](../app_pages/1_0.0_Test_Page.py) |  |  |

# Organizing-help activity and problem-type inventory

Generated from the current route catalog and generator/worksheet metadata, with
explicit adapters for custom pages. **41 routes; 138 problem-type/mode rows.**

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
| Type 1 | [generator metadata](../utils/generators/kinematics/projectile_generator.py) |  |  |
| Type 2 | [generator metadata](../utils/generators/kinematics/projectile_generator.py) |  |  |
| Type 3 | [generator metadata](../utils/generators/kinematics/projectile_generator.py) |  |  |

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

## Dynamics / Newton's Second Law

Route: `file:app_pages/1_2.1_Forces.py::newtons_2nd` ([page](../app_pages/1_2.1_Forces.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Newton's Second Law | [generator metadata](../utils/generators/force_generator.py) |  |  |

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
| Elastic Potential Energy | [generator metadata](../utils/generators/energy/energy_basics.py) |  |  |
| Kinetic Energy | [generator metadata](../utils/generators/energy/energy_basics.py) |  |  |
| Gravitational Potential Energy | [generator metadata](../utils/generators/energy/energy_basics.py) |  |  |
| Work | [generator metadata](../utils/generators/energy/energy_basics.py) |  |  |

## Energy / Conservation of Energy

Route: `file:app_pages/1_6.1_Energy.py::energy_conserv_page` ([page](../app_pages/1_6.1_Energy.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Elastic <--> Kinetic | [generator metadata](../utils/generators/energy/energy_conserv.py) |  |  |
| Gravitational <--> Kinetic | [generator metadata](../utils/generators/energy/energy_conserv.py) |  |  |
| Gravitational <--> Elastic | [generator metadata](../utils/generators/energy/energy_conserv.py) |  |  |

## Energy / Thermal Energy

Route: `file:app_pages/1_6.1_Energy.py::thermal_energy_page` ([page](../app_pages/1_6.1_Energy.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Elastic <--> Kinetic | [generator metadata](../utils/generators/energy/thermal_loss.py) |  |  |
| Gravitational <--> Kinetic | [generator metadata](../utils/generators/energy/thermal_loss.py) |  |  |
| Gravitational <--> Elastic | [generator metadata](../utils/generators/energy/thermal_loss.py) |  |  |

## Energy / Friction and Distance

Route: `file:app_pages/1_6.1_Energy.py::friction_distance_page` ([page](../app_pages/1_6.1_Energy.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Elastic <--> Kinetic | [generator metadata](../utils/generators/energy/frict_and_dist.py) |  |  |
| Gravitational <--> Kinetic | [generator metadata](../utils/generators/energy/frict_and_dist.py) |  |  |
| Gravitational <--> Elastic | [generator metadata](../utils/generators/energy/frict_and_dist.py) |  |  |

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

## ⚡Electricity⚡ / Current Electricity / Circuit Ohm's Law

Route: `file:app_pages/1_3.4_Current_Electricity_Circuits.py::current_electricity_circuits_page` ([page](../app_pages/1_3.4_Current_Electricity_Circuits.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Single Resistor | [custom mode/task](../app_pages/1_3.4_Current_Electricity_Circuits.py) |  |  |
| Series Current | [custom mode/task](../app_pages/1_3.4_Current_Electricity_Circuits.py) |  |  |
| Voltage Drop | [custom mode/task](../app_pages/1_3.4_Current_Electricity_Circuits.py) |  |  |

## ⚡Electricity⚡ / Current Electricity / Series and Parallel Circuits

Route: `file:app_pages/1_3.5_Current_Electricity_Series_Parallel.py::current_electricity_series_parallel_page` ([page](../app_pages/1_3.5_Current_Electricity_Series_Parallel.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Series Equivalent Resistance | [custom mode/task](../app_pages/1_3.5_Current_Electricity_Series_Parallel.py) |  |  |
| Series Total Current | [custom mode/task](../app_pages/1_3.5_Current_Electricity_Series_Parallel.py) |  |  |
| Parallel Equivalent Resistance | [custom mode/task](../app_pages/1_3.5_Current_Electricity_Series_Parallel.py) |  |  |
| Parallel Branch Current | [custom mode/task](../app_pages/1_3.5_Current_Electricity_Series_Parallel.py) |  |  |

## Waves / Wave Properties

Route: `file:app_pages/1_7.1_Waves.py::wave_properties` ([page](../app_pages/1_7.1_Waves.py)); minimum level: high.

| Problem type / mode | Discovery source | Review | Findings / next work |
|---|---|---|---|
| Wave Properties | [generator metadata](../utils/generators/waves_generator.py) |  |  |

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

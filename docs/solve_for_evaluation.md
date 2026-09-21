# Solve-for evaluation and implementation

All 39 routed activities in `Home.py` were evaluated, including custom layouts,
chemistry, labs, and the three charging-by-friction modes. This change exposes
existing, identifiable targets; it does not redesign difficulty or invent inverses.

**Implemented** means browser controls and `DocumentGenerator.question()` use the
same declared target catalog. **Implemented partly** means only the clear subtypes
were changed. Fixed-task pages keep their current controls. Deferred decisions are
recorded separately in [solve_for_deferred.md](solve_for_deferred.md).

The shared interface is `utils/solve_for.py`. The explicit, checked-in
`utils/solve_for_catalog.json` lists labels, stable target IDs, supported levels,
and the exact existing method/arguments for every target. Listing choices never
builds a random case. Relative Motion uses named subject/reference pairs instead
of public numeric link indices. See [the readable target list](solve_for_targets.md).

## Page-by-page findings

| Activity | Status | Current code and scope | Route source |
|---|---|---|---|

| Algebra | Deferred | A randomly named symbol is isolated step by step. Choosing a symbol would mostly rename the exercise; inverse target semantics and worksheet representation need a decision. | [algebra.main](../app_pages/1_0.1.1_Math_Skills.py) |
| Scientific Notation | Fixed task | Evaluate the generated expression in scientific notation. Operation choices are not unknown-quantity choices; inverse operands would be new questions. | [sci_notate.main](../app_pages/1_0.1.1_Math_Skills.py) |
| Arithmetic | Fixed task | Sum, difference, product or quotient is already selected by Problem Type. Missing-operand questions are not implemented. | [arithmetic.main](../app_pages/1_0.1.1_Math_Skills.py) |
| Vector Practice | Fixed task | Components, resultant, or sum already selected by Problem Type; paired magnitude/direction answers stay together. Inverting individual inputs would require new prompts and diagrams. | [vectors.vector_practice](../app_pages/1_1.1.0_Vectors_and_Displacement.py) |
| Relative Motion | Implemented | Explicit result and each identifiable velocity link, named by subject and reference frame. Scenario/result restrictions remain level-specific; shared current in Combined is excluded because it cancels. | [relative_motion](../app_pages/1_1.1.4_Relative_Motion.py) |
| Distance & Displacement | Fixed task | Existing questions ask for distance, displacement and direction together. Selecting a subset or recovering a journey leg would create new variants. | [dist_disp.distance_displacement](../app_pages/1_1.1.0_Vectors_and_Displacement.py) |
| Constant Motion | Implemented partly | Constant Speed: distance, speed, time. Average speed/velocity and combined journeys retain their existing fixed answer sets. | [constant_motion](../app_pages/1_1.1.1_Motion.py) |
| Accelerated Motion | Implemented partly | All existing targets in the four omitted-variable equation types. Mixed retains its existing equation selection; a cross-equation target filter needs a policy. | [accelerated_motion](../app_pages/1_1.1.1_Motion.py) |
| Types of Motion Graphs | Fixed task | Existing answers are direction and motion state together. Choosing graph family is a content option, not solve-for. | [motion_graph_types](../app_pages/1_1.1.1_Motion.py) |
| Matching Motion Graphs | Fixed task | Choose the matching graph; the existing position-first/velocity-first control already selects direction. No numerical inverse target is defined. | [motion_graph_matching](../app_pages/1_1.1.1_Motion.py) |
| Projectiles | Implemented | Type 1 and Type 2 existing single/multipart targets; Type 3 explicit off-cliff/onto-cliff target pairs. Type 2 Easy remains its fixed range-and-height pair. | [projectiles](../app_pages/1_1.1.1_Motion.py) |
| Rotational Kinematics | Implemented partly | All existing targets for the four omitted-variable equation types, retaining level-specific unit conversions. Mixed stays unchanged. | [rotational_kinematics](../app_pages/1_1.1.2_Rotational_Motion.py) |
| Torque | Fixed task | Perpendicular/angled/net problems currently solve torque only; comparison/ranking have fixed qualitative answers. Force, lever arm and angle inverses need new prompts and masked diagrams. | [torque_activity](../app_pages/1_1.1.3_Torque.py) |
| Newton's Second Law | Implemented | Easy: acceleration, net force, mass. Medium/Hard: existing pairs of net force with coefficient, acceleration, or applied force. | [newtons_2nd](../app_pages/1_2.1_Forces.py) |
| Center of Mass | Fixed task | Compute center coordinates from supplied masses/positions. Recovering a mass or position is not an existing prompt branch. | [center_of_mass](../app_pages/1_2.1_Forces.py) |
| Tension | Fixed task | Solve both wire tensions from geometry/load. Inverting mass or angle would require new feasibility rules and diagrams. | [tension](../app_pages/1_2.1_Forces.py) |
| Atwood Machines | Implemented | Existing static/frictionless single targets and all ten kinetic target pairs. Calls preserve existing prompt/given variants and diagram context. | [atwood](../app_pages/1_2.1_Forces.py) |
| Inclined Planes | Implemented | Maximum static angle/minimum static coefficient, frictionless angle/acceleration, kinetic acceleration/coefficient. No extra inverse angle branch introduced. | [inclines](../app_pages/1_2.1_Forces.py) |
| Momentum | Implemented | Momentum, mass, velocity; existing leaf method exposed through shared request. | [momentum](../app_pages/1_4.1_Momentum_and_Impulse.py) |
| Impulse | Implemented partly | Every existing numeric Impulse and Change in Momentum target at its supported level. Multiple-choice activity retains its fixed answer task. | [impulse](../app_pages/1_4.1_Momentum_and_Impulse.py) |
| Collisions | Fixed task | Current elastic problem asks for the second final velocity; inelastic asks for combined final velocity. Other inverses require explicit givens/solvability choices. | [collisions](../app_pages/1_4.1_Momentum_and_Impulse.py) |
| Types of Energy | Implemented | Existing energy/work, distance/height/compression/speed, mass/force/spring-strength branches. Easy retains its forward-only restriction. | [energy_basics_page](../app_pages/1_6.1_Energy.py) |
| Conservation of Energy | Implemented | Existing velocity/height/mass/compression/spring-strength targets. Alternative existing scenarios with the same target remain mixed within that target. | [energy_conserv_page](../app_pages/1_6.1_Energy.py) |
| Thermal Energy | Implemented | Existing loss and inverse quantity branches, with conversion direction named in the choice. Easy still asks for thermal loss. | [thermal_energy_page](../app_pages/1_6.1_Energy.py) |
| Friction and Distance | Implemented | Existing target pairs on Easy and single targets on higher levels; conversion direction is explicit. No split of required multipart answers. | [friction_distance_page](../app_pages/1_6.1_Energy.py) |
| Charging by Friction | Deferred | Evaluated all modes: Explorer changes materials; Comparison predicts charge signs; Ranking orders materials from clues. Selecting which inference to ask needs a pedagogical choice. | [charging_by_friction_page](../app_pages/1_3.1_Static_Electricity.py) |
| Charging by Conduction | Fixed task | Final charge signs, mechanism, and level-dependent amounts form the existing task. No inverse initial-charge branches exist. | [charging_by_conduction_page](../app_pages/1_3.2_Static_Electricity_Conduction.py) |
| Charging by Induction | Deferred | Signs/mechanism/amounts depend on the classroom charge-chunk model and event sequence. Inverse starting states may be nonunique; do not expose invented inverses. | [charging_by_induction_page](../app_pages/1_3.3_Static_Electricity_Induction.py) |
| Circuit Ohm's Law | Implemented partly | Single Resistor: voltage, current, resistance; same masked schematic for browser/export. Series Current and Voltage Drop remain their fixed existing tasks. | [current_electricity_circuits_page](../app_pages/1_3.4_Current_Electricity_Circuits.py) |
| Series and Parallel Circuits | Fixed task | Problem Type already selects equivalent resistance, total current, or branch current. Inverse component/source values are not implemented. | [current_electricity_series_parallel_page](../app_pages/1_3.5_Current_Electricity_Series_Parallel.py) |
| Wave Properties | Implemented | Wave speed, wavelength, frequency from the existing three branches. | [wave_properties](../app_pages/1_7.1_Waves.py) |
| Harmonics | Implemented | Existing fundamental wavelength/frequency/length, higher-level harmonic sets and paired inverse answers for strings/open/closed columns. Required answer sets are retained. | [Harmonics](../app_pages/1_7.1_Waves.py) |
| deciBel Scale | Deferred | Reachable questions solve sound level. A distance-ratio else branch is unreachable and has unclear/incorrect answer semantics; it is not exposed. | [deciBel_practice](../app_pages/1_7.1_Waves.py) |
| Compound Names Practice | Fixed task | Formula-to-name only; compound-family selection differs from target selection. Name-to-formula needs a formula-aware grading contract. | [practice_quiz_page](../app_pages/1_Chem-_Compound_Names.py) |
| Compound Formula Explorer | Not a question generator | Interactive construction from selected elements/charges. Already configurable, with no hidden random unknown to expose. | [create_exploration_page](../app_pages/1_Chem-_Compound_Names.py) |
| Stoichiometry Practice | Implemented partly | Medium: product moles from reactant mass or product mass from reactant moles. Easy/Hard keep fixed output modes. Specific species and inverse reactant targets remain deferred. | [stoichiometry_practice_page](../app_pages/1_Chem-_Stoichiometry.py) |
| Stoichiometry Explorer | Not a question generator | Manual balancing/conversion/limiting-reagent tools already take user inputs. No common random-question target API to expose. | [stoichiometry_explorer_page](../app_pages/1_Chem-_Stoichiometry.py) |
| Roulette | Not a question generator | Simulation inputs and statistics; no physics solve-for task. | [roulette](../app_pages/1_0.0_Test_Page.py) |
| Reverse Engineering | Not a question generator | Planner already targets a probability/profit constraint. Turning planner outputs into worksheet unknowns is separate design work. | [planner_tab](../app_pages/1_0.0_Test_Page.py) |

## Website lifecycle and compatibility

Targets refresh after changing type or difficulty. An unavailable selection resets
to Mixed practice; a single available target needs no dropdown. Target changes
produce a fresh question and clear its submission state. New Question and automatic
advancement preserve the selected target. Existing progress IDs and difficulty-based
star awards remain unchanged; target-level performance analytics are not added.

Mixed practice retains the old generator sampling behavior. Existing direct leaf
calls and old worksheet presets remain supported. Internal numeric `variant` inputs
are adapter details; callers should use validated target IDs through the shared API.
Unsupported type/level/target combinations fail before question generation.

## Worksheet usage

Run from the repository root. This uses the real exporter, not a separate renderer:

```python
from utils.generators.kinematics.relative_motion_generator import RelativeMotionGenerator
from xtrct_docs.payload_adapter import DocumentGenerator
from xtrct_docs.document_creator import create_doc

doc_generator = DocumentGenerator(RelativeMotionGenerator())
for option in doc_generator.targets("Nested reference frames", "Hard"):
    print(option["id"], option["label"])

# An explicit target, independent of the random numbers in the generated case.
recipe = doc_generator.section(
    "Walkway velocity practice", "Nested reference frames", "Hard",
    solve_for="selected-question.moving-walkway-velocity-relative-to-boat",
    count=8,
)
create_doc("Relative motion", recipe, 2,
           output_path="relative_motion_targets.docx", open_document=False)
```

Alternatively use `Org.solve_for_practice(generator, problem_type, difficulty,
solve_for, count)` as `question_generator` in `xtrct_docs/doc_face.py`. Each version
calls the factory again, producing fresh questions. Diagrams retain problem type,
difficulty, and masked unknowns. Existing presets are not silently retargeted.

For circuit worksheets, pass `OhmsLawTargets()` from `utils.solve_for_custom`.
For stoichiometry, pass `StoichiometryTargets(generate_stoichiometry_problem,
reaction_type)` using the existing page's factory; it converts the legacy tuple
into the shared document payload. A supported target does not imply every custom
activity has been converted into a worksheet generator.

## Verification

Local results: all seven guardrail scripts passed; all 39 routed activities loaded
without AppTest exceptions. The target sweep covered 522 supported combinations
with five seeds each and Word serialization, plus separate stoichiometry conversion
and custom-page lifecycle checks. The original 4,200-payload guardrail also passed.
Harmonic prompts now state the existing 343 m/s wave-speed assumption needed for
their frequency inverses; an uphill-motion velocity label was corrected to initial
velocity. No new inverse equations or difficulty tiers were introduced.

Every file in `app_pages` is represented by these routes or their shared helpers.
Unrouted fractal/chaos demonstration functions in the lab module are interactive
visualizations rather than question factories and received no solve-for controls.

`python tools/test_solve_for.py` sweeps every declared generator target at every
supported difficulty over five seeds, validates payloads, compares direct and
export requests, serializes target worksheets, verifies withheld Relative Motion
and Ohm's-law givens, and exercises selector state. The inventory coverage test
requires a row for every routed activity. The Relative Motion interaction suite
now visits each declared target, not just the three old broad categories.

Automated serialization is not a visual certification of Word pagination. Existing
human layout review remains useful, particularly for longer target labels.

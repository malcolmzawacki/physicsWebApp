# Solve-for decisions intentionally deferred

These cases were evaluated and left unimplemented. See the complete
[39-activity evaluation](solve_for_evaluation.md) for both implemented and fixed
tasks. Absence of a dropdown does not mean a page was overlooked.

| Area | Why it is not a straightforward target exposure | Decision needed |
|---|---|---|
| Algebra | The generator chooses symbol names and then builds an equation around the target. Choosing a letter mostly changes notation; it does not select a different physical unknown. The UI grades a sequence of transformations. | Whether control should select equation structure, variable role, or just notation; how a worksheet represents the task. |
| Accelerated/rotational Mixed | An individual equation has explicit targets, but Mixed chooses among equations and has additional difficulty handling. | Whether choosing a target filters equations, chooses them uniformly, or preserves existing weights. Specific equation types are implemented now. |
| Charging by Friction | Explorer, sign comparison, and material ranking are distinct tasks, not reversible numeric formulas. | Which inference or answer subset should be selectable, if any. |
| Charging by Induction | Signs, mechanisms, and amounts depend on the event sequence and the declared charge-chunk classroom model. Multiple initial states can yield the same final state. | Define physically/model-identifiable inverses and their givens before exposing them. |
| deciBel Scale | Current random selection only reaches sound-level questions. An unreachable distance branch returns an exponent-like value rather than a clearly specified distance factor. | Specify and validate a distance-ratio problem, its logarithmic conventions, units, and wording. Do not expose this dead branch as working functionality. |
| Stoichiometry species selection | Medium conversion direction is explicit and implemented. Reactant/product identities depend on a generated reaction; not every species pair can be treated as interchangeable. | Decide whether reaction generation precedes species selection, which reaction families are valid, and which inverse/limiting-reagent targets are intended. |
| Compound naming inversion | Existing quiz expects a name for a formula. Formula construction exists in the explorer, but formula-answer grading is not the quiz's string-name grading contract. | Define accepted formula notation, equivalent forms, and charge/subscript handling before a name-to-formula quiz. |

## Fixed answer sets that should not acquire invented inverses

- Scientific notation and arithmetic evaluate expressions. Operation controls and
  missing-operand tasks are different designs.
- Vector, distance/displacement, average/combined motion, center-of-mass, tension,
  and collision activities have explicit current outputs but no alternate inverse
  prompt branches to expose. Splitting multipart answers also changes the task.
- Torque computes torque or compares/ranks it. Force/radius/angle inverses require
  new solvability constraints and diagrams that hide those values.
- Graph analysis and matching have fixed qualitative answers. Graph-family and
  distractor controls belong to content/complexity settings.
- Conduction asks for final signs/mechanism/amounts; inverse initial charges are not
  already implemented.
- Series/parallel circuit targets are already represented by problem types. New
  unknown component/source values require additional prompt/diagram variants.
- Impulse multiple choice retains its current task. Changing which quantity the
  student chooses requires new distractors, not just a target label.

## Explorers and labs

Compound Formula Explorer, Stoichiometry Explorer, Roulette, and Reverse Engineering
already have domain-specific inputs and outputs. Converting these tools into random
worksheet questions is separate work; no solve-for mechanism was imposed on them.

Difficulty definitions, star calibration, target-level progress analytics, and
cross-equation selection policies are deliberately outside this implementation.

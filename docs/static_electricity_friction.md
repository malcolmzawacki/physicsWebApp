# Charging by Friction Scope

_Created: 2026-03-15_

This note defines the first-pass content model for the charging-by-friction subpage so later UI and generator work can share one consistent set of assumptions.

## Instructional Goal

Students should be able to use a simplified triboelectric series to predict the outcome when two materials are rubbed together:

- the material higher on the classroom reference list tends to lose electrons
- the material lower on the classroom reference list tends to gain electrons
- the electron-losing material becomes positive
- the electron-gaining material becomes negative

## Initial Scope

The first version of the charging-by-friction page should focus on insulating materials and a simplified ranking model.

Included:

- a reusable ordered list of common classroom-friendly materials
- pairwise outcome prediction for two selected materials
- direct-comparison practice with a displayed reference series
- anonymous ranking logic puzzles built from the same hidden order

Deferred for later pages or follow-up revisions:

- microscopic explanation of electron energy states beyond a classroom model
- conductor-specific charge redistribution while rubbing
- humidity, contamination, surface area, pressure, and other real-world exceptions
- quantitative charge magnitude
- grounding, induction, conduction, and polarization interactions

## Modeling Assumptions

- The ranking is a simplified classroom triboelectric series, not a laboratory-precision database.
- If two identical materials are rubbed together, the model treats the result as no reliable net charging outcome.
- If two materials are adjacent or close in the ranking, the page may still show a deterministic outcome, but later activities can describe the transfer as weaker or less dramatic.
- The same ordered material data should drive the explorer, comparison questions, and logic puzzles.

## Initial Material Set

Ordered from more likely to become positive to more likely to become negative:

1. Glass
2. Human hair
3. Nylon
4. Wool
5. Silk
6. Paper
7. Cotton
8. Wood
9. Amber
10. Polyester
11. Styrofoam
12. Teflon

## Shared Data Requirements

The reusable triboelectric data module should live alongside future static-electricity generators under `utils/generators/static_electricity/` and should provide:

- the ordered material records
- display labels and optional short descriptions
- helper lookup by key
- pairwise comparison helpers
- a charge-outcome helper returning which material becomes positive and negative
- a default subset for short classroom reference charts if a smaller series is needed later

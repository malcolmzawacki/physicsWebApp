# Shared question controls

Edit `utils/layout_config.py` to tune the question rows across the standard
generator pages, Relative Motion, current-electricity pages, and Stoichiometry
Practice. No solve-for labels or available targets were changed in this update.

| Setting | Default | Purpose |
|---|---:|---|
| `PROBLEM_TYPE_WIDTH` | 3 | Problem type (reaction type in Stoichiometry) |
| `DIFFICULTY_WIDTH` | 1.2 | Difficulty selector |
| `SOLVE_FOR_WIDTH` | 4 | Solve-for selector when available |
| `CONTROL_GAP` | `"small"` | Space between columns |
| `EQUATION_EXPANDER_WIDTH` | 5 | Equation expander share on its own row |
| `EQUATION_TOGGLE_WIDTH` | 1.5 | More Equations checkbox share |

Widths are relative shares of the available row, not pixels. Increase only
`DIFFICULTY_WIDTH` to give Medium more room; the other columns surrender space
proportionally. Streamlit controls narrow-screen stacking; these settings do not
guarantee a particular minimum width or prevent long labels being truncated.

The control order is Problem Type, Difficulty, Solve for. A missing solve-for
selector leaves that position empty, preserving consistent column proportions.
Current-electricity type/difficulty radios are now dropdowns to fit the same row.
This changes presentation, not circuit content or targets.

More Equations sits to the right of the equation expander on a separate full-width
row. It keeps the existing widget key and updates the displayed equation set on
the same rerun without generating a new question. Equations remain hidden on pages
that already disable them. Matching graph layout is unchanged.

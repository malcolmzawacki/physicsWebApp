# Activity Page Conventions

_Created: 2026-04-02_

This note captures the stable UI conventions that should carry across activity pages, even when the exact layout changes to fit a custom interaction.

The goal is to preserve the student experience established by the older generator-driven pages while allowing newer custom pages to use more specialized layouts.

## Core Principle

Layout can vary. Core behaviors should not vary without an explicit reason.

In practice, this means:

- a page may use the shared `Interface` flow or a custom Streamlit layout
- but the page should still preserve the app's equation handling, scoring, feedback, performance tracking, and general interaction rhythm

## Non-Negotiable Behaviors

Unless a page has a strong instructional reason to do otherwise, future implementations should preserve all of the following.

### 1. LaTeX Equations

- Equations should be rendered with Streamlit LaTeX, not plain markdown code formatting.
- Use `st.latex(...)` directly or route through `utils.ui_components.show_equations_expander(...)`.
- Pages should not fall back to inline monospace equations unless there is a temporary technical limitation.

Why:

- students are already used to the visual clarity of LaTeX in older units
- the older kinematics, forces, energy, and waves pages consistently present equations in LaTeX form

### 2. Two Equation Levels

- Pages should support two equation views:
  - base/algebraic formula view
  - expanded non-algebraic / rearranged view
- The current UI label for this toggle is `More Equations`.
- New custom pages should preserve this distinction even if the equations are placed differently than in the older shared layout.

Interpretation:

- the simpler view should show the main governing relationship
- the expanded view should show the rearranged forms students at that level are allowed to use directly

### 3. Stars For Correct Answers

- Correct answers should award stars.
- Stars should be visible in the page header when the page structure supports it.
- If a custom page does not currently use the shared header helpers, it should still preserve the underlying star mechanic or intentionally replace it with an equivalent system.

Why:

- this is a recurring part of the app's student-facing identity
- older students have noticed when stars are missing

### 4. Performance Tracking

- Pages should track attempts and correct responses by problem type and difficulty.
- The student should be able to inspect performance without leaving the page.
- Reuse `init_performance`, `record_performance`, `build_performance_table`, and `performance_expander` when possible.

### 5. Stable Rerender / Submission Behavior

- Submission flows should not require double-clicking.
- Prefer `st.form(...)` with `st.form_submit_button(...)` for text-input answer submission.
- Custom pages should explicitly manage `submitted`, `last_result`, and reruns in the same way the newer static electricity pages do.

### 6. Immediate Feedback

- After submission, pages should clearly show:
  - whether the answer was correct
  - the correct answer when appropriate
  - a short explanation or worked reasoning
- Correct responses may auto-advance, but only after feedback is visible briefly.

### 7. Namespaced Session State

- All custom pages should use `utils.ui_state.State`.
- Keys should be namespaced by page/activity prefix to avoid collisions across activities.

## Strong Default Patterns

These are not absolute requirements, but future implementations should start here unless the activity demands something else.

### 1. Lazy Imports In Page Entrypoints

- Older pages consistently lazy-import generators inside the activity function.
- Continue doing this for cold-start performance and router responsiveness.

### 2. Difficulty Structure

- Use the standard `Easy`, `Medium`, `Hard` progression when it fits the content.
- If a page deviates, it should do so intentionally and clearly.

### 3. Shared Generator Metadata

- Generators should expose equation metadata through `stored_metadata()` when possible.
- For custom pages that are not built around a `BaseGenerator`, provide an equivalent fallback metadata dict.

Recommended metadata shape:

- `honors`: the compact/base equation set
- `conceptual`: the rearranged or student-scaffolded set

### 4. Side-By-Side Layout For Diagram-Dependent Tasks

- When students need to repeatedly reference a diagram, keep the diagram visible beside the prompt.
- Avoid designs that force scrolling back and forth between the diagram and the answer area.

### 5. Compact Left Column

- In side-by-side pages, the left column should prioritize the most instructionally necessary material:
  - diagram
  - givens
  - equations
- Optional extras such as symbol legends, long notes, or reference prose should be removable if they create scrolling friction.

## Common Patterns Found In Older Pages

The older kinematics, forces, energy, and waves pages reveal a consistent backbone:

- Page entrypoint creates a generator, title, prefix, metadata, and difficulty list.
- Shared UI handles:
  - problem type selection
  - difficulty selection
  - equation toggle
  - LaTeX equation rendering
  - star display and awarding
  - performance table
  - answer validation
  - auto-advance after correct answers

This means future custom pages should not improvise those mechanics unless the activity type truly requires a different rule.

## When Custom Layouts Are Appropriate

Custom layouts are appropriate when:

- diagrams must remain visible during answer entry
- the activity uses unusual widgets or multi-part visual states
- the shared `Interface` layout creates too much scrolling or hides essential references

When using a custom layout, the page should still preserve the non-negotiable behaviors listed above.

## Recommended Checklist For New Pages

Before considering a new page complete, check:

1. Does it use LaTeX equations?
2. Does it support both base and expanded equation views?
3. Does it award stars for correct answers?
4. Does it track performance by difficulty/problem type?
5. Does it avoid double-click submission issues?
6. Does it keep diagrams visible when students need them?
7. Does it use namespaced `State` session keys?

## Current Gap To Watch

The newer current electricity custom pages improved layout clarity, but they initially drifted away from:

- LaTeX equation rendering
- the algebraic vs non-algebraic equation distinction
- star-based gamification

Future implementations should treat those as baseline expectations, not optional embellishments.

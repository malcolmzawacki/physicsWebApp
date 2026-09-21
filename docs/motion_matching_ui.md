# Matching motion graphs

The matching page uses clickable graph cards. Click a graph (or focus it with
Tab and press Space/Enter), then use **Check Match** to submit. Selection alone
does not score an attempt. After submission, choices lock and the correct
answer is labeled as well as outlined. Correct answers retain the existing
pauseable automatic advance.

**Graph layout** offers two views without changing the question or selection:

- **Options in a column** (default): a nearly square reference on the left,
  A/B/C stacked in a narrower column on the right. Column widths have a 1.65:1
  ratio; images retain their natural proportions instead of fixed-height padding.
- **Compact grid**: reference and A above B and C.

Below 550 pixels of available board width, both views become a single column
to keep axes readable. This is the component's width, not the whole screen;
an open sidebar reduces available space. The column view deliberately trades
vertical space for a larger reference graph. Neither view guarantees that all
graphs fit above the fold on a Chromebook.

## Implementation

- `utils/graph_cards.py` encodes each question's figures once and validates
  returned selection events against the current question ID.
- `utils/graph_cards_frontend/index.html` is a local Streamlit components-v1
  frontend with native buttons, visible focus/selection states, and automatic
  iframe sizing. It needs no external scripts, new dependency, or build step.
- `utils/layouts/diagram_match_layout.py` owns selection, grading and advancement.
  Correct-answer metadata is sent to the component only after submission.
- Graph figures remain in the payload for the document exporter. Closing their
  pyplot managers after image encoding does not prevent figure export.

The frontend follows the [Streamlit components-v1 protocol](https://docs.streamlit.io/develop/concepts/custom-components/components-v1/intro).
Sizing is controlled by the CSS in the frontend, independently of the shared
problem-type/difficulty/solve-for control widths.

## Verification and limits

Browser checks at 1366 x 768 and 800 x 768 covered rendering, pointer selection,
Tab/Space selection, layout switching, submission locking, correct-answer
marking and resetting the set. Regression tests cover stale/malformed events,
selection without submission, preserved selection across views, locked answers,
single scoring, question resets, and worksheet diagram export.

The cards support keyboard interaction, but generic image alt text does not
provide a complete nonvisual equivalent of the plotted motion. A full accessible
graph-description activity remains separate work. This change retains the
existing qualitative graph families and scoring rules.

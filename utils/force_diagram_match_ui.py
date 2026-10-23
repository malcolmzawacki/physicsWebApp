"""C5 diagram selection with explicit checks and retryable conceptual practice."""
import base64
import random

import streamlit as st

from utils.activity_flow import next_question_countdown
from utils.force_activity_ui import question_title, separate_assumptions
from utils.force_diagram_match import (
    CASE_BY_ID, available_cases, describe_diagram, diagram_matches,
    make_options, render_force_diagram, SHORT_LABELS,
)
from utils.recognizing_forces import PRACTICE_SETS
from utils.graph_cards import graph_cards, selected_index
from utils.session_progress import record_answer
from utils.force_activity_ui import force_activity_header as render_header
from utils.ui_state import State


@st.cache_data(show_spinner=False)
def diagram_image(arrows):
    """Cache the larger, readable force-diagram artwork."""
    return render_force_diagram(arrows)


def render_force_diagram_match():
    state = State("force_diagram_match")
    state.ensure("records", [])
    state.ensure("question_id", 0)

    def start(case_id):
        if state.has("attempt"):
            state.set("records", [*state.get("records"), state.get("attempt")])
        state.inc("question_id")
        state.set("attempt", {"case_id": case_id, "options": make_options(CASE_BY_ID[case_id]),
                              "checks": [], "selection": None, "hint_used": False,
                              "completed": False, "outcome": None})

    def fresh(context):
        ids = [c.id for c in available_cases(context)]
        remaining = [i for i in ids if i not in state.get("seen", [])]
        if not remaining:
            remaining = [i for i in ids if i != state.get("attempt", {}).get("case_id")]
            state.set("seen", [])
        case_id = random.choice(remaining)
        state.set("seen", [*state.get("seen", []), case_id])
        start(case_id)

    records = [*state.get("records"), state.get("attempt", {})]
    render_header("Match the Free-Body Diagram", sum(bool(r.get("completed")) for r in records))
    with st.sidebar.expander("Practice settings"):
        context = st.selectbox("Practice contexts", PRACTICE_SETS, key=state.key("context"))
    if state.get("active_context") != context or not state.has("attempt"):
        state.set("active_context", context)
        state.set("seen", [])
        fresh(context)
    attempt = state.get("attempt")
    case = CASE_BY_ID[attempt["case_id"]]
    qid = state.get("question_id")
    prompt, assumptions = separate_assumptions(case.prompt)
    question_title(case.scenario.title,
                   "Arrow direction shows force direction. Compare opposing lengths along the same axis; no exact numerical ratios are implied.",
                   "Select one diagram, then use Check diagram to submit it.", assumptions)
    st.write(prompt)
    st.markdown(f"Which diagram shows the forces on **{case.scenario.target}**?")
    if attempt["hint_used"]:
        st.info(case.scenario.hint + " Think about which way each interaction acts and whether opposing forces balance.")

    letters = "ABCD"
    images = ["data:image/png;base64," + base64.b64encode(diagram_image(option["arrows"])).decode("ascii")
              for option in attempt["options"]]
    correct_index = next(i for i, option in enumerate(attempt["options"])
                         if diagram_matches(case, option["arrows"]))
    event = graph_cards(images, list(letters), qid, attempt["selection"],
                        attempt["completed"], "Four across", key=state.key(f"cards_{qid}"),
                        correct_index=correct_index, has_reference=False,
                        option_name="Diagram", check_label="Check diagram",
                        captions=[" · ".join(SHORT_LABELS[a.force] + " " +
                                  {"up":"↑", "down":"↓", "left":"←", "right":"→"}[a.direction]
                                  for a in o["arrows"]) or "No forces" for o in attempt["options"]],
                        descriptions=[describe_diagram(o["arrows"]) for o in attempt["options"]])
    index = selected_index(event, qid, len(attempt["options"]))
    if not attempt["completed"] and index is not None and index != attempt["selection"]:
        attempt["selection"] = index
        state.set("attempt", attempt)
        st.rerun()
    with st.expander("Text descriptions of diagrams"):
        for letter, option in zip(letters, attempt["options"]):
            st.write(f"**{letter}:** {describe_diagram(option['arrows'])}")

    selected = attempt["selection"]
    with st.form(state.key(f"form_{qid}")):
        check_col, hint_col = st.columns(2)
        with check_col:
            checked = st.form_submit_button("Check diagram", type="primary", width="stretch",
                                           disabled=attempt["completed"])
        with hint_col:
            hinted = st.form_submit_button("Show interaction hint", width="stretch",
                                          disabled=attempt["completed"])
    if hinted:
        attempt["hint_used"] = True
        attempt["selection"] = selected
        state.set("attempt", attempt)
        st.rerun()
    if checked and selected is None:
        st.warning("Choose a diagram before checking.")
    elif checked and not attempt["completed"]:
        attempt["selection"] = selected
        if not attempt["checks"] or attempt["checks"][-1]["selection"] != selected:
            correct = diagram_matches(case, attempt["options"][selected]["arrows"])
            attempt["checks"].append({"selection": selected, "correct": correct})
            if correct:
                attempt["completed"] = True
                attempt["outcome"] = ("Completed with help" if attempt["hint_used"] else
                                      "First try" if len(attempt["checks"]) == 1 else "Corrected after feedback")
            record_answer("Match the Free-Body Diagram", case.prompt + " Forces on: " + case.scenario.target,
                          describe_diagram(attempt["options"][selected]["arrows"]),
                          describe_diagram(case.arrows), correct, explanation=case.explanation,
                          diagrams={label: "data:image/png;base64," + base64.b64encode(diagram_image(arrows)).decode("ascii")
                                    for label, arrows in (("Your diagram", attempt["options"][selected]["arrows"]),
                                                          ("Correct diagram", case.arrows))})
        state.set("attempt", attempt)
        st.rerun()

    if attempt["checks"]:
        last = attempt["checks"][-1]
        st.caption(f"Feedback for your last check: Diagram {letters[last['selection']]}. Check again after revising.")
        if last["correct"]:
            st.success("Correct — that diagram matches the situation. ⭐")
        else:
            st.warning("That diagram does not match yet. Revise your choice and check again.")
        st.write(attempt["options"][last["selection"]]["feedback"])

    def next_question():
        if state.get("question_id") == qid:
            fresh(context)

    def related():
        if state.get("question_id") == qid:
            related_id = case.scenario.related
            if related_id not in CASE_BY_ID:
                related_id = next(c.id for c in available_cases(case.scenario.context) if c.id != case.id)
            start(related_id)
            state.set("seen", [*state.get("seen", []), related_id])

    left, right = st.columns(2)
    with left:
        st.button("Next question" if attempt["completed"] else "Skip question",
                  key=state.key(f"next_{qid}"), on_click=next_question, width="stretch")
    with right:
        st.button("Try a related case", key=state.key(f"related_{qid}"), on_click=related, width="stretch")
    with st.expander("Your Performance"):
        st.caption("This session only. One star per completed case; repeated checks of the same choice do not add attempts.")
        st.dataframe([{"Case": CASE_BY_ID[r["case_id"]].scenario.title,
                       "Checks": len(r["checks"]), "Hint used": r["hint_used"],
                       "Result": r["outcome"] or ("In progress" if r is attempt else "Skipped")}
                      for r in [*state.get("records"), attempt]], hide_index=True, width="stretch")

        def reset():
            state.set("records", [])
            state.pop("attempt")
            state.pop("active_context")
            state.set("seen", [])
        st.button("Reset practice", key=state.key("reset"), on_click=reset)
    if attempt["completed"]:
        def advance():
            next_question()
            st.rerun()
        next_question_countdown(state, qid, advance, seconds=5)

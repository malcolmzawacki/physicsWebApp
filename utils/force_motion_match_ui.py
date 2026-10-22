"""C2 multiple-answer motion matching, independent of numerical scoring flows."""
import base64
import random

import streamlit as st

from utils.activity_flow import next_question_countdown
from utils.force_diagram_match_ui import diagram_image
from utils.force_motion_match import (
    CASE_BY_ID, PRACTICE_SETS, available_cases, compatible, explanation,
    new_attempt, render_motion, submit_attempt,
)
from utils.graph_cards import graph_cards, selected_indices
from utils.session_progress import record_answer
from utils.ui_components import render_header
from utils.ui_state import State


@st.cache_data(show_spinner=False)
def motion_image(motion, axis):
    return render_motion(motion, axis)


def data_url(png):
    return "data:image/png;base64," + base64.b64encode(png).decode("ascii")


def render_force_motion_match():
    state = State("force_motion_match")
    state.ensure("records", [])
    state.ensure("question_id", 0)

    def start(case_id):
        if state.has("attempt"):
            state.set("records", [*state.get("records"), state.get("attempt")])
        state.inc("question_id")
        state.set("attempt", new_attempt(case_id))

    def fresh(context):
        ids = [c.id for c in available_cases(context)]
        remaining = [i for i in ids if i not in state.get("seen", [])]
        if not remaining:
            remaining = [i for i in ids if i != state.get("attempt", {}).get("case_id")]
            state.set("seen", [])
        case_id = random.choice(remaining)
        state.set("seen", [*state.get("seen", []), case_id])
        start(case_id)

    render_header("Force and Motion Matching", sum(bool(r.get("completed")) for r in [*state.get("records"), state.get("attempt", {})]))
    st.write("**Check all that apply.** Select every motion that could go with the force diagram. More than one answer can be correct.")
    context = st.selectbox("Practice situations", PRACTICE_SETS, key=state.key("context"))
    if state.get("active_context") != context or not state.has("attempt") or len(state.get("attempt", {}).get("options", [])) != 4:
        state.set("active_context", context)
        state.set("seen", [])
        fresh(context)
    attempt = state.get("attempt")
    case = CASE_BY_ID[attempt["case_id"]]
    qid = state.get("question_id")
    reference, question = st.columns([1, 3])
    with reference:
        st.markdown("**Initial forces**")
        st.image(diagram_image(case.arrows), width="stretch")
    with question:
        st.markdown(f"**{case.title}**")
        st.write(case.prompt)
        st.caption("The shown forces stay constant throughout each possible motion. Consider the named object only. The diagrams are qualitative; exact force and acceleration magnitudes are not supplied.")
        st.info(f"Compare {'horizontal' if case.axis == 'horizontal' else 'vertical'} motion. The initial direction of motion is unknown.")
    if attempt["hint_used"]:
        st.info("First compare opposing forces. Net force determines acceleration; the velocity may point either way. Equal-time dot gaps grow when speed increases and shrink when speed decreases.")
    st.caption("Dots 1–4 mark equal time steps. Read them in numbered order. Each card has its own schematic scale; compare how gaps change within a card.")
    letters = "ABCD"
    images = [data_url(motion_image(m, case.axis)) for m in attempt["options"]]
    expected = tuple(i for i, m in enumerate(attempt["options"]) if compatible(case, m))
    event = graph_cards(images, list(letters), qid, list(attempt["selection"]), attempt["completed"],
                        "Four across", key=state.key(f"cards_{qid}"), has_reference=False,
                        option_name="Motion", check_label="Check motions", multi_select=True,
                        correct_indices=expected, captions=[m.description(case.axis) for m in attempt["options"]], descriptions=[m.description(case.axis) for m in attempt["options"]])
    indices = selected_indices(event, qid, len(images))
    if not attempt["completed"] and indices is not None and indices != attempt["selection"]:
        attempt["selection"] = indices
        state.set("attempt", attempt)
        st.rerun()
    with st.expander("Text descriptions of forces and motion"):
        from utils.force_diagram_match import describe_diagram
        st.write(describe_diagram(case.arrows))
        for letter, m in zip(letters, attempt["options"]):
            st.write(f"**{letter}:** {m.description(case.axis)}. Successive positions: {', '.join(str(p) for p in m.positions)} (schematic units, positive {'right' if case.axis == 'horizontal' else 'up'}).")
    checks_col, hints_col = st.columns(2)
    with checks_col:
        checked = st.button("Check motions", type="primary", key=state.key(f"check_{qid}"), disabled=attempt["completed"], width="stretch")
    with hints_col:
        hinted = st.button("Show interaction hint", key=state.key(f"hint_{qid}"), disabled=attempt["completed"], width="stretch")
    if hinted:
        attempt["hint_used"] = True
        state.set("attempt", attempt)
        st.rerun()
    if checked:
        if not attempt["selection"]:
            st.warning("Select one or more motions before checking. At least one option is compatible.")
        elif submit_attempt(attempt):
            record_answer("Force and Motion Matching", case.prompt,
                          [attempt["options"][i].description(case.axis) for i in attempt["selection"]],
                          [attempt["options"][i].description(case.axis) for i in expected], attempt["completed"],
                          explanation=explanation(case), diagrams={"Forces": data_url(diagram_image(case.arrows)),
                                                                 **{f"Motion {letter}": image for letter, image in zip(letters, images)}})
            state.set("attempt", attempt)
            st.rerun()
    if attempt["checks"]:
        last = attempt["checks"][-1]
        st.caption("Feedback is for your last check. Select or deselect cards, then check again.")
        if last["correct"]:
            st.success("Correct — you selected every compatible motion. ⭐")
        else:
            st.warning("Revise your set of motions and check again.")
            if last["missing"]:
                st.write("There are other compatible motions you haven't selected. Check how each card's dot spacing changes.")
            if last["extra"]:
                st.write("At least one selected motion doesn't fit. Compare its acceleration with the net force.")
        if last["correct"]:
            st.write(explanation(case))

    def next_question():
        if state.get("question_id") == qid:
            fresh(context)

    def related():
        if state.get("question_id") == qid:
            group = [c.id for c in available_cases(context) if c.axis == case.axis and c.id != case.id]
            if not group:
                group = [c.id for c in available_cases(context) if c.id != case.id]
            case_id = random.choice(group)
            start(case_id)
            state.set("seen", [*state.get("seen", []), case_id])

    a, b = st.columns(2)
    with a:
        st.button("Next question" if attempt["completed"] else "Skip question", key=state.key(f"next_{qid}"), on_click=next_question, width="stretch")
    with b:
        st.button("Try a related case", key=state.key(f"related_{qid}"), on_click=related, width="stretch")
    with st.expander("Your Performance"):
        st.caption("This session only. One star per completed set. Choosing cards or requesting hints does not score an answer.")
        st.dataframe([{"Case": CASE_BY_ID[r["case_id"]].title, "Checks": len(r["checks"]), "Hint used": r["hint_used"],
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

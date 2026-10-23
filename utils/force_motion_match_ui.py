"""C2 multiple-answer motion matching, independent of numerical scoring flows."""
import base64
import random

import streamlit as st

from utils.activity_flow import next_question_countdown
from utils.force_activity_ui import question_title, separate_assumptions
from utils.force_diagram_match_ui import diagram_image
from utils.force_motion_match import (
    CASE_BY_ID, MOTION_DISPLAYS, PRACTICE_SETS, available_cases, compatible, explanation,
    graph_description, graph_kind, new_attempt, render_motion, render_motion_graph, submit_attempt,
)
from utils.graph_cards import graph_cards, selected_indices
from utils.session_progress import record_answer
from utils.force_activity_ui import force_activity_header as render_header
from utils.ui_state import State


@st.cache_data(show_spinner=False)
def motion_image(motion, axis):
    return render_motion(motion, axis)


@st.cache_data(show_spinner=False)
def motion_graph_image(motion, kind):
    """Cache graph artwork with labels sized for four-across answer cards."""
    return render_motion_graph(motion, kind)


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
    with st.sidebar.expander("Practice settings"):
        context = st.selectbox("Practice situations", PRACTICE_SETS, key=state.key("context"))
    if state.get("active_context") != context or not state.has("attempt") or len(state.get("attempt", {}).get("options", [])) != 4:
        state.set("active_context", context)
        state.set("seen", [])
        fresh(context)
    attempt = state.get("attempt")
    case = CASE_BY_ID[attempt["case_id"]]
    qid = state.get("question_id")
    reference, question = st.columns([1.2, 4])
    with reference, st.container(key="force_motion_reference"):
        st.markdown("**Initial forces**")
        st.image(diagram_image(case.arrows), width="stretch")
    with question:
        prompt, assumptions = separate_assumptions(case.prompt)
        question_title(case.title,
                       "The shown forces stay constant throughout each possible motion. Consider the named object only. The diagrams are qualitative; exact force and acceleration magnitudes are not supplied.",
                       "Dots 1–4 mark equal time steps. Read them in numbered order. Each card has its own schematic scale; compare how gaps change within a card.",
                       "Graphs show the same motion over relative times 0–3 in schematic units. Positive means right for horizontal motion and up for vertical motion. Position is displacement from the starting point, not total distance traveled. Position-graph slope gives velocity; velocity-graph slope gives acceleration. The mixed view uses two of each type, with one graph per choice. Check each graph's y-axis.", assumptions)
        st.write(prompt)
        st.markdown(f"Which **{'horizontal' if case.axis == 'horizontal' else 'vertical'} motions** fit? **Check all that apply.** Initial motion is unknown.")
        display_col, _ = st.columns([1.3, 2])
        with display_col:
            if state.get("display") == "Position + velocity graphs":
                state.set("display", "Mixed graph types")
            display = st.selectbox("Motion display", MOTION_DISPLAYS, key=state.key("display"))
    if attempt["hint_used"]:
        st.info("First compare opposing forces. Net force determines acceleration; the velocity may point either way. An object speeds up when velocity and acceleration point the same way and slows down when they point opposite ways.")
    letters = "ABCD"
    graph_view = display not in MOTION_DISPLAYS[:2]
    kinds = [graph_kind(display, i, qid) for i in range(4)] if graph_view else []
    if graph_view:
        st.caption(f"Positive = {'right' if case.axis == 'horizontal' else 'up'} · Schematic units · Same time interval on every graph")
        images = [data_url(motion_graph_image(m, kind)) for m, kind in zip(attempt["options"], kinds)]
        captions = [{"position": "Position–time", "velocity": "Velocity–time"}[kind] for kind in kinds]
        descriptions = [graph_description(m, case.axis, kind) for m, kind in zip(attempt["options"], kinds)]
    else:
        images = [data_url(motion_image(m, case.axis)) if display == "Dot diagrams" else None for m in attempt["options"]]
        captions = descriptions = [m.description(case.axis) for m in attempt["options"]]
    expected = tuple(i for i, m in enumerate(attempt["options"]) if compatible(case, m))
    event = graph_cards(images, list(letters), qid, list(attempt["selection"]), attempt["completed"],
                        "Four across", key=state.key(f"cards_{qid}"), has_reference=False,
                        option_name="Motion", check_label="Check motions", multi_select=True,
                        correct_indices=expected, captions=captions, descriptions=descriptions)
    indices = selected_indices(event, qid, len(images))
    if not attempt["completed"] and indices is not None and indices != attempt["selection"]:
        attempt["selection"] = indices
        state.set("attempt", attempt)
        st.rerun()
    with st.expander("Text descriptions of forces and motion"):
        from utils.force_diagram_match import describe_diagram
        st.write(describe_diagram(case.arrows))
        for letter, m in zip(letters, attempt["options"]):
            detail = descriptions[letters.index(letter)] if graph_view else m.description(case.axis) + "."
            st.write(f"**{letter}:** {detail}")
            if display == "Dot diagrams":
                st.caption(f"Successive positions: {', '.join(str(p) for p in m.positions)} (schematic units, positive {'right' if case.axis == 'horizontal' else 'up'}).")
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
                                                                 **{f"Motion {letter}": image for letter, image in zip(letters, images) if image}})
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
                st.write("There are other compatible motions you haven't selected. Compare each motion's change in speed and direction.")
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

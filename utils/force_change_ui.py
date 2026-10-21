"""C3 before/after force-diagram decisions with exact-set revision."""
import random

import streamlit as st

from utils.activity_flow import next_question_countdown
from utils.force_change import (
    CASE_BY_ID, PRACTICE_SETS, accepted, available_cases, change_description,
    explanation, new_attempt, render_change_diagram, submit_attempt,
)
from utils.force_motion_match_ui import data_url
from utils.graph_cards import graph_cards, selected_indices
from utils.session_progress import record_answer
from utils.ui_components import render_header
from utils.ui_state import State


@st.cache_data(show_spinner=False)
def change_image(force_state):
    return render_change_diagram(force_state)


def render_force_change():
    state = State("force_change")
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

    render_header("Change of State", sum(bool(r.get("completed")) for r in [*state.get("records"), state.get("attempt", {})]))
    st.write("Select **every** one-force change that produces the requested motion.")
    context = st.selectbox("Practice situations", PRACTICE_SETS, key=state.key("context"))
    if state.get("active_context") != context or not state.has("attempt") or len(state.get("attempt", {}).get("options", [])) != 4:
        state.set("active_context", context)
        state.set("seen", [])
        fresh(context)
    attempt = state.get("attempt")
    case = CASE_BY_ID[attempt["case_id"]]
    qid = state.get("question_id")
    st.markdown(f"**{case.title}**")
    st.write(case.motion)
    st.info(case.request)
    st.caption("The same cart stays on a level, frictionless track. Air resistance is neglected. Its mass, 20 N weight and 20 N normal force stay unchanged. A hand pushes right; a winch-controlled rope can pull left. Zero means no contact/pull. Each choice changes just one horizontal interaction and then holds its new force constant.")
    st.caption("A force change does not instantly change velocity. Judge the motion immediately afterward, before the cart could stop or reverse.")
    if attempt["hint_used"]:
        st.info("Find the required acceleration first. Then compare the rightward push with the leftward rope pull. Balanced forces mean no acceleration; a force opposite the current velocity slows the cart.")
    letters = "ABCD"
    descriptions = [change_description(case.initial, after) for after in attempt["options"]]
    images = [data_url(change_image(after)) for after in attempt["options"]]
    expected = tuple(i for i, after in enumerate(attempt["options"]) if accepted(case, after))
    st.markdown("**Possible diagrams after the change**")
    event = graph_cards([data_url(change_image(case.initial)), *images], list(letters), qid, list(attempt["selection"]), attempt["completed"],
                        "Reference beside options", key=state.key(f"cards_{qid}"), reference_label="Before the change", multi_select=True,
                        option_name="Change", check_label="Check changes", correct_indices=expected,
                        descriptions=[d + " " + after.description for d, after in zip(descriptions, attempt["options"])])
    indices = selected_indices(event, qid, len(images))
    if not attempt["completed"] and indices is not None and indices != attempt["selection"]:
        attempt["selection"] = indices
        state.set("attempt", attempt)
        st.rerun()
    with st.expander("What changed? / Text descriptions"):
        st.write("**Before:** " + case.initial.description)
        for letter, description, after in zip(letters, descriptions, attempt["options"]):
            st.write(f"**{letter}:** {description} {after.description}")
    a, b = st.columns(2)
    with a:
        checked = st.button("Check changes", key=state.key(f"check_{qid}"), type="primary", disabled=attempt["completed"], use_container_width=True)
    with b:
        hinted = st.button("Show interaction hint", key=state.key(f"hint_{qid}"), disabled=attempt["completed"], use_container_width=True)
    if hinted:
        attempt["hint_used"] = True
        state.set("attempt", attempt)
        st.rerun()
    if checked:
        if not attempt["selection"]:
            st.warning("Select at least one possible change before checking.")
        elif submit_attempt(attempt):
            record_answer("Change of State", case.motion + " " + case.request,
                          [descriptions[i] for i in attempt["selection"]], [descriptions[i] for i in expected],
                          attempt["completed"], explanation=explanation(case),
                          diagrams={"Before": data_url(change_image(case.initial)),
                                    **{f"Change {letter}": image for letter, image in zip(letters, images)}})
            state.set("attempt", attempt)
            st.rerun()
    if attempt["checks"]:
        last = attempt["checks"][-1]
        st.caption("Feedback describes your last check. Change your selected cards, then check again.")
        if last["correct"]:
            st.success("Correct — you found every valid change. ⭐")
        else:
            st.warning("Revise your set of changes and check again.")
            for i in last["missing"]:
                st.write(f"Also works — {letters[i]}: {descriptions[i]}")
            for i in last["extra"]:
                after = attempt["options"][i]
                net_description = f"{abs(after.net)} N {'right' if after.net > 0 else 'left'}" if after.net else "0 N (balanced)"
                st.write(f"Does not meet the request — {letters[i]}: the new net force is {net_description}.")
        st.write(explanation(case))

    def next_question():
        if state.get("question_id") == qid:
            fresh(context)

    def related():
        if state.get("question_id") == qid:
            ids = [c.id for c in available_cases(context) if c.category == case.category and c.id != case.id]
            if not ids:
                ids = [c.id for c in available_cases(context) if c.id != case.id]
            case_id = random.choice(ids)
            start(case_id)
            state.set("seen", [*state.get("seen", []), case_id])

    a, b = st.columns(2)
    with a:
        st.button("Next question" if attempt["completed"] else "Skip question", key=state.key(f"next_{qid}"), on_click=next_question, use_container_width=True)
    with b:
        st.button("Try a related case", key=state.key(f"related_{qid}"), on_click=related, use_container_width=True)
    with st.expander("Your Performance"):
        st.caption("This session only. One star per completed set; partial sets are revisable and do not earn a star.")
        st.dataframe([{"Case": CASE_BY_ID[r["case_id"]].title, "Checks": len(r["checks"]), "Hint used": r["hint_used"],
                       "Result": r["outcome"] or ("In progress" if r is attempt else "Skipped")}
                      for r in [*state.get("records"), attempt]], hide_index=True, use_container_width=True)

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

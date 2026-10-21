"""Widget-driven I2 editor: live preview, explicit checks, and useful revision."""
import base64
import random

import streamlit as st

from utils.activity_flow import next_question_countdown
from utils.force_diagram_builder import (
    SIZE_LABELS, SYMBOLS, describe_builder, new_builder_attempt,
    render_builder_diagram, submit_builder,
)
from utils.force_diagram_match import CASE_BY_ID, DIRECTIONS, ForceArrow, available_cases
from utils.recognizing_forces import FORCE_LABELS, PRACTICE_SETS
from utils.session_progress import record_answer
from utils.ui_components import render_header
from utils.ui_state import State


@st.cache_data(show_spinner=False)
def builder_image(arrows):
    return render_builder_diagram(arrows)


def render_force_diagram_builder():
    state = State("force_diagram_builder")
    state.ensure("records", [])
    state.ensure("question_id", 0)

    def start(case_id):
        if state.has("attempt"):
            state.set("records", [*state.get("records"), state.get("attempt")])
        state.inc("question_id")
        state.set("attempt", new_builder_attempt(case_id))

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
    render_header("Free-Body Diagram Builder", sum(bool(r.get("completed")) for r in records))
    st.write("Build the forces on one object. Your diagram updates as you edit; checking is a separate step.")
    context = st.selectbox("Practice contexts", PRACTICE_SETS, key=state.key("context"))
    if state.get("active_context") != context or not state.has("attempt"):
        state.set("active_context", context)
        state.set("seen", [])
        fresh(context)
    attempt = state.get("attempt")
    case = CASE_BY_ID[attempt["case_id"]]
    qid = state.get("question_id")
    st.markdown(f"**{case.scenario.title}**")
    st.write(case.prompt)
    st.info(f"Build only the forces acting on **{case.scenario.target}**.")
    if attempt["hint_used"]:
        st.info(case.scenario.hint + " Decide which interactions act on the object, their directions, and whether opposing forces balance.")

    editor = st.container(key=state.key(f"editor_{qid}"))
    controls, preview = editor.columns([1.05, 1], gap="large")
    draft_by_force = {item["force"]: item for item in attempt["draft"]}
    with controls:
        state.ensure(f"forces_{qid}", list(draft_by_force))
        selected = st.multiselect("Forces on the object", list(FORCE_LABELS),
                                  format_func=FORCE_LABELS.get, key=state.key(f"forces_{qid}"),
                                  disabled=attempt["completed"], placeholder="Add a force…")
        st.caption("Short, Medium, and Long show relative strength. Compare opposing forces on the same axis; exact ratios are not required.")
        draft = []
        for force in selected:
            saved = draft_by_force.get(force, {})
            st.markdown(f"**{SYMBOLS[force]} · {FORCE_LABELS[force]}**")
            direction_col, length_col = st.columns(2)
            state.ensure(f"direction_{qid}_{force}", saved.get("direction"))
            state.ensure(f"size_{qid}_{force}", saved.get("size", 2))
            with direction_col:
                direction = st.selectbox("Direction", [None, *DIRECTIONS],
                                         format_func=lambda d: d.capitalize() if d else "Choose direction",
                                         key=state.key(f"direction_{qid}_{force}"), disabled=attempt["completed"])
            with length_col:
                size = st.select_slider("Arrow length", list(SIZE_LABELS), format_func=SIZE_LABELS.get,
                                        key=state.key(f"size_{qid}_{force}"), disabled=attempt["completed"])
            draft.append({"force": force, "direction": direction, "size": size})
        attempt["draft"] = draft
        state.set("attempt", attempt)
        check_col, hint_col = st.columns(2)
        with check_col:
            checked = st.button("Check diagram", type="primary", use_container_width=True,
                                key=state.key(f"check_{qid}"), disabled=attempt["completed"])
        with hint_col:
            hinted = st.button("Show interaction hint", use_container_width=True,
                               key=state.key(f"hint_{qid}"), disabled=attempt["completed"])

    arrows = tuple(ForceArrow(d["force"], d["direction"], d["size"]) for d in draft if d["direction"])
    incomplete = [d for d in draft if d["direction"] is None]
    with preview:
        st.markdown("**Your diagram**")
        st.image(builder_image(arrows), use_container_width=True)
        st.caption("The box represents the named object. Its size has no physical meaning.")
        if selected:
            st.caption(" · ".join(f"{SYMBOLS[f]} = {FORCE_LABELS[f]}" for f in selected))
        if incomplete:
            st.caption("Choose a direction for each added force to show all arrows.")
        with st.expander("Text description of your diagram"):
            st.write(describe_builder(arrows))
            for item in incomplete:
                st.write(f"{FORCE_LABELS[item['force']]}: direction not chosen.")

    if hinted:
        attempt["hint_used"] = True
        state.set("attempt", attempt)
        st.rerun()
    if checked:
        if incomplete:
            st.warning("Choose a direction for each added force before checking. This has not counted as an attempt.")
        elif submit_builder(attempt, arrows):
            result = attempt["checks"][-1]
            record_answer("Free-Body Diagram Builder", case.prompt + " Forces on: " + case.scenario.target,
                          describe_builder(arrows), describe_builder(case.arrows), result["correct"],
                          explanation=case.explanation + " Any arrow lengths with the same required relationships are accepted.",
                          diagrams={label: "data:image/png;base64," + base64.b64encode(builder_image(a)).decode("ascii")
                                    for label, a in (("Your diagram", arrows), ("One valid diagram", case.arrows))})
            state.set("attempt", attempt)
            st.rerun()

    if attempt["checks"]:
        last = attempt["checks"][-1]
        st.caption("Feedback describes your last check. Editing the preview does not recheck or score your work.")
        if last["correct"]:
            st.success("Correct — your diagram matches the situation. ⭐")
            st.write(case.explanation)
        else:
            st.warning("Revise your diagram and check again.")
        with st.container(border=True):
            st.markdown("**Force types**")
            if last["forces_ok"]:
                st.write("✓ You have the right forces.")
            for feedback in last["force_feedback"]:
                st.write(feedback)
            st.markdown("**Directions**")
            for feedback in last["direction_feedback"]:
                st.write(feedback)
            if not last["direction_feedback"]:
                included = any(a.force in case.scenario.forces for a in last["arrows"])
                st.write("✓ Directions of the expected forces you included are correct." if included else "Add the expected forces to check their directions.")
            st.markdown("**Relative sizes**")
            for feedback in last["size_feedback"]:
                st.write(feedback)
            if last["size_deferred"]:
                st.write("Fix missing forces or directions before comparing those arrow lengths.")
            elif len(case.arrows) == 1:
                st.write("No opposing-force length comparison is required in this case.")
            elif not last["size_feedback"]:
                st.write("✓ The required size relationships are satisfied. Exact ratios are not required.")

    def next_question():
        if state.get("question_id") == qid:
            fresh(context)

    def related():
        if state.get("question_id") == qid:
            case_id = case.scenario.related
            if case_id not in CASE_BY_ID:
                case_id = next(c.id for c in available_cases(case.scenario.context) if c.id != case.id)
            start(case_id)
            state.set("seen", [*state.get("seen", []), case_id])

    left, right = st.columns(2)
    with left:
        st.button("Next question" if attempt["completed"] else "Skip question",
                  key=state.key(f"next_{qid}"), on_click=next_question, use_container_width=True)
    with right:
        st.button("Try a related case", key=state.key(f"related_{qid}"), on_click=related, use_container_width=True)
    with st.expander("Your Performance"):
        st.caption("This session only. One star per completed case. Draft edits and hints do not count as answer checks.")
        st.dataframe([{"Case": CASE_BY_ID[r["case_id"]].scenario.title, "Checks": len(r["checks"]),
                       "Hint used": r["hint_used"], "Result": r["outcome"] or ("In progress" if r is attempt else "Skipped")}
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

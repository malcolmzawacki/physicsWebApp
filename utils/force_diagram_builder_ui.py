"""Widget-driven I2 editor: live preview, explicit checks, and useful revision."""
import base64
import random

import streamlit as st

from utils.activity_flow import next_question_countdown
from utils.force_activity_ui import question_title, separate_assumptions
from utils.force_diagram_builder import (
    SIZE_LABELS, SYMBOLS, describe_builder, new_builder_attempt,
    render_builder_diagram, submit_builder,
)
from utils.force_diagram_match import CASE_BY_ID, SHORT_LABELS, ForceArrow, available_cases
from utils.recognizing_forces import FORCE_LABELS, PRACTICE_SETS
from utils.session_progress import record_answer
from utils.force_activity_ui import force_activity_header as render_header
from utils.ui_state import State


@st.cache_data(show_spinner=False)
def builder_image(arrows):
    return render_builder_diagram(arrows)


def render_force_diagram_builder():
    from utils.worksheet_ui import worksheet_shortcut
    worksheet_shortcut('Free-Body Diagram Builder')
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
                   "Place each force where its arrow points. Select all that apply in each menu. Adding a force in a new position moves it from its old position.",
                   "Short, Medium, and Long show relative strength. Compare opposing forces on the same axis; exact ratios are not required.",
                   "Your diagram updates as you edit; use Check diagram to submit it.", assumptions)
    st.write(prompt)
    st.markdown(f"Build forces on **{case.scenario.target}**. **Select all that apply.**")
    if attempt["hint_used"]:
        st.info(case.scenario.hint + " Decide which interactions act on the object, their directions, and whether opposing forces balance.")

    editor = st.container(key=state.key(f"editor_{qid}"))
    st.markdown(f"""<style>
        .st-key-{state.key(f"editor_{qid}")} [data-testid="stImage"] {{
            max-width: 180px;
        }}
        .st-key-{state.key(f"editor_{qid}")} [data-testid="stFullScreenFrame"] {{
            display: flex;
            justify-content: center;
        }}
        .st-key-{state.key(f"editor_{qid}")} [data-testid="stVerticalBlock"] {{
            gap: .4rem;
        }}
        .st-key-{state.key(f"editor_{qid}")} [class*="st-key-force_diagram_builder_position_panel_"] {{
            padding: .5rem;
        }}
    </style>""", unsafe_allow_html=True)
    draft_by_force = {item["force"]: item for item in attempt["draft"]}
    positions = ("up", "left", "right", "down")
    headings = {"up": "↑ Above", "left": "← Left", "right": "Right →", "down": "↓ Below"}
    for direction in positions:
        state.ensure(f"position_{qid}_{direction}",
                     [force for force, item in draft_by_force.items() if item.get("direction") == direction])
    lengths = attempt.setdefault("lengths", {force: draft_by_force.get(force, {}).get("size", 2)
                                            for force in FORCE_LABELS})
    for force in FORCE_LABELS:
        state.set(f"size_{qid}_{force}", lengths[force])

    def save_length(force):
        current = state.get("attempt")
        current["lengths"][force] = state.get(f"size_{qid}_{force}")
        state.set("attempt", current)

    def move_forces(direction):
        # Callbacks run before widgets render, so a force can move between menus
        # without duplicates or changes to already-created widget values.
        moved = set(state.get(f"position_{qid}_{direction}", []))
        for other in positions:
            if other != direction:
                state.set(f"position_{qid}_{other}",
                          [force for force in state.get(f"position_{qid}_{other}", []) if force not in moved])

    if attempt["completed"]:
        draft = attempt["draft"]
    else:
        draft = [{"force": force, "direction": direction, "size": lengths[force]}
                 for direction in positions for force in state.get(f"position_{qid}_{direction}", [])]
        attempt["draft"] = draft
        state.set("attempt", attempt)
    arrows = tuple(ForceArrow(d["force"], d["direction"], d["size"]) for d in draft)

    def position_panel(direction):
        with st.container(border=True, key=state.key(f"position_panel_{direction}")):
            st.markdown(f"**{headings[direction]}**")
            selected = [d["force"] for d in draft if d["direction"] == direction]
            menu, single_length = st.columns([1.4, 1]) if len(selected) == 1 else (st.container(), None)
            with menu:
                if attempt["completed"]:
                    st.multiselect(f"Forces pointing {direction}", list(FORCE_LABELS), default=selected,
                                   format_func=lambda force: f"{SYMBOLS[force]} · {SHORT_LABELS[force]}",
                                   key=state.key(f"position_{qid}_{direction}_completed"), disabled=True,
                                   label_visibility="collapsed", placeholder="Add forces…")
                else:
                    selected = st.multiselect(f"Forces pointing {direction}", list(FORCE_LABELS),
                                              format_func=lambda force: f"{SYMBOLS[force]} · {SHORT_LABELS[force]}",
                                              key=state.key(f"position_{qid}_{direction}"),
                                              on_change=move_forces, args=(direction,),
                                              label_visibility="collapsed", placeholder="Add forces…")
            for force in selected:
                if single_length is None:
                    label, length = st.columns([1, 1.3])
                    label.caption(f"{SYMBOLS[force]} · {SHORT_LABELS[force]}")
                else:
                    length = single_length
                with length:
                    if attempt["completed"]:
                        size = next(d["size"] for d in draft if d["force"] == force)
                        st.selectbox(f"{FORCE_LABELS[force]} arrow length", list(SIZE_LABELS), index=size - 1,
                                     format_func=SIZE_LABELS.get, key=state.key(f"size_{qid}_{force}_completed"),
                                     disabled=True, label_visibility="collapsed")
                    else:
                        st.selectbox(f"{FORCE_LABELS[force]} arrow length", list(SIZE_LABELS),
                                     format_func=SIZE_LABELS.get, key=state.key(f"size_{qid}_{force}"),
                                     on_change=save_length, args=(force,), label_visibility="collapsed")

    with editor:
        top = st.columns([1, 1.35, 1], gap="small")
        with top[1]:
            position_panel("up")
        left, preview, right = st.columns([1, 1.35, 1], gap="small", vertical_alignment="center")
        with left:
            position_panel("left")
        with preview:
            st.image(builder_image(arrows), width="stretch")
        with right:
            position_panel("right")
        bottom = st.columns([1, 1.35, 1], gap="small")
        with bottom[1]:
            position_panel("down")
        check_col, hint_col = st.columns(2)
        with check_col:
            checked = st.button("Check diagram", type="primary", width="stretch",
                                key=state.key(f"check_{qid}"), disabled=attempt["completed"])
        with hint_col:
            hinted = st.button("Show interaction hint", width="stretch",
                               key=state.key(f"hint_{qid}"), disabled=attempt["completed"])
        with st.expander("Text description of your diagram"):
            st.write(describe_builder(arrows))
            st.caption("The box represents the named object. Its size has no physical meaning.")

    if hinted:
        attempt["hint_used"] = True
        state.set("attempt", attempt)
        st.rerun()
    if checked:
        if submit_builder(attempt, arrows):
            result = attempt["checks"][-1]
            record_answer("Free-Body Diagram Builder", case.prompt + " Forces on: " + case.scenario.target,
                          describe_builder(arrows), describe_builder(case.arrows), result["correct"], problem_type=case.scenario.context,
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
                  key=state.key(f"next_{qid}"), on_click=next_question, width="stretch")
    with right:
        st.button("Try a related case", key=state.key(f"related_{qid}"), on_click=related, width="stretch")
    with st.expander("Your Performance"):
        st.caption("This session only. One star per completed case. Draft edits and hints do not count as answer checks.")
        st.dataframe([{"Case": CASE_BY_ID[r["case_id"]].scenario.title, "Checks": len(r["checks"]),
                       "Hint used": r["hint_used"], "Result": r["outcome"] or ("In progress" if r is attempt else "Skipped")}
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

"""Per-question organizing help, checked independently of final answers."""

import streamlit as st
from utils.setup_feedback import check_entry, evaluate_entry, normalize_entry
from utils.quantities import PROFILES
from utils.setup_schema import expected_entries

def render_setup_workspace(state):
    question_id = state.get("question_id", 0)
    if state.get("setup_question_id") != question_id:
        state.set("setup_question_id", question_id)
        state.set("setup_submission", None)
        state.set("setup_draft", None)
    payload = state.get("payload")
    setup = payload.extras.get("setup") if payload else None
    if setup is None:
        return
    expected = expected_entries(setup)
    roles = PROFILES[setup["profile"]]
    quantities = [(key, role.name, role.symbol) for key, role in roles.items()]
    with st.expander("Organizing help", expanded=False):
        st.caption("Enter a number in the problem's units. Use ? for the quantity asked for, or x (or X) for neither provided nor asked for.")
        with st.form(state.key(f"setup_form_{question_id}"), clear_on_submit=False, enter_to_submit=True, border=False):
            columns = st.columns(len(quantities))
            entries = {}
            for column, (key, name, symbol) in zip(columns, quantities):
                with column:
                    st.markdown(f"**{name}** (${symbol}$)")
                    entries[key] = st.text_input(
                        name, label_visibility="collapsed",
                        key=state.key(f"setup_input_{question_id}_{key}"),
                    )
            state.set("setup_draft", dict(entries))
            submitted = st.form_submit_button("Check setup")
        if submitted:
            state.set("setup_submission", {key: normalize_entry(value) for key, value in entries.items()})
        snapshot = state.get("setup_submission")
        if snapshot is not None:
            st.caption("Results from your last check. Press Enter or Check setup to check revisions.")
            if expected is None:
                st.info("Setup checking is not available for this problem yet.")
                return
            for column, (key, name, _) in zip(columns, quantities):
                with column:
                    current = normalize_entry(entries[key])
                    if current != snapshot[key]:
                        st.caption(f"{name}: changed — check again")
                        continue
                    feedback = evaluate_entry(current, key, expected, roles)
                    label = f"{name}: {'Check this entry' if feedback.status == 'incorrect' else feedback.message}"
                    if feedback.status == "correct":
                        st.success(label, icon=":material/check_circle:")
                    elif feedback.status == "incorrect":
                        st.error(label, icon=":material/error:")
                        st.markdown(feedback.message)
                    else:
                        st.caption(label)

"""Advanced relative motion using shared scoring and equation helpers."""


def relative_motion():
    import math
    import streamlit as st
    from utils.generators.kinematics.relative_motion_generator import RelativeMotionGenerator
    from utils.ui import Interface
    from utils.ui_components import show_equations_expander
    from utils.activity_flow import next_question_countdown
    from utils.word_lists import random_correct_message, random_error_message

    if st.session_state.get("nav_level") != "advanced":
        st.info("Relative Motion is available at the Advanced course level.")
        return
    generator = RelativeMotionGenerator()
    ui = Interface("relative_motion", "Relative Motion", generator, generator.stored_metadata(), list(generator.DIFFICULTIES))
    ui.initialize_session_state()
    state = ui.state
    ui.header_component()
    st.caption("Constant velocity in one dimension. Every velocity is measured relative to a named observer.")
    cols = st.columns([3, 2, 2])
    kind = cols[0].selectbox("Problem Type", generator.TYPES, key=state.key("type_select"))
    difficulty = cols[1].selectbox("Difficulty", generator.DIFFICULTIES, key=state.key("difficulty_select"))
    target = cols[2].selectbox("Solve for", generator.TARGETS, key=state.key("target_select"))
    descriptions = {
        "Independent motion": "Easy: relative velocity. Medium: separation after a time. Hard: meeting or catch-up time.",
        "Nested reference frames": "Easy: 2 velocity links. Medium: 3 links. Hard: 4 links, including a moving walkway.",
        "Combined": "Easy: 2 links per person. Medium: 3 links per person. Hard: 4 links per person. Shared currents cancel.",
    }
    st.caption(descriptions[kind])
    selection = (kind, difficulty, target)
    if state.get("selection") != selection or state.get("payload") is None:
        state.set("payload", generator.choose_problem_dict(kind, difficulty, target))
        state.set("selection", selection)
        state.set("submitted", False)
        state.inc("question_id")
        state.pop("last_result")
        state.pop("feedback_message")
    payload = state.get("payload")
    left, right = st.columns([1, 1.25])
    with left:
        st.pyplot(generator.generate_diagram(payload["diagram_data"], kind, difficulty))
        more = st.checkbox("More Equations", key=state.key("more_equations"))
        show_equations_expander(generator=generator, problem_type=kind, level=more, fallback_dict=generator.stored_metadata(), expanded=True)
    with right:
        st.write(payload["question"])
        with st.form(state.key("answer_form")):
            raw = st.text_input(payload["units"][0], key=state.key(f"answer_{state.get('question_id')}"), disabled=state.get("submitted"))
            submitted = st.form_submit_button("Submit", disabled=state.get("submitted"))
        if submitted and not state.get("submitted"):
            try:
                value = float(raw.strip())
                if not math.isfinite(value):
                    raise ValueError
            except ValueError:
                st.error("Enter a finite number, including a minus sign when needed.")
            else:
                correct = math.isclose(value, payload["answers"][0], rel_tol=.1, abs_tol=1e-9)
                ui.update_performance(kind, difficulty, correct)
                if correct:
                    state.inc("stars", ui.give_stars(difficulty, kind))
                state.set("submitted", True)
                state.set("last_result", correct)
                state.set("feedback_message", random_correct_message() if correct else random_error_message())
                st.rerun()
        if state.get("submitted"):
            if state.get("last_result"):
                st.success(state.get("feedback_message"))
            else:
                st.error(f"{state.get('feedback_message')} The correct answer is {payload['answers'][0]:g}. {payload['units'][0]}")
            st.write(payload["extras"]["explanation"])
            for equation in payload["extras"]["solution_equations"]:
                st.latex(equation)
        else:
            with st.expander("Hint"):
                st.write(payload["hints"][0])
    def next_question():
        state.pop("payload")
        st.rerun()

    if st.button("New Question", key=state.key("new_question")):
        next_question()
    ui.performance_dropdown()
    with st.expander("Worked example: find the river current"):
        st.write(generator.example()["question"])
        st.latex(r"4=-1+3+v_{water/shore}")
        st.latex(r"v_{water/shore}=4-(-1)-3=2\;\mathrm{m/s}")
        st.write("The current flows downstream at 2 m/s relative to the shore.")
    if state.get("submitted") and state.get("last_result"):
        next_question_countdown(state, state.get("question_id"), next_question)

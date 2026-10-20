"""Temporary practice preferences and answer history, scoped to one connection.

Keep these in session_state only: no caches, files, cookies, or browser storage.
A browser refresh starts a new Streamlit session and discards this history.
"""
from copy import deepcopy
import base64

import streamlit as st

AUTO_LOAD_KEY = "practice_auto_load"
HISTORY_KEY = "practice_answer_history"


def record_answer(activity, question, submitted, expected, correct, *,
                  difficulty="", explanation="", equations=None, diagrams=None):
    """Snapshot one valid answer check, called only in submission handlers."""
    history = st.session_state.setdefault(HISTORY_KEY, [])
    history.append(deepcopy({
        "Activity": activity, "Question": question, "Your answer": submitted,
        "Correct answer": expected, "Result": "Correct" if correct else "Incorrect",
        "Difficulty": difficulty, "Explanation": explanation,
        "Equations": equations or [],
        "Diagrams": diagrams or {},
    }))


def format_answers(answers, units):
    return "; ".join(f"{answer} {units[i] if i < len(units) else ''}".strip()
                     for i, answer in enumerate(answers))


def render_session_controls():
    """Render once in the shared sidebar, on every route."""
    st.checkbox("Automatically load next question", value=True, key=AUTO_LOAD_KEY,
                help="After a correct answer, load the next question automatically. Turn off to review at your own pace.")
    st.caption("Settings and progress last until you refresh or close this session.")


def render_session_progress():
    st.title("My Current Session Progress")
    st.caption("Answer checks from this session only. Refreshing the browser clears this history and your practice settings.")
    history = st.session_state.get(HISTORY_KEY, [])
    if not history:
        st.info("No answers checked yet. Choose an activity to start practicing.")
        return
    correct = sum(row["Result"] == "Correct" for row in history)
    st.write(f"{len(history)} answers checked · {correct} correct · {len(history) - correct} incorrect")
    st.caption("Each check counts once, including retries. These counts describe practice, not mastery.")
    activities = list(dict.fromkeys(row["Activity"] for row in history))
    selected = st.selectbox("Activity", ["All activities", *activities], key="progress_activity_filter")
    for index, row in reversed(list(enumerate(history, 1))):
        if selected != "All activities" and row["Activity"] != selected:
            continue
        with st.expander(f"{index}. {row['Activity']} — {row['Result']}"):
            if row["Difficulty"]:
                st.caption(str(row["Difficulty"]))
            st.write(row["Question"])
            for label, data_url in row["Diagrams"].items():
                st.image(base64.b64decode(data_url.split(",", 1)[1]), caption=label)
            st.write("**Your answer**")
            st.write(row["Your answer"])
            st.write("**Correct answer**")
            st.write(row["Correct answer"])
            if row["Explanation"]:
                st.write(row["Explanation"])
            for equation in row["Equations"]:
                st.latex(equation)

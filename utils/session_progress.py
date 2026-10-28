"""Existing answer history, mirrored to browser storage for a fixed 24 hours.

Practice preferences and activity state remain scoped to the live connection.
"""
from copy import deepcopy
import base64
import secrets
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

import streamlit as st

AUTO_LOAD_KEY = "practice_auto_load"
HISTORY_KEY = "practice_answer_history"
SESSION_CODE_KEY = "practice_session_code"


def session_code():
    """Return the browser-restored label, or a temporary label before hydration."""
    if SESSION_CODE_KEY not in st.session_state:
        digits = f"{secrets.randbelow(10**16):016d}"
        st.session_state[SESSION_CODE_KEY] = "-".join(digits[i:i + 4] for i in range(0, 16, 4))
    return st.session_state[SESSION_CODE_KEY]


def progress_date(now=None):
    """Use the school's day even when hosting runs in UTC."""
    return (now or datetime.now(timezone.utc)).astimezone(ZoneInfo("America/New_York")).date()


def daily_history(history, day):
    # Keep records from sessions opened before dates were added reviewable.
    return [row for row in history if row.get("Date", day.isoformat()) == day.isoformat()]


def activity_summary(history):
    """Count checks, not unique questions: several activities allow retries."""
    summary = {}
    for row in history:
        problem_type = row.get("Problem type") or "Unspecified"
        key = (row["Activity"], problem_type)
        stats = summary.setdefault(key, {"Activity": row["Activity"], "Problem type": problem_type,
                                         "Checks": 0, "Correct": 0, "Incorrect": 0, "Stars": 0})
        stats["Checks"] += 1
        stats[row["Result"]] += 1
        stats["Stars"] += row["Result"] == "Correct"
    return list(summary.values())


def record_answer(activity, question, submitted, expected, correct, *,
                  difficulty="", explanation="", equations=None, diagrams=None, problem_type=""):
    """Snapshot one valid answer check, called only in submission handlers."""
    session_code()
    history = st.session_state.setdefault(HISTORY_KEY, [])
    history.append(deepcopy({
        "Date": progress_date().isoformat(),
        "Activity": activity, "Question": question, "Your answer": submitted,
        "Problem type": problem_type or "Unspecified",
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
    st.caption("Progress is saved on this browser for a fixed 24 hours. Your code stays until you delete it. Settings reset on refresh.")


def render_session_progress():
    today = progress_date()
    session_history = st.session_state.get(HISTORY_KEY, [])
    days = sorted({row.get("Date", today.isoformat()) for row in session_history} | {today.isoformat()}, reverse=True)
    if st.session_state.get("progress_day") not in days:
        st.session_state["progress_day"] = today.isoformat()
    if len(days) > 1:
        selected_day = st.selectbox("Progress date", days, key="progress_day",
                                    format_func=lambda value: f"{value} (today)" if value == today.isoformat() else value)
    else:
        selected_day = today.isoformat()
    day = date.fromisoformat(selected_day)
    st.title(f"Progress for {day.strftime('%B')} {day.day}, {day.year}")
    st.caption(f"Session code: **{session_code()}**")
    st.metric("Total stars in saved progress", f"⭐ {sum(row['Result'] == 'Correct' for row in session_history)}")
    history = daily_history(session_history, day)
    if not history:
        st.info("No answers checked on this date. Choose an activity to start practicing.")
        return
    view = st.radio("Progress view", ["Summary", "Review answers"], horizontal=True,
                    key="progress_view", label_visibility="collapsed")
    correct = sum(row["Result"] == "Correct" for row in history)
    st.write(f"{len(history)} answers checked · {correct} correct · {len(history) - correct} incorrect")
    if view == "Summary":
        rows = activity_summary(history)
        # A bounded number of rows per column keeps a varied class session compact.
        columns = st.columns(min(2, (len(rows) + 7) // 8))
        rows_per_column = (len(rows) + len(columns) - 1) // len(columns)
        for index, column in enumerate(columns):
            with column:
                st.table(rows[index * rows_per_column:(index + 1) * rows_per_column])
        st.caption("Selected date only · Checks include retries. Days change at midnight, New York time.")
        return
    render_answer_review(history)


def render_answer_review(history):
    """Show one selected answer so diagrams never create a stack of panels."""
    activities = list(dict.fromkeys(row["Activity"] for row in history))
    selected = st.selectbox("Activity", ["All activities", *activities], key="progress_activity_filter")
    options = [index for index in reversed(range(len(history)))
               if selected == "All activities" or history[index]["Activity"] == selected]
    index = st.selectbox("Answer to review", options,
                         format_func=lambda i: f"{i + 1}. {history[i]['Activity']} / {history[i].get('Problem type') or 'Unspecified'} — {history[i]['Result']}",
                         key="progress_answer_selection")
    row = history[index]
    if row["Difficulty"]:
        st.caption(str(row["Difficulty"]))
    st.write(row["Question"])
    for label, data_url in row["Diagrams"].items():
        st.image(base64.b64decode(data_url.split(",", 1)[1]), caption=label)
    answer_col, expected_col = st.columns(2)
    with answer_col:
        st.write("**Your answer**")
        st.write(row["Your answer"])
    with expected_col:
        st.write("**Correct answer**")
        st.write(row["Correct answer"])
    if row["Explanation"]:
        st.write(row["Explanation"])
    for equation in row["Equations"]:
        st.latex(equation)

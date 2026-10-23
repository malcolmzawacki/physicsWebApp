"""Browser-only persistence for the existing answer snapshots (no new scores)."""
import json
import math
from pathlib import Path
from datetime import date
import base64
import uuid

import streamlit as st
import streamlit.components.v1 as components

HISTORY_KEY = "practice_answer_history"
CODE_KEY = "practice_session_code"
STATE_KEY = "_progress_storage_state"

_storage = components.declare_component(
    "practice_progress_storage",
    path=str(Path(__file__).with_name("progress_storage_frontend")),
)


def _json_default(value):
    # Existing snapshots can contain NumPy scalars/arrays and tuples.
    if hasattr(value, "tolist"):
        return value.tolist()
    raise TypeError(f"Unsupported progress value: {type(value).__name__}")


def history_for_storage(known_ids=()):
    history = st.session_state.get(HISTORY_KEY, [])
    for row in history:
        if "_record_id" not in row:
            row["_record_id"] = uuid.uuid4().hex
    pending = [row for row in history if row["_record_id"] not in known_ids]
    return json.loads(json.dumps(pending, default=_json_default, allow_nan=False))


def valid_snapshot(snapshot):
    """Treat browser input as untrusted; never execute or unpickle saved data."""
    if not isinstance(snapshot, dict) or snapshot.get("version") != 1:
        return False
    code = snapshot.get("code", "")
    if not isinstance(code, str) or len(code) != 19 or not all(
        len(part) == 4 and part.isascii() and part.isdigit() for part in code.split("-")
    ):
        return False
    if not isinstance(snapshot.get("generation"), str) or not snapshot["generation"]:
        return False
    if type(snapshot.get("expires_at")) not in (int, float) or not math.isfinite(snapshot["expires_at"]):
        return False
    history = snapshot.get("history")
    if not isinstance(history, list):
        return False
    ids = set()
    for row in history:
        if not isinstance(row, dict):
            return False
        record_id = row.get("_record_id")
        if not isinstance(record_id, str) or not record_id or record_id in ids:
            return False
        ids.add(record_id)
        if not isinstance(row.get("Activity"), str) or row.get("Result") not in ("Correct", "Incorrect"):
            return False
        if not all(key in row for key in ("Question", "Your answer", "Correct answer")):
            return False
        if not all(isinstance(row.get(key), str) for key in ("Date", "Difficulty", "Explanation")):
            return False
        try:
            date.fromisoformat(row["Date"])
        except ValueError:
            return False
        if not isinstance(row.get("Equations"), list) or not isinstance(row.get("Diagrams"), dict):
            return False
        if not all(isinstance(value, str) for value in row["Equations"]):
            return False
        for label, image in row["Diagrams"].items():
            if not isinstance(label, str) or not isinstance(image, str) or not image.startswith("data:image/png;base64,"):
                return False
            try:
                base64.b64decode(image.split(",", 1)[1], validate=True)
            except ValueError:
                return False
    return True


def accept_snapshot(snapshot):
    """Merge late hydration with new work; a reset generation discards old work."""
    if not valid_snapshot(snapshot):
        return False
    previous = st.session_state.get(STATE_KEY)
    local = history_for_storage()
    if previous is None or previous["generation"] == snapshot["generation"]:
        known = {row["_record_id"] for row in snapshot["history"]}
        history = snapshot["history"] + [row for row in local if row["_record_id"] not in known]
    else:
        history = snapshot["history"]
    changed = (history != local or st.session_state.get(CODE_KEY) != snapshot["code"])
    st.session_state[HISTORY_KEY] = history
    st.session_state[CODE_KEY] = snapshot["code"]
    st.session_state[STATE_KEY] = snapshot
    return changed


@st.fragment(run_every="30s")
def render_progress_storage():
    """Mounted on every route, after submissions; poll expiry and other tabs too."""
    snapshot = st.session_state.get(STATE_KEY)
    try:
        known_ids = ({row["_record_id"] for row in snapshot["history"]}
                     if snapshot and st.session_state.get("_progress_storage_saved", True) else set())
        history = history_for_storage(known_ids)
    except (TypeError, ValueError):
        st.warning("Progress could not be saved in this browser. This session still works.")
        return
    # Send only new records. In particular, do not retransmit saved diagrams on
    # every polling tick over the school's connection.
    metadata = {key: value for key, value in snapshot.items() if key != "history"} if snapshot else None
    event = _storage(snapshot=metadata, history=history,
                     key="practice_progress_browser", default=None)
    if isinstance(event, dict) and event.get("snapshot"):
        # Component values persist across reruns. Consume each response only once.
        if event != st.session_state.get("_progress_storage_event"):
            st.session_state["_progress_storage_event"] = event
            st.session_state["_progress_storage_saved"] = event.get("saved", False)
            if accept_snapshot(event["snapshot"]):
                st.rerun()
    # Midnight changes the selected default day even on a page left open overnight.
    from utils.session_progress import progress_date
    day = progress_date().isoformat()
    previous_day = st.session_state.get("_progress_storage_day", day)
    st.session_state["_progress_storage_day"] = day
    if previous_day != day:
        st.session_state.pop("progress_day", None)
        st.rerun()

import importlib
import importlib.util
from pathlib import Path
import streamlit as st

from config import AUTHOR_MODE
st.set_page_config(page_title="Physics Practice", layout="wide")

COURSE_LEVELS = (
    ("middle", "Middle School", 0),
    ("high", "High School", 1),
    ("college", "College Preview", 2),
)
COURSE_LEVEL_LABELS = {key: label for key, label, _ in COURSE_LEVELS}
COURSE_LEVEL_RANKS = {key: rank for key, _, rank in COURSE_LEVELS}

BASE_DIR = Path(__file__).resolve().parent
FILE_PREFIX = "file:"
HANDLER_CACHE = {}

SECTIONS = (
    "Foundations",
    "Kinematics",
    "Dynamics",
    "Momentum",
    "Energy",
    "Waves",
    "Chemistry",
    "Labs",
)

ACTIVITIES = {
    "Foundations": {
        "Algebra": {"handler": "file:app_pages/1_0.1.1_Math_Skills.py::algebra.main", "min_level": "middle"},
        "Scientific Notation": {
            "handler": "file:app_pages/1_0.1.1_Math_Skills.py::sci_notate.main",
            "min_level": "middle",
        },
        "Arithmetic": {"handler": "file:app_pages/1_0.1.1_Math_Skills.py::arithmetic.main", "min_level": "middle"},
    },
    "Kinematics": {
        "Distance & Displacement": {
            "handler": "file:app_pages/1_1.1.0_Vectors_and_Displacement.py::dist_disp.distance_displacement",
            "min_level": "middle",
        },
        "Vector Practice": {
            "handler": "file:app_pages/1_1.1.0_Vectors_and_Displacement.py::vectors.vector_practice",
            "min_level": "middle",
        },
        "Constant Motion": {
            "handler": "file:app_pages/1_1.1.1_Motion.py::constant_motion",
            "min_level": "middle",
        },
        "Accelerated Motion": {
            "handler": "file:app_pages/1_1.1.1_Motion.py::accelerated_motion",
            "min_level": "middle",
        },
        "Types of Motion Graphs": {
            "handler": "file:app_pages/1_1.1.1_Motion.py::motion_graph_types",
            "min_level": "middle",
        },
        "Matching Motion Graphs": {
            "handler": "file:app_pages/1_1.1.1_Motion.py::motion_graph_matching",
            "min_level": "middle",
        },
        "Projectiles": {"handler": "file:app_pages/1_1.1.1_Motion.py::projectiles", "min_level": "middle"},
        "Rotational Kinematics": {
            "handler": "file:app_pages/1_1.1.2_Rotational_Motion.py::rotational_kinematics",
            "min_level": "high",
        },
    },
    "Dynamics": {
        "Newton's Second Law": {"handler": "file:app_pages/1_2.1_Forces.py::newtons_2nd", "min_level": "middle"},
        "Center of Mass": {"handler": "file:app_pages/1_2.1_Forces.py::center_of_mass", "min_level": "middle"},
        "Tension": {"handler": "file:app_pages/1_2.1_Forces.py::tension", "min_level": "middle"},
        "Atwood Machines": {"handler": "file:app_pages/1_2.1_Forces.py::atwood", "min_level": "high"},
        "Inclined Planes": {"handler": "file:app_pages/1_2.1_Forces.py::inclines", "min_level": "high"},
    },
    "Momentum": {
        "Momentum": {"handler": "file:app_pages/1_4.1_Momentum_and_Impulse.py::momentum", "min_level": "middle"},
        "Impulse": {"handler": "file:app_pages/1_4.1_Momentum_and_Impulse.py::impulse", "min_level": "middle"},
        "Collisions": {"handler": "file:app_pages/1_4.1_Momentum_and_Impulse.py::collisions", "min_level": "middle"},
    },
    "Energy": {
        "Types of Energy": {"handler": "file:app_pages/1_6.1_Energy.py::energy_basics_page", "min_level": "middle"},
        "Conservation of Energy": {
            "handler": "file:app_pages/1_6.1_Energy.py::energy_conserv_page",
            "min_level": "middle",
        },
        "Thermal Energy": {"handler": "file:app_pages/1_6.1_Energy.py::thermal_energy_page", "min_level": "middle"},
        "Friction and Distance": {
            "handler": "file:app_pages/1_6.1_Energy.py::friction_distance_page",
            "min_level": "middle",
        },
    },
    "Waves": {
        "Wave Properties": {"handler": "file:app_pages/1_7.1_Waves.py::wave_properties", "min_level": "middle"},
        "Harmonics": {"handler": "file:app_pages/1_7.1_Waves.py::Harmonics", "min_level": "middle"},
        "deciBel Scale": {"handler": "file:app_pages/1_7.1_Waves.py::deciBel_practice", "min_level": "middle"},
    },
    "Chemistry": {
        "Compound Names Practice": {
            "handler": "file:app_pages/1_Chem-_Compound_Names.py::practice_quiz_page",
            "min_level": "high",
        },
        "Compound Formula Explorer": {
            "handler": "file:app_pages/1_Chem-_Compound_Names.py::create_exploration_page",
            "min_level": "high",
        },
        "Stoichiometry Practice": {
            "handler": "file:app_pages/1_Chem-_Stoichiometry.py::stoichiometry_practice_page",
            "min_level": "high",
        },
        "Stoichiometry Explorer": {
            "handler": "file:app_pages/1_Chem-_Stoichiometry.py::stoichiometry_explorer_page",
            "min_level": "high",
        },
    },
    "Labs": {
        "Roulette": {"handler": "file:app_pages/1_0.0_Test_Page.py::roulette", "min_level": "middle"},
        "Reverse Engineering": {"handler": "file:app_pages/1_0.0_Test_Page.py::planner_tab", "min_level": "middle"},
    },
}

if "router_section" not in st.session_state:
    st.session_state.router_section = "root"
if "router_activity" not in st.session_state:
    st.session_state.router_activity = None


def set_section(section: str) -> None:
    st.session_state.router_section = section
    st.session_state.router_activity = None


def set_activity(activity: str) -> None:
    st.session_state.router_activity = activity


def level_rank(level_key: str) -> int:
    return COURSE_LEVEL_RANKS.get(level_key, 1)


def activity_visible(activity_meta: dict, current_level: str) -> bool:
    min_level = activity_meta.get("min_level", "middle")
    return level_rank(current_level) >= level_rank(min_level)


def _resolve_attr(obj, path: str):
    value = obj
    for part in path.split("."):
        value = getattr(value, part)
    return value


def _load_module_from_path(path: Path):
    key = str(path)
    if key in HANDLER_CACHE:
        return HANDLER_CACHE[key]
    module_name = f"file_module_{abs(hash(key))}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    HANDLER_CACHE[key] = module
    return module


def resolve_handler(handler: str):
    if handler.startswith(FILE_PREFIX):
        payload = handler[len(FILE_PREFIX) :]
        path_str, callable_path = payload.split("::", 1)
        module_path = (BASE_DIR / path_str).resolve()
        module = _load_module_from_path(module_path)
        return _resolve_attr(module, callable_path)
    module_name, func_path = handler.split(":", 1)
    module = importlib.import_module(module_name)
    return _resolve_attr(module, func_path)


def validate_activity_handlers() -> list[str]:
    errors = []
    for section, activities in ACTIVITIES.items():
        for name, meta in activities.items():
            handler = meta.get("handler")
            if not handler:
                errors.append(f"{section} / {name}: missing handler")
                continue
            try:
                resolve_handler(handler)
            except Exception as exc:
                errors.append(f"{section} / {name}: {handler} -> {exc}")
    return errors


with st.sidebar:
    st.header("Directory")
    level_key = st.selectbox(
        "Course level",
        options=[key for key, _, _ in COURSE_LEVELS],
        format_func=lambda key: COURSE_LEVEL_LABELS.get(key, key),
        key="nav_level",
    )
    if AUTHOR_MODE:
        st.warning("AUTHOR MODE ENABLED")

    if st.session_state.router_section == "root":
        st.subheader("Main areas")
        for section in SECTIONS:
            if st.button(section, use_container_width=True):
                set_section(section)
                st.rerun()
    else:
        st.subheader(st.session_state.router_section)
        if st.button("Back to Main", use_container_width=True):
            set_section("root")
            st.rerun()

        section = st.session_state.router_section
        activities = ACTIVITIES.get(section, {})
        visible = [
            name
            for name, meta in activities.items()
            if activity_visible(meta, level_key)
        ]
        if not visible:
            st.caption("No activities available for this level yet.")
        for activity in visible:
            if st.button(activity, use_container_width=True):
                set_activity(activity)
                st.rerun()

if AUTHOR_MODE:
    handler_errors = validate_activity_handlers()
    if handler_errors:
        st.sidebar.warning("Activity handler issues detected:")
        for error in handler_errors:
            st.sidebar.write(f"- {error}")

section = st.session_state.router_section
activity = st.session_state.router_activity

if section == "root":
    st.title("Physics Practice")
    st.write("Choose a main area from the sidebar to get started.")
    st.write(
        "Each area has its own sidebar menu so students see only the next level of options."
    )
else:
    st.title(section)
    activities = ACTIVITIES.get(section, {})
    visible = [
        name
        for name, meta in activities.items()
        if activity_visible(meta, level_key)
    ]
    if activity is None:
        if not visible:
            st.info("No activities available here for this level yet.")
        else:
            st.write("Select an activity from the sidebar.")
    else:
        if activity not in activities:
            st.warning("That activity is not available here.")
        elif not activity_visible(activities[activity], level_key):
            st.info("That activity is not available at this course level.")
        else:
            handler = activities[activity].get("handler")
            if not handler:
                st.error("Activity handler is missing.")
            else:
                resolve_handler(handler)()

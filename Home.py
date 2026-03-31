import importlib
import importlib.util
from pathlib import Path
import streamlit as st

from config import AUTHOR_MODE
st.set_page_config(page_title="Physics Practice", layout="wide")

COURSE_LEVELS = (
    ("high", "High School", 0),
    ("advanced", "Advanced", 1),
)
COURSE_LEVEL_LABELS = {key: label for key, label, _ in COURSE_LEVELS}
COURSE_LEVEL_RANKS = {key: rank for key, _, rank in COURSE_LEVELS}

BASE_DIR = Path(__file__).resolve().parent
FILE_PREFIX = "file:"
HANDLER_CACHE = {}

SECTIONS = (
    "Foundations",
    "Kinematics",
    "Rotation (Advanced)",
    "Dynamics",
    "Momentum",
    "Energy",
    "⚡Electricity⚡",
    "Waves",
    "Chemistry",
    "Labs",
)

ACTIVITIES = {
    "Foundations": {
        "Algebra": {"handler": "file:app_pages/1_0.1.1_Math_Skills.py::algebra.main", "min_level": "high"},
        "Scientific Notation": {
            "handler": "file:app_pages/1_0.1.1_Math_Skills.py::sci_notate.main",
            "min_level": "high",
        },
        "Arithmetic": {"handler": "file:app_pages/1_0.1.1_Math_Skills.py::arithmetic.main", "min_level": "high"},
        "Vector Practice": {
            "handler": "file:app_pages/1_1.1.0_Vectors_and_Displacement.py::vectors.vector_practice",
            "min_level": "high",
        },
    },
    "Kinematics": {
        "Distance & Displacement": {
            "handler": "file:app_pages/1_1.1.0_Vectors_and_Displacement.py::dist_disp.distance_displacement",
            "min_level": "high",
        },
        "Constant Motion": {
            "handler": "file:app_pages/1_1.1.1_Motion.py::constant_motion",
            "min_level": "high",
        },
        "Accelerated Motion": {
            "handler": "file:app_pages/1_1.1.1_Motion.py::accelerated_motion",
            "min_level": "high",
        },
        "Types of Motion Graphs": {
            "handler": "file:app_pages/1_1.1.1_Motion.py::motion_graph_types",
            "min_level": "high",
        },
        "Matching Motion Graphs": {
            "handler": "file:app_pages/1_1.1.1_Motion.py::motion_graph_matching",
            "min_level": "high",
        },
        "Projectiles": {"handler": "file:app_pages/1_1.1.1_Motion.py::projectiles", "min_level": "high"},
    },
    "Rotation (Advanced)": {
        "Rotational Kinematics": {
            "handler": "file:app_pages/1_1.1.2_Rotational_Motion.py::rotational_kinematics",
            "min_level": "advanced",
        },
        "Torque": {
            "handler": "file:app_pages/1_1.1.3_Torque.py::torque_activity",
            "min_level": "advanced",
        },
    },
    "Dynamics": {
        "Newton's Second Law": {"handler": "file:app_pages/1_2.1_Forces.py::newtons_2nd", "min_level": "high"},
        "Center of Mass": {"handler": "file:app_pages/1_2.1_Forces.py::center_of_mass", "min_level": "advanced"},
        "Tension": {"handler": "file:app_pages/1_2.1_Forces.py::tension", "min_level": "advanced"},
        "Atwood Machines": {"handler": "file:app_pages/1_2.1_Forces.py::atwood", "min_level": "advanced"},
        "Inclined Planes": {"handler": "file:app_pages/1_2.1_Forces.py::inclines", "min_level": "advanced"},
    },

    "Momentum": {
        "Momentum": {"handler": "file:app_pages/1_4.1_Momentum_and_Impulse.py::momentum", "min_level": "high"},
        "Impulse": {"handler": "file:app_pages/1_4.1_Momentum_and_Impulse.py::impulse", "min_level": "high"},
        "Collisions": {"handler": "file:app_pages/1_4.1_Momentum_and_Impulse.py::collisions", "min_level": "high"},
    },
    "Energy": {
        "Types of Energy": {"handler": "file:app_pages/1_6.1_Energy.py::energy_basics_page", "min_level": "high"},
        "Conservation of Energy": {
            "handler": "file:app_pages/1_6.1_Energy.py::energy_conserv_page",
            "min_level": "high",
        },
        "Thermal Energy": {"handler": "file:app_pages/1_6.1_Energy.py::thermal_energy_page", "min_level": "high"},
        "Friction and Distance": {
            "handler": "file:app_pages/1_6.1_Energy.py::friction_distance_page",
            "min_level": "high",
        },
    },

    "⚡Electricity⚡": {
        "Static Electricity": {
            "min_level": "high",
            "items": {
                "Charging by Friction": {
                    "handler": "file:app_pages/1_3.1_Static_Electricity.py::charging_by_friction_page",
                    "min_level": "high",
                },
                "Charging by Conduction": {
                    "handler": "file:app_pages/1_3.2_Static_Electricity_Conduction.py::charging_by_conduction_page",
                    "min_level": "high",
                },
                "Charging by Induction": {
                    "handler": "file:app_pages/1_3.3_Static_Electricity_Induction.py::charging_by_induction_page",
                    "min_level": "high",
                },
            },
        },
        "Current Electricity": {
            "min_level": "high",
            "items": {
                "Circuit Ohm's Law": {
                    "handler": "file:app_pages/1_3.4_Current_Electricity_Circuits.py::current_electricity_circuits_page",
                    "min_level": "high",
                },
                "Series and Parallel Circuits": {
                    "handler": "file:app_pages/1_3.5_Current_Electricity_Series_Parallel.py::current_electricity_series_parallel_page",
                    "min_level": "high",
                },
            },
        },
    },

    "Waves": {
        "Wave Properties": {"handler": "file:app_pages/1_7.1_Waves.py::wave_properties", "min_level": "high"},
        "Harmonics": {"handler": "file:app_pages/1_7.1_Waves.py::Harmonics", "min_level": "high"},
        "deciBel Scale": {"handler": "file:app_pages/1_7.1_Waves.py::deciBel_practice", "min_level": "high"},
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
        "Roulette": {"handler": "file:app_pages/1_0.0_Test_Page.py::roulette", "min_level": "high"},
        "Reverse Engineering": {"handler": "file:app_pages/1_0.0_Test_Page.py::planner_tab", "min_level": "high"},
    },
}

if "router_section" not in st.session_state:
    st.session_state.router_section = "root"
if "router_activity" not in st.session_state:
    st.session_state.router_activity = None
if "router_group" not in st.session_state:
    st.session_state.router_group = None


def set_section(section: str) -> None:
    st.session_state.router_section = section
    st.session_state.router_group = None
    st.session_state.router_activity = None


def set_group(group: str | None) -> None:
    st.session_state.router_group = group
    st.session_state.router_activity = None


def set_activity(activity: str) -> None:
    st.session_state.router_activity = activity


def level_rank(level_key: str) -> int:
    return COURSE_LEVEL_RANKS.get(level_key, 1)


def entry_is_group(entry_meta: dict) -> bool:
    return isinstance(entry_meta, dict) and isinstance(entry_meta.get("items"), dict)


def activity_visible(activity_meta: dict, current_level: str) -> bool:
    min_level = activity_meta.get("min_level", "high")
    if level_rank(current_level) < level_rank(min_level):
        return False
    if entry_is_group(activity_meta):
        return any(activity_visible(child_meta, current_level) for child_meta in activity_meta["items"].values())
    return True


def get_visible_entry_names(entries: dict, current_level: str) -> list[str]:
    return [
        name
        for name, meta in entries.items()
        if activity_visible(meta, current_level)
    ]


def get_current_entries(section: str, group: str | None = None) -> dict:
    activities = ACTIVITIES.get(section, {})
    if group is None:
        return activities
    group_meta = activities.get(group, {})
    if not entry_is_group(group_meta):
        return {}
    return group_meta["items"]


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

    def walk(entries: dict, trail: list[str]) -> None:
        for name, meta in entries.items():
            path = trail + [name]
            if entry_is_group(meta):
                walk(meta["items"], path)
                continue
            handler = meta.get("handler")
            if not handler:
                errors.append(f"{' / '.join(path)}: missing handler")
                continue
            try:
                resolve_handler(handler)
            except Exception as exc:
                errors.append(f"{' / '.join(path)}: {handler} -> {exc}")

    for section, activities in ACTIVITIES.items():
        walk(activities, [section])
    return errors


with st.sidebar:
    st.header("Directory")
    level_options = [key for key, _, _ in COURSE_LEVELS]
    if st.session_state.get("nav_level") not in level_options:
        st.session_state["nav_level"] = level_options[0]
    level_key = st.selectbox(
        "Course level",
        options=level_options,
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
        section = st.session_state.router_section
        group = st.session_state.router_group

        if group is None:
            if st.button("Back to Main", use_container_width=True):
                set_section("root")
                st.rerun()
        else:
            st.caption(group)
            if st.button("Back to Section", use_container_width=True):
                set_group(None)
                st.rerun()

        entries = get_current_entries(section, group)
        visible = get_visible_entry_names(entries, level_key)
        if not visible:
            st.caption("No activities available for this level yet.")
        for entry_name in visible:
            entry_meta = entries[entry_name]
            if entry_is_group(entry_meta):
                if st.button(entry_name, use_container_width=True):
                    set_group(entry_name)
                    st.rerun()
            else:
                if st.button(entry_name, use_container_width=True):
                    set_activity(entry_name)
                    st.rerun()

if AUTHOR_MODE:
    handler_errors = validate_activity_handlers()
    if handler_errors:
        st.sidebar.warning("Activity handler issues detected:")
        for error in handler_errors:
            st.sidebar.write(f"- {error}")

section = st.session_state.router_section
group = st.session_state.router_group
activity = st.session_state.router_activity

if section == "root":
    st.title("Physics Practice")
    st.write("Choose a main area from the sidebar to get started.")
    st.write(
        "Each area has its own sidebar menu so students see only the next level of options."
    )
else:
    st.title(section)
    if group is not None:
        st.subheader(group)
    entries = get_current_entries(section, group)
    visible = get_visible_entry_names(entries, level_key)
    if activity is None:
        if not visible:
            st.info("No activities available here for this level yet.")
        else:
            if any(entry_is_group(entries[name]) for name in visible):
                st.write("Select a subpage from the sidebar.")
            else:
                st.write("Select an activity from the sidebar.")
    else:
        if activity not in entries:
            st.warning("That activity is not available here.")
        elif not activity_visible(entries[activity], level_key):
            st.info("That activity is not available at this course level.")
        else:
            handler = entries[activity].get("handler")
            if not handler:
                st.error("Activity handler is missing.")
            else:
                resolve_handler(handler)()

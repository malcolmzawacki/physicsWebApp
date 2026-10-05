"""Bounded pilot for student worksheets, independent of practice state."""
import io
import logging
import time

import streamlit as st

from utils.generators.kinematics.linear_motion_generator import LinearMotionGenerator
from utils.generators.kinematics.const_motion_generator import ConstantMotionGenerator
from utils.generators.kinematics.dist_disp_generator import DistDispGenerator
from utils.generators.kinematics.projectile_generator import ProjectileGenerator
from utils.generators.kinematics.relative_motion_generator import RelativeMotionGenerator
from utils.generators.force_generator import ForceGenerator
from utils.generators.forces.center_of_mass_generator import CenterOfMassGenerator
from utils.generators.forces.tension_generator import TensionGenerator
from utils.generators.forces.atwood_generator import AtwoodGenerator
from utils.generators.forces.incline_generator import InclineGenerator
from utils.solve_for import MIXED, target_options
from xtrct_docs.document_creator import create_doc
from xtrct_docs.payload_adapter import DocumentGenerator
from xtrct_docs.pdf_converter import PdfConversionError, docx_to_pdf, libreoffice_path
from xtrct_docs.pdf_preview import page_summary, render_page
from xtrct_docs.motion_graph_adapter import WorksheetMotionGraphs
from xtrct_docs.matching_graph_adapter import WorksheetMatchingGraphs

PREFIX = "kinematics_worksheet_"
ACTIVITIES = {"Accelerated Motion": LinearMotionGenerator, "Constant Motion": ConstantMotionGenerator,
              "Distance & Displacement": DistDispGenerator, "Projectiles": ProjectileGenerator,
              "Relative Motion": RelativeMotionGenerator, "Types of Motion Graphs": WorksheetMotionGraphs,
              "Matching Motion Graphs": WorksheetMatchingGraphs}
KINEMATICS_ACTIVITIES = tuple(ACTIVITIES)
FORCES_ACTIVITIES = {
    "Newton's Second Law": ForceGenerator, "Center of Mass": CenterOfMassGenerator,
    "Tension": TensionGenerator, "Atwood Machines": AtwoodGenerator,
    "Inclined Planes": InclineGenerator,
}
ACTIVITIES.update(FORCES_ACTIVITIES)
UNIT_ACTIVITIES = {"Kinematics": KINEMATICS_ACTIVITIES, "Forces": tuple(FORCES_ACTIVITIES)}
ACTIVITY_LEVELS = {name: "advanced" for name in ("Relative Motion", "Center of Mass", "Tension", "Atwood Machines", "Inclined Planes")}
WORKSHEET_DIFFICULTIES = {"Atwood Machines": ("Medium",), "Inclined Planes": ("Medium",)}


def activity_difficulties(activity):
    return WORKSHEET_DIFFICULTIES.get(activity, getattr(ACTIVITIES[activity], "DIFFICULTIES", ("Easy", "Medium", "Hard")))


# These prompts include all givens in text; diagrams remain available in practice.
TEXT_ONLY_ADAPTERS = {"Distance & Displacement", "Relative Motion", "Center of Mass", "Tension", "Atwood Machines"}


def available_activities(unit="Kinematics"):
    return [name for name in UNIT_ACTIVITIES[unit]
            if ACTIVITY_LEVELS.get(name, "high") == "high" or st.session_state.get("nav_level", "high") == "advanced"]
SPACING = {"Compact": 0.25, "Standard": 0.5, "Extra writing space": 1.0}


def _set_preview_page(page, prefix=PREFIX):
    result = st.session_state.get(prefix + "result")
    if result:
        result["selected_page"] = page


def generate_sections(requests):
    requests = [("Accelerated Motion", *r) if len(r) == 4 else r for r in requests]
    requests = [(activity, kind, getattr(ACTIVITIES.get(activity), "FIXED_DIFFICULTY", difficulty), target, count)
                for activity, kind, difficulty, target, count in requests]
    if not requests or len(requests) > 20:
        raise ValueError("Choose between 1 and 20 sections")
    total = 0
    for activity, kind, difficulty, target, count in requests:
        if activity not in ACTIVITIES:
            raise ValueError("Unsupported worksheet activity")
        generator = ACTIVITIES[activity]()
        if kind not in generator.get_problem_types() or difficulty not in activity_difficulties(activity):
            raise ValueError("Unsupported worksheet topic or difficulty")
        if type(count) is not int or not 1 <= count <= 20:
            raise ValueError("Unsupported question count")
        if target not in [MIXED] + [o["id"] for o in target_options(generator, kind, difficulty)]:
            raise ValueError("Unsupported worksheet target")
        total += count
    if total > 20:
        raise ValueError("Choose no more than 20 questions across all sections")
    sections = []
    generators = {}
    for activity, kind, difficulty, target, count in requests:
        if activity not in ACTIVITIES:
            raise ValueError("Unsupported worksheet activity")
        generator = ACTIVITIES[activity]()
        if activity not in generators:
            generators[activity] = generator
        generator = generators[activity]
        labels = {o["id"]: o["label"] for o in target_options(generator, kind, difficulty)}
        heading = f"{activity}: {kind} - {difficulty}"
        if getattr(generator, "FIXED_DIFFICULTY", None):
            heading = f"{activity}: {kind}"
        if target != MIXED:
            heading += f" - {labels[target]}"
        generated = DocumentGenerator(generator).section(heading, kind, difficulty, target, count=count, gap=0)()
        if activity in TEXT_ONLY_ADAPTERS:
            for section in generated:
                for problem in section["problems"]:
                    if activity == "Tension":
                        problem["optional_tension_diagram"] = problem["diagram_data"]
                        problem["question"] = problem.pop("worksheet_question")
                    problem["diagram_data"] = None
                    problem.pop("diagram_renderer", None)
                    if activity == "Distance & Displacement":
                        problem["question"] += "\n\nFind the total distance travelled, the magnitude of the net displacement, and its direction."
        if activity in FORCES_ACTIVITIES:
            for section in generated:
                for problem in section["problems"]:
                    if activity != "Tension":
                        problem["question"] += "\n\nUse g = 10 m/s² where needed."
                    if activity == "Center of Mass":
                        problem["question"] += " All coordinates are in meters."
        sections.extend(generated)
    return sections


def render_document(sections, spacing, answers, title="Kinematics Practice", diagrams=False, answer_boxes=True):
    if spacing not in SPACING or not 1 <= sum(len(s["problems"]) for s in sections) <= 20:
        raise ValueError("Unsupported worksheet length or spacing")
    sections = [{**section, "writing_space_inches": SPACING[spacing]} for section in sections]
    # Render-time copies preserve both answers and diagram specs when toggling layout.
    from xtrct_docs.tension_diagram import tension_inset
    sections = [{**section, "problems": [dict(problem) for problem in section["problems"]]} for section in sections]
    if diagrams:
        for section in sections:
            for problem in section["problems"]:
                if problem.get("optional_tension_diagram"):
                    problem.update(diagram_data=problem["optional_tension_diagram"],
                                   diagram_renderer=tension_inset, inset_diagram=True)
    output = io.BytesIO()
    create_doc(title, lambda: sections, 1, output_path=output, tables=answer_boxes,
               open_document=False, include_answer_key=answers, answer_key_new_page=True)
    return output.getvalue()


def build_worksheet(problem_type, difficulty, target, count, spacing, answers, *, sections=None):
    sections = generate_sections([(problem_type, difficulty, target, count)]) if sections is None else sections
    return render_document(sections, spacing, answers)


def _section_controls(prefix, unit="Kinematics"):
    activities = available_activities(unit)
    if st.session_state.get(prefix + "activity") not in activities:
        st.session_state[prefix + "activity"] = activities[0]
    activity = st.selectbox("Activity", activities, key=prefix + "activity")
    generator = ACTIVITIES[activity]()
    kinds = generator.get_problem_types()
    if "Mixed" in kinds:
        kinds = ["Mixed"] + [k for k in kinds if k != "Mixed"]
    if st.session_state.get(prefix + "kind") not in kinds:
        st.session_state[prefix + "kind"] = kinds[0]
    kind = st.selectbox("Worksheet problem type", kinds, key=prefix + "kind")
    levels = list(activity_difficulties(activity))
    if st.session_state.get(prefix + "difficulty") not in levels:
        st.session_state[prefix + "difficulty"] = levels[min(1, len(levels) - 1)]
    if getattr(generator, "FIXED_DIFFICULTY", None):
        difficulty = generator.FIXED_DIFFICULTY
        st.session_state[prefix + "difficulty"] = difficulty
        st.caption("Includes all six motion shapes: constant velocity, speeding up, and slowing down in both directions.")
    else:
        difficulty = st.selectbox("Worksheet difficulty", levels, disabled=len(levels) == 1, key=prefix + "difficulty")
    if activity == "Matching Motion Graphs":
        st.caption("Match position and velocity graphs using three distinct choices. Includes all six motion shapes.")
    labels = {MIXED: "Mixed practice", **{o["id"]: o["label"] for o in target_options(generator, kind, difficulty)}}
    if st.session_state.get(prefix + "target") not in labels:
        st.session_state[prefix + "target"] = MIXED
    target = st.selectbox("Worksheet solve for", list(labels), format_func=labels.get,
                          disabled=len(labels) == 1, key=prefix + "target")
    count = st.number_input("Number of questions", min_value=1, max_value=20, value=5, key=prefix + "count")
    return activity, kind, difficulty, target, count



def worksheet_shortcut(activity):
    if st.button("Create a worksheet", key="worksheet_shortcut_" + activity):
        unit = "Forces" if activity in FORCES_ACTIVITIES else "Kinematics"
        st.session_state[unit.lower() + "_worksheet_start_activity"] = activity
        st.session_state.router_section = "Dynamics" if unit == "Forces" else "Kinematics"
        st.session_state.router_group = None
        st.session_state.router_activity = "Create a worksheet"
        st.rerun()


def render_unit_worksheet(unit):
    """Shared builder with unit-scoped choices and session state; no global unit selector."""
    prefix = unit.lower() + "_worksheet_"
    start_activity = st.session_state.pop(prefix + "start_activity", None)
    if start_activity in available_activities(unit):
        # An explicit activity shortcut starts a fresh recipe for that activity.
        for key in list(st.session_state):
            if key.startswith(prefix):
                del st.session_state[key]
        st.session_state[prefix + "activity"] = start_activity
    st.subheader("Create a worksheet")
    with st.container():
        st.caption(f"Build {unit} practice with up to 20 questions in total. Add sections to combine topics from this unit.")
        section_ids = st.session_state.setdefault(prefix + "section_ids", [0])
        requests = []
        for position, section_id in enumerate(list(section_ids)):
            st.markdown(f"**Section {position + 1}**")
            requests.append(_section_controls(prefix if section_id == 0 else prefix + f"section_{section_id}_", unit))
            if len(section_ids) > 1 and st.button("Remove section", key=prefix + f"remove_{section_id}"):
                section_ids.remove(section_id)
                st.rerun()
        if st.button("Add section", key=prefix + "add", disabled=len(section_ids) >= 20):
            next_id = st.session_state.get(prefix + "next_section_id", 1)
            section_ids.append(next_id)
            st.session_state[prefix + "next_section_id"] = next_id + 1
            st.rerun()
        requests = tuple(requests)
        count = sum(request[4] for request in requests)
        st.caption(f"{count} / 20 questions across {len(requests)} section(s)")
        over_limit = count > 20
        if over_limit:
            st.warning("Reduce the question counts to 20 or fewer in total.")
        spacing = st.selectbox("Writing space", list(SPACING), index=1, key=prefix + "spacing")
        st.caption(f"Reserves {SPACING[spacing]:g} inches below each question. Page count depends on question length.")
        answers = st.checkbox("Include answer key at the end", value=True, key=prefix + "answers")
        diagrams = False
        if any(request[0] == "Tension" for request in requests):
            diagrams = st.checkbox("Include compact Tension diagrams", value=False, key=prefix + "diagrams")
            st.caption("Adds a wire-and-angle sketch beside each Tension question. Toggle and update layout to compare the same questions.")
        answer_boxes = st.checkbox("Include answer boxes", value=True, key=prefix + "answer_boxes",
                                   help="Show labeled answer boxes for questions with multiple answers. Writing space and the answer key are separate options.")
        settings = (requests, spacing, answers, diagrams, answer_boxes)
        available = bool(libreoffice_path())
        if not available:
            st.info("PDF conversion needs LibreOffice installed on the computer running this app. If it is installed in a custom location, set LIBREOFFICE_PATH to its executable and restart the app.")
        previous = st.session_state.get(prefix + "result")
        same_questions = bool(previous and previous.get("sections") and previous["settings"][0] == settings[0])
        layout_changed = same_questions and previous["settings"][1:] != settings[1:]
        action = "Update layout" if layout_changed else "Generate worksheet"
        if layout_changed:
            st.caption("Updating the layout keeps your questions and answers unchanged.")
        generate_column, download_column = st.columns(2)
        if generate_column.button(action, key=prefix + "generate", type="primary", disabled=not available or over_limit):
            st.session_state.pop(prefix + "result", None)
            started = time.perf_counter()
            progress = st.empty()
            progress.info("Preparing your worksheet…")
            with st.spinner("Working…"):
                try:
                    sections = previous["sections"] if layout_changed else generate_sections(requests)
                    document = render_document(sections, spacing, answers, title=f"{unit} Practice", diagrams=diagrams, answer_boxes=answer_boxes)
                    timings = {"document": time.perf_counter() - started}
                    result = {"settings": settings, "sections": sections, "docx": document, "pdf": None, "error": None, "timings": timings}
                    st.session_state[prefix + "result"] = result
                    if available:
                        try:
                            result["pdf"] = docx_to_pdf(document, on_stage=progress.info, timings=timings)
                        except PdfConversionError as exc:
                            result["error"] = str(exc)
                except Exception:
                    logging.getLogger(__name__).exception("Worksheet generation failed")
                    st.error("We couldn't create this worksheet. Please try again.")
                finally:
                    progress.empty()
                    logging.getLogger(__name__).warning("worksheet generation elapsed_seconds=%.3f", time.perf_counter() - started)
        result = st.session_state.get(prefix + "result")
        if not result:
            return
        if result["settings"] != settings:
            st.info("Settings changed. Update the layout to keep these questions." if layout_changed else
                    "Settings changed. Generate a new worksheet to download these choices.")
            return
        if result["error"]:
            st.warning(result["error"])
            if st.button("Retry PDF conversion", key=prefix + "retry", disabled=not available):
                try:
                    with st.spinner("Preparing PDF…"):
                        progress = st.empty()
                        try:
                            result["pdf"] = docx_to_pdf(result["docx"], on_stage=progress.info, timings=result.setdefault("timings", {}))
                        finally:
                            progress.empty()
                    result["error"] = None
                    st.rerun()
                except PdfConversionError as exc:
                    result["error"] = str(exc)
                    st.error(str(exc))
        if result["pdf"]:
            download_column.download_button("Download worksheet", result["pdf"], f"{unit.lower()}-practice.pdf", "application/pdf",
                                            key=prefix + "pdf", on_click="ignore", type="primary")
            try:
                if "summary" not in result:
                    with st.spinner("Preparing your preview…"):
                        preview_started = time.perf_counter()
                        result["summary"] = page_summary(result["pdf"])
                        result["preview_png"] = render_page(result["pdf"], 0)
                        result["preview_page"] = 0
                        result.setdefault("timings", {})["preview"] = time.perf_counter() - preview_started
                        result["timings"]["total"] = sum(result["timings"].get(stage, 0) for stage in ("document", "wait", "conversion", "preview"))
                        logging.getLogger(__name__).warning("worksheet timings %s", result["timings"])
                summary = result["summary"]
                st.write(f"**{count} questions · {summary['total']} total pages**")
                st.caption(f"Question pages: {summary['questions']} · Answer-key pages: {summary['answers']}")
                if st.checkbox("Show print preview", value=True, key=prefix + "preview"):
                    last_page = summary["total"] - 1
                    page = max(0, min(result.get("selected_page", 0), last_page))
                    first, previous, indicator, next_page, last = st.columns([1, 1, 2, 1, 1])
                    for column, label, name, destination, disabled in (
                        (first, "⏮", "First page", 0, page == 0),
                        (previous, "◀", "Previous page", page - 1, page == 0),
                        (next_page, "▶", "Next page", page + 1, page == last_page),
                        (last, "⏭", "Last page", last_page, page == last_page),
                    ):
                        column.button(label, key=prefix + name, help=name,
                                      disabled=disabled, use_container_width=True,
                                      on_click=_set_preview_page, args=(destination, prefix))
                    indicator.markdown(f"**Page {page + 1} of {summary['total']}**")
                    if result.get("preview_page") != page:
                        result["preview_png"] = render_page(result["pdf"], page)
                        result["preview_page"] = page
                    st.image(result["preview_png"], caption=f"Page {page + 1} of the downloadable PDF")
            except Exception:
                logging.getLogger(__name__).exception("PDF preview failed")
                st.info("Preview is unavailable. You can still download the PDF.")

            from config import AUTHOR_MODE
            if AUTHOR_MODE and result.get("timings"):
                st.caption("Timing (seconds): " + " · ".join(f"{name}: {seconds:.2f}" for name, seconds in result["timings"].items()))


def render_kinematics_worksheet():
    render_unit_worksheet("Kinematics")


def render_forces_worksheet():
    render_unit_worksheet("Forces")


# Compatibility for callers of the original pilot entry point.
render_accelerated_worksheet = render_kinematics_worksheet

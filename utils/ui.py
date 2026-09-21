"""Streamlit interface helpers that connect problem generators to the UI layer."""

from utils.grading import answer_matches, DIFFICULTY_STARS
from utils.layout_config import question_columns
from utils.ui_components import equation_controls
from utils.solve_for import generate_selected, select_target, MIXED
import pandas as pd
import streamlit as st

from config import AUTHOR_MODE
from utils.word_lists import random_correct_message, random_error_message
from utils.ui_state import State
from utils.ui_components import (render_header, build_performance_table, performance_expander, draw_answer_inputs, render_button_options, render_dropdown_options, render_hints, init_performance, record_performance, show_equations_expander)
from utils.problem_payload import payload_from_dict, ProblemPayload, ProblemPayloadError


class Interface:
    """High-level controller that wires generators into the Streamlit UI."""

    def __init__(
        self,
        prefix: str,
        title: str,
        generator: object,
        problem_type_dict: dict | list[str] | None,
        difficulties: list,
        type_weight: bool = False,
    ) -> None:
        """Store generator metadata and configure the namespaced session state."""
        self.prefix = prefix
        self.title = title
        self.generator = generator
        if isinstance(problem_type_dict, dict):
            self.problem_type_dict = problem_type_dict
            self.problem_types = list(problem_type_dict.keys())
        elif isinstance(problem_type_dict, list):
            self.problem_type_dict = None
            self.problem_types = list(problem_type_dict)
        else:
            self.problem_type_dict = None
            inferred_types = self._infer_problem_types()
            if not inferred_types:
                raise ValueError(
                    "Interface requires a problem type list or a generator that implements get_problem_types()."
                )
            self.problem_types = inferred_types
        self.difficulties = difficulties
        self.type_weight = type_weight
        self.state = State(prefix)

    def _infer_problem_types(self) -> list[str]:
        """Ask the generator for its supported problem types when none were provided."""
        getter = getattr(self.generator, "get_problem_types", None)
        if callable(getter):
            try:
                types = getter()
            except Exception:
                return []
            if isinstance(types, list):
                return list(types)
            if types is None:
                return []
            try:
                return list(types)
            except TypeError:
                return []
        return []

    # region performance
    def clear_performance_dataframe(self) -> dict:
        """Create a fresh performance dict (pure) using ui_components helper."""
        return init_performance([self.problem_id(label) for label in self.problem_types], self.difficulties)

    def create_performance_dataframe(self) -> pd.DataFrame:
        performance = self.state.get("performance")
        ordered = list(self.difficulties)
        labels = {self.problem_id(label): label for label in self.problem_types}
        displayed = {labels.get(key, key): value for key, value in performance.items()}
        return build_performance_table(displayed, ordered)

    def problem_id(self, label: str) -> str:
        """Use an explicit stable metadata ID; retain legacy label keys by default."""
        getter = getattr(self.generator, "get_problem_metadata", None)
        metadata = getter(label) if callable(getter) else {}
        return metadata.get("id", label)

    def update_performance(self, problem_type: str, difficulty: str, is_correct: bool) -> None:
        performance = self.state.get("performance")
        new_perf = record_performance(performance, self.problem_id(problem_type), difficulty, is_correct)
        self.state.set("performance", new_perf)

    def performance_dropdown(self) -> None:
        performance_df = self.create_performance_dataframe()
        performance_expander(performance_df)
    # endregion

    def initialize_session_state(self) -> None:
        """Ensure all interface-managed session-state keys exist with sensible defaults."""
        none_vars = [
            "current_question",
            "correct_answer",
            "unit",
            "user_answer",
            "submitted",
            "difficulty",
            "problem_type",
            "movements",
        ]
        zero_vars = ["question_id", "stars"]

        for var in none_vars:
            self.state.ensure(var, None)
        for var in zero_vars:
            self.state.ensure(var, 0)
        # Performance tracking
        # Lazily initialize performance dict to avoid resetting on reruns
        self.state.ensure_lazy("performance", self.clear_performance_dataframe)
        # Migrate existing display-label history when a generator adopts IDs or
        # declares old labels as aliases. Never discard prior attempts.
        performance = self.state.get("performance")
        getter = getattr(self.generator, "get_problem_metadata", None)
        for label in self.problem_types:
            identity = self.problem_id(label)
            metadata = getter(label) if callable(getter) else {}
            for old in [label, *metadata.get("aliases", [])]:
                if old != identity and old in performance:
                    previous = performance.pop(old)
                    target = performance.setdefault(identity, {})
                    for difficulty, stats in previous.items():
                        bucket = target.setdefault(difficulty, {"attempts": 0, "correct": 0})
                        for metric in ("attempts", "correct"):
                            bucket[metric] += stats.get(metric, 0)
        # Equation level toggle default
        if self.state.get("level") is None:
            self.state.set("level", False)

    def header_component(self) -> None:
        """Render the title banner along with any earned star count."""
        stars = self.state.get("stars", 0)
        render_header(self.title, stars if stars else None)

    # region unified helpers
    def add_diagram_smart(self, expander_title: str = "Diagram", **kwargs) -> None:
        """Render a generator-provided diagram in an expander when diagram data is available."""
        diagram_data = self.state.get("diagram_data")
        if diagram_data is None:
            return
        expanded = kwargs.get("expanded", False)
        if not isinstance(expanded, bool):
            expanded = bool(expanded)
        problem_type = self.state.get("problem_type")
        difficulty = self.state.get("difficulty")
        if hasattr(diagram_data, "savefig"):
            with st.expander(expander_title, expanded=expanded):
                st.pyplot(diagram_data)
            return
        renderer = self.get_current_problem_features().get("diagram_renderer")
        if callable(renderer):
            fig = renderer(diagram_data)
            if fig is not None:
                with st.expander(expander_title, expanded=expanded):
                    st.pyplot(fig)
            return
        if hasattr(self.generator, "generate_diagram"):
            try:
                fig = self.generator.generate_diagram(diagram_data, problem_type, difficulty)
                if fig is not None:
                    with st.expander(expander_title, expanded=expanded):
                        st.pyplot(fig)
            except Exception as e:
                if AUTHOR_MODE:
                    st.exception(e)

    def get_current_problem_features(self) -> dict:
        """Collect optional features saved in session state for the current question."""
        payload = self.state.get("payload")
        if payload is None:
            return {}
        return {**payload.extras, "diagram_data": payload.diagram_data,
                "hints": payload.hints, "button_options": payload.button_options}

    def show_hints(self) -> None:
        """Display ordered hints, if any were supplied by the generator."""
        render_hints(self.state.get("hints", []))

    def show_problem_tags(self, tags: list) -> None:
        """Render topic tags for the current question when generators provide them."""
        if tags:
            st.caption(" · ".join(tags))

    def generate_question_once(self, problem_type: str, difficulty: str) -> None:
        """Fetch a new problem from the generator, normalize it, and trigger a rerun."""
        try:
            result = generate_selected(self.generator, problem_type, difficulty, self.state.get("solve_for", MIXED))
        except Exception as e:
            if AUTHOR_MODE:
                st.exception(e)
            else:
                st.error(f"Failed to generate problem: {e}")
            raise
        self._store_dict_result(result, problem_type, difficulty)
        st.rerun()

    def _store_dict_result(self, result: dict, problem_type: str, difficulty: str) -> None:
        """Validate the generator payload and persist the normalized data in session state."""
        try:
            payload: ProblemPayload = payload_from_dict(result)
        except ProblemPayloadError as e:
            if AUTHOR_MODE:
                st.exception(e)
            else:
                st.error(f"Generator returned invalid payload: {e}")
            raise

        self.state.inc("question_id", 1)
        self.state.set("problem_type", problem_type)
        self.state.set("difficulty", difficulty)
        self.state.set("generated_solve_for", self.state.get("solve_for", MIXED))
        self.state.set("current_question", payload.question)
        self.state.set("correct_answers", payload.answers)
        self.state.set("units", payload.units)
        self.state.set("submitted", False)

        self.state.set("payload", payload)
        self.state.set("user_answers_selected", [None] * len(payload.answers))
        self.state.pop("answer_options")
        self.state.pop("last_result")
        self.state.pop("feedback_message")
        features = {**payload.extras, "diagram_data": payload.diagram_data,
                    "hints": payload.hints, "button_options": payload.button_options}
        for feature in ("diagram_data", "hints", "button_options", "timer", "time_limit",
                        "explanation", "tags", "show_equations", "answer_input_mode",
                        "unique_choices", "grading", "solution_equations"):
            self.state.set(feature, features.get(feature))

    def unified_question_options(self, equations: bool = True, ifDifficulty: bool = True) -> None:
        """Render selectors for problem type and difficulty, auto-refreshing when the choice changes."""
        col1, col2, col3 = question_columns()
        with col1:
            selected_problem_type = st.selectbox(
                "Problem Type", options=list(self.problem_types), key=f"{self.prefix}_problem_type_select_unified"
            )
        with col2:
            if ifDifficulty:
                difficulty = st.selectbox(
                    "Difficulty", self.difficulties, key=f"{self.prefix}_difficulty_select_unified"
                )
            else:
                difficulty = "Easy"
        with col3:
            target = select_target(self.generator, selected_problem_type, difficulty, self.state)
        self.state.set("solve_for", target)
        if (
            selected_problem_type != self.state.get("problem_type")
            or self.state.get("current_question") is None
            or self.state.get("payload") is None
            or difficulty != self.state.get("difficulty")
            or target != self.state.get("generated_solve_for")
        ):
            self.generate_question_once(selected_problem_type, difficulty)

        if equations:
            equation_controls(
                generator=self.generator,
                problem_type=selected_problem_type,
                state=self.state,
                checkbox_key=f"{self.prefix}_levels_check_unified",
                fallback_dict=self.problem_type_dict,
                expanded=True,
            )

    def unified_smart_layout(self, **kwargs):
        """Co-ordinate the full question lifecycle, handling diagrams, hints, and answer UIs."""
        self.initialize_session_state()
        self.header_component()
        equations = kwargs.get("equations", self.state.get("show_equations") is not False)
        self.unified_question_options(equations)
        available_features = self.get_current_problem_features()
        timer = kwargs.get("timer", available_features.get("time_limit", available_features.get("timer", 3)))
        if timer is None:
            timer = 3

        if kwargs.get("side_by_side", available_features.get("side_by_side", False)):
            col1, col2 = st.columns(2)
            with col1:
                if available_features.get("diagram_data") is not None:
                    self.add_diagram_smart(kwargs.get("diagram_title", "Diagram"), expanded=kwargs.get("expanded"))
            with col2:
                if available_features.get("button_options"):
                    self.question_ui_buttons(timer)
                else:
                    self.question_ui_dict(timer)
        else:
            if available_features.get("button_options"):
                self.question_ui_buttons(timer)
            else:
                self.question_ui_dict(timer)
            if available_features.get("diagram_data") is not None:
                self.add_diagram_smart(kwargs.get("diagram_title", "Diagram"), expanded=kwargs.get("expanded"))
        if available_features.get("hints"):
            self.show_hints()
        if available_features.get("tags"):
            self.show_problem_tags(available_features["tags"])
        if AUTHOR_MODE:
            self.debug_panel()
        self.footer_dict()

    def new_question_dict(self, problem_type: str, difficulty: str) -> None:
        """Expose a manual new-question button that respects the current selections."""
        if st.button("New Question", key=f"{self.prefix}_new_question"):
            self.generate_question_once(problem_type, difficulty)

    def footer_dict(self) -> None:
        """Render the footer controls for generating new questions and showing performance."""
        col1, col2 = st.columns([1, 4], vertical_alignment="center")
        with col1:
            self.new_question_dict(self.state.get("problem_type"), self.state.get("difficulty"))
        with col2:
            self.performance_dropdown()

    def question_ui_dict(self, timer: float = 3.0, big_font: bool = False) -> None:
        """Render the free-response form and enforce numeric validation with tolerance."""
        q = self.state.get("current_question")
        st.title(q) if big_font else st.write(q)
        with st.form(f"{self.prefix}_form", clear_on_submit=True):
            user_answers = draw_answer_inputs(
                self.prefix,
                self.state.get("units", []),
                self.state.get("correct_answers", []),
                self.state.get("question_id", 0),
            )
            submitted = st.form_submit_button("Submit", disabled=bool(self.state.get("submitted")))
        if submitted and not self.state.get("submitted"):
            self.check_answers_dict(user_answers, timer)
        self.render_feedback(timer)

    def question_ui_buttons(self, timer: float = 3) -> None:
        """Render multiple-choice style inputs when generators provide answer options."""
        st.write(self.state.get("current_question"))
        correct_answers = self.state.get("correct_answers", [])
        units = self.state.get("units", [])
        answer_input_mode = self.state.get("answer_input_mode")
        options = self.state.get("button_options")
        if options is None:
            options = self.state.get("answer_options")
        if options is None:
            answer_options = self.generator.get_answer_options(units) or {}
            if not answer_options:
                for i, unit in enumerate(units):
                    if unit == "Direction":
                        answer_options[i] = ["Positive", "Negative"]
                    elif unit == "Motion State":
                        answer_options[i] = ["Constant Velocity", "Speeding Up", "Slowing Down"]
                    else:
                        answer_options[i] = []
            self.state.set("answer_options", answer_options)
            options = answer_options
        if answer_input_mode == "dropdown":
            render_dropdown_options(
                self.prefix,
                units,
                options,
                self.state.get("question_id", 0),
            )
        else:
            render_button_options(
                self.prefix,
                units,
                options,
                self.state.get("question_id", 0),
            )
        if st.button(
            "Submit Answers", key=f"{self.prefix}_submit_button_{self.state.get('question_id', 0)}",
            disabled=bool(self.state.get("submitted")),
        ):
            user_answers = self.state.get("user_answers_selected", [])
            if None in user_answers:
                st.error("Please answer all questions before submitting.")
            elif self.state.get("unique_choices") and len(set(user_answers)) != len(user_answers):
                st.error("Each option can be used only once in the ranking.")
            else:
                self.check_button_answers(user_answers)
        self.render_feedback(timer)

    def check_button_answers(self, user_answers):
        """Choice and text fallback parts share parsing and grading."""
        self.check_answers_dict(user_answers, 3)

    def check_answers_dict(self, user_answers: list, timer: float):
        if self.state.get("submitted"):
            return
        expected = self.state.get("correct_answers", [])
        if len(user_answers) != len(expected) or any(v is None or not str(v).strip() for v in user_answers):
            st.error("Please enter all answers before submitting.")
            return
        try:
            results = [answer_matches(value, answer, self.state.get("grading"))
                       for value, answer in zip(user_answers, expected)]
        except (ValueError, TypeError):
            st.error("Enter a finite number for each numeric answer.")
            return
        correct = all(results)
        difficulty, problem_type = self.state.get("difficulty"), self.state.get("problem_type")
        self.update_performance(problem_type, difficulty, correct)
        self.state.set("submitted", True)
        self.state.set("last_result", correct)
        self.state.set("feedback_message", random_correct_message() if correct else random_error_message())
        if correct:
            self.state.inc("stars", self.give_stars(difficulty, problem_type))

    def render_feedback(self, timer: float):
        """Render saved feedback and pending advancement on every rerun."""
        if not self.state.get("submitted"):
            return
        if self.state.get("last_result"):
            st.success(self.state.get("feedback_message"))
        else:
            answers = ", ".join(str(a) if isinstance(a, str) else f"{a:g}"
                                for a in self.state.get("correct_answers", []))
            st.error(f"{self.state.get('feedback_message')} The correct answers are: {answers}.")
        if self.state.get("explanation"):
            st.write(self.state.get("explanation"))
        for equation in self.state.get("solution_equations") or []:
            st.latex(equation)
        if self.state.get("last_result"):
            self.loading_q_dict(timer)

    def give_stars(self, difficulty: str, problem_type: str) -> int:
        metadata = self.generator.get_problem_metadata(problem_type) if hasattr(self.generator, "get_problem_metadata") else {}
        weight = metadata.get("star_weight", 1) if self.type_weight else 1
        return DIFFICULTY_STARS.get(difficulty, 1) * weight

    def loading_q_dict(self, timer: float = 3) -> None:
        """Adapt the reusable countdown to Interface's standard generation flow."""
        from utils.activity_flow import next_question_countdown

        problem_type = self.state.get("problem_type")
        difficulty = self.state.get("difficulty")
        next_question_countdown(
            self.state, self.state.get("question_id", 0),
            lambda: self.generate_question_once(problem_type, difficulty), seconds=timer,
        )

    def debug_panel(self) -> None:
        """In author mode, summarize the payload and metadata for quick inspection."""
        try:
            problem_type = self.state.get("problem_type")
            difficulty = self.state.get("difficulty")
            answers = self.state.get("correct_answers", [])
            units = self.state.get("units", [])
            features = self.get_current_problem_features()
            with st.expander("Debug", expanded=False):
                st.write(f"Type: {problem_type} | Difficulty: {difficulty}")
                st.write(f"Answers: {answers}")
                st.write(f"Units: {units}")
                st.json(features)
        except Exception as e:
            st.write(f"Debug panel error: {e}")


# Backwards compatibility for existing imports
interface = Interface



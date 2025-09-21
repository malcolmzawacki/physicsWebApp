import time
import pandas as pd
import streamlit as st

from utils.config import AUTHOR_MODE
from utils.word_lists import random_correct_message, random_error_message
from utils.ui_state import State
from utils.ui_components import (render_header, build_performance_table, performance_expander, draw_answer_inputs, render_button_options, render_hints, init_performance, record_performance, show_equations_expander, render_debug_panel)
from utils.problem_payload import payload_from_dict, ProblemPayload, ProblemPayloadError


class Interface:
    def __init__(
        self,
        prefix: str,
        title: str,
        generator: object,
        problem_type_dict: dict | list[str] | tuple[str, ...] | None,
        difficulties: list,
        type_weight: bool = False,
    ) -> None:
        self.prefix = prefix
        self.title = title
        self.generator = generator
        if isinstance(problem_type_dict, dict):
            self.problem_type_dict = problem_type_dict
            self.problem_types = list(problem_type_dict.keys())
        elif isinstance(problem_type_dict, (list, tuple)):
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
        getter = getattr(self.generator, "get_problem_types", None)
        if callable(getter):
            try:
                types = getter()
            except Exception:
                return []
            if isinstance(types, (list, tuple)):
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
        return init_performance(self.problem_types, self.difficulties)

    def create_performance_dataframe(self) -> pd.DataFrame:
        performance = self.state.get("performance")
        ordered = list(self.difficulties)
        return build_performance_table(performance, ordered)

    def update_performance(self, problem_type: str, difficulty: str, is_correct: bool) -> None:
        performance = self.state.get("performance")
        new_perf = record_performance(performance, problem_type, difficulty, is_correct)
        self.state.set("performance", new_perf)

    def performance_dropdown(self) -> None:
        performance_df = self.create_performance_dataframe()
        performance_expander(performance_df)
    # endregion

    def initialize_session_state(self) -> None:
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
        self.state.ensure_lazy("performance", lambda: init_performance(self.problem_types, self.difficulties))
        # Equation level toggle default
        if self.state.get("level") is None:
            self.state.set("level", False)

    def header_component(self) -> None:
        stars = self.state.get("stars", 0)
        render_header(self.title, stars if stars else None)

    # region unified helpers
    def add_diagram_smart(self, expander_title: str = "Diagram", **kwargs) -> None:
        diagram_data = self.state.get("diagram_data")
        if diagram_data is None:
            return
        problem_type = self.state.get("problem_type")
        difficulty = self.state.get("difficulty")
        if hasattr(self.generator, "generate_diagram"):
            try:
                fig = self.generator.generate_diagram(diagram_data, problem_type, difficulty)
                if fig is not None:
                    with st.expander(expander_title, expanded=kwargs.get("expanded", False)):
                        st.pyplot(fig)
            except Exception as e:
                if AUTHOR_MODE:
                    st.exception(e)

    def get_current_problem_features(self) -> dict:
        features = {}
        for feature in ["diagram_data", "hints", "button_options", "time_limit", "explanation", "tags", "show_equations"]:
            val = self.state.get(feature)
            if val is not None:
                features[feature] = val
        return features

    def show_hints(self) -> None:
        render_hints(self.state.get("hints", []))

    def show_problem_tags(self, tags: list) -> None:
        if tags:
            st.caption(" ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¢ ".join(tags))

    def generate_question_once(self, problem_type: str, difficulty: str) -> None:
        try:
            result = self.generator.choose_problem_dict(problem_type, difficulty)
        except Exception as e:
            if AUTHOR_MODE:
                st.exception(e)
            else:
                st.error(f"Failed to generate problem: {e}")
            raise
        self._store_dict_result(result, problem_type, difficulty)
        st.rerun()

    def _store_dict_result(self, result: dict, problem_type: str, difficulty: str) -> None:
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
        self.state.set("current_question", payload.question)
        self.state.set("correct_answers", payload.answers)
        self.state.set("units", payload.units)
        self.state.set("submitted", False)
        self.state.set("generation_format", "dict")

        for feature in ["diagram_data", "hints", "button_options", "timer", "explanation", "tags", "show_equations"]:
            if feature in result:
                self.state.set(feature, result[feature])
            else:
                self.state.pop(feature)

    def _store_legacy_result(self, result: tuple, problem_type: str, difficulty: str) -> None:
        question, answers, units, diagram_data = result
        self.state.inc("question_id", 1)
        self.state.set("problem_type", problem_type)
        self.state.set("difficulty", difficulty)
        self.state.set("current_question", question)
        self.state.set("correct_answers", answers)
        self.state.set("units", units)
        self.state.set("submitted", False)
        self.state.set("generation_format", "legacy")
        if diagram_data is not None:
            self.state.set("diagram_data", diagram_data)

    def unified_question_options(self, equations: bool = True, ifDifficulty: bool = True) -> None:
        col1, col2, col3 = st.columns([3, 2, 2], vertical_alignment="bottom", gap="medium")
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
            if equations:
                lvl = st.checkbox(
                    "More Equations", value=self.state.get('level',False), key=f"{self.prefix}_levels_check_unified"
                )

        if (
            selected_problem_type != self.state.get("problem_type")
            or self.state.get("current_question") is None
            or difficulty != self.state.get("difficulty")
        ):
            self.generate_question_once(selected_problem_type, difficulty)

        if equations:
            show_equations_expander(
                generator=self.generator,
                problem_type=selected_problem_type,
                level=lvl,
                fallback_dict=self.problem_type_dict,
                expanded=True,
            )

    def _show_equations_unified(self, problem_type: str) -> None:
        with st.expander("equation(s)", expanded=True):
            if hasattr(self.generator, "get_problem_metadata"):
                metadata = self.generator.get_problem_metadata(problem_type)
                if self.state.get("level"):
                    equation = metadata.get("conceptual", "")
                else:
                    equation = metadata.get("honors", "")
                if equation:
                    st.latex(equation)
                    return
            if self.problem_type_dict is not None:
                equation_dict = self.problem_type_dict.get(problem_type, {})
                if self.state.get("level"):
                    equation = equation_dict.get("conceptual", "")
                else:
                    equation = equation_dict.get("honors", "")
                if equation:
                    st.latex(equation)

    def unified_smart_layout(self, **kwargs):
        """Smart layout that works with both legacy and dictionary generators"""
        self.initialize_session_state()
        self.header_component()
        equations = kwargs.get("equations", True)
        self.unified_question_options(equations)
        generation_format = self.state.get("generation_format", "legacy")
        if generation_format == "dict":
            available_features = self.get_current_problem_features()
            if kwargs.get("side_by_side"):
                col1, col2 = st.columns(2)
                with col1:
                    if available_features.get("diagram_data") is not None:
                        self.add_diagram_smart(kwargs.get("diagram_title", "Diagram"), expanded=kwargs.get("expanded"))
                with col2:
                    if available_features.get("button_options"):
                        self.question_ui_buttons()
                    else:
                        timer = kwargs.get("timer", 3)
                        self.question_ui_dict(timer)
            else:
                if available_features.get("button_options"):
                    self.question_ui_buttons()
                else:
                    timer = kwargs.get("timer", 3)
                    self.question_ui_dict(timer)
                if available_features.get("diagram_data") is not None:
                    self.add_diagram_smart(kwargs.get("diagram_title", "Diagram"))
            if available_features.get("hints"):
                self.show_hints()
            if AUTHOR_MODE:
                self.debug_panel()
        else:
            # Legacy fallback if needed
            timer = kwargs.get("timer", 3)
            self.question_ui_dict(timer)
        self.footer_dict()

    def new_question_dict(self, problem_type: str, difficulty: str) -> None:
        if st.button("New Question", key=f"{self.prefix}_new_question"):
            self.generate_question_once(problem_type, difficulty)

    def footer_dict(self) -> None:
        col1, col2 = st.columns([1, 4], vertical_alignment="center")
        with col1:
            self.new_question_dict(self.state.get("problem_type"), self.state.get("difficulty"))
        with col2:
            self.performance_dropdown()

    def question_ui_dict(self, timer: float = 3.0, big_font: bool = False) -> None:
        q = self.state.get("current_question")
        st.title(q) if big_font else st.write(q)
        with st.form(f"{self.prefix}_form", clear_on_submit=True):
            user_answers = draw_answer_inputs(
                self.prefix,
                self.state.get("units", []),
                self.state.get("correct_answers", []),
                self.state.get("question_id", 0),
            )
            submitted = st.form_submit_button("Submit")
        if submitted:
            validated_answers = []
            validation_passed = True
            units = self.state.get("units", [])
            for i, (raw_answer, correct_answer) in enumerate(
                zip(user_answers, self.state.get("correct_answers", []))
            ):
                if isinstance(correct_answer, str):
                    validated_answers.append(raw_answer)
                else:
                    if not raw_answer or not raw_answer.strip():
                        st.error(f"Please enter a value for {units[i] if i < len(units) else ''}")
                        validation_passed = False
                        validated_answers.append(None)
                    else:
                        try:
                            validated_answers.append(float(raw_answer.strip()))
                        except ValueError:
                            st.error(
                                f"'{raw_answer}' is not a valid number for {units[i] if i < len(units) else ''}"
                            )
                            validation_passed = False
                            validated_answers.append(None)
            if validation_passed:
                self.check_answers_dict(validated_answers, timer)
            else:
                st.warning("Please fix the errors above and try again.")

    def question_ui_buttons(self) -> None:
        st.write(self.state.get("current_question"))
        correct_answers = self.state.get("correct_answers", [])
        units = self.state.get("units", [])
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
        render_button_options(
            self.prefix,
            units,
            options,
            self.state.get("question_id", 0),
        )
        if st.button(
            "Submit Answers", key=f"{self.prefix}_submit_button_{self.state.get('question_id', 0)}"
        ):
            user_answers = self.state.get("user_answers_selected", [])
            if None in user_answers:
                st.error("Please answer all questions before submitting.")
            else:
                self.check_button_answers(user_answers)

    def check_button_answers(self, user_answers):
        correct_answers = self.state.get("correct_answers", [])
        all_correct = True
        for user_input, correct_answer in zip(user_answers, correct_answers):
            is_correct = user_input == correct_answer
            all_correct = all_correct and is_correct
        if not self.state.get("submitted", False):
            problem_type = self.state.get("problem_type")
            difficulty = self.state.get("difficulty")
            self.update_performance(problem_type, difficulty, all_correct)
            self.state.set("submitted", True)
            if all_correct:
                st.success(f"{random_correct_message()}")
                self.state.set("stars", self.state.get("stars", 0) + self.give_stars(difficulty, problem_type))
                self.state.set("show_loading", True)
            else:
                answer_display = ", ".join([f"{ans}" for ans in correct_answers])
                st.error(f"{random_error_message()} The correct answers are: {answer_display}.")
                self.state.set("show_loading", True)
        self.state.set("user_answers_selected", [None] * len(correct_answers))

    def check_answers_dict(self, user_answers: list, timer: float):
        correct_answers = self.state.get("correct_answers", [])
        all_correct = True
        if None not in user_answers:
            for user_input, correct_answer in zip(user_answers, correct_answers):
                if isinstance(user_input, str):
                    is_correct = user_input.lower().strip() == str(correct_answer).lower()
                else:
                    tolerance = correct_answer * 0.1
                    is_correct = abs(user_input - correct_answer) <= abs(tolerance)
                all_correct = all_correct and is_correct
            if not self.state.get("submitted", False):
                problem_type = self.state.get("problem_type")
                difficulty = self.state.get("difficulty")
                self.update_performance(problem_type, difficulty, all_correct)
                self.state.set("submitted", True)
                if all_correct:
                    st.success(f"{random_correct_message()}")
                    self.state.set("stars", self.state.get("stars", 0) + self.give_stars(difficulty, problem_type))
                    self.loading_q_dict(timer)
                else:
                    answers_disp = []
                    for ans in correct_answers:
                        answers_disp.append(f"{ans if isinstance(ans, str) else f'{ans:.2f}'}")
                    article = "is" if len(correct_answers) < 2 else "are"
                    st.error(
                        f"{random_error_message()} The correct answers {article}: {', '.join(answers_disp)}."
                    )
        else:
            st.error("Please enter all answers before submitting")

    def give_stars(self, difficulty: str, problem_type: str) -> int:
        problem_type_bonus = self.problem_types.index(problem_type) + 1 if self.type_weight else 1
        difficulty_bonus = self.difficulties.index(difficulty) + 1
        return problem_type_bonus * difficulty_bonus

    def loading_q_dict(self, timer: float = 3) -> None:
        problem_type = self.state.get("problem_type")
        difficulty = self.state.get("difficulty")
        i = 0
        loading_text = "Next Question"
        timer *= 100
        col1, col2 = st.columns([5, 2])
        with col1:
            loading_question = st.progress(0, loading_text)
        with col2:
            pause = st.checkbox("Cancel Next Question")
        while i < timer and not pause:
            time.sleep(0.01)
            loading_question.progress((i + 1) / timer, loading_text)
            i += 1
        if i == timer and not pause:
            self.generate_question_once(problem_type, difficulty)

    def debug_panel(self) -> None:
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

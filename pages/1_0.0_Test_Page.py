import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))
from utils.generators.linear_motion_generator import LinearMotionGenerator
from utils.rendering import rendering
class test:
    @ staticmethod
    def question_parameters():
            """Holds current options for questions for centralized updating"""

            problem_type_dict = {
                "Mixed": {
                      "honors": r"",
                      "conceptual": r"""v_f^2 = v_i^2 + 2ax \;\;,
                      \;\;v_f = v_i + at\;\;,
                      \;\;x = \frac{v_f + v_i}{2} t\;\;,
                      \;\;x = v_i t + \frac{1}{2} at^2"""},
                "No Time": {
                    "honors" : r"v_f^2 = v_i^2 + 2ax", 
                    "conceptual": r"""v_f = \sqrt{v_i^2 + 2ax} \;\; , 
                    \;\; v_i = \sqrt{2ax - v_f^2} \;\; , 
                    \;\;  x = \frac{v_f^2 - v_i^2}{2a} \;\;,
                    \;\;  a = \frac{v_f^2 - v_i^2}{2x}"""
                    },
                "No Distance": {
                    "honors": r"v_f = v_i + at",
                    "conceptual": r"""KE = \frac{1}{2} m v^2\;\; ,
                    \;\; m = \frac{2 \cdot K}{v^2} \;\; ,
                    \;\; v = \sqrt{\frac{2 \cdot K}{m}}"""
                },               
                "No Acceleration" : {
                    "honors": r"x = \frac{v_f + v_i}{2} t",
                    "conceptual": r"""GPE = mgh\;\; ,
                    \;\; m = \frac{GPE}{gh} \;\; ,
                    \;\; h = \frac{GPE}{mg}"""
                },
                "No Final Velocity": {
                    "honors": r"x = v_i t + \frac{1}{2} at^2",
                    "conceptual": r"""W = Fd\;\; ,
                    \;\; F = \frac{W}{d} \;\; ,
                    \;\; d = \frac{W}{F}"""
                },
                }
            problem_types = list(problem_type_dict.keys())
            difficulties = ["Easy","Medium","Hard"]
            return problem_type_dict, problem_types, difficulties

    @staticmethod
    def main():
        st.title("Test Page")
        prefix = "test"
        problem_type_dict, problem_types, difficulties = test.question_parameters()
        render = rendering()
        generator = LinearMotionGenerator()
        render.initialize_session_state(prefix, problem_types, difficulties)
        performance = st.session_state[f"{prefix}_performance"]
        render.subheader_ui(prefix,performance)
        render.question_ui(prefix, problem_type_dict, problem_types ,difficulties, generator)


if __name__ == "__main__":
    test.main()
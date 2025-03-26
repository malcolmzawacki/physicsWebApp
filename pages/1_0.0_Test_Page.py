import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.generators.projectile_generator import ProjectileGenerator
from utils.generators.linear_motion_generator import LinearMotionGenerator
from utils.rendering import rendering

class constant_motion:
    @ staticmethod
    def question_parameters():
            """Holds current options for questions for centralized updating"""

            problem_type_dict = {
                "One Dimensional": {
                      "honors": r"""\textrm{currently under construction, ask your teacher to hurry up!}""",

                      "conceptual": r"""\textrm{currently under construction, ask your teacher to hurry up!}
                      """},
                "Two Dimensional": {
                      "honors": r"""\textrm{currently under construction, ask your teacher to hurry up!}""",

                      "conceptual": r"""\textrm{currently under construction, ask your teacher to hurry up!}
                      """},
                
                }
            problem_types = list(problem_type_dict.keys())
            difficulties = ["Easy","Medium","Hard"]
            return problem_type_dict, problem_types, difficulties

    @staticmethod
    def main():
        st.title("Constant Motion")
        prefix = "constant"
        problem_type_dict, problem_types, difficulties = constant_motion.question_parameters()
        render = rendering()
        generator = LinearMotionGenerator()
        render.initialize_session_state(prefix, problem_types, difficulties)
        performance = st.session_state[f"{prefix}_performance"]
        render.subheader_ui(prefix,performance)
        render.question_ui_3_with_diagrams(prefix, problem_type_dict, problem_types ,difficulties, generator)

def main():
     tab1, tab2 = st.tabs(["Constant","Projectile Problems"])
     with tab1:
          constant_motion.main()
     with tab2:
          pass


if __name__ == "__main__":
    main()
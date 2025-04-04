import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.rendering import rendering
from utils.generators.force_generator import ForceGenerator




class forces:
     @ staticmethod
     def question_parameters():
            """Holds current options for questions for centralized updating"""

            problem_type_dict = {
                "Newton's Second Law": {
                      "honors": r"""
                      \Sigma F \;=\; ma""",

                      "conceptual": r"""\Large{
                      \Sigma F \;=\; ma 
                      \quad\quad | \quad\quad
                      m \;=\; \frac{\Sigma F}{a}
                      \quad\quad | \quad\quad
                      a \;=\; \frac{\Sigma F}{m}
                      }"""},
                }
            problem_types = list(problem_type_dict.keys())
            difficulties = ["Easy","Medium","Hard"]
            return problem_type_dict, problem_types, difficulties

     @staticmethod
     def main():
        st.title("Newton's Second Law")
        prefix = "newtons_2nd"
        problem_type_dict, problem_types, difficulties = forces.question_parameters()
        render = rendering()
        generator = ForceGenerator()
        render.initialize_session_state(prefix, problem_types, difficulties)
        performance = st.session_state[f"{prefix}_performance"]
        render.subheader_ui(prefix,performance)
        render.question_ui_3(prefix, problem_type_dict, problem_types ,difficulties, generator)

def main():
     tab1,tab2 = st.tabs(["Newton's Second Law","TBD"])
     with tab1:
          forces.main()
     with tab2:
        st.write("Currently Under Construction")

if __name__ == "__main__":
    main()
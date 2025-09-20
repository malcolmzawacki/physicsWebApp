import streamlit as st
from utils.ui import interface
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
            difficulties = ["Easy","Medium","Hard"]
            return problem_type_dict, difficulties

     @staticmethod
     def main():
        title = "Newton's Second Law"
        prefix = "newtons_2nd"
        problem_type_dict, difficulties = forces.question_parameters()
        generator = ForceGenerator()
        ui = interface(prefix,title,generator,problem_type_dict,difficulties)
        ui.unified_smart_layout()

def main():
     tab1,tab2 = st.tabs(["Newton's Second Law","TBD"])
     with tab1:
          forces.main()
     with tab2:
        st.write("Currently Under Construction")

if __name__ == "__main__":
    main()
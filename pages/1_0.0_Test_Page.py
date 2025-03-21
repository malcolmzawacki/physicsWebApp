import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.generators.projectile_generator import ProjectileGenerator
from utils.generators.linear_motion_generator import LinearMotionGenerator
from utils.rendering import rendering

class linear_fns:
    @ staticmethod
    def question_parameters():
        """Holds current options for questions for centralized updating"""

        problem_type_dict = {
                        "Mixed": {
                            "honors": r"""v_f^2 = v_i^2 + 2ax \quad ,
                            \quad v_f = v_i +at  \quad ,
                            \quad x = \frac{v_f + v_i}{2} t  \quad ,
                            \quad x = v_i t + \frac{1}{2} at^2""",

                            "conceptual": r"""
                            \quad x = \frac{v_f + v_i}{2} t  \quad
                            \quad x = \frac{1}{2} at^2  \quad
                            \quad x = \frac{v_f^2 - v_i^2}{2a}  \quad

                            \newline ~ \newline ~ \newline
                            \quad v_f = \frac{2x}{t} - v_i  \quad
                            \quad v_f = \sqrt{v_i^2 + 2ax}  \quad
                            \quad v_f = v_i + at  \quad
                            
                            \newline ~ \newline ~ \newline
                            \quad v_i = \sqrt{2ax - v_f^2}  \quad
                            \quad v_i = at - v_f  \quad
                            \quad v_i = \frac{2x}{t} - v_f  \quad
                            \newline ~ \newline ~ \newline
                            \quad t = \frac{2x}{v_f + v_i}  \quad 
                            \quad t = \sqrt{ \frac{2x}{a} }  \quad
                            \quad t = \frac{v_f - v_i}{a}  \quad
                            \newline ~ \newline ~ \newline
                                \quad a = \frac{2x}{t^2}  \quad 
                                \quad a = \frac{v_f - v_i}{t}  \quad
                                \quad a = \frac{v_f^2 - v_i^2}{2x}  \quad
                            
                            """},
                        "No Time": {
                            "honors" : r"v_f^2 = v_i^2 + 2ax", 
                            "conceptual": r"""v_f = \sqrt{v_i^2 + 2ax}  \quad , 
                            \quad v_i = \sqrt{2ax - v_f^2}  \quad , 
                            \quad  x = \frac{v_f^2 - v_i^2}{2a}  \quad,
                            \quad  a = \frac{v_f^2 - v_i^2}{2x}"""
                            },
                        "No Distance": {
                            "honors": r"v_f = v_i + at",
                            "conceptual": r"""v_f = v_i +at  \quad ,
                            \quad v_i = at - v_f  \quad ,
                            \quad a = \frac{v_f - v_i}{t}  \quad,
                            \quad t = \frac{v_f - v_i}{a}"""
                        },               
                        "No Acceleration" : {
                            "honors": r"x = \frac{v_f + v_i}{2} t",
                            "conceptual": r"""x = \frac{v_f + v_i}{2} t  \quad ,
                            \quad t = \frac{2d}{v_f + v_i}  \quad ,
                            \quad v_f = \frac{2d}{t} - v_i  \quad , 
                            \quad v_i = \frac{2d}{t} - v_f  \quad """
                        },
                        "No Final Velocity": {
                            "honors": r"x = v_i t + \frac{1}{2} at^2",
                            "conceptual": r"""x = \frac{1}{2} at^2  \quad ,
                            \quad a = \frac{2x}{t^2}  \quad ,
                            \quad t = \sqrt{ \frac{2d}{a} }"""
                        },
                        }


        problem_types = list(problem_type_dict.keys())
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, problem_types, difficulties

    @staticmethod
    def main():
        st.title("Linear Motion")
        prefix = "linear"
        problem_type_dict, problem_types, difficulties = linear_fns.question_parameters()
        render = rendering()
        generator = LinearMotionGenerator()
        render.initialize_session_state(prefix, problem_types, difficulties)
        performance = st.session_state[f"{prefix}_performance"]
        render.subheader_ui(prefix,performance)
        render.question_ui_2(prefix, problem_type_dict, problem_types ,difficulties, generator)



class Projectile_fns:
    @ staticmethod
    def question_parameters():
            """Holds current options for questions for centralized updating"""

            problem_type_dict = {
                "Type 1": {
                      "honors": r"""currently under construction, ask your teacher to hurry up!""",

                      "conceptual": r"""currently under construction, ask your teacher to hurry up!
                      """},
                "Type 2": {
                    "honors" : r"currently under construction, ask your teacher to hurry up!", 
                    "conceptual": r"""currently under construction, ask your teacher to hurry up!"""
                    },
                "Type 3": {
                    "honors": r"currently under construction, ask your teacher to hurry up!",
                    "conceptual": r"""currently under construction, ask your teacher to hurry up!"""
                }
                }
            problem_types = list(problem_type_dict.keys())
            difficulties = ["Easy","Medium","Hard"]
            return problem_type_dict, problem_types, difficulties

    @staticmethod
    def main():
        st.title("Projectiles")
        prefix = "projectiles"
        problem_type_dict, problem_types, difficulties = Projectile_fns.question_parameters()
        render = rendering()
        generator = ProjectileGenerator()
        render.initialize_session_state(prefix, problem_types, difficulties)
        performance = st.session_state[f"{prefix}_performance"]
        render.subheader_ui(prefix,performance)
        render.question_ui_2(prefix, problem_type_dict, problem_types ,difficulties, generator)


def main():
     tab1, tab2 = st.tabs(["Linear Motion Problems","Projectile Problems"])
     with tab1:
          linear_fns.main()
     with tab2:
          Projectile_fns.main()


if __name__ == "__main__":
    main()
# pages/collisions.py
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.generators.collision_generator import CollisionGenerator
from utils.rendering import rendering

class collisions:
    @staticmethod
    def question_parameters():
        """Holds current options for questions for centralized updating"""
        problem_type_dict = {
            "Inelastic Collision": {
                "honors": r"p_1 + p_2 = p'",
                "conceptual": r""" \frac{m_1v_1 + m_2v_2}{m_1+m_2}=v'
                """
                },
            "Elastic Collision": {
                "honors": r"p_1 + p_2 = p_1' + p_2'",
                "conceptual": r"""m_1v_1+m_2v_2 = m_1v_1' + m_2v_2'"""
                },
            }
        problem_types = list(problem_type_dict.keys())
        difficulties = ["Easy"]
        return problem_type_dict, problem_types, difficulties

    @staticmethod
    def main():
        st.title("Collisions")
        prefix = "collisions"
        problem_type_dict, problem_types, difficulties = collisions.question_parameters()
        render = rendering()
        generator = CollisionGenerator()
        render.initialize_session_state(prefix, problem_types, difficulties)
        performance = st.session_state[f"{prefix}_performance"]
        render.subheader_ui(prefix,performance)
        render.question_ui_3(prefix, problem_type_dict, problem_types ,difficulties, generator)


if __name__ == "__main__":
    collisions.main()

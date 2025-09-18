# pages/collisions.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.generators.collision_generator import CollisionGenerator
from utils.ui import interface

class collisions:
    
    @staticmethod
    def main():
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
        difficulties = ["Easy"]
        title = "Collisions"
        prefix = "collisions"
    
        generator = CollisionGenerator()
        ui = interface(prefix,title,generator,problem_type_dict,difficulties)
        ui.unified_smart_layout()


if __name__ == "__main__":
    collisions.main()

import random
from random import randint as ri
import math
from utils.word_lists import random_noun
from utils.generators.base_generator import BaseGenerator

class TensionGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="tension_")

    
    def tension_nums(self):
        mass = ri(5,50)
        theta1 = ri(1,89)
        theta2 = ri(1,89)
        return mass, theta1, theta2
    
    def quadrant_phrases(self,quadrant):
        quadrant_dict = {
            1: {
                "direction": "up and to the right",
                "signs": (1, 1)
            },
            2: {
                "direction": "up and to the left",
                "signs": (-1,1)
            },
            3: {
                "direction": "down and to the left",
                "signs": (-1,-1)
            },
            4: {
                "direction": "down and to the right",
                "signs": (1,-1)
            }
        }
        return quadrant_dict.get(quadrant)
    
    def tension_scenario(self, difficulty):
        mass, theta1, theta2 = self.tension_nums()
        if difficulty == "Easy": # both upwards
            scenario = random.choice([(1,2),(2,1)])
        else: # opposing directions
            scenario = random.choice([(2,4),(4,2),(1,3),(3,1)])
        tension1_info = self.quadrant_phrases(scenario[0])
        tension2_info = self.quadrant_phrases(scenario[1])
        tension1_phrase = tension1_info["direction"]
        tension2_phrase = tension2_info["direction"]
        tension1_vert = tension1_info["signs"][1]
        tension2_vert = tension2_info["signs"][1]
        tension1_div = tension2_vert*math.sin(theta1*math.pi/180) + tension1_vert*math.cos(theta1*math.pi/180)*math.tan(theta2*math.pi/180)
        tension2_div = tension1_vert*math.sin(theta2*math.pi/180) + tension2_vert*math.cos(theta2*math.pi/180)*math.tan(theta1*math.pi/180)
        if tension1_div or tension2_div == 0:
            while (tension1_div or tension2_div) == 0:
                theta1 = ri(1,89)
                theta2 = ri(1,89)
                tension1_div = tension2_vert*math.sin(theta1*math.pi/180) + tension1_vert*math.cos(theta1*math.pi/180)*math.tan(theta2*math.pi/180)
                tension2_div = tension1_vert*math.sin(theta2*math.pi/180) + tension2_vert*math.cos(theta2*math.pi/180)*math.tan(theta1*math.pi/180)
        tension1 = mass*10 / tension1_div
        tension2 = mass*10 / tension2_div
        return {
            "mass": mass,
            "theta 1": theta1,
            "theta 2": theta2,
            "tension 1 direction": tension1_phrase,
            "tension 2 direction": tension2_phrase,
            "tension 1": tension1,
            "tension 2": tension2,
            "scenario": (scenario[0], scenario[1])
        }

    def suspension_question(self, difficulty):
        tension_info = self.tension_scenario(difficulty)
        noun = random_noun()
        question = f"""A priceless {tension_info["mass"]} kg {noun} is 
        suspended above the floor of a high security vault by two wires.
        The first wire is angled {tension_info["tension 1 direction"]} at {tension_info["theta 1"]} degrees.
        The second wire is angled {tension_info["tension 2 direction"]} at {tension_info["theta 2"]} degrees.
        In order to keep the {noun} perfectly still, what tension is required for each wire?"""
        answers = [tension_info["tension 1"], tension_info["tension 2"]]
        units = ["Tension 1 (Newtons)", "Tension 2 (Newtons)"]

        diagram_data = {
            "theta1": tension_info["theta 1"],
            "theta2": tension_info["theta 2"],
            "scenario": tension_info["scenario"]
        }

        return {"question": question, "answers": answers, "units": units, "diagram_data": diagram_data}
    
    def _get_polar_angle(self, quadrant, theta):
        """Helper to convert a quadrant and horizontal angle to a polar angle for Matplotlib."""
        if quadrant == 1:  # Up-right
            return theta
        elif quadrant == 2:  # Up-left
            return 180 - theta
        elif quadrant == 3:  # Down-left
            return 180 + theta
        elif quadrant == 4:  # Down-right
            return 360 - theta
        return 0

    def generate_diagram(self, diagram_data: dict, problem_type: str, difficulty: str):
        """
        Generate a Matplotlib figure for the tension problem.
        This method is called by the Interface's add_diagram_smart().
        """
        import matplotlib.pyplot as plt
        plt.tight_layout()
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(4, 3))

        
        # 1. Get the data
        theta1 = diagram_data["theta1"]
        theta2 = diagram_data["theta2"]
        q1, q2 = diagram_data["scenario"]

        # 2. Convert to polar angles (in radians) for drawing
        angle1_rad = math.radians(self._get_polar_angle(q1, theta1))
        angle2_rad = math.radians(self._get_polar_angle(q2, theta2))

        # 3. Get (x, y) coordinates for the end of the tension vectors
        v1_x, v1_y = 3 * math.cos(angle1_rad), 3 * math.sin(angle1_rad)
        v2_x, v2_y = 3 * math.cos(angle2_rad), 3 * math.sin(angle2_rad)

        # 4. Draw the vectors
        # Tension 1
        ax.arrow(0, 0, v1_x, v1_y, head_width=0.2, head_length=0.2, fc='red', ec='red', length_includes_head=True)
        ax.text(v1_x * 1.15, v1_y * 1.15, '$T_1$', color='red', ha='center', va='center', fontsize=12)
        
        # Tension 2
        ax.arrow(0, 0, v2_x, v2_y, head_width=0.2, head_length=0.2, fc='red', ec='red', length_includes_head=True)
        ax.text(v2_x * 1.15, v2_y * 1.15, '$T_2$', color='red', ha='center', va='center', fontsize=12)

        # Weight (mg)
        ax.arrow(0, 0, 0, -2, head_width=0.2, head_length=0.2, fc='blue', ec='blue', length_includes_head=True)
        ax.text(0, -2.3, '$W = mg$', color='blue', ha='center', va='top', fontsize=12)

        # 5. Draw helper lines
        ax.plot(0, 0, 'o', markersize=8, color='white') # Central mass
        ax.plot([-4, 4], [0, 0], ls='--', color='white', linewidth=0.5) # Horizontal

        # 6. Clean up the plot
        ax.set_xlim(-4, 4)
        ax.set_ylim(-3, 4)
        ax.set_aspect('equal')  # Make it square
        ax.axis('off')          # Hide the x/y axes

        return fig

    def choose_problem_dict(self, problem_type, difficulty):
        if problem_type == "Suspension":
            return self.suspension_question(difficulty)


    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "Suspension": {
                "honors": r"""
                      \Sigma F \;=\; ma""",

                "conceptual": r"""\Large{
                      \Sigma F \;=\; ma 
                      \quad\quad | \quad\quad
                      m \;=\; \frac{\Sigma F}{a}
                      \quad\quad | \quad\quad
                      a \;=\; \frac{\Sigma F}{m}
                      }"""
            }
        }
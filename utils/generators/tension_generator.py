import random
from random import randint as ri
import math
from utils.word_lists import random_noun

from utils.generators.base_generator import BaseGenerator

from utils.word_lists import random_noun

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
        tension1 = mass*10 / (tension2_vert*math.sin(theta1*math.pi/180) + tension1_vert*math.cos(theta1*math.pi/180)*math.tan(theta2*math.pi/180))
        tension2 = mass*10 / (tension1_vert*math.sin(theta2*math.pi/180) + tension2_vert*math.cos(theta2*math.pi/180)*math.tan(theta1*math.pi/180))
        return {
            "mass": mass,
            "theta 1": theta1,
            "theta 2": theta2,
            "tension 1 direction": tension1_phrase,
            "tension 2 direction": tension2_phrase,
            "tension 1": tension1,
            "tension 2": tension2
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
        return {"question": question, "answers": answers, "units": units}
    
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
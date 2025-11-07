import random
from random import randint as ri
import math
from utils.word_lists import random_noun
from utils.generators.base_generator import BaseGenerator


class InclineGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="incline_")
    
    def choose_problem_dict(self, problem_type, difficulty):
        if problem_type == "Static Incline":
            return self.static_incline()
        elif problem_type == "Frictionless Incline":
            return self.frictionless_incline()
        elif problem_type == "Kinetic Friction Incline":
            return self.kinetic_friction_incline()
    
    
    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "Static Incline": {
                "honors": r"""
                      \Sigma F \;=\; ma""",

                "conceptual": r"""\Large{
                      \Sigma F \;=\; ma 
                      \quad\quad | \quad\quad
                      m \;=\; \frac{\Sigma F}{a}
                      \quad\quad | \quad\quad
                      a \;=\; \frac{\Sigma F}{m}
                      }"""
            },
            "Frictionless Incline": {
                "honors": r"""
                      \Sigma F \;=\; ma""",

                "conceptual": r"""\Large{
                      \Sigma F \;=\; ma 
                      \quad\quad | \quad\quad
                      m \;=\; \frac{\Sigma F}{a}
                      \quad\quad | \quad\quad
                      a \;=\; \frac{\Sigma F}{m}
                      }"""
            },
            "Kinetic Friction Incline": {
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
    
    def incline_nums(self):
        theta = ri(1,44)
        mu_max = math.tan(math.pi*theta/180)
        accel_no_mu = 10*math.sin(math.pi*theta/180)
        mu_k = ri(1, math.floor(100*mu_max)-1)/100
        accel_mu_k = accel_no_mu - 10*mu_k*math.cos(math.pi*theta/180)
        return {
            "angle": theta,
            "static coeff": mu_max,
            "accel w/o frict": accel_no_mu,
            "kinetic coeff": mu_k,
            "accel w/ frict": accel_mu_k
        }

    def static_incline(self, solve_for = None):
        """solve for options are: angle, or static coeff"""
        if solve_for == None:
            solve_for = random.choice([
                "angle",
                "static coeff"
            ])
        q_nums = self.incline_nums()
        noun = random_noun()
        mass = ri(1,25)
        if solve_for == "angle":
            question = f"""A {mass} kg {noun} sits at rest on an inclined plane.
            The coefficient of static friction between the {noun} and the plane is {q_nums["static coeff"]:.2f}.
            What is the angle of the inclined plane?"""
            answer = [q_nums["angle"]]
            unit = ["Angle (degrees)"]
        else:
            question = f"""A {mass} kg {noun} sits at rest on an inclined plane.
            The plane sits at an angle of {q_nums["angle"]} degrees.
            What is the coefficient of static friction between the {noun} and the plane?"""
            answer = [q_nums["static coeff"]]
            unit = ["Coefficient of Static Friction"]
        return {"question": question, "answers": answer, "units": unit}
    
    def frictionless_incline(self, solve_for = None):
        """solve for options are: angle, or accel"""
        if solve_for == None:
            solve_for = random.choice([
                "angle",
                "accel"
            ])
        q_nums = self.incline_nums()
        accel = q_nums["accel w/o friction"]
        noun = random_noun()
        mass = ri(1,25)
        if solve_for == "angle":
            question = f"""A {mass} kg {noun} accelerates down an inclined plane at a rate of {accel:.2f}.
            What is the angle of the inclined plane?"""
            answer = [q_nums["angle"]]
            unit = ["Angle (degrees)"]
        else:
            question = f"""A {mass} kg {noun} accelerates down an inclined plane.
            The plane sits at an angle of {q_nums["angle"]} degrees.
            What is the acceleration of the {noun} down the plane?"""
            answer = [accel]
            unit = [f"{noun}'s acceleration (m/s^2)"]
        return {"question": question, "answers": answer, "units": unit}
    
        
    def kinetic_friction_incline(self, solve_for = None):
        """solve for options are: angle, accel, coeff"""
        if solve_for == None:
            solve_for = random.choice([
                "angle",
                "accel",
                "coeff"
            ])
        q_nums = self.incline_nums()
        accel = q_nums["accel w/ friction"]
        coeff = q_nums["kinetic coeff"]
        noun = random_noun()
        mass = ri(1,25)
        if solve_for == "angle":
            question = f"""A {mass} kg {noun} accelerates down an inclined plane at a rate of {accel:.2f}.
            The coefficient of kinetic friction between the {noun} and the plane is {coeff:.2f}.
            What is the angle of the inclined plane?"""
            answer = [q_nums["angle"]]
            unit = ["Angle (degrees)"]
        elif solve_for == "accel":
            question = f"""A {mass} kg {noun} accelerates down an inclined plane.
            The plane sits at an angle of {q_nums["angle"]} degrees.
            The coefficient of kinetic friction between the {noun} and the plane is {coeff:.2f}.
            What is the acceleration of the {noun} down the plane?"""
            answer = [accel]
            unit = [f"{noun}'s acceleration (m/s^2)"]
        else:
            question = f"""A {mass} kg {noun} accelerates down an inclined plane at a rate of {accel:.2f}.
            The plane sits at an angle of {q_nums["angle"]} degrees.
            What is the coefficient of kinetic friction between the {noun} and the plane?"""
            answer = [coeff]
            unit = ["Coefficient of Kinetic Friction"]
        return {"question": question, "answers": answer, "units": unit}
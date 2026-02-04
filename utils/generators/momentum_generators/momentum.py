import random

from utils.generators.base_generator import BaseGenerator

#from base_generator import BaseGenerator
from utils.word_lists import random_noun


class MomentumGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="momentum_")



    def choose_problem_dict(self, problem_type, difficulty):
        if problem_type == "Momentum":
            return self.momentum_q()
        

    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "Momentum": {
                "honors": r"""
                 p \;=\; m \cdot v
                """,

                "conceptual": r"""
                    p \;=\; m \cdot v
                    \quad , \quad
                    m \;=\; \frac{p}{v}
                    \quad , \quad
                    v \;=\; \frac{p}{m}
                """}
        }

    

    def momentum_q(self, solve_for = None):
        """
        momentum_q
        
        :param solve_for: accepts momentum, mass, or velocity
        """
        noun = random_noun()
        mass  = random.randint(1,25)
        velocity = random.randint(1,25)
        momentum = mass*velocity

        if solve_for == None:
            solve_for = random.choice(["momentum","mass","velocity"])
        
        if solve_for == "momentum":
            question = f"A {mass} kg {noun} moves at {velocity} m/s. What is the {noun}'s momentum?"
            answer = momentum
            unit = "Momentum (Ns)"
        if solve_for == "mass":
            question = f"A {noun} moves at {velocity} m/s, and has a momentum of {momentum} Ns. What is the {noun}'s mass?"
            answer = mass
            unit = "Mass (kg)"
        if solve_for == "velocity":
            question = f"A {mass} kg {noun} has a momentum of {momentum} Ns. What is the {noun}'s velocity?"
            answer = velocity
            unit = "Velocity (m/s)"
            
        return {"question": question, "answers": [answer], "units": [unit]}


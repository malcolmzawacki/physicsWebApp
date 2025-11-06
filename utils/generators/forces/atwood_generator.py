import random
from random import randint as ri
import math
from utils.word_lists import random_noun
from utils.generators.base_generator import BaseGenerator


class AtwoodGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="atwood_")
    

    def half_atwood_nums(self):
        mass_1 = ri(1,20)
        mass_2 = ri(1,20)
        mu_max = mass_2 / mass_1
        return {
            "mass 1": mass_1,
            "mass 2": mass_2,
            "mu max": mu_max
        }
    

    def static_half_atwood(self, solve_for = None):
        """solve for options: tension, mass 1, mass 2, coefficient of friction"""
        eq_nums = self.half_atwood_nums()
        tension = 10*eq_nums["mu max"]*eq_nums["mass 1"]
        if solve_for == None:
            solve_for = random.choice(
                [
                    "tension",
                    "mass 1",
                    "mass 2",
                    "coefficient of friction"
                ]
            )
        noun1 = random_noun()
        noun2 = random_noun()
        if solve_for == "tension":
          question = f"""A {eq_nums["mass 1"]} kg {noun1} is at rest on a table, 
          despite being attached by a string to a {eq_nums["mass 2"]} kg {noun2} hanging off the table.
          This is mainly due to the {eq_nums['mu max']:.2f} coefficient of static friction.
          What is the tension in the string?"""
          answer = [tension]
          unit = ["Tension (Newtons)"]
        elif solve_for == "mass 1":
          question = f"""A {noun1} is at rest on a table, 
          despite being attached by a string to a {eq_nums["mass 2"]} kg {noun2} hanging off the table.
          This is partly due to the {eq_nums['mu max']:.2f} coefficient of static friction, which is just high enough to keep the system at rest.
          What mass of the {noun1} would produce the necessary frictional force to hold the system in place?"""
          answer = [eq_nums["mass 1"]]
          unit = ["mass 1 (kg)"]
        elif solve_for == "mass 2":
          question = f"""A {eq_nums["mass 1"]} kg {noun1} is at rest on a table, 
          despite being attached by a string to a {noun2} hanging off the table.
          This is partly due to the {eq_nums['mu max']:.2f} coefficient of static friction, which is just high enough to keep the system at rest.
          What is the maximum mass of the {noun2} that the frictional force could oppose to hold the system in place?"""
          answer = [eq_nums["mass 2"]]
          unit = ["mass 2 (kg)"]
        else: # coef of frict
          question = f"""A {eq_nums["mass 1"]} kg {noun1} is at rest on a table, 
          despite being attached by a string to a {eq_nums["mass 2"]} kg {noun2} hanging off the table.
          This is partly due to the coefficient of static friction, which is just high enough to keep the system at rest.
          What coefficient of static friction would hold the system in place?"""
          answer = [eq_nums["mu max"]]
          unit = ["coefficient of friction"]
        return {"question": question, "answers": answer, "units": unit}
           
            


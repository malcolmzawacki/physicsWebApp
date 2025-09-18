# utils/generators/collision_generator.py
import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
try:
    from .base_generator import BaseGenerator
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from utils.generators.base_generator import BaseGenerator

from utils.word_lists import random_noun

class ForceGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="force_")
    


        
    def numbers(self, difficulty):
        mu = random.randint(1,99) / 100
        m = random.randint(1,difficulty)
        a = random.randint(1,difficulty)
        friction = mu*m*10
        netForce = m*a
        appliedForce = netForce + friction
        return m, a, netForce, mu, appliedForce
       
    
    def generate_force_question(self, difficulty):
        range = self.get_difficulty_range(difficulty)
        m, a, netForce, mu, appliedForce = self.numbers(range)
        object1 = random_noun()
        if difficulty == "Easy":

            flip = random.randint(1,3)
            if flip == 1: # find acceleration
                 question = f"""A net force of {netForce:.2f} Newtons accelerates a {m:.2f} kg {object1}.
                 What is the resulting acceleration?"""
                 answer = [a]
                 unit = [f"{object1} acceleration (m/s2)"]
            elif flip == 2: # find net force
                question = f"""A {m:.2f} kg {object1} accelerates at {a:.2f} m/s2.
                What net Force caused this?"""
                answer = [netForce]
                unit = [f"Net Force on {object1} (N)"]
            else: #flip = 3, find mass
                question = f"""A net force of {netForce:.2f} Newtons accelerates a {object1} at {a:.2f} m/s2.
                What is the mass of the {object1}?"""
                answer = [m]
                unit = [f"{object1} mass (kg)"]

        else:
            flip = random.randint(1,3)
            if flip == 1: # find friction, mu
                question = f"""A {appliedForce} Newton force accelerates a {m:.2f} kg {object1} at {a:.2f} m/s2.
                What is the net force on {object1}? What is the coefficient of friction?"""
                answer = [netForce, mu]
                unit = [f"Net Force (N)",f"coefficient of friction"]

            elif flip == 2: # find acceleration
                question = f"""A {appliedForce} Newton force accelerates a {m:.2f} kg {object1} over a surface with a
                 coefficient of friction of {mu:.2f} .
                What is the net force on {object1}? What is the resulting acceleration?"""
                answer = [netForce, a]
                unit = [f"Net Force (N)",f"acceleration (m/s2)"]

            else: # flip == 3, find applied force
                question = f"""A {m:.2f} kg {object1} accelerates at {a:.2f} m/s2 
                over a surface with a coefficient of friction of {mu:.2f} .
                What is the net force on {object1}? What applied force produced this acceleration?"""
                answer = [netForce, appliedForce]
                unit = [f"Net Force (N)",f"Applied Force (N)"]

    
        return {"question": question, "answers": answer, "units": unit}
        

        
    def choose_problem_dict(self,problem_type,difficulty):
        if problem_type == "Newton's Second Law":
            return self.generate_force_question(difficulty)



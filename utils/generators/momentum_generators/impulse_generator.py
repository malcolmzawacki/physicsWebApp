import random

from utils.generators.base_generator import BaseGenerator

#from base_generator import BaseGenerator
from utils.word_lists import random_noun


class ImpulseGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="impulse_")
    

    def choose_problem_dict(self, problem_type, difficulty):
        if problem_type == "Change in Momentum":
            return self.change_in_momentum(difficulty)
        

    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "Change in Momentum": {
                "honors": r"""
                 \Delta p \;=\; F \cdot t \;=\; m \cdot \Delta v
                """,

                "conceptual": r"""
                     \Delta p \;=\; F \cdot t
                     \Delta p \;=\; m \cdot \Delta v
                     \Delta p \;=\; m (v_f - v_i)
                """}
        }
           
    
    def impulse_q(self, difficulty, solve_for = None):
        pass


    def change_in_momentum(difficulty, solve_for = None):
        """Easy solve_fors: change in momentum, initial momentum, final momentum
        Medium solve_fors: mass, change in velocity, change in momentum
        Hard solve_fors: initial velocity, final velocity, mass, change in momentum"""
        noun = random_noun()
        if difficulty == "Easy":
            p_i = random.randint(5,50)
            delta_p = random.randint(3,p_i - 1)
            sign = random.choice([(1,"speeds up"),(-1,"slows down")]) # half the time loses momentum
            delta_p*=sign[0]
            p_f = p_i + delta_p
            if solve_for == None:
                solve_for = random.choice([
                    "change in momentum",
                    "initial momentum",
                    "final momentum"])
            if solve_for == "change in momentum":
                question = f"""A {noun} starts with {p_i} Ns of momentum, 
                and {sign[1]} until its momentum is {p_f}. How much did the momentum change?"""
                answer = [delta_p]
                unit = ["Change in Momentum (Ns)"]

            elif solve_for == "initial momentum":
                question = f"""A {noun} {sign[1]} by {delta_p} Ns,
                leaving it with a momentum of {p_f}. 
                How much momentum did the {noun} start with?"""
                answer = [p_i]
                unit = ["Initial Momentum (Ns)"]

            else:
                question = f"""A {noun} starts with {p_i} Ns of momentum, 
                and {sign[1]} by {delta_p} Ns. 
                How much momentum does the {noun} have now?"""
                answer = [p_f]
                unit = ["Final Momentum (Ns)"]
            return {"question": question, "answers": [answer], "units": [unit]}

        elif difficulty == "Medium":
            if solve_for == None:
                solve_for = random.choice([
                    "change in momentum",
                    "mass",
                    "change in velocity"])
            mass = random.randint(2,20)
            v_i = random.randint(4,20)
            delta_v = random.randint(3,v_i - 1)
            sign = random.choice([(1,"speeds up"),(-1,"slows down")]) # half the time loses momentum
            delta_v*=sign[0]
            v_f = v_i + delta_v
            delta_p = mass*delta_v
            if solve_for == "change in momentum":
                question = f"""A {mass} kg {noun} {sign[1]} from {v_i} m/s to {v_f} m/s.
                What is the change in the {noun}'s momentum?"""
                answer = [delta_p]
                unit = ["Change in Momentum (Ns)"]
            elif solve_for == "mass":
                question = f"""A {noun} {sign[1]} from {v_i} m/s to {v_f} m/s.
                If this changed the {noun}'s momentum by {delta_p} Ns, 
                what is the mass of the {noun}?"""
                answer = [mass]
                unit = ["Mass (kg)"]
            else:
                question = f"""A {mass} kg {noun} {sign[1]}.
                It started with a momentum of {mass*v_i} Ns, and ended with {mass*v_f} Ns.
                How much did the velocity of the {noun} change?"""
                answer = [delta_v]
                unit = ["Change in Velocity (m/s)"]
            return {"question": question, "answers": [answer], "units": [unit]}

        
        
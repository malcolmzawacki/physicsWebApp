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
                 \Delta p \;=\; m  (v_f - v_i)
                """,

                "conceptual": r"""
                     \Delta p \;=\; p_f - p_i 
                     \quad , \quad
                     p_f \;=\; p_i + \Delta p
                     \quad , \quad
                     p_i \;=\; p_f - \Delta p
                     \newline ~ \newline ~ \newline
                     \Delta p \;=\; m (v_f - v_i)
                      \quad , \quad
                      v_f \;=\; v_i + \frac{\Delta p}{m}
                      \quad , \quad
                      v_i \;=\; v_f - \frac{\Delta p}{m}
                     \newline ~ \newline ~ \newline 
                     \Delta p \;=\; m \Delta v
                     \quad , \quad
                     m \;=\; \frac{\Delta p}{\Delta v}
                     \quad , \quad
                     \Delta v \;=\; \frac{\Delta p}{m}
                     \newline ~ \newline ~ \newline 
                     \Delta v \;=\; v_f - v_i 
                     \quad , \quad
                     v_f \;=\; v_i + \Delta v
                     \quad , \quad
                     v_i \;=\; v_f - \Delta v
                      

    
                """}
        }
           
    
    def impulse_q(self, difficulty, solve_for = None):
        """
        Docstring for impulse_q
        
        :param solve_for: 
        Easy - ["change in momentum", "force","time"]
        \n Medium - ["mass","change in velocity","force", "time"]
        \n Hard - ["mass", "initial velocity", "final velocity", "force", "time"]
   
        """
        noun = random_noun()
        if difficulty == "Easy":

            force = random.randint(5,40)
            time = random.randint(5,40)
            delta_p = force*time

            if solve_for == None:
                solve_for = random.choice([
                    "change in momentum", 
                    "force",
                    "time"])
                
            if solve_for == "change in momentum":
                question = f""" """
                answer = [delta_p]
                unit = ["Impulse (Ns)"]

            elif solve_for == "force":
                question = f""""""
                answer = []
                unit = ["Force (N)"]

            else: # time
                question = f""""""
                answer = []
                unit = ["Time (s)"]

        elif difficulty == "Medium":

            mass = random.randint(2,20)
            v_i = random.randint(4,20)
            delta_v = random.randint(3,v_i - 1)
            sign = random.choice([(1,"speeds up"),(-1,"slows down")]) # half the time loses momentum
            delta_v*=sign[0]
            v_f = v_i + delta_v
            delta_p = mass*delta_v
        
            if solve_for == None:
                solve_for = random.choice([
                    "mass",
                    "change in velocity",
                    "force", 
                    "time"])
           
            if solve_for == "change in velocity":
                question = f""" """
                answer = [delta_v]
                unit = ["Change in Velocity (m/s)"]
            
            elif solve_for == "mass":
                question = f""""""
                answer = []
                unit = ["mass (kg)"]

            elif solve_for == "force":
                question = f""""""
                answer = []
                unit = ["Force (N)"]

            else: # time
                question = f""""""
                answer = []
                unit = ["Time (s)"]

        elif difficulty == "Hard":

            mass = random.randint(2,20)
            v_i = random.randint(4,20)
            delta_v = random.randint(3,v_i - 1)
            sign = random.choice([(1,"speeds up"),(-1,"slows down")]) # half the time loses momentum
            delta_v*=sign[0]
            v_f = v_i + delta_v
            delta_p = mass*delta_v
        
            if solve_for == None:
                solve_for = random.choice([
                    "mass", 
                    "initial velocity", 
                    "final velocity", 
                    "force", 
                    "time"
                ])
           
            if solve_for == "initial velocity":
                question = f"""A {mass} kg {noun} .
                What was the initial velocity of the {noun}?"""
                answer = [v_i]
                unit = ["Initial Velocity (m/s)"]
            elif solve_for == "final velocity":
                question = f"""A {mass} kg {noun} .
                What is the final velocity of the {noun}?"""
                answer = [v_f]
                unit = ["Final Velocity (m/s)"]
            elif solve_for == "mass":
                question = f"""?"""
                answer = [mass]
                unit = ["Mass (kg)"]
            elif solve_for == "force":
                question = f""" """
                answer = []
                unit = ["Force (N)"]
            else: # time
                question = f""" """
                answer = []
                unit = ["Time (s)"]
        return {"question": question, "answers": answer, "units": unit}


    def change_in_momentum(self, difficulty, solve_for = None):
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
                and {sign[1]} until its momentum is {p_f} Ns. How much did the momentum change?"""
                answer = [delta_p]
                unit = ["Change in Momentum (Ns)"]

            elif solve_for == "initial momentum":
                question = f"""A {noun} {sign[1]} by {delta_p} Ns,
                leaving it with a momentum of {p_f} Ns. 
                How much momentum did the {noun} start with?"""
                answer = [p_i]
                unit = ["Initial Momentum (Ns)"]

            else: # final momentum
                question = f"""A {noun} starts with {p_i} Ns of momentum, 
                and {sign[1]} by {delta_p} Ns. 
                How much momentum does the {noun} have now?"""
                answer = [p_f]
                unit = ["Final Momentum (Ns)"]

        elif difficulty == "Medium":

            mass = random.randint(2,20)
            v_i = random.randint(4,20)
            delta_v = random.randint(3,v_i - 1)
            sign = random.choice([(1,"speeds up"),(-1,"slows down")]) # half the time loses momentum
            delta_v*=sign[0]
            v_f = v_i + delta_v
            delta_p = mass*delta_v
        
            if solve_for == None:
                solve_for = random.choice([
                    "change in momentum",
                    "mass",
                    "change in velocity"])
           
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

            else: # change in velocity
                question = f"""A {mass} kg {noun} {sign[1]}.
                It started with a momentum of {mass*v_i} Ns, and ended with {mass*v_f} Ns.
                How much did the velocity of the {noun} change?"""
                answer = [delta_v]
                unit = ["Change in Velocity (m/s)"]

        elif difficulty == "Hard":

            mass = random.randint(2,20)
            v_i = random.randint(4,20)
            delta_v = random.randint(3,v_i - 1)
            sign = random.choice([(1,"speeds up"),(-1,"slows down")]) # half the time loses momentum
            delta_v*=sign[0]
            v_f = v_i + delta_v
            delta_p = mass*delta_v
        
            if solve_for == None:
                solve_for = random.choice([
                    "initial velocity", 
                    "final velocity",
                    "mass", 
                    "change in momentum"
                ])
           
            if solve_for == "initial velocity":
                question = f"""A {mass} kg {noun} {sign[1]}, changing its momentum by {delta_p} Ns.
                It ends up moving at {v_f} m/s.
                What was the initial velocity of the {noun}?"""
                answer = [v_i]
                unit = ["Initial Velocity (m/s)"]
            elif solve_for == "final velocity":
                question = f"""A {mass} kg {noun} {sign[1]} from {v_i} m/s, 
                changing its momentum by {delta_p} Ns.
                What is the final velocity of the {noun}?"""
                answer = [v_f]
                unit = ["Final Velocity (m/s)"]
            elif solve_for == "mass":
                question = f"""A {noun} {sign[1]} from {v_i} m/s to {v_f} m/s.
                If this changed the {noun}'s momentum by {delta_p} Ns, 
                what is the mass of the {noun}?"""
                answer = [mass]
                unit = ["Mass (kg)"]
            else: # change in momentum
                question = f"""A {mass} kg {noun} {sign[1]} from {v_i} m/s to {v_f} m/s.
                What is the change in the {noun}'s momentum?"""
                answer = [delta_p]
                unit = ["Change in Momentum (Ns)"]
        return {"question": question, "answers": answer, "units": unit}

        
        
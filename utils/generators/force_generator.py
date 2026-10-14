# Newton's second law: scalar net-force cases and legacy friction branches.
import random

from utils.generators.base_generator import BaseGenerator

from utils.word_lists import random_noun
from utils.quantities import PROFILES, QUANTITIES, equation
from utils.setup_schema import make_setup

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
       
    
    def generate_force_question(self, difficulty, *, variant=None):
        range = self.get_difficulty_range(difficulty)
        m, a, netForce, mu, appliedForce = self.numbers(range)
        object1 = random_noun()
        if difficulty == "Easy":
            flip = random.randint(1, 3) if variant is None else variant
            if flip not in (1, 2, 3):
                raise ValueError("Newton's Second Law requires variant 1, 2, or 3")
            target = {1: "a", 2: "Fnet", 3: "m"}[flip]
            roles = PROFILES["newtons_second_law"]
            values = {"Fnet": netForce, "m": m, "a": a}
            units = {key: QUANTITIES[role.quantity].unit for key, role in roles.items()}
            if target == "a":
                question = (f"A net force of {netForce:.2f} {units['Fnet']} acts on a {m:.2f} {units['m']} {object1}. "
                            "What is the resulting acceleration?")
            elif target == "Fnet":
                question = (f"A {m:.2f} {units['m']} {object1} accelerates at {a:.2f} {units['a']}. "
                            "What is the net force on it?")
            else:
                question = (f"A net force of {netForce:.2f} {units['Fnet']} accelerates a {object1} at {a:.2f} {units['a']}. "
                            f"What is the mass of the {object1}?")
            return {
                "question": question, "answers": [values[target]],
                "units": [f"{roles[target].name} ({units[target]})"],
                "extras": {"setup": make_setup("newtons_second_law", values, set(values) - {target}, [target])},
            }

        else:
            flip = random.randint(1,3) if variant is None else variant
            if flip == 1: # find friction, mu
                question = f"""A {appliedForce:.2f} Newton force accelerates a {m:.2f} kg {object1} at {a:.2f} m/s².
                What is the net force on {object1}? What is the coefficient of friction?"""
                answer = [netForce, mu]
                unit = [f"Net Force (N)",f"coefficient of friction"]

            elif flip == 2: # find acceleration
                question = f"""A {appliedForce:.2f} Newton force accelerates a {m:.2f} kg {object1} over a surface with a
                 coefficient of friction of {mu:.2f} .
                What is the net force on {object1}? What is the resulting acceleration?"""
                answer = [netForce, a]
                unit = [f"Net Force (N)",f"acceleration (m/s²)"]

            else: # flip == 3, find applied force
                question = f"""A {m:.2f} kg {object1} accelerates at {a:.2f} m/s²
                over a surface with a coefficient of friction of {mu:.2f} .
                What is the net force on {object1}? What applied force produced this acceleration?"""
                answer = [netForce, appliedForce]
                unit = [f"Net Force (N)",f"Applied Force (N)"]

    
        question += " The object slides on level ground, with a horizontal applied force in the direction of motion."
        given = {"Mass (kg)": m, "Applied force (N)": appliedForce, "Acceleration (m/s²)": a} if flip == 1 else {"Mass (kg)": m, "Applied force (N)": appliedForce, "Coefficient of friction": mu} if flip == 2 else {"Mass (kg)": m, "Acceleration (m/s²)": a, "Coefficient of friction": mu}
        steps = [{"label": "Normal force (N)", "hint": "Level ground: normal force = mass × g.", "answer": m * 10}]
        if flip == 1:
            steps.append({"label": "Net force (N)", "hint": "Use mass × acceleration. This is also your first final answer.", "answer": netForce})
            steps.append({"label": "Friction force (N)", "hint": "Applied force − net force.", "answer": appliedForce - netForce})
        else:
            steps.append({"label": "Friction force (N)", "hint": "Coefficient of friction × normal force.", "answer": appliedForce - netForce})
            if flip == 3:
                steps.append({"label": "Net force (N)", "hint": "Use mass × acceleration. This is also your first final answer.", "answer": netForce})
        return {"question": question, "answers": answer, "units": unit,
                "extras": {"force_plan": {"given": given, "steps": steps, "targets": unit}}}
        

        
    def choose_problem_dict(self,problem_type,difficulty):
        if problem_type == "Newton's Second Law":
            return self.generate_force_question(difficulty)

    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "Newton's Second Law": {
                      "id": "force.newton-s-second-law",
                      "aliases": ["Newton's Second Law"],
                      "honors": equation("newtons_second_law", r"${Fnet} \;=\; ${m}${a}"),

                      "conceptual": r""" 
                      \Sigma F \;=\; m \cdot a \quad , \quad 
                      a \;=\; \frac{\Sigma F}{m} \quad , \quad 
                      m \;=\; \frac{\Sigma F}{a}
                      \newline ~ \newline ~ \newline
                      \Sigma F \;=\; F_{right} \;-\; F_{left} \quad , \quad 
                      F_{right} \;=\; \Sigma F \;+\; F_{left} \quad , \quad 
                      F_{left} \;=\; F_{right} \;-\; \Sigma F
                      \newline ~ \newline ~ \newline
                      F_g \;=\; m \cdot g \quad , \quad 
                      m \;=\; \frac{F_g}{g} \quad , \quad 
                      F_g \;=\; F_N
                      \newline ~ \newline ~ \newline
                      F_f \;=\; \mu \cdot m \cdot g \quad , \quad 
                      \mu \;=\; \frac{F_f}{m \cdot g} \quad , \quad 
                      F_N \;=\; \frac{F_f}{\mu}
                      """
            },
        }




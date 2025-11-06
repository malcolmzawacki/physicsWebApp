import random
from random import randint as ri
import math
from utils.word_lists import random_noun
from utils.generators.base_generator import BaseGenerator


class AtwoodGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="atwood_")
    
    def choose_problem_dict(self, problem_type, difficulty):
        if problem_type == "Static Friction Half Atwood":
            return self.static_half_atwood()
        elif problem_type == "Frictionless Half Atwood":
           return self.frictionless_half_atwood()
        elif problem_type == "Kinetic Friction Half Atwood":
           return self.kinetic_half_atwood()
    
    
    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "Static Friction Half Atwood": {
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
            "Frictionless Half Atwood": {
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
            "Kinetic Friction Half Atwood": {
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

    def half_atwood_nums(self):
        mass_1 = ri(5,25)
        mass_2 = ri(1,mass_1-1) # ensures mu_max < 1
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
    

    def frictionless_half_atwood(self, solve_for = None):
       """solve_for options: tension, mass 1, mass 2, acceleration"""
       if solve_for == None:
          solve_for = random.choice([
             "tension",
             "mass 1",
             "mass 2",
             "acceleration"
          ])
       eq_nums = self.half_atwood_nums()
       noun1 = random_noun()
       noun2 = random_noun()
       accel = 10*eq_nums["mass 2"] / (eq_nums["mass 1"] + eq_nums["mass 2"])
       tension = eq_nums["mass 1"]*accel

       q_template_m1_m2 = f"""A {eq_nums["mass 1"]} kg {noun1} is placed on a table with negligible friction. 
          It is attached by a string to a {eq_nums["mass 2"]} kg {noun2} hanging off the table."""
       q_template_m1_a = f"""A {eq_nums["mass 1"]} kg {noun1} is placed on a table with negligible friction. 
          It is attached by a string to a {noun2} hanging off the table, 
          which causes the system to accelerate at {accel:.2f} m/s2."""
       q_template_m1_Ft = f"""A {eq_nums["mass 1"]} kg {noun1} is placed on a table with negligible friction. 
          It is attached by a string to a {noun2} hanging off the table, 
          which produces a tension of {tension:.2f} Newtons."""
       q_template_m2_a = f"""A {noun1} is placed on a table with negligible friction. 
          It is attached by a string to a {eq_nums["mass 2"]} kg {noun2} hanging off the table, 
          which causes the system to accelerate at {accel:.2f} m/s2."""
       q_template_m2_Ft = f"""A {noun1} is placed on a table with negligible friction. 
          It is attached by a string to a {eq_nums["mass 2"]} kg {noun2} hanging off the table, 
          which produces a tension of {tension:.2f} Newtons."""
       q_template_a_Ft = f"""A {noun1} is placed on a table with negligible friction. 
          It is attached by a string to a {noun2} hanging off the table, 
          which produces a tension of {tension:.2f} Newtons and an acceleration of {accel:.2f} m/s2."""
       if solve_for == "tension":
          question = random.choice([q_template_m1_m2, q_template_m1_a, q_template_m2_a])
          question = question + " What is the tension in the string?"
          answer = [tension]
          unit = ["Tension (Newtons)"]
       elif solve_for == "mass 1":
          question = random.choice([q_template_a_Ft, q_template_m2_a, q_template_m2_Ft])
          question = question + f" What is the mass of the {noun1}?"
          answer = [eq_nums["mass 1"]]
          unit = [f"{noun1} mass (kg)"]
       elif solve_for == "mass 2":
          question = random.choice([q_template_a_Ft, q_template_m1_a, q_template_m1_Ft])
          question = question + f" What is the mass of the {noun2}?"
          answer = [eq_nums["mass 2"]]
          unit = [f"{noun2} mass (kg)"]
       else: # acceleration
          question = random.choice([q_template_m1_Ft, q_template_m2_Ft, q_template_m1_m2])
          question = question + f" What is the mass of the {noun1}?"
          answer = [accel]
          unit = ["acceleration (m/s2)"]
       return {"question": question, "answers": answer, "units": unit}


    def kinetic_half_atwood(self, solve_for = None):
       """Solve for options: 
       acceleration and tension,
       acceleration and coefficient,
       coefficient and tension,
       mass 2 and tension,
       mass 2 and coefficient,
       mass 1 and acceleration,
       mass 1 and tension,
       mass 1 and coefficient,
       mass 1 and mass 2
       """

       eq_nums = self.half_atwood_nums()
       mu_max = eq_nums["mu max"]
       mu_range = math.floor(100*mu_max)
       mu = ri(1,mu_range)/100
       m1 = eq_nums["mass 1"]
       m2 = eq_nums["mass 2"]
       accel = 10*((m2 - mu*m1)/(m1+m2))
       tension = m2*(10-accel)

       if solve_for == None:
          solve_for = random.choice([
             "acceleration and tension",
             "acceleration and coefficient",
             "coefficient and tension",
             "mass 2 and acceleration",
             "mass 2 and tension",
             "mass 2 and coefficient",
             "mass 1 and acceleration",
             "mass 1 and tension",
             "mass 1 and coefficient",
             "mass 1 and mass 2"
          ])
       
       noun1 = random_noun()
       noun2 = random_noun()
       start_str1_w_m1 = f"A {m1} kg {noun1} on a table is connected by a string to "
       start_str2_w_m2 = f"a {m2} kg {noun2} hanging off the table. "
       start_str1_no_m1 = f"A {noun1} on a table is connected by a string to "
       start_str2_no_m2 = f"a {noun2} hanging off the table. "
       coeff_str = f"The coefficient of kinetic friction between the {noun1} and the table is {mu:.2f}. "
       tension_str = f"The tension in the string is {tension:.2f} Newtons. "
       accel_str = f"The system accelerates at {accel:.2f} m/s^2. "
       m1_q = f"What is the mass of the {noun1}? "
       m2_q = f"What is the mass of the {noun2}? "
       mu_q = f"What is the coefficient of friction between the {noun1} and the table? "
       tension_q = "What is the tension in the string? "
       accel_q = "What is the acceleration of the system? "
       if solve_for == "acceleration and tension":
         question = start_str1_w_m1 + start_str2_w_m2 + coeff_str + accel_q + tension_q
         answers = [accel, tension]
         units = ["Acceleration (m/s^2)", "Tension (Newtons)"]
       elif solve_for == "acceleration and coefficient":
         question = question = start_str1_w_m1 + start_str2_w_m2 + tension_str + mu_q + accel_q
         answers = [mu, accel]
         units = ["Coefficient of Kinetic Friction","Acceleration (m/s^2)"]
       elif solve_for == "coefficient and tension":
         question = start_str1_w_m1 + start_str2_w_m2 + accel_str + mu_q + tension_q
         answers = [mu, tension]
         units = ["Coefficient of Kinetic Friction","Tension (Newtons)"]
       elif solve_for == "mass 2 and acceleration":
         question = start_str1_w_m1 + start_str2_no_m2 + coeff_str + tension_str + m2_q + accel_q
         answers = [m2, accel]
         units = [f"{noun2} mass (kg)","Acceleration (m/s^2)"]
       elif solve_for == "mass 2 and tension":
         question = start_str1_w_m1 + start_str2_no_m2 + coeff_str + accel_str + m2_q + tension_q
         answers = [m2, tension]
         units = [f"{noun2} mass (kg)","Tension (Newtons)"]
       elif solve_for == "mass 2 and coefficient":
         question = start_str1_w_m1 + start_str2_no_m2 + tension_str + accel_str + m2_q + mu_q
         answers = [m2, mu]
         units = [f"{noun2} mass (kg)","Coefficient of Kinetic Friction"]
       elif solve_for == "mass 1 and acceleration":
         question = start_str1_no_m1 + start_str2_w_m2 + coeff_str + tension_str + m1_q + accel_q
         answers = [m1, accel]
         units = [f"{noun1} mass (kg)","Acceleration (m/s^2)"]
       elif solve_for == "mass 1 and tension":
         question = start_str1_no_m1 + start_str2_w_m2 + coeff_str + accel_str + m1_q + tension_q
         answers = [m1, tension]
         units = [f"{noun1} mass (kg)","Tension (Newtons)"]
       elif solve_for == "mass 1 and coefficient":
         question = start_str1_no_m1 + start_str2_w_m2 + tension_str + accel_str + m1_q + mu_q
         answers = [m1, mu]
         units = [f"{noun1} mass (kg)","Coefficient of Kinetic Friction"]
       elif solve_for == "mass 1 and mass 2":
         question = start_str1_no_m1 + start_str2_no_m2 + coeff_str + tension_str + accel_str + m1_q + m2_q
         answers = [m1, m2]
         units = [f"{noun1} mass (kg)", f"{noun2} mass (kg)"]
       return {"question": question, "answers": answers, "units": units}
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
    
    # region static atwood
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

        diagram_data = {
            "m1": eq_nums["mass 1"],
            "m2": eq_nums["mass 2"],
            "mu_s": eq_nums["mu max"]
        }
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
        return {"question": question, "answers": answer, "units": unit, "diagram_data": diagram_data}
    

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

       diagram_data = {
           "m1": eq_nums["mass 1"],
           "m2": eq_nums["mass 2"]
       }

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
       return {"question": question, "answers": answer, "units": unit, "diagram_data": diagram_data}


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

       diagram_data = {
            "m1": m1,
            "m2": m2,
            "mu_k": mu
        }

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
       return {"question": question, "answers": answers, "units": units, "diagram_data": diagram_data}
    

    def generate_diagram(self, diagram_data: dict, problem_type: str, difficulty: str):
        """
        Generate a Matplotlib figure for the half-Atwood problem.
        This method is called by the Interface's add_diagram_smart().
        """
        import matplotlib.pyplot as plt
        plt.tight_layout()
        plt.style.use("dark_background")
        # Increase figsize height to fit table
        fig, ax = plt.subplots(figsize=(5, 4))

        # 1. Get data
        m1 = diagram_data.get("m1")
        m2 = diagram_data.get("m2")
        
        # 2. Draw static components (table, pulley, blocks, strings)
        
        # Table
        ax.plot([-5, 1], [0, 0], 'w-', lw=2)  # Table surface
        ax.plot([1, 1], [0, -5], 'w-', lw=2)  # Table leg
        
        # Pulley
        circle = plt.Circle((1, 0), 0.5, color='gray', fill=True, zorder=5)
        ax.add_artist(circle)
        
        # Mass 1 (on table)
        rect1 = plt.Rectangle((-2, 0), 1.5, 1, color='cyan', zorder=10)
        ax.add_artist(rect1)
        ax.text(-1.25, 0.5, '$m_1$', color='black', ha='center', va='center', fontsize=12, zorder=11)

        
        # Mass 2 (hanging)
        rect2 = plt.Rectangle((1.5, -4), 1, 1, color='magenta', zorder=10)
        ax.add_artist(rect2)
        ax.text(2, -3.5, '$m_2$', color='black', ha='center', va='center', fontsize=12, zorder=11)
 
        
        # Strings
        ax.plot([-0.5, 1], [0.5, 0.5], 'w-', zorder=7)  # Horizontal string
        ax.plot([1.5, 1.5], [-3, 0.25], 'w-', zorder=7)  # Vertical string

        # 3. Draw dynamic components (force/acceleration arrows)
        
        # Arrow style
        arrow_style = dict(head_width=0.2, head_length=0.2, fc='yellow', ec='yellow', length_includes_head=True, zorder=20)
        
        if "Static" in problem_type:
            mu_s = diagram_data.get("mu_s", 0)
            ax.set_title(f"Static System (a=0)", color='white')
            # Static friction arrow
            ax.arrow(-1.25, -0.25, -1, 0, **arrow_style)
            ax.text(-2.25, -0.5, '$f_s$', color='yellow', ha='center', va='top', fontsize=12)
            # Tension arrows (equal to m2g)
            ax.arrow(-0.5, 0.25, 0.75, 0, **arrow_style) # On m1
            ax.text(0.125, 0.5, '$F_T$', color='yellow', ha='center', va='bottom', fontsize=12)
            ax.arrow(2, -4, 0, -0.75, **arrow_style) # On m2 (down)
            ax.text(2, -5.5, '$W_2$', color='yellow', ha='center', va='bottom', fontsize=12)
            ax.arrow(2, -3, 0, 0.75, **arrow_style) # On m2 (up)
            ax.text(2, -1.5, '$F_T$', color='yellow', ha='center', va='top', fontsize=12)


        elif "Frictionless" in problem_type:
            ax.set_title("Frictionless System (a > 0)", color='white')
            # Acceleration arrows
            ax.arrow(-1.25, 1.25, 1, 0, **arrow_style) # m1 right
            ax.text(0, 1.25, 'a', color='yellow', ha='center', va='center', fontsize=12)
            ax.arrow(2.5, -3.5, 0, -1, **arrow_style) # m2 down
            ax.text(2.5, -2.5, 'a', color='yellow', ha='center', va='center', fontsize=12)

        elif "Kinetic" in problem_type:
            mu_k = diagram_data.get("mu_k", 0)
            ax.set_title(f"Kinetic System (a > 0, $\mu_k$ > 0)", color='white')
            # Kinetic friction arrow
            ax.arrow(-1.25, -0.25, -1, 0, **arrow_style)
            ax.text(-2.25, -0.5, '$f_k$', color='yellow', ha='center', va='top', fontsize=12)
            # Acceleration arrows
            ax.arrow(-1.25, 1.25, 1, 0, **arrow_style) # m1 right
            ax.text(0, 1.25, 'a', color='yellow', ha='center', va='center', fontsize=12)
            ax.arrow(2.5, -3.5, 0, -1, **arrow_style) # m2 down
            ax.text(2.5, -2.5, 'a', color='yellow', ha='center', va='center', fontsize=12)

        # 4. Clean up the plot
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 3)
        ax.set_aspect('equal')
        ax.axis('off')

        return fig
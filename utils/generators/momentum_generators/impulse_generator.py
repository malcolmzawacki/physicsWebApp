import random
from math import floor
from utils.generators.base_generator import BaseGenerator

#from base_generator import BaseGenerator
from utils.word_lists import random_noun


class ImpulseGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="impulse_")
    

    def choose_problem_dict(self, problem_type, difficulty):
        if problem_type == "Change in Momentum":
            return self.change_in_momentum(difficulty)
        if problem_type == "Change in Momentum (Multiple Choice)":
            return self.change_in_momentum_multiple_choice(difficulty)
        if problem_type == "Impulse":
            return self.impulse_q(difficulty)
        

    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            

            "Change in Momentum (Multiple Choice)": {
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
                """
            },

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
    
                """},

                "Impulse": {
                "honors": r"""
                 F \cdot t \;=\; m  (v_f - v_i)
                """,

                "conceptual": r"""
                     \Delta p \;=\; F \cdot t 
                     \quad , \quad
                     F \;=\; \frac{\Delta p}{t}
                     \quad , \quad
                     t \;=\; \frac{\Delta p}{F}
                     \newline ~ \newline ~ \newline
                     F \;=\; \frac{m \Delta v}{t}
                      \quad , \quad
                      t \;=\; \frac{m \Delta v}{F}
                      \quad , \quad
                      m \;=\; \frac{F \cdot t}{\Delta v}
                      \quad , \quad
                      \Delta v \;=\; \frac{F \cdot t}{m}
                     \newline ~ \newline ~ \newline
                    F \;=\; \frac{m (v_f - v_i)}{t}
                      \quad , \quad
                      t \;=\; \frac{m (v_f - v_i)}{F}
                      \quad , \quad
                      m \;=\; \frac{F \cdot t}{v_f - v_i}
                      \newline ~ \newline ~ \newline 
                      v_f \;=\; v_i + \frac{F \cdot t}{m}
                      \quad , \quad
                      v_i \;=\; v_f - \frac{F \cdot t}{m}
                     \newline ~ \newline ~ \newline 
                     \Delta v \;=\; v_f - v_i 
                     \quad , \quad
                     v_f \;=\; v_i + \Delta v
                     \quad , \quad
                     v_i \;=\; v_f - \Delta v
                """},
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
                question = f"""How large of an impulse would a {force} Newton force produce if it was applied for {time} seconds?"""
                answer = [delta_p]
                unit = ["Impulse (Ns)"]

            elif solve_for == "force":
                question = f"""How large of a force is needed to create a {delta_p} Ns impulse over {time} seconds?"""
                answer = [force]
                unit = ["Force (N)"]

            else: # time
                question = f"""A {force} Newton force produces a {delta_p} Ns impulse. How long was the force applied for?"""
                answer = [time]
                unit = ["Time (s)"]

        elif difficulty == "Medium":

            mass = random.randint(2,20)
            v_i = random.randint(9,20)
            acc = random.randint(2, floor((v_i**(0.5))))
            time = random.randint(2, floor((v_i**(0.5))))
            sign = random.choice([(1,"speeds up"),(-1,"slows down")]) # half the time loses momentum
            acc*=sign[0]
            delta_v = acc*time
            force = mass*acc
        
            if solve_for == None:
                solve_for = random.choice([
                    "mass",
                    "change in velocity",
                    "force", 
                    "time"])
           
            if solve_for == "change in velocity":
                question = f"""A {force} Newton force pushes a {mass} kg {noun} for {time} seconds. 
                How much does the {noun}'s velocity change?"""
                answer = [delta_v]
                unit = ["Change in Velocity (m/s)"]
            
            elif solve_for == "mass":
                question = f"""A {force} Newton force pushes a {noun} for {time} seconds. 
                If the {noun} {sign[1]} by {delta_v} m/s as a result, what is the mass of the {noun}?"""
                answer = [mass]
                unit = ["mass (kg)"]

            elif solve_for == "force":
                question = f"""A {mass} kg {noun} {sign[1]} by {delta_v} m/s over {time} seconds.
                How much force was needed to cause this?"""
                answer = [force]
                unit = ["Force (N)"]

            else: # time
                question = f"""A {force} Newton force pushes a {mass} kg {noun}. 
                 The {noun} {sign[1]} by {delta_v} m/s. How much time was the force applied for?"""
                answer = [time]
                unit = ["Time (s)"]

        elif difficulty == "Hard":

            mass = random.randint(2,20)
            v_i = random.randint(9,20)
            acc = random.randint(2, floor((v_i**(0.5))))
            time = random.randint(2, floor((v_i**(0.5))))
            sign = random.choice([(1,"speeds up"),(-1,"slows down")]) # half the time loses momentum
            acc*=sign[0]
            delta_v = acc*time
            v_f = v_i + delta_v
            force = mass*acc
        
            if solve_for == None:
                solve_for = random.choice([
                    "mass", 
                    "initial velocity", 
                    "final velocity", 
                    "force", 
                    "time"
                ])
           
            if solve_for == "initial velocity":
                question = f"""A {force} Newton force pushes a {mass} kg {noun} for {time} seconds. 
                The {noun} {sign[1]} to {v_f} m/s.
                What was the initial velocity of the {noun}?"""
                answer = [v_i]
                unit = ["Initial Velocity (m/s)"]
            elif solve_for == "final velocity":
                question = f"""A {force} Newton force pushes a {noun} for {time} seconds.
                If the velocity of the {noun} was originally {v_i} m/s, 
                what is the final velocity of the {noun}?"""
                answer = [v_f]
                unit = ["Final Velocity (m/s)"]
            elif solve_for == "mass":
                question = f"""A {force} Newton force pushes a {noun} for {time} seconds. 
                If the {noun} {sign[1]} from {v_i} m/s to {v_f} m/s, what is the mass of the {noun}?"""
                answer = [mass]
                unit = ["Mass (kg)"]
            elif solve_for == "force":
                question = f""""A {mass} kg {noun} {sign[1]} from {v_i} m/s to {v_f} m/s over {time} seconds.
                How much force was needed to cause this?"""
                answer = [force]
                unit = ["Force (N)"]
            else: # time
                question = f"""A {force} Newton force pushes a {mass} kg {noun}. 
                 The {noun} {sign[1]} from {v_i} m/s to {v_f} m/s. 
                 How much time was the force applied for?"""
                answer = [time]
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

    def _format_signed_value(self, value: int, unit: str) -> str:
        return f"{value} {unit}"

    def _build_delta_p_options(self, delta_p: int, unit: str) -> tuple[list[str], str]:
        correct = self._format_signed_value(delta_p, unit)
        wrong_values = { -delta_p }
        while len(wrong_values) < 3:
            offset = random.randint(2, 12)
            candidate = delta_p + random.choice([-1, 1]) * offset
            if candidate != delta_p:
                wrong_values.add(candidate)
        options = [correct] + [self._format_signed_value(val, unit) for val in wrong_values]
        random.shuffle(options)
        return options, correct

    def _build_force_time_options(self, delta_p: int) -> tuple[list[str], str]:
        abs_dp = abs(delta_p)
        factor_pairs = [(f, abs_dp // f) for f in range(2, 21) if abs_dp % f == 0]
        if not factor_pairs:
            factor_pairs = [(1, abs_dp)]
        force, time = random.choice(factor_pairs)
        force *= 1 if delta_p >= 0 else -1
        correct = f"F = {force} N, t = {time} s"

        wrong_options = set()
        attempts = 0
        while len(wrong_options) < 3 and attempts < 100:
            attempts += 1
            f = random.randint(2, 25)
            t = random.randint(1, 12)
            sign = random.choice([-1, 1])
            if sign * f * t == delta_p:
                continue
            wrong_options.add(f"F = {sign * f} N, t = {t} s")

        options = [correct] + list(wrong_options)
        random.shuffle(options)
        return options, correct

    def _diagram_payload(self, mass: int, before_value: int, after_value: int, label_type: str) -> dict:
        if label_type == "momentum":
            unit = "Ns"
            prefix = "p"
        else:
            unit = "m/s"
            prefix = "v"
        before_label = f"{prefix}_i = {before_value} {unit}"
        after_label = f"{prefix}_f = {after_value} {unit}"
        return {
            "mass": mass,
            "before_value": before_value,
            "after_value": after_value,
            "before_label": before_label,
            "after_label": after_label,
            "label_type": label_type,
        }

    def change_in_momentum_multiple_choice(self, difficulty: str) -> dict:
        noun = random_noun()
        if difficulty == "Easy":
            mass = random.randint(2, 10)
            p_i = random.randint(10, 60)
            delta_p = random.randint(4, p_i - 1) * random.choice([-1, 1])
            p_f = p_i + delta_p
            question = f"Use the diagram below to find the change in momentum for the {noun}."
            options, correct = self._build_delta_p_options(delta_p, "Ns")
            diagram_data = self._diagram_payload(mass, p_i, p_f, "momentum")
            unit = ["Change in Momentum (Ns)"]
            return {
                "question": question,
                "answers": [correct],
                "units": unit,
                "diagram_data": diagram_data,
                "button_options": {0: options},
            }

        mass = random.randint(2, 20)
        v_i = random.randint(4, 16)
        if difficulty == "Hard" and random.random() < 0.4:
            v_f = -random.randint(2, 12)
        else:
            delta_v = random.randint(2, v_i - 1) * random.choice([-1, 1])
            v_f = v_i + delta_v
        delta_p = mass * (v_f - v_i)
        diagram_data = self._diagram_payload(mass, v_i, v_f, "velocity")

        if difficulty == "Medium":
            question = f"Use the diagram to find the change in momentum for the {noun}."
            options, correct = self._build_delta_p_options(delta_p, "Ns")
            unit = ["Change in Momentum (Ns)"]
        else:
            question = "Use the diagram to choose the force-time pair that matches the impulse."
            options, correct = self._build_force_time_options(delta_p)
            unit = ["Impulse (N*s)"]

        return {
            "question": question,
            "answers": [correct],
            "units": unit,
            "diagram_data": diagram_data,
            "button_options": {0: options},
        }

    def generate_diagram(self, diagram_data: dict, problem_type: str, difficulty: str):
        import math
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle, Polygon

        fig, ax = plt.subplots(figsize=(7, 3.5))
        fig.patch.set_facecolor("#0b1220")
        ax.set_facecolor("#0b1220")
        ax.set_xlim(-1, 10)
        ax.set_ylim(-0.5, 3.5)
        ax.axis("off")

        box_w = 2.4
        box_h = 1.3
        left_x = 0.6
        right_x = 6.8
        box_y = 0.6

        left_box = Rectangle((left_x, box_y), box_w, box_h, facecolor="#1e3a8a", edgecolor="#93c5fd", linewidth=2)
        right_box = Rectangle((right_x, box_y), box_w, box_h, facecolor="#14532d", edgecolor="#86efac", linewidth=2)
        ax.add_patch(left_box)
        ax.add_patch(right_box)

        mass = diagram_data["mass"]
        ax.text(left_x + box_w / 2, box_y + box_h / 2, f"m = {mass} kg", ha="center", va="center", fontsize=10, color="#f8fafc")
        ax.text(right_x + box_w / 2, box_y + box_h / 2, f"m = {mass} kg", ha="center", va="center", fontsize=10, color="#f8fafc")
        ax.text(left_x + box_w / 2, box_y - 0.2, "Before", ha="center", va="top", fontsize=9, color="#e2e8f0")
        ax.text(right_x + box_w / 2, box_y - 0.2, "After", ha="center", va="top", fontsize=9, color="#e2e8f0")

        before_value = diagram_data["before_value"]
        after_value = diagram_data["after_value"]
        max_value = max(abs(before_value), abs(after_value), 1)
        arrow_max = 2.6
        arrow_min = 1.2

        def draw_arrow(center_x: float, center_y: float, value: int, label: str, color: str) -> None:
            magnitude = abs(value)
            length = arrow_min + (arrow_max - arrow_min) * (magnitude / max_value)
            direction = 1 if value >= 0 else -1
            start_x = center_x - (length / 2) * direction
            ax.arrow(
                start_x,
                center_y,
                length * direction,
                0,
                head_width=0.18,
                head_length=0.25,
                length_includes_head=True,
                color=color,
                linewidth=2,
            )
            ax.text(center_x, center_y + 0.25, label, ha="center", va="bottom", fontsize=10, color=color)

        arrow_y = box_y + box_h + 0.6
        draw_arrow(left_x + box_w / 2, arrow_y, before_value, diagram_data["before_label"], "#93c5fd")
        draw_arrow(right_x + box_w / 2, arrow_y, after_value, diagram_data["after_label"], "#86efac")

        boom_center_x = (left_x + box_w + right_x) / 2
        boom_center_y = box_y + box_h / 2 + 0.3
        spikes = 12
        inner_r = 0.6
        outer_r = 1.1
        points = []
        for i in range(spikes * 2):
            angle = i * (math.pi / spikes)
            radius = outer_r if i % 2 == 0 else inner_r
            points.append(
                (boom_center_x + radius * math.cos(angle), boom_center_y + radius * math.sin(angle))
            )
        boom = Polygon(points, closed=True, facecolor="#f59e0b", edgecolor="#fbbf24", linewidth=2)
        ax.add_patch(boom)
        ax.text(boom_center_x, boom_center_y, "IMPULSE", ha="center", va="center", fontsize=10, weight="bold", color="#0f172a")

        return fig

        
        

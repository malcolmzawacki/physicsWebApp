from random import randint as ri
from utils.generators.base_generator import BaseGenerator
from utils.word_lists import random_noun
from utils.generators.energy.energy_basics import EnergyBasicsGenerator
import math
EBG = EnergyBasicsGenerator()

class EnergyConservationGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="energy_conserv_")

    @staticmethod
    def _organized(family, values, target, question, unit, reverse):
        # The same displayed facts drive organizer checks and the final answer.
        values = {key: round(value, 2) for key, value in values.items()}
        if family == "gravity_spring" and target != "m":
            values["m"] = max(0.01, values["m"])
        m = values["m"]
        if family == "gravity_motion":
            answer = math.sqrt(20 * values["h"]) if target == "v" else values["v"] ** 2 / 20
            stages = [("At ground level", ("v",)), ("At highest point", ("h",))] if reverse else [("At release", ("h",)), ("At ground level", ("v",))]
        elif family == "spring_motion":
            k, x, v = values["k"], values["x"], values["v"]
            answer = {"k": lambda: m * v*v / (x*x), "x": lambda: math.sqrt(m*v*v/k), "v": lambda: x*math.sqrt(k/m), "m": lambda: k*x*x/(v*v)}[target]()
            stages = [("Start: spring compressed", ("k", "x")), ("End: spring relaxed", ("v",))] if reverse else [("Start: spring relaxed", ("v",)), ("End: object stopped", ("k", "x"))]
        else:
            k, x, h = values["k"], values["x"], values["h"]
            answer = {"k": lambda: 20*m*h/(x*x), "x": lambda: math.sqrt(20*m*h/k), "h": lambda: k*x*x/(20*m), "m": lambda: k*x*x/(20*h)}[target]()
            stages = [("Start: spring compressed", ("k", "x")), ("End: highest point", ("h",))] if reverse else [("Start: released from rest", ("h",)), ("End: spring compressed", ("k", "x"))]
        labels = {"m": "Mass (kg)", "v": "Speed (m/s)", "h": "Vertical change (m)", "k": "Spring constant (N/m)", "x": "Compression (m)"}
        groups = []
        for title, keys in [("Shared", ("m",)), *stages]:
            fields = [{"id": key, "label": labels[key], "value": values[key]} for key in keys if key != target]
            if fields:
                groups.append({"label": title, "fields": fields})
        steps = []
        # Offer an energy calculation only when all its inputs are supplied.
        if "k" in values and target not in ("k", "x"):
            steps = [{"id": "energy", "label": "Elastic potential energy (J)", "value": .5*values["k"]*values["x"]**2, "help": "EPE = ½ k (compression)². With no energy loss, this equals the energy transferred to the other form."}]
        elif "h" in values and target not in ("m", "h"):
            steps = [{"id": "energy", "label": "Gravitational energy change (J)", "value": m*10*values["h"], "help": "Energy change = mass × g × vertical change. Use g = 10 m/s²."}]
        elif "v" in values and target not in ("m", "v"):
            steps = [{"id": "energy", "label": "Kinetic energy (J)", "value": .5*m*values["v"]**2, "help": "KE = ½ mass × speed². With no energy loss, this equals the energy transferred to the other form."}]
        return {"question": question, "answers": [answer], "units": [unit],
                "extras": {"energy_plan": {"groups": groups, "steps": steps, "target": target,
                            "family": family, "reverse": reverse, "givens": {key: value for key, value in values.items() if key != target}}}}
    
    # # # E N E R G Y   C 0 N S E R V A T I 0 N   P R 0 B L E M S # # # 
    def kinetic_gravitational_problem(self,difficulty, *, variant=None):
        mass, velocity, _ = EBG.kinetic_energy(difficulty)
        height = velocity**2 / 20
        q_type = ri(0,3) if variant is None else variant
        noun = random_noun()
        if q_type == 0:
            question = f"""A {mass:.2f} kg {noun} is dropped from a height of {height:.2f} meters.
            \n How fast is it moving when it hits the ground?"""
            answer = velocity
            unit = "Velocity (m/s)"
        elif q_type == 1:
            question = f"""A {mass:.2f} kg {noun} is released from rest and hits the ground at {velocity:.2f} m/s.
            \n How high up was it dropped from?"""
            answer = height
            unit = "Height (meters)"
        elif q_type == 2:
            question = f"""A {mass:.2f} kg {noun} is thrown upwards with an initial velocity of {velocity:.2f} m/s.
           \nWhat is the highest point the {noun} reaches?"""
            answer = height
            unit = "Height (meters)"
        else:
            question = f"""A {mass:.2f} kg {noun} is thrown upwards, 
            reaching a maximum height of {height:.2f} meters.
            \n How fast was the {noun} originally thrown?"""
            answer = velocity
            unit = "Velocity (m/s)"

        question = question.replace("thrown upwards", "thrown upwards from ground level")
        return self._organized("gravity_motion", {"m": mass, "v": velocity, "h": height}, "v" if q_type in (0, 3) else "h", question, unit.replace("Velocity", "Speed"), q_type >= 2)
    
    def elastic_gravitational_problem(self, difficulty, *, variant=None):
        spring_constant, compression, elastic_e = EBG.elastic_potential_energy(difficulty)
        height = compression * ri(2, int(elastic_e//5  + 3))
        mass = max(0.01, round(elastic_e / (10*height), 2))

        q_type = ri(0,7) if variant is None else variant
        noun = random_noun()
        if q_type == 0:
            # find k
            question = f"""A {mass:.2f} kg {noun} is dropped from a height of {height:.2f} meters.
            \n A spring has to compress by {compression:.2f} meters to stop it. 
            \n How strong is the spring?"""
            answer = spring_constant
            unit = "Spring Strength (N/m)"
        elif q_type == 1:
            # find height
            question = f"""A {mass:.2f} kg {noun} is released from rest and dropped on a spring of strength {spring_constant:.2f} N/m.
            \n If the spring compresses {compression:.2f} meters before the {noun} comes to rest, how high up was it dropped from?"""
            answer = height
            unit = "Height (meters)"
        elif q_type == 2:
            # find compression
            question = f"""A {mass:.2f} kg {noun} is dropped from {height:.2f} meters onto a spring of strength {spring_constant:.2f} N/m.
            \n How much does the spring have to compress to bring the {noun} to rest?"""
            answer = compression
            unit = "Compression Distance (meters)"
        elif q_type == 3: 
            question = f"""A {noun} is dropped from {height:.2f} meters onto a spring of strength {spring_constant:.2f} N/m.
            \n If the spring compresses by {compression:.2f} meters to bring the {noun} to rest, how much mass does the {noun} have?"""
            answer = mass
            unit = "Mass (kilograms)"
        elif q_type == 4:# NEW STARTS HERE
            # find height
            question = f"""A {mass:.2f} kg {noun} is launched by
              a spring of strength {spring_constant:.2f} N/m.
              \n If the spring was compressed {compression:.2f} meters before launch, 
              how high up did the {noun} get?"""
            answer = height
            unit = "Height (meters)"
        elif q_type == 5:
            # find compression
            question = f"""A {mass:.2f} kg {noun} is 
            launched {height:.2f} meters into the air by 
            a spring of strength {spring_constant:.2f} N/m.
            \n How much did the spring have to compress to launch the {noun} that high?"""
            answer = compression
            unit = "Compression Distance (meters)"
        elif q_type == 6:
            # find k
            question = f"""A {mass:.2f} kg {noun} is launched to a height of {height:.2f} meters.
            \n A spring had to be compressed by {compression:.2f} meters to do this. 
            \n How strong is the spring?"""
            answer = spring_constant
            unit = "Spring Strength (N/m)"
        else:
            question = f"""A {noun} is launched to a height of {height:.2f} meters 
            by a spring of strength {spring_constant:.2f} N/m.
            \n If the spring was compressed {compression:.2f} meters to do this, 
            how much mass does the {noun} have?"""
            answer = mass
            unit = "Mass (kilograms)"

        # h is the complete vertical change between the two rest positions,
        # including compression/expansion, rather than height above the spring.
        question = question.replace("dropped from a height of", "released from rest and falls a total vertical distance of").replace("dropped from", "released from rest and falls a total vertical distance of")
        question = question.replace("how high up was it dropped from?", "what total vertical distance does it fall before stopping?")
        question = question.replace("onto a spring", "before stopping against a spring")
        question = question.replace("how high up did", "what total vertical distance did").replace("get?", "rise from its initial compressed position?")
        question = question.replace("launched to a height of", "launched through a total vertical rise of").replace("meters into the air", "meters above its initial compressed position")
        question = question.replace("How strong is the spring?", "What is the spring constant?")
        target = ("k", "h", "x", "m", "h", "x", "k", "m")[q_type]
        return self._organized("gravity_spring", {"m": mass, "k": spring_constant, "x": compression, "h": height}, target, question, unit.replace("Spring Strength", "Spring constant"), q_type >= 4)

    def elastic_kinetic_problem(self, difficulty, *, variant=None):
            spring_constant, compression, _ = EBG.elastic_potential_energy(difficulty)
            upper = self.get_difficulty_range(difficulty)
            mass = ri(1,upper)
            velocity = compression  * (spring_constant / mass )**(1/2)
            
            q_type = ri(0,7) if variant is None else variant
            noun = random_noun()
            if q_type == 0:
                # find k
                question = f"""A {mass:.2f} kg {noun} strikes a spring while moving as {velocity:.2f} m/s. 
                 \n The spring has to compress by {compression:.2f} meters to stop it. 
                 \n How strong is the spring?"""
                answer = spring_constant
                unit = "Spring Strength (N/m)"
            elif q_type == 1:
                # find velocity
                question = f"""A {mass:.2f} kg {noun} hits a spring of strength {spring_constant:.2f} N/m.
                \n If the spring compresses {compression:.2f} meters before the {noun} comes to rest,
                  how fast was the {noun} initially moving?"""
                answer = velocity
                unit = "Velocity (m/s)"

            elif q_type == 2:
                # find compression
                question = f"""A {mass:.2f} kg {noun} moving at {velocity:.2f} m/s 
                hits a spring of strength {spring_constant:.2f} N/m.
                \n How much does the spring have to compress to bring the {noun} to rest?"""
                answer = compression
                unit = "Compression Distance (meters)"
            elif q_type == 3:
                question = f"""A {noun} moving as {velocity:.2f} m/s hits 
                a spring of strength {spring_constant:.2f} N/m.
                \n If the spring compresses by {compression:.2f} meters to bring the {noun} to rest, 
                how much mass does the {noun} have?"""
                answer = mass
                unit =  "Mass (kilograms)"
            elif q_type == 4: # REVERSE STARTS HERE
                # find k
                question = f"""A {mass:.2f} kg {noun} is accelerated from rest by 
                a spring that was compressed by {compression:.2f} meters.
                \n If the {noun} is now moving at {velocity:.2f} m/s, how strong is the spring?"""
                answer = spring_constant
                unit = "Spring Strength (N/m)"
            elif q_type == 5:
                # find velocity
                question = f"""A {mass:.2f} kg {noun} is accelerated from rest by 
                a spring of strength {spring_constant:.2f} N/m.
                \n If the spring was compressed by {compression:.2f} meters, 
                how fast is the {noun} now moving?"""
                answer = velocity
                unit = "Velocity (m/s)"

            elif q_type == 6:
                # find compression
                question = f"""A {mass:.2f} kg {noun} is moving at {velocity:.2f} m/s 
                after being accelerated from rest by a spring of strength {spring_constant:.2f} N/m.
                \n How much did the spring have to compress to achieve this?"""
                answer = compression
                unit = "Compression Distance (meters)"
            else:
                question = f"""A {noun} is moving at {velocity:.2f} m/s 
                after being accelerated from rest by a spring of strength {spring_constant:.2f} N/m.
                \n If the spring was compressed by {compression:.2f} meters,  
                how much mass does the {noun} have?"""
                answer = mass
                unit =  "Mass (kilograms)"

            question = question.replace("moving as", "moving at").replace("How strong is the spring?", "What is the spring constant?").replace("how strong is the spring?", "what is the spring constant?")
            question += " The motion is horizontal and frictionless."
            return self._organized("spring_motion", {"m": mass, "k": spring_constant, "x": compression, "v": velocity}, ("k", "v", "x", "m")[q_type % 4], question, unit.replace("Velocity", "Speed").replace("Spring Strength", "Spring constant"), q_type >= 4)
   # # # I N T E R F A C E  W I T H   R E N D E R E R # # # 
    def choose_problem_dict(self,problem_type, difficulty):
        if problem_type == "Mixed":
            method = (self.elastic_kinetic_problem, self.kinetic_gravitational_problem,
                      self.elastic_gravitational_problem)[ri(0, 2)]
            return method(difficulty)
        if problem_type == "Elastic <--> Kinetic":
            return self.elastic_kinetic_problem(difficulty)
        elif problem_type == "Gravitational <--> Kinetic":
            return self.kinetic_gravitational_problem(difficulty)
        elif problem_type == "Gravitational <--> Elastic":
              return self.elastic_gravitational_problem(difficulty)
        else:
            pass

    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "Mixed": {
                "id": "energy-conservation.mixed",
                "aliases": ["Mixed"],
                "honors": r"KE_i + GPE_i + EPE_i = KE_f + GPE_f + EPE_f",
                "conceptual": r"KE = \frac{1}{2}mv^2 \quad,\quad GPE = mgh \quad,\quad EPE = \frac{1}{2}k(\Delta x)^2",
            },
            "Elastic <--> Kinetic": {
                "id": "energy-conservation.elastic-kinetic",
                "aliases": ["Elastic <--> Kinetic"],
                "honors": r"\frac{1}{2} m v^2 = \frac{1}{2} k \Delta x^2",
                "conceptual": r""" m = k \cdot \left( \frac{ \Delta x}{v} \right)^2 \;\; ,
                \;\; v = \Delta x \cdot \sqrt{\frac{k}{m}} \;\; ,
                \;\; k = m \cdot \left( \frac{v}{ \Delta x} \right)^2 \;\; ,
                \;\; \Delta x = v \cdot \sqrt{\frac{m}{k}}"""
                },
            "Gravitational <--> Kinetic": {
                "id": "energy-conservation.gravitational-kinetic",
                "aliases": ["Gravitational <--> Kinetic"],
                "honors": r"mgh = \frac{1}{2} m v^2",
                "conceptual": r"""h = \frac{v^2}{2g} \;\;,
                 \;\; v = \sqrt{2gh}"""
                },
            "Gravitational <--> Elastic" : {
                "id": "energy-conservation.gravitational-elastic",
                "aliases": ["Gravitational <--> Elastic"],
                "honors": r"mgh = \frac{1}{2} k \Delta x^2",
                "conceptual": r"""m = \frac{k \Delta x^2}{2gh}\;\;,
                \;\; h = \frac{k \Delta x^2}{2mg} \;\;,
                \;\; k = \frac{2mgh}{\Delta x^2}\;\;,
                \;\; \Delta x = \sqrt{\frac{2mgh}{k}}"""
                }
            }


from random import randint as ri
from utils.generators.base_generator import BaseGenerator
from utils.word_lists import random_noun
from utils.generators.energy.energy_basics import EnergyBasicsGenerator
EBG = EnergyBasicsGenerator()

class EnergyConservationGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="energy_conserv_")
    
    # # # E N E R G Y   C 0 N S E R V A T I 0 N   P R 0 B L E M S # # # 
    def kinetic_gravitational_problem(self,difficulty):
        mass, velocity, _ = EBG.kinetic_energy(difficulty)
        height = velocity**2 / 20
        q_type = ri(0,3)
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

        return {"question": question, "answers": [answer], "units": [unit]}
    
    def elastic_gravitational_problem(self, difficulty):
        spring_constant, compression, elastic_e = EBG.elastic_potential_energy(difficulty)
        height = compression * ri(2, int(elastic_e//5  + 3))
        mass = elastic_e / (10*height)

        q_type = ri(0,7)
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

        return {"question": question, "answers": [answer], "units": [unit]}

    def elastic_kinetic_problem(self, difficulty):
            spring_constant, compression, _ = EBG.elastic_potential_energy(difficulty)
            upper = self.get_difficulty_range(difficulty)
            mass = ri(1,upper)
            velocity = compression  * (spring_constant / mass )**(1/2)
            
            q_type = ri(0,7)
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

            return {"question": question, "answers": [answer], "units": [unit]}
   # # # I N T E R F A C E  W I T H   R E N D E R E R # # # 
    def choose_problem_dict(self,problem_type, difficulty):

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
            "Elastic <--> Kinetic": {
                "honors": r"\frac{1}{2} m v^2 = \frac{1}{2} k \Delta x^2",
                "conceptual": r""" m = k \cdot \left( \frac{ \Delta x}{v} \right)^2 \;\; ,
                \;\; v = \Delta x \cdot \sqrt{\frac{k}{m}} \;\; ,
                \;\; k = m \cdot \left( \frac{v}{ \Delta x} \right)^2 \;\; ,
                \;\; \Delta x = v \cdot \sqrt{\frac{m}{k}}"""
                },
            "Gravitational <--> Kinetic": {
                "honors": r"mgh = \frac{1}{2} m v^2",
                "conceptual": r"""h = \frac{v^2}{2g} \;\;,
                 \;\; v = \sqrt{2gh}"""
                },
            "Gravitational <--> Elastic" : {
                "honors": r"mgh = \frac{1}{2} k \Delta x^2",
                "conceptual": r"""m = \frac{k \Delta x^2}{2gh}\;\;,
                \;\; h = \frac{k \Delta x^2}{2mg} \;\;,
                \;\; k = \frac{2mgh}{\Delta x^2}\;\;,
                \;\; \Delta x = \sqrt{\frac{2mgh}{k}}"""
                }
            }


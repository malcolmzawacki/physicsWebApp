from random import randint as ri
from utils.generators.base_generator import BaseGenerator
from utils.word_lists import random_noun
from utils.generators.energy.energy_basics import EnergyBasicsGenerator
EBG = EnergyBasicsGenerator()

class ThermalLossGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="thermal_loss_")
    
# # # T H E R M A L    E N E R G Y   L 0 S S   N U M B E R S # # # 
    def grav_to_kin_thermal_nums(self):
        #grav -> Kin
        mass, height, grav = EBG.gravitational_potential_energy("Hard")
        thermal = ri(1,int(grav//2 + 2))
        kinetic = grav - thermal
        velocity = (2*kinetic/mass)**(1/2)
        return mass, height, velocity, thermal

    def kin_to_grav_thermal_nums(self):
        mass, velocity, kinetic_e = EBG.kinetic_energy("Hard")
        thermal = ri(1,int(kinetic_e//2 + 2))
        grav = kinetic_e - thermal
        height = grav / (10*mass)
        return mass, height, velocity, thermal

    def grav_to_elastic_thermal_nums(self):
        
        mass, height, grav = EBG.gravitational_potential_energy("Hard")
        thermal = ri(1,int(grav//2 + 2))
        elastic = grav - thermal
        compression = height / ri(2,10)
        spring_constant = (2*elastic/(compression**2))
        return mass, height, spring_constant, compression, thermal

    def elastic_to_grav_thermal_nums(self):
        spring_constant, compression, elastic_e = EBG.elastic_potential_energy("Hard")
        thermal = ri(1,int(elastic_e//2 +2))
        grav = elastic_e - thermal
        height = compression * ri(2,10)
        mass = grav / (10*height)
        return mass, height, spring_constant, compression, thermal

    def kinetic_to_elastic_thermal_nums(self):

        mass, velocity, kinetic = EBG.kinetic_energy("Hard")
        thermal = ri(1,int(kinetic//2 + 2))
        elastic = kinetic - thermal
        spring_constant = ri(2,int(elastic//2 + 3))
        compression = (2*elastic/spring_constant)**(1/2)

        return mass, velocity, spring_constant, compression, thermal
    
    def elastic_to_kinetic_thermal_nums(self):

        spring_constant, compression, elastic_e = EBG.elastic_potential_energy("Hard")
        thermal = ri(1,int(elastic_e//2 + 2))
        kinetic = elastic_e - thermal
        mass = ri(2,int(kinetic//2 + 3))
        velocity = (2*kinetic/mass)**(1/2)

        return mass, velocity, spring_constant, compression, thermal


    # # # T H E R M A L    E N E R G Y   L 0 S S   P R 0 B L E M S # # # 


    def grav_to_kin_thermal_q(self,difficulty):
        mass, height, velocity, thermal = self.grav_to_kin_thermal_nums()
        flip = ri(0,2)
        noun = random_noun()
        if flip == 0 or difficulty == "Easy":
            # just find the difference
            question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a {height:.2f} meter tall ramp.
            \n If the {noun}'s velocity at the bottom is {velocity:.2f} m/s, how much energy was lost as heat?"""
            answer = thermal
            unit = "Work done by Friction (Joules)"
        elif flip == 1:
            # give the initial and the loss, find final info
            question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a {height:.2f} meter tall ramp.
            \n If the {noun} loses {thermal} Joules due to friction / heat along the way, 
            what will its velocity be when it reaches the bottom?"""
            answer = velocity
            unit = "Velocity (m/s)"
        elif flip == 2:
            # give the final and the loss, find initial info
            question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a ramp,
            losing {thermal} Joules due to friction / heat along the way. 
            \n If the {noun} reaches the bottom moving at 
            {velocity:.2f} m/s, what was the original height of the ramp?"""
            answer = height
            unit = "Height (meters)"
        return {"question": question, "answers": [answer], "units": [unit]}
    
    def kin_to_grav_thermal_q(self,difficulty):
        flip = ri(0,2)
        noun = random_noun()
        mass, height, velocity, thermal = self.kin_to_grav_thermal_nums()
        if flip == 0 or difficulty == "Easy":
            # just find the difference
            question = f"""A {mass:.2f} kg {noun} is initially moving with a velocity of {velocity:.2f} m/s.
            \n The {noun} slides up a ramp, reaching a height of {height:.2f} meters.
            \n How much energy was lost as heat?"""
            answer = thermal
            unit = "Work done by Friction (Joules)"
        elif flip == 1:
            # give the initial and the loss, find final info
            question = f"""A {mass:.2f} kg {noun} slides {height:.2f} meters up a ramp.
            \n If the {noun} lost {thermal} Joules due to friction / heat along the way, 
            what was its velocity at the bottom of the ramp?"""
            answer = velocity
            unit = "Velocity (m/s)"
        elif flip == 2:
            # give the final and the loss, find initial info
            question = f"""A {mass:.2f} kg {noun} slides up a ramp,
            losing {thermal} Joules due to friction / heat along the way. 
            \n If the {noun} was moving at 
            {velocity:.2f} m/s at the bottom of the ramp,
                how high up the ramp does it reach?"""
            answer = height
            unit = "Height (meters)"
        return {"question": question, "answers": [answer], "units": [unit]}
   
    
    def grav_kin_thermal(self, difficulty):
        dirn = ri(0,1)
        if dirn == 0:
           return self.grav_to_kin_thermal_q(difficulty)
        else:
            return self.kin_to_grav_thermal_q(difficulty)



    def grav_to_elastic_thermal_q(self,difficulty):
        noun = random_noun()
        flip = ri(0,4)
        mass, height, spring_constant, compression, thermal = self.grav_to_elastic_thermal_nums()        
        if flip == 0 or difficulty == "Easy":
            # just find the difference
            question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a {height:.2f} meter tall ramp.
            \n It collides with a spring of strength {spring_constant:.2f} N/m, which compresses {compression:.2f} meters before coming to rest.
            \n How much energy was lost as heat?"""
            answer = thermal
            unit = "Work done by Friction (Joules)"
        elif flip == 1:
            # give the initial and the loss, find final info
            question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a {height:.2f} meter tall ramp.
            \n The {noun} loses {thermal} Joules due to friction / heat along the way, and ends up compressing the spring at the bottom by
            {compression:.2f} meters. 
            \n How strong is the spring?"""
            answer = spring_constant
            unit = "Spring Strength (N/m)"
        elif flip == 2:
            # give the initial and the loss, find final info
            question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a {height:.2f} meter tall ramp.
            \n The {noun} loses {thermal} Joules due to friction / heat along the way, and ends up compressing a
            spring that has a strength of {spring_constant:.2f} N/m. 
            \n How much does the spring compress?"""
            answer = compression
            unit = "Compression Distance (meters)"
        elif flip == 3:
            # give final and loss, find initial
            question = f"""A {noun} is released from rest and slides down a {height:.2f} meter tall ramp.
        \n The {noun} loses {thermal} Joules due to friction / heat along the way, and ends up compressing a
            spring that has a strength of {spring_constant:.2f} N/m by {compression:.2f} meters. 
            \n How much mass does the {noun} have?"""
            answer = mass
            unit = "Mass (kilograms)"
        elif flip == 4:
            question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a ramp.
            \n The {noun} loses {thermal} Joules due to friction / heat along the way, and ends up compressing a
            spring that has a strength of {spring_constant:.2f} N/m by {compression:.2f} meters. 
            \n How tall is the ramp?"""
            answer = height
            unit = "Ramp Height (meters)"
        return {"question": question, "answers": [answer], "units": [unit]}


    def elastic_to_grav_thermal_q(self,difficulty):
        noun = random_noun()
        flip = ri(0,4)
        mass, height, spring_constant, compression, thermal = self.elastic_to_grav_thermal_nums()        
        if flip == 0 or difficulty == "Easy":
            # just find the difference
            question = f"""A {mass:.2f} kg {noun} compresses a spring of strength 
            {spring_constant:.2f} N/m by {compression:.2f} meters.
            \n It slides up a ramp to a height of {height:.2f} meters.
            \n How much energy was lost as heat?"""
            answer = thermal
            unit = "Work done by Friction (Joules)"
        elif flip == 1:
            # give the initial and the loss, find final info
            question = f"""A {mass:.2f} kg {noun} slides up to the top of a {height:.2f} meter tall ramp.
            \n The {noun} loses {thermal} Joules due to friction / heat along the way. 
            \n If the {noun} was launched up the ramp by a spring that was compressed by
            {compression:.2f} meters, how strong is the spring?"""
            answer = spring_constant
            unit = "Spring Strength (N/m)"
        elif flip == 2:
            # give the initial and the loss, find final info
            question = f"""A {mass:.2f} kg {noun} is launched up a ramp by a spring
            with a strength of {spring_constant:.2f} N/m.
            \n The {noun} loses {thermal} Joules due to friction / heat along the way, 
            and reaches a height of {height:.2f} meters.
            \n How much was the spring compressed?"""
            answer = compression
            unit = "Compression Distance (meters)"
        elif flip == 3:
            # give final and loss, find initial
            question = f"""A {noun} is launched up a ramp to a height of {height:.2f} meters.
        \n The {noun} loses {thermal} Joules due to friction / heat along the way.
            \n It was launched by a spring that has a strength of {spring_constant:.2f} N/m, 
            and was compressed by {compression:.2f} meters. 
            \n How much mass does the {noun} have?"""
            answer = mass
            unit = "Mass (kilograms)"
        elif flip == 4:
            question = f"""A {mass:.2f} kg {noun} sits at rest, compressing a
            spring that has a strength of {spring_constant:.2f} N/m by {compression:.2f} meters.
            \n The {noun} is released and launched up a ramp, but loses {thermal} Joules 
            due to friction / heat along the way.  
            \n What height up the ramp does the {noun} reach?"""
            answer = height
            unit = "Ramp Height (meters)"
        return {"question": question, "answers": [answer], "units": [unit]}


    def grav_elastic_thermal(self, difficulty):
        dirn = ri(0,1)
        if dirn == 0:
           return self.grav_to_elastic_thermal_q(difficulty)
        else: 
            return self.elastic_to_grav_thermal_q(difficulty)


    def kinetic_to_elastic_thermal_q(self,difficulty):
        noun = random_noun()
        flip = ri(0,4)
        mass, velocity, spring_constant, compression, thermal = self.kinetic_to_elastic_thermal_nums()
        if flip == 0 or difficulty == "Easy":
            # just find the difference
            question = f"""A {mass:.2f} kg {noun} is moving at {velocity:.2f} m/s when it collides with a spring of strength {spring_constant:.2f} N/m.
            \n If the spring compresses {compression:.2f} meters before coming to rest, how much energy was lost as heat?"""
            answer = thermal
            unit = "Work done by Friction (Joules)"
        elif flip == 1:
            # give the initial and the loss, find final info
            question = f"""A {mass:.2f} kg {noun} is moving at {velocity:.2f} m/s when it collides with a spring, and ends up 
            compressing the spring at the bottom by {compression:.2f} meters.
            \n The {noun} lost {thermal} Joules due to friction / heat along the way. 
            \n How strong is the spring?"""
            answer = spring_constant
            unit = "Spring Strength (N/m)"
        elif flip == 2:
            # give the initial and the loss, find final info
            question = f"""A {mass:.2f} kg {noun} is moving at {velocity:.2f} m/s when it collides with a spring 
            that has a strength of {spring_constant:.2f} N/m.
            \n The {noun} lost {thermal} Joules due to friction / heat along the way. 
            \n How much does the spring compress?"""
            answer = compression
            unit = "Compression Distance (meters)"
        elif flip == 3:
            # give final and loss, find initial
            question = f"""A {noun} is moving at {velocity:.2f} m/s, and ends up compressing a
            spring that has a strength of {spring_constant:.2f} N/m by {compression:.2f} meters.
            \n The {noun} loses {thermal} Joules due to friction / heat along the way. 
            \n How much mass does the {noun} have?"""
            answer = mass
            unit = "Mass (kilograms)"
        elif flip == 4:
            question = f"""A {mass:.2f} kg {noun} collides with a spring that has a strength of {spring_constant:.2f} N/m,
            compressing it by {compression:.2f} meters.
            \n The {noun} loses {thermal} Joules due to friction / heat along the way. 
            \n How fast was it moving?"""
            answer = velocity
            unit = "Velocity (m/s)"
        return  {"question": question, "answers": [answer], "units": [unit]}
    
    def elastic_to_kinetic_thermal_q(self,difficulty):
        noun = random_noun()
        flip = ri(0,4)
        mass, velocity, spring_constant, compression, thermal = self.elastic_to_kinetic_thermal_nums()
        if flip == 0 or difficulty == "Easy":
            # just find the difference
            question = f"""A {mass:.2f} kg {noun} is moving at {velocity:.2f} m/s 
            after being pushed by a spring of strength {spring_constant:.2f} N/m.
            \n If the spring was originally compressed by {compression:.2f} meters, 
            how much energy has been lost as heat?"""
            answer = thermal
            unit = "Work done by Friction (Joules)"
        elif flip == 1:
            # give the initial and the loss, find final info
            question = f"""A {mass:.2f} kg {noun} is moving at {velocity:.2f} m/s 
            after being pushed by a spring originally compressed by {compression:.2f} meters.
            \n If the {noun} lost {thermal} Joules due to friction / heat along the way, 
            how strong is the spring?"""
            answer = spring_constant
            unit = "Spring Strength (N/m)"
        elif flip == 2:
            # give the initial and the loss, find final info
            question = f"""A {mass:.2f} kg {noun} is moving at {velocity:.2f} m/s 
            after being pushed by a spring that has a strength of {spring_constant:.2f} N/m.
            \n The {noun} was lost {thermal} Joules due to friction / heat. 
            \n How much was the spring compressed?"""
            answer = compression
            unit = "Compression Distance (meters)"
        elif flip == 3:
            # give final and loss, find initial
            question = f"""A {noun} is moving at {velocity:.2f} m/s 
            after being pushed by a spring that has a strength of {spring_constant:.2f} N/m.
            \n If the spring was compressed by {compression:.2f} meters, and 
            the {noun} has lost {thermal} Joules due to friction / heat,  
            how much mass does the {noun} have?"""
            answer = mass
            unit = "Mass (kilograms)"
        elif flip == 4:
            question = f"""A {mass:.2f} kg {noun} was accelerated by a spring that has 
            a strength of {spring_constant:.2f} N/m,
            and was compressed by {compression:.2f} meters.
            \n If the {noun} has lost {thermal} Joules due to friction / heat, 
            how fast is it currently moving?"""
            answer = velocity
            unit = "Velocity (m/s)"
        return {"question": question, "answers": [answer], "units": [unit]}

    def kinetic_elastic_thermal(self,difficulty):
        dirn = ri(0,1)
        if dirn == 0:
            return self.kinetic_to_elastic_thermal_q(difficulty)
        else:
           return self.elastic_to_kinetic_thermal_q(difficulty) 



   


  # # # I N T E R F A C E  W I T H   R E N D E R E R # # # 
    def choose_problem_dict(self,problem_type, difficulty):

        if problem_type == "Elastic <--> Kinetic":
            return self.kinetic_elastic_thermal(difficulty)
        elif problem_type == "Gravitational <--> Kinetic":
            return self.grav_kin_thermal(difficulty)
        elif problem_type == "Gravitational <--> Elastic":
              return self.grav_elastic_thermal(difficulty)
        else:
            pass
    

    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "Elastic <--> Kinetic": {
                "honors": r"""\Delta E = W_f
                \newline ~ \newline ~ \newline
                EPE = \frac{1}{2} k \Delta x^2 \quad ,
                \quad KE = \frac{1}{2} m v^2
                """,

                "conceptual": r"""W_f = E_f - E_i
                \newline ~ \newline ~ \newline
                EPE = \frac{1}{2} k \Delta x^2 \;\; , 
                \;\; k = \frac{2 \cdot EPE}{\Delta x^2} \;\; , 
                \;\; \Delta x = \sqrt{\frac{2 \cdot EPE}{k}}
                \newline ~ \newline ~ \newline
                KE = \frac{1}{2} m v^2\;\; ,
                \;\; m = \frac{2KE}{v^2} \;\; ,
                \;\; v = \sqrt{\frac{2KE}{m}}
                """
                },
            "Gravitational <--> Kinetic": {
                "honors": r"""\Delta E = W_f
                \newline ~ \newline ~ \newline
                GPE = mgh \quad ,
                \quad KE = \frac{1}{2} m v^2
                """,

                "conceptual": r"""W_f = E_f - E_i
                \newline ~ \newline ~ \newline
                GPE = mgh\;\; ,
                \;\; m = \frac{GPE}{gh} \;\; ,
                \;\; h = \frac{GPE}{mg}
                \newline ~ \newline ~ \newline
                KE = \frac{1}{2} m v^2\;\; ,
                \;\; m = \frac{2KE}{v^2} \;\; ,
                \;\; v = \sqrt{\frac{2KE}{m}}
                """
                },
            "Gravitational <--> Elastic" : {
                "honors": r"""\Delta E = W_f
                \newline ~ \newline ~ \newline
                GPE = mgh \quad , \quad
                EPE = \frac{1}{2} k \Delta x^2
                """,
                "conceptual": r"""W_f = E_f - E_i
                \newline ~ \newline ~ \newline
                GPE = mgh\;\; ,
                \;\; m = \frac{GPE}{gh} \;\; ,
                \;\; h = \frac{GPE}{mg}
                \newline ~ \newline ~ \newline
                EPE = \frac{1}{2} k \Delta x^2 \;\; , 
                \;\; k = \frac{2 \cdot EPE}{\Delta x^2} \;\; , 
                \;\; \Delta x = \sqrt{\frac{2 \cdot EPE}{k}}
                """
                }
        }


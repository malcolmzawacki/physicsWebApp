from random import randint as ri
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

class EnergyGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="energy_")

    def get_difficulty_range(self, difficulty):
        if difficulty == "Easy":
            return 5
        elif difficulty == "Hard":
            return 20
        return 10
    
    # # # B A S I C    E N E R G Y    N U M B E R S # # # 
    def kinetic_energy(self,difficulty):
        upper = self.get_difficulty_range(difficulty)
        mass = ri(1,upper)
        velocity = ri(1,upper)
        flip = ri(0,1)
        if flip == 0:
            mass*=2
        else:
            velocity*=2
        return mass, velocity, 0.5*mass*velocity**2

    def gravitational_potential_energy(self,difficulty):
        upper = self.get_difficulty_range(difficulty)
        mass = ri(1,upper)
        height = ri(1,upper)
        return mass, height, mass*10*height

    def elastic_potential_energy(self,difficulty):
        upper = self.get_difficulty_range(difficulty)
        spring_constant = ri(2,upper)
        compression = ri(1,upper)
        flip = ri(0,1)
        if flip == 0:
            spring_constant*=2
        else:
            compression*=2
        return spring_constant, compression, 0.5*spring_constant*compression**2

    def work(self,difficulty):
        upper = self.get_difficulty_range(difficulty)
        force = ri(1,upper)
        distance = ri(1,upper)
        return force, distance, force*distance


    # # # B A S I C    E N E R G Y    P R 0 B L E M S # # # 
    def elastic_problem(self,difficulty):
        spring_constant, compression, elastic_e = self.elastic_potential_energy(difficulty)
        q_type = ri(0,2)
        dirn = ri(0,1)
        dirn_string = "compressed" if dirn == 0 else "stretched"
        if q_type == 0 or difficulty == "Easy":
            question = f"""A spring with strength {spring_constant:.2f} N/m is {dirn_string} by {compression:.2f} meters.
            \n What is the amount of elastic potential energy held in the spring?"""
            answer = elastic_e
            unit = "Elastic Potential Energy (Joules)"
        elif q_type == 1:
            question = f"""A spring with strength {spring_constant:.2f} N/m contains {elastic_e} Joules of elastic potential energy.
            \n How much was this spring {dirn_string}?"""
            answer = compression
            unit = "Compression Distance (meters)"
        else:
            question = f"""A spring is {dirn_string} by {compression:.2f} meters, and contains {elastic_e} Joules of elastic potential energy.
            \n What is the strength of the spring constant?"""
            answer = spring_constant
            unit = "Spring Strength (N/m)"

        return question, [answer], [unit], None
    
    def kinetic_problem(self,difficulty):
        mass, velocity, kinetic_e = self.kinetic_energy(difficulty)
        q_type = ri(0,2)
        noun = random_noun()
        if q_type == 0 or difficulty == "Easy":
            question = f"""How much kinetic energy does a {mass:.2f} kg {noun} moving at {velocity:.2f} m/s have?"""
            answer = kinetic_e
            unit = "Kinetic Energy (Joules)"
        elif q_type == 1:
            question = f"""How fast would a {mass:.2f} kg {noun} have to move to have {kinetic_e} Joules of kinetic energy?"""
            answer = velocity
            unit = "Velocity (m/s)"
        else:
            question = f"""How much mass would a {noun} moving at {velocity:.2f} m/s need to have to contain {kinetic_e} Joules of kinetic energy?"""
            answer = mass
            unit = "Mass (kilograms)"

        return question, [answer], [unit], None
    
    def gravitational_problem(self,difficulty):
        mass, height, gravit_e = self.gravitational_potential_energy(difficulty)
        q_type = ri(0,2)
        noun = random_noun()
        if q_type == 0 or difficulty == "Easy":
            question = f"""How much gravitational potential energy does a {mass:.2f} kg {noun} 
            held {height:.2f} meters above the ground have?"""
            answer = gravit_e
            unit = "Gravitational Potential Energy (Joules)"
        elif q_type == 1:
            question = f"""How high up would a {mass:.2f} kg {noun} have to be to have 
            {gravit_e} Joules of gravitational potential energy?"""
            answer = height
            unit = "Height (meters)"
        else:
            question = f"""How much mass would a {noun} at a height of {height:.2f} meters need to have 
            to contain {gravit_e} Joules of gravitational potential energy?"""
            answer = mass
            unit = "Mass (kilograms)"

        return question, [answer], [unit], None
    
    def work_problem(self,difficulty):
        force, distance, work = self.work(difficulty)
        q_type = ri(0,2)
        noun = random_noun()
        if q_type == 0 or difficulty == "Easy":
            question = f"""A {noun} is moved {distance:.2f} meters by a {force} Newton force. 
            \n How much work was done?"""
            answer = work
            unit = "Work (Joules)"
        elif q_type == 1:
            question = f"""Over how much distance would a {force} Newton force 
            have to push a {noun} before it did {work} Joules of work?"""
            answer = distance
            unit = "Distance (meters)"
        else:
            question = f"""{work} Joules of work are done on a {noun} over a distance of {distance:.2f} meters.
            \n How much force was applied?"""
            answer = force
            unit = "Force (Newtons)"

        return question, [answer], [unit], None

    
    # # # E N E R G Y   C 0 N S E R V A T I 0 N   P R 0 B L E M S # # # 
    def kinetic_gravitational_problem(self,difficulty):
        mass, velocity, _ = self.kinetic_energy(difficulty)
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

        return question, [answer], [unit], None
    
    def elastic_gravitational_problem(self, difficulty):
        spring_constant, compression, elastic_e = self.elastic_potential_energy(difficulty)
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

        return question, [answer], [unit], None

    def elastic_kinetic_problem(self, difficulty):
            spring_constant, compression, _ = self.elastic_potential_energy(difficulty)
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

            return question, [answer], [unit], None


    # # # T H E R M A L    E N E R G Y   L 0 S S   N U M B E R S # # # 
    def grav_to_kin_thermal_nums(self):
        #grav -> Kin
        mass, height, grav = self.gravitational_potential_energy("Hard")
        thermal = ri(1,int(grav//2 + 2))
        kinetic = grav - thermal
        velocity = (2*kinetic/mass)**(1/2)
        return mass, height, velocity, thermal

    def kin_to_grav_thermal_nums(self):
        mass, velocity, kinetic_e = self.kinetic_energy("Hard")
        thermal = ri(1,int(kinetic_e//2 + 2))
        grav = kinetic_e - thermal
        height = grav / (10*mass)
        return mass, height, velocity, thermal

    def grav_to_elastic_thermal_nums(self):
        
        mass, height, grav = self.gravitational_potential_energy("Hard")
        thermal = ri(1,int(grav//2 + 2))
        elastic = grav - thermal
        compression = height / ri(2,10)
        spring_constant = (2*elastic/(compression**2))
        return mass, height, spring_constant, compression, thermal

    def elastic_to_grav_thermal_nums(self):
        spring_constant, compression, elastic_e = self.elastic_potential_energy("Hard")
        thermal = ri(1,int(elastic_e//2 +2))
        grav = elastic_e - thermal
        height = compression * ri(2,10)
        mass = grav / (10*height)
        return mass, height, spring_constant, compression, thermal

    def kinetic_to_elastic_thermal_nums(self):

        mass, velocity, kinetic = self.kinetic_energy("Hard")
        thermal = ri(1,int(kinetic//2 + 2))
        elastic = kinetic - thermal
        spring_constant = ri(2,int(elastic//2 + 3))
        compression = (2*elastic/spring_constant)**(1/2)

        return mass, velocity, spring_constant, compression, thermal
    
    def elastic_to_kinetic_thermal_nums(self):

        spring_constant, compression, elastic_e = self.elastic_potential_energy("Hard")
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
        return question, [answer], [unit], None
    
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
        return question, [answer], [unit], None
   
    
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
        return question, [answer], [unit], None


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
        return question, [answer], [unit], None


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
        return  question, [answer], [unit], None
    
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
        return question, [answer], [unit], None

    def kinetic_elastic_thermal(self,difficulty):
        dirn = ri(0,1)
        if dirn == 0:
            return self.kinetic_to_elastic_thermal_q(difficulty)
        else:
           return self.elastic_to_kinetic_thermal_q(difficulty) 



    # chooser for thermal energy problems
    def thermal_quant_problems(self, difficulty):
        flip = ri(0,2)
        if flip == 0:
            #grav -> Kin
            return self.grav_kin_thermal(difficulty)
        elif flip == 1:
            #grav -> elastic
            return self.grav_elastic_thermal(difficulty)
        elif flip == 2:
            #kinetic -> elastic
            return self.kinetic_elastic_thermal(difficulty)




    # # # F R I C T I 0 N   A N D   D I S T A N C E   P R 0 B L E M S # # # 
    def grav_to_kinetic_friction_distance_q(self, difficulty):
        
        mass, height, velocity, thermal = self.grav_to_kin_thermal_nums()
        distance = height + ri(int(height//2 + 1),int(2*height + 1))
        friction = thermal / distance

        noun = random_noun()
        if difficulty == "Easy":
            flip = ri(0,2)
            if flip == 0: 
                question = f"""A {mass:.2f} kg {noun} is released from rest and 
                slides down a {height:.2f} meter tall ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how fast is it moving at the bottom?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = velocity
                unit2 = "Final Velocity (m/s)"
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how tall is the ramp?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = height
                unit2 = "Ramp Height (meters)"
            else:
                question = f"""A {noun} is released from rest and slides down a {height:.2f} meter tall ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much mass does the {noun} have?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = mass
                unit2 = "Mass (kilograms)"
            return question, [answer1, answer2], [unit1, unit2], None
        else:
            flip = ri(0,4)
            if flip == 0: 
                question = f"""A {mass:.2f} kg {noun} is released from rest and 
                slides down a {height:.2f} meter tall ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How fast is it moving at the bottom?"""
                answer = velocity
                unit = "Final Velocity (m/s)"
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How tall is the ramp?"""
                answer = height
                unit = "Ramp Height (meters)"
            elif flip == 2:
                question = f"""A {noun} is released from rest and slides down a {height:.2f} meter tall ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much mass does the {noun} have?"""
                answer = mass
                unit = "Mass (kilograms)"
            elif flip == 3:
                question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a {height:.2f} meter tall ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force. 
                \n What is the length of the ramp?"""
                answer = distance
                unit = "Ramp Length (meters)"
            else:
                question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a {height:.2f} meter tall ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n If the ramp is {distance:.2f} meters long, how strong was the force of friction?"""
                answer = friction
                unit = "Force of Friction (Newtons)"
            return question, [answer], [unit], None
        
    def kinetic_to_grav_friction_distance_q(self, difficulty):
        
        mass, height, velocity, thermal = self.kin_to_grav_thermal_nums()
        distance = height + ri(int(height//2 + 1),int(2*height + 1))
        friction = thermal / distance

        noun = random_noun()
        if difficulty == "Easy":
            flip = ri(0,2)
            if flip == 0: 
                question = f"""A {mass:.2f} kg {noun} height increases by {height:.2f} meters 
                as it slides up a ramp before it comes to rest.
                \n It experienced {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how fast was it moving initially?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = velocity
                unit2 = "Final Velocity (m/s)"
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} initially moving at {velocity:.2f} m/s slides up a ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much does the height of the {noun} increase?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = height
                unit2 = "Ramp Height (meters)"
            else:
                question = f"""A {noun} is initially moving at {velocity:.2f} m/s 
                increases its height by {height:.2f} meters by sliding up a ramp before coming to rest.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much mass does the {noun} have?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = mass
                unit2 = "Mass (kilograms)"
            return question, [answer1, answer2], [unit1, unit2], None
        else:
            flip = ri(0,4)
            if flip == 0: 
                question = f"""A {mass:.2f} kg {noun} increases its height by {height:.2f} meters
                 by sliding up a ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How fast was it moving initially?"""
                answer = velocity
                unit = "Final Velocity (m/s)"
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} initially moving at {velocity:.2f} m/s slides up a ramp. 
                \n It reaches rest after it experiences {friction:.2f} N of frictional force 
                over the {distance:.2f} m ramp length. 
                \n How high up on the ramp did the {noun} get?"""
                answer = height
                unit = "Ramp Height (meters)"
            elif flip == 2:
                question = f"""A {mass:.2f} kg {noun} initially moving at {velocity:.2f} m/s 
                slides up a ramp, increasing its height by {height:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length.
                \n How much mass does the {noun} have?"""
                answer = mass
                unit = "Mass (kilograms)"
            elif flip == 3:
                question = f"""A {mass:.2f} kg {noun} initially moving at {velocity:.2f} m/s
                slides {height:.2f} meters tall ramp, 
                reaching a velocity of  at the bottom.
                \n It experiences {friction:.2f} N of frictional force. 
                \n What is the length of the ramp?"""
                answer = distance
                unit = "Ramp Length (meters)"
            else:
                question = f"""A {mass:.2f} kg {noun} initially moving at {velocity:.2f} m/s 
                slides up a ramp, increasing its height by {height:.2f} meters.
                \n If the ramp is {distance:.2f} meters long, how strong was the force of friction?"""
                answer = friction
                unit = "Force of Friction (Newtons)"
            return question, [answer], [unit], None

    def grav_to_elastic_friction_distance_q(self, difficulty):
        mass, height, spring_constant, compression, thermal = self.grav_to_elastic_thermal_nums()        
        distance = height + ri(int(height//2 + 1), int(2*height + 1))
        friction = thermal / distance
        
        noun = random_noun()
        if difficulty == "Easy":
            flip = ri(0,3)
            if flip == 0: 
                question = f"""A {mass:.2f} kg {noun} is released from rest and 
                slides down a {height:.2f} meter tall ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length,
                and compresses a spring of strength {spring_constant:.2f} N/m at the bottom. 
                \n How much energy was lost as heat, and how much does the spring compress?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = compression
                unit2 = "Spring Compression (meters)"
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} is released from rest and 
                slides down a {height:.2f} meter tall ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length, 
                and compresses a spring by {compression:.2f} meters at the bottom.
                \n How much energy was lost as heat, and how strong is the spring?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = spring_constant
                unit2 = "Spring Constant (N/m)"
            elif flip == 2:
                question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length, 
                and compresses a spring with strength {spring_constant:.2f} by 
                {compression:.2f} meters at the bottom.
                \n How much energy was lost as heat, and how high up was the {noun} initially?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = height
                unit2 = "Ramp Height (meters)"
            else:
                question = f"""A {noun} is released from rest and slides down a {height:.2f} meter tall ramp, 
                and compresses a spring of strength {spring_constant:.2f} N/m by {compression:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much mass does the {noun} have?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = mass
                unit2 = "Mass (kilograms)"
            return question, [answer1, answer2], [unit1, unit2], None
        else:
            flip = ri(0,5)
            if flip == 0: 
                question = f"""A {mass:.2f} kg {noun} is released from rest and 
                slides down a {height:.2f} meter tall ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length, 
                and compresses a spring of strength {spring_constant:.2f} N/m at the bottom.
                \n How much does the spring compress?"""
                answer = compression
                unit = "Spring Compression (meters)"
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} is released from rest and 
                slides down a {height:.2f} meter tall ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length, 
                and compresses a spring by {compression:.2f} meters at the bottom.
                \n How strong is the spring?"""
                answer = spring_constant
                unit = "Spring Constant (N/m)"
            elif flip == 2:
                question = f"""A {noun} is released from rest and slides down a {height:.2f} meter tall ramp, 
                and compresses a spring of strength {spring_constant:.2f} N/m by {compression:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much mass does the {noun} have?"""
                answer = mass
                unit = "Mass (kilograms)"
            elif flip == 3:
                question = f"""A {mass:.2f} kg {noun} is released from rest 
                and slides down a {height:.2f} meter tall ramp, 
                and compresses a spring of strength {spring_constant:.2f} N/m by {compression:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force.
                \n What is the length of the ramp?"""
                answer = distance
                unit = "Ramp Length (meters)"
            elif flip == 4:
                question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length, 
                and compresses a spring with strength {spring_constant:.2f} by 
                {compression:.2f} meters at the bottom.
                \n How high up was the {noun} initially?"""
                answer = height
                unit = "Ramp Height (meters)"
            else:
                question = f"""A {mass:.2f} kg {noun} is released from rest 
                and slides down a {height:.2f} meter tall ramp, 
                and compresses a spring of strength {spring_constant:.2f} N/m by {compression:.2f} meters.
                \n If the ramp is {distance:.2f} meters long, how strong was the force of friction?"""
                answer = friction
                unit = "Force of Friction (Newtons)"
            return question, [answer], [unit], None

    def elastic_to_grav_friction_distance_q(self, difficulty):
        mass, height, spring_constant, compression, thermal = self.elastic_to_grav_thermal_nums()        
        distance = height + ri(int(height//2 + 1), int(2*height + 1))
        friction = thermal / distance
        
        noun = random_noun()
        if difficulty == "Easy":
            flip = ri(0,3)
            if flip == 0: 
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by 
                {compression:.2f} meters and launches a {mass:.2f} kg {noun} up a ramp.
                \n The {noun} experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how high does the {noun} reach?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = height
                unit2 = "Height (meters)"
            elif flip == 1:
                question = f"""A spring of strength {spring_constant:.2f} N/m 
                launches a {mass:.2f} kg {noun} up a ramp to a height of {height:.2f} meters.
                \n The {noun} experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much was the spring compressed?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = compression
                unit2 = "Spring Compression (meters)"
            elif flip == 2:
                question = f"""A {mass:.2f} kg {noun} is launched to a height of {height:.2f} meters up a ramp 
                by a spring compressed by {compression:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length.
                \n How much energy was lost as heat, and how strong is the spring?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = spring_constant
                unit2 = "Spring Constant (N/m)"
            else:
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by {compression:.2f} meters 
                and launches a {noun} up a ramp to a height of {height:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much mass does the {noun} have?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = mass
                unit2 = "Mass (kilograms)"
            return question, [answer1, answer2], [unit1, unit2], None
        else:
            flip = ri(0,5)
            if flip == 0: 
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by {compression:.2f} meters 
                and launches a {mass:.2f} kg {noun} up a ramp.
                \n The {noun} experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How high does the {noun} reach?"""
                answer = height
                unit = "Height (meters)"
            elif flip == 1:
                question = f"""A spring of strength {spring_constant:.2f} N/m launches a {mass:.2f} kg {noun} 
                up a ramp to a height of {height:.2f} meters.
                \n The {noun} experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length.
                \n By how much was the spring compressed?"""
                answer = compression
                unit = "Spring Compression (meters)"
            elif flip == 2:
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by {compression:.2f} meters 
                and launches a {noun} up a ramp to a height of {height:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much mass does the {noun} have?"""
                answer = mass
                unit = "Mass (kilograms)"
            elif flip == 3:
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by {compression:.2f} meters 
                and launches a {mass:.2f} kg {noun} up a ramp to a height of {height:.2f} meters.
                \n The {noun} experiences {friction:.2f} N of frictional force.
                \n What is the length of the ramp?"""
                answer = distance
                unit = "Ramp Length (meters)"
            elif flip == 4:
                question = f"""A {mass:.2f} kg {noun} is launched to a height of {height:.2f} meters up a ramp 
                by a spring compressed by {compression:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length.
                \n How strong is the spring?"""
                answer = spring_constant
                unit = "Spring Constant (N/m)"
            else:
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by {compression:.2f} meters 
                and launches a {mass:.2f} kg {noun} up a ramp to a height of {height:.2f} meters.
                \n If the ramp is {distance:.2f} meters long, how strong was the force of friction?"""
                answer = friction
                unit = "Force of Friction (Newtons)"
            return question, [answer], [unit], None

    def kinetic_to_elastic_friction_distance_q(self, difficulty):
        mass, velocity, spring_constant, compression, thermal = self.kinetic_to_elastic_thermal_nums()
        distance = ri(int(velocity*2), int(velocity*4))  # Reasonable distance range
        friction = thermal / distance
        
        noun = random_noun()
        if difficulty == "Easy":
            flip = ri(0,3)
            if flip == 0: 
                question = f"""A {mass:.2f} kg {noun} moving at {velocity:.2f} m/s slides along a surface
                with {friction:.2f} N of friction over {distance:.2f} m before compressing a spring.
                \n The spring has a strength of {spring_constant:.2f} N/m.
                \n How much energy was lost to heat, and how much does the spring compress?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = compression
                unit2 = "Spring Compression (meters)"
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} moving at {velocity:.2f} m/s slides along a surface
                with {friction:.2f} N of friction over {distance:.2f} m 
                before compressing a spring by {compression:.2f} m.
                \n How much energy was lost to heat, and what is the spring constant?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = spring_constant
                unit2 = "Spring Constant (N/m)"
            elif flip == 2:
                question = f"""A {mass:.2f} kg {noun} enters a section of rough surface
                with {friction:.2f} N of friction over {distance:.2f} m. 
                It then compresses a spring of strength {spring_constant:.2f} by {compression:.2f} m.
                \n How much energy was lost to heat, and how fast was the {noun} initially moving?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = velocity
                unit2 = "Initial Velocity (m/s)"
            else:
                question = f"""A {noun} moving at {velocity:.2f} m/s 
                slides along a surface with {friction:.2f} N of friction
                over {distance:.2f} m before compressing a spring 
                with spring constant {spring_constant:.2f} N/m by {compression:.2f} m.
                \n How much energy was lost to heat, and what is the mass of the {noun}?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = mass
                unit2 = "Mass (kilograms)"
            return question, [answer1, answer2], [unit1, unit2], None
        else:
            flip = ri(0,5)
            if flip == 0: 
                question = f"""A {mass:.2f} kg {noun} moving at 
                {velocity:.2f} m/s slides along a surface
                with {friction:.2f} N of friction over {distance:.2f} m before hitting a spring 
                with spring constant {spring_constant:.2f} N/m.
                \n How much does the spring compress?"""
                answer = compression
                unit = "Spring Compression (meters)"
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} moving at {velocity:.2f} m/s slides along a surface
                with {friction:.2f} N of friction over {distance:.2f} m before 
                compressing a spring by {compression:.2f} m.
                \n What is the spring constant?"""
                answer = spring_constant
                unit = "Spring Constant (N/m)"
            elif flip == 2:
                question = f"""A {noun} moving at {velocity:.2f} m/s slides along a surface 
                with {friction:.2f} N of friction
                over {distance:.2f} m before hitting a spring 
                with spring constant {spring_constant:.2f} N/m, 
                compressing it by {compression:.2f} m.
                \n What is the mass of the {noun}?"""
                answer = mass
                unit = "Mass (kilograms)"
            elif flip == 3:
                question = f"""A {mass:.2f} kg {noun} moving at {velocity:.2f} m/s slides along a surface 
                with {friction:.2f} N of friction
                before hitting a spring with spring constant {spring_constant:.2f} N/m, 
                compressing it by {compression:.2f} m.
                \n How far did the {noun} slide before hitting the spring?"""
                answer = distance
                unit = "Distance (meters)"
            elif flip == 4:
                question = f"""A {mass:.2f} kg {noun} enters a section of rough surface
                with {friction:.2f} N of friction over {distance:.2f} m. 
                It then compresses a spring of strength {spring_constant:.2f} by {compression:.2f} m.
                \n How fast was the {noun} initially moving?"""
                answer = velocity
                unit = "Initial Velocity (m/s)"
            else:
                question = f"""A {mass:.2f} kg {noun} moving at {velocity:.2f} m/s slides along a surface 
                for {distance:.2f} m
                before hitting a spring with spring constant {spring_constant:.2f} N/m, 
                compressing it by {compression:.2f} m.
                \n What was the force of friction?"""
                answer = friction
                unit = "Force of Friction (Newtons)"
            return question, [answer], [unit], None

    def elastic_to_kinetic_friction_distance_q(self, difficulty):
        mass, velocity, spring_constant, compression, thermal = self.elastic_to_kinetic_thermal_nums()
        distance = ri(int(velocity*2), int(velocity*4))  # Reasonable distance range
        friction = thermal / distance
        
        noun = random_noun()
        if difficulty == "Easy":
            flip = ri(0,3)
            if flip == 0: 
                question = f"""A spring of strength {spring_constant:.2f} N/m is 
                compressed by {compression:.2f} m
                and launches a {mass:.2f} kg {noun} along a 
                surface with {friction:.2f} N of friction over {distance:.2f} m.
                \n How much energy was lost to heat, and what is the final velocity of the {noun}?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = velocity
                unit2 = "Velocity (m/s)"
            elif flip == 1:
                question = f"""A spring with strength {spring_constant:.2f} N/m 
                launches a {mass:.2f} kg {noun}.
                \n After the {noun} slides along a surface with {friction:.2f} N of friction over {distance:.2f} m,
                the {noun} is moving at a velocity of {velocity:.2f} m/s.
                \n How much energy was lost to heat, and by how much was the spring compressed?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = compression
                unit2 = "Spring Compression (meters)"
            elif flip == 2:
                question = f"""A spring is compressed by {compression:.2f} m and launches a {mass:.2f} kg {noun}.
                \n After the {noun} slides along a surface with {friction:.2f} N of friction over {distance:.2f} m,
                the {noun} is moving at a velocity of {velocity:.2f} m/s
                \n How much energy was lost to heat, and what is the strength of the spring?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = spring_constant
                unit2 = "Spring Constant (N/m)"
            else:
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by {compression:.2f} m
                and launches a {noun} along a surface with {friction:.2f} N of friction over {distance:.2f} m.
                \n The {noun} reaches a velocity of {velocity:.2f} m/s.
                \n How much energy was lost to heat, and what is the mass of the {noun}?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = mass
                unit2 = "Mass (kilograms)"
            return question, [answer1, answer2], [unit1, unit2], None
        else:
            flip = ri(0,5)
            if flip == 0: 
                question = f"""A spring of strength {spring_constant:.2f} N/m 
                is compressed by {compression:.2f} m
                and launches a {mass:.2f} kg {noun} along a surface with 
                {friction:.2f} N of friction over {distance:.2f} m.
                \n What is the final velocity of the {noun}?"""
                answer = velocity
                unit = "Velocity (m/s)"
            elif flip == 1:
                question = f"""A spring with strength {spring_constant:.2f} N/m 
                launches a {mass:.2f} kg {noun}.
                \n After the {noun} slides along a surface with {friction:.2f} N of friction over {distance:.2f} m,
                the {noun} is moving at a velocity of {velocity:.2f} m/s.
                \n By how much was the spring compressed?"""
                answer = compression
                unit = "Spring Compression (meters)"
            elif flip == 2:
                question = f"""A spring of strength {spring_constant:.2f} N/m 
                is compressed by {compression:.2f} m
                and launches a {noun} along a surface with {friction:.2f} N of friction over {distance:.2f} m.
                \n The {noun} reaches a velocity of {velocity:.2f} m/s.
                \n What is the mass of the {noun}?"""
                answer = mass
                unit = "Mass (kilograms)"
            elif flip == 3:
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed 
                by {compression:.2f} m
                and launches a {mass:.2f} kg {noun} along a surface with {friction:.2f} N of friction.
                \n The {noun} reaches a velocity of {velocity:.2f} m/s.
                \n How far was the rough section that the {noun} travelled through?"""
                answer = distance
                unit = "Distance (meters)"
            elif flip == 4:
                question = f"""A spring is compressed by {compression:.2f} m and launches a {mass:.2f} kg {noun}.
                \n After the {noun} slides along a surface with 
                {friction:.2f} N of friction over {distance:.2f} m,
                the {noun} is moving at a velocity of {velocity:.2f} m/s
                \n What is the strength of the spring?"""
                answer = spring_constant
                unit = "Spring Constant (N/m)"
            else:
                question = f"""A spring of strength {spring_constant:.2f} N/m 
                is compressed by {compression:.2f} m
                and launches a {mass:.2f} kg {noun} along a surface for {distance:.2f} m.
                \n The {noun} reaches a velocity of {velocity:.2f} m/s.
                \n What was the force of friction experienced by the {noun}?"""
                answer = friction
                unit = "Force of Friction (Newtons)"
            return question, [answer], [unit], None

    # chooser for friction and distance problems
    def friction_and_distance_problems(self,difficulty):
        flip = ri(0,5)
        if flip == 0:
            return self.grav_to_kinetic_friction_distance_q(difficulty)
        elif flip == 1:
            return self.kinetic_to_grav_friction_distance_q(difficulty)
        elif flip == 2:
            return self.elastic_to_kinetic_friction_distance_q(difficulty)
        elif flip == 3:
            return self.kinetic_to_elastic_friction_distance_q(difficulty)
        elif flip == 4:
            return self.grav_to_elastic_friction_distance_q(difficulty)
        else:
            return self.elastic_to_grav_friction_distance_q(difficulty)



    # # # I N T E R F A C E  W I T H   R E N D E R E R # # # 
    def choose_problem(self,problem_type, difficulty):
        if problem_type == "Elastic Potential Energy":
            return self.elastic_problem(difficulty)
        elif problem_type == "Kinetic Energy":
            return self.kinetic_problem(difficulty)
        elif problem_type == "Gravitational Potential Energy":
            return self.gravitational_problem(difficulty)
        elif problem_type == "Work":
            return self.work_problem(difficulty)

        elif problem_type == "Elastic <--> Kinetic":
            return self.elastic_kinetic_problem(difficulty)
        elif problem_type == "Gravitational <--> Kinetic":
            return self.kinetic_gravitational_problem(difficulty)
        elif problem_type == "Gravitational <--> Elastic":
              return self.elastic_gravitational_problem(difficulty)

        elif problem_type == "Quantifying Thermal Energy":
            return self.thermal_quant_problems(difficulty)
        elif problem_type == "Friction and Distance":
            return self.friction_and_distance_problems(difficulty)
        else:
            pass

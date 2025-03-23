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

    def elastic_problem(self,difficulty):
        spring_constant, compression, elastic_e = self.elastic_potential_energy(difficulty)
        q_type = ri(0,2)
        dirn = ri(0,1)
        dirn_string = "compressed" if dirn == 0 else "stretched"
        if q_type == 0 or difficulty == "Easy":
            question = f"""A spring with strength {spring_constant} N/m is {dirn_string} by {compression} meters.
            \n What is the amount of elastic potential energy held in the spring?"""
            answer = elastic_e
            unit = "Elastic Potential Energy (Joules)"
        elif q_type == 1:
            question = f"""A spring with strength {spring_constant} N/m contains {elastic_e} Joules of elastic potential energy.
            \n How much was this spring {dirn_string}?"""
            answer = compression
            unit = "Compression Distance (meters)"
        else:
            question = f"""A spring is {dirn_string} by {compression} meters, and contains {elastic_e} Joules of elastic potential energy.
            \n What is the strength of the spring constant?"""
            answer = spring_constant
            unit = "Spring Strength (N/m)"

        return question, [answer], [unit]
    
    def kinetic_problem(self,difficulty):
        mass, velocity, kinetic_e = self.kinetic_energy(difficulty)
        q_type = ri(0,2)
        noun = random_noun()
        if q_type == 0 or difficulty == "Easy":
            question = f"""How much kinetic energy does a {mass} kg {noun} moving at {velocity} m/s have?"""
            answer = kinetic_e
            unit = "Kinetic Energy (Joules)"
        elif q_type == 1:
            question = f"""How fast would a {mass} kg {noun} have to move to have {kinetic_e} Joules of kinetic energy?"""
            answer = velocity
            unit = "Velocity (m/s)"
        else:
            question = f"""How much mass would a {noun} moving at {velocity} m/s need to have to contain {kinetic_e} Joules of kinetic energy?"""
            answer = mass
            unit = "Mass (kilograms)"

        return question, [answer], [unit]
    
    def gravitational_problem(self,difficulty):
        mass, height, gravit_e = self.gravitational_potential_energy(difficulty)
        q_type = ri(0,2)
        noun = random_noun()
        if q_type == 0 or difficulty == "Easy":
            question = f"""How much gravitational potential energy does a {mass} kg {noun} 
            held {height} meters above the ground have?"""
            answer = gravit_e
            unit = "Gravitational Potential Energy (Joules)"
        elif q_type == 1:
            question = f"""How high up would a {mass} kg {noun} have to be to have 
            {gravit_e} Joules of gravitational potential energy?"""
            answer = height
            unit = "Height (meters)"
        else:
            question = f"""How much mass would a {noun} at a height of {height} meters need to have 
            to contain {gravit_e} Joules of gravitational potential energy?"""
            answer = mass
            unit = "Mass (kilograms)"

        return question, [answer], [unit]
    
    def work_problem(self,difficulty):
        force, distance, work = self.work(difficulty)
        q_type = ri(0,2)
        noun = random_noun()
        if q_type == 0 or difficulty == "Easy":
            question = f"""A {noun} is moved {distance} meters by a {force} Newton force. 
            \n How much work was done?"""
            answer = work
            unit = "Work (Joules)"
        elif q_type == 1:
            question = f"""Over how much distance would a {force} Newton force 
            have to push a {noun} before it did {work} Joules of work?"""
            answer = distance
            unit = "Distance (meters)"
        else:
            question = f"""{work} Joules of work are done on a {noun} over a distance of {distance} meters.
            \n How much force was applied?"""
            answer = force
            unit = "Force (Newtons)"

        return question, [answer], [unit]

    
    def kinetic_gravitational_problem(self,difficulty):
        mass, velocity, _ = self.kinetic_energy(difficulty)
        height = velocity**2 / 20
        q_type = ri(0,3)
        noun = random_noun()
        if q_type == 0:
            question = f"""A {mass} kg {noun} is dropped from a height of {height:.2f} meters.
            \n How fast is it moving when it hits the ground?"""
            answer = velocity
            unit = "Velocity (m/s)"
        elif q_type == 1:
            question = f"""A {mass} kg {noun} is released from rest and hits the ground at {velocity} m/s.
            \n How high up was it dropped from?"""
            answer = height
            unit = "Height (meters)"
        elif q_type == 2:
            question = f"""A {mass} kg {noun} is thrown upwards with an initial velocity of {velocity} m/s.
           \nWhat is the highest point the {noun} reaches?"""
            answer = height
            unit = "Height (meters)"
        else:
            question = f"""A {mass} kg {noun} is thrown upwards, 
            reaching a maximum height of {height:.2f} meters.
            \n How fast was the {noun} originally thrown?"""
            answer = velocity
            unit = "Velocity (m/s)"

        return question, [answer], [unit]
    
    def elastic_gravitational_problem(self, difficulty):
        spring_constant, compression, elastic_e = self.elastic_potential_energy(difficulty)
        height = compression * ri(2, int(elastic_e//5  + 3))
        mass = elastic_e / (10*height)

        q_type = ri(0,7)
        noun = random_noun()
        if q_type == 0:
            # find k
            question = f"""A {mass:.2f} kg {noun} is dropped from a height of {height:.2f} meters.
            \n A spring has to compress by {compression} meters to stop it. 
            \n How strong is the spring?"""
            answer = spring_constant
            unit = "Spring Strength (N/m)"
        elif q_type == 1:
            # find height
            question = f"""A {mass:.2f} kg {noun} is released from rest and dropped on a spring of strength {spring_constant} N/m.
            \n If the spring compresses {compression} meters before the {noun} comes to rest, how high up was it dropped from?"""
            answer = height
            unit = "Height (meters)"
        elif q_type == 2:
            # find compression
            question = f"""A {mass:.2f} kg {noun} is dropped from {height:.2f} meters onto a spring of strength {spring_constant} N/m.
            \n How much does the spring have to compress to bring the {noun} to rest?"""
            answer = compression
            unit = "Compression Distance (meters)"
        elif q_type == 3: 
            question = f"""A {noun} is dropped from {height:.2f} meters onto a spring of strength {spring_constant} N/m.
            \n If the spring compresses by {compression} meters to bring the {noun} to rest, how much mass does the {noun} have?"""
            answer = mass
            unit = "Mass (kilograms)"
        elif q_type == 4:# NEW STARTS HERE
            # find height
            question = f"""A {mass:.2f} kg {noun} is launched by
              a spring of strength {spring_constant} N/m.
              \n If the spring was compressed {compression} meters before launch, 
              how high up did the {noun} get?"""
            answer = height
            unit = "Height (meters)"
        elif q_type == 5:
            # find compression
            question = f"""A {mass:.2f} kg {noun} is 
            launched {height:.2f} meters into the air by 
            a spring of strength {spring_constant} N/m.
            \n How much did the spring have to compress to launch the {noun} that high?"""
            answer = compression
            unit = "Compression Distance (meters)"
        elif q_type == 6:
            # find k
            question = f"""A {mass:.2f} kg {noun} is launched to a height of {height:.2f} meters.
            \n A spring had to be compressed by {compression} meters to do this. 
            \n How strong is the spring?"""
            answer = spring_constant
            unit = "Spring Strength (N/m)"
        else:
            question = f"""A {noun} is launched to a height of {height:.2f} meters 
            by a spring of strength {spring_constant} N/m.
            \n If the spring was compressed {compression} meters to do this, 
            how much mass does the {noun} have?"""
            answer = mass
            unit = "Mass (kilograms)"

        return question, [answer], [unit]


    def elastic_kinetic_problem(self, difficulty):
            spring_constant, compression, _ = self.elastic_potential_energy(difficulty)
            upper = self.get_difficulty_range(difficulty)
            mass = ri(1,upper)
            velocity = compression  * (spring_constant / mass )**(1/2)
            
            q_type = ri(0,7)
            noun = random_noun()
            if q_type == 0:
                # find k
                question = f"""A {mass} kg {noun} strikes a spring while moving as {velocity:.2f} m/s. 
                 \n The spring has to compress by {compression} meters to stop it. 
                 \n How strong is the spring?"""
                answer = spring_constant
                unit = "Spring Strength (N/m)"
            elif q_type == 1:
                # find velocity
                question = f"""A {mass} kg {noun} hits a spring of strength {spring_constant} N/m.
                \n If the spring compresses {compression} meters before the {noun} comes to rest,
                  how fast was the {noun} initially moving?"""
                answer = velocity
                unit = "Velocity (m/s)"

            elif q_type == 2:
                # find compression
                question = f"""A {mass} kg {noun} moving at {velocity:.2f} m/s 
                hits a spring of strength {spring_constant} N/m.
                \n How much does the spring have to compress to bring the {noun} to rest?"""
                answer = compression
                unit = "Compression Distance (meters)"
            elif q_type == 3:
                question = f"""A {noun} moving as {velocity:.2f} m/s hits 
                a spring of strength {spring_constant} N/m.
                \n If the spring compresses by {compression} meters to bring the {noun} to rest, 
                how much mass does the {noun} have?"""
                answer = mass
                unit =  "Mass (kilograms)"
            elif q_type == 4: # REVERSE STARTS HERE
                # find k
                question = f"""A {mass} kg {noun} is accelerated from rest by 
                a spring that was compressed by {compression} meters.
                \n If the {noun} is now moving at {velocity:.2f} m/s, how strong is the spring?"""
                answer = spring_constant
                unit = "Spring Strength (N/m)"
            elif q_type == 5:
                # find velocity
                question = f"""A {mass} kg {noun} is accelerated from rest by 
                a spring of strength {spring_constant} N/m.
                \n If the spring was compressed by {compression} meters, 
                how fast is the {noun} now moving?"""
                answer = velocity
                unit = "Velocity (m/s)"

            elif q_type == 6:
                # find compression
                question = f"""A {mass} kg {noun} is moving at {velocity:.2f} m/s 
                after being accelerated from rest by a spring of strength {spring_constant} N/m.
                \n How much did the spring have to compress to achieve this?"""
                answer = compression
                unit = "Compression Distance (meters)"
            else:
                question = f"""A {noun} is moving at {velocity:.2f} m/s 
                after being accelerated from rest by a spring of strength {spring_constant} N/m.
                \n If the spring was compressed by {compression} meters,  
                how much mass does the {noun} have?"""
                answer = mass
                unit =  "Mass (kilograms)"

            return question, [answer], [unit]

    
    def grav_kin_thermal_nums(self):
        #grav -> Kin
        mass, height, grav = self.gravitational_potential_energy("Hard")
        thermal = ri(1,int(grav//2 + 2))
        kinetic = grav - thermal
        velocity = (2*kinetic/mass)**(1/2)
        return mass, height, velocity, thermal


    def grav_kin_thermal(self, difficulty):
        #grav -> Kin
        flip = ri(0,2)
        noun = random_noun()
        mass, height, velocity, thermal = self.grav_kin_thermal_nums()
        if flip == 0 or difficulty == "Easy":
            # just find the difference
            question = f"""A {mass} kg {noun} is released from rest and slides down a {height} meter tall ramp.
            \n If the {noun}'s velocity at the bottom is {velocity:.2f} m/s, how much energy was lost as heat?"""
            answer = thermal
            unit = "Work done by Friction (Joules)"
        elif flip == 1:
            # give the initial and the loss, find final info
            question = f"""A {mass} kg {noun} is released from rest and slides down a {height} meter tall ramp.
            \n If the {noun} loses {thermal} Joules due to friction / heat along the way, 
            what will it's velocity be when it reaches the bottom?"""
            answer = velocity
            unit = "Velocity (m/s)"
        elif flip == 2:
            # give the final and the loss, find initial info
            question = f"""A {mass} kg {noun} is released from rest and slides down a ramp,
            losing {thermal} Joules due to friction / heat along the way. 
            \n If the {noun} reaches the bottom moving at 
            {velocity:.2f} m/s, what was the original height of the ramp?"""
            answer = height
            unit = "Height (meters)"
        return question, [answer], [unit]

    def grav_elastic_thermal_nums(self):
        
        mass, height, grav = self.gravitational_potential_energy("Hard")
        thermal = ri(1,grav//2 + 2)
        elastic = grav - thermal
        spring_constant = ri(2,int(elastic//2 + 3))
        compression = (2*elastic/spring_constant)**(1/2)
        return mass, height, spring_constant, compression, thermal


    def grav_elastic_thermal(self, difficulty):
        
        mass, height, spring_constant, compression, thermal = self.grav_elastic_thermal_nums()

        noun = random_noun()
        flip = ri(0,4)
        if flip == 0 or difficulty == "Easy":
            # just find the difference
            question = f"""A {mass} kg {noun} is released from rest and slides down a {height} meter tall ramp.
            \n It collides with a spring of strength {spring_constant} N/m, which compresses {compression:.2f} meters before coming to rest.
            \n How much energy was lost as heat?"""
            answer = thermal
            unit = "Work done by Friction (Joules)"
        elif flip == 1:
            # give the initial and the loss, find final info
            question = f"""A {mass} kg {noun} is released from rest and slides down a {height} meter tall ramp.
            \n The {noun} loses {thermal} Joules due to friction / heat along the way, and ends up compressing the spring at the bottom by
            {compression:.2f} meters. 
            \n How strong is the spring?"""
            answer = spring_constant
            unit = "Spring Strength (N/m)"
        elif flip == 2:
            # give the initial and the loss, find final info
            question = f"""A {mass} kg {noun} is released from rest and slides down a {height} meter tall ramp.
            \n The {noun} loses {thermal} Joules due to friction / heat along the way, and ends up compressing a
            spring that has a strength of {spring_constant} N/m. 
            \n How much does the spring compress?"""
            answer = compression
            unit = "Compression Distance (meters)"
        elif flip == 3:
            # give final and loss, find initial
            question = f"""A {noun} is released from rest and slides down a {height} meter tall ramp.
           \n The {noun} loses {thermal} Joules due to friction / heat along the way, and ends up compressing a
            spring that has a strength of {spring_constant} N/m by {compression:.2f} meters. 
            \n How much mass does the {noun} have?"""
            answer = mass
            unit = "Mass (kilograms)"
        elif flip == 4:
            question = f"""A {mass} kg {noun} is released from rest and slides down a ramp.
            \n The {noun} loses {thermal} Joules due to friction / heat along the way, and ends up compressing a
            spring that has a strength of {spring_constant} N/m by {compression:.2f} meters. 
            \n How tall is the ramp?"""
            answer = height
            unit = "Ramp Height (meters)"
        return question, [answer], [unit]

    def kinetic_elastic_thermal_nums(self):

        mass, velocity, kinetic = self.kinetic_energy("Hard")
        thermal = ri(1,int(kinetic//2 + 2))
        elastic = kinetic - thermal
        spring_constant = ri(2,int(elastic//2 + 3))
        compression = (2*elastic/spring_constant)**(1/2)

        return mass, velocity, spring_constant, compression, thermal


    def kinetic_elastic_thermal(self,difficulty):

        mass, velocity, spring_constant, compression, thermal = self.kinetic_elastic_thermal_nums()
        
        noun = random_noun()
        flip = ri(0,4)
        if flip == 0 or difficulty == "Easy":
            # just find the difference
            question = f"""A {mass} kg {noun} is moving at {velocity} m/s when it collides with a spring of strength {spring_constant} N/m.
            \n If the spring compresses {compression:.2f} meters before coming to rest, how much energy was lost as heat?"""
            answer = thermal
            unit = "Work done by Friction (Joules)"
        elif flip == 1:
            # give the initial and the loss, find final info
            question = f"""A {mass} kg {noun} is moving at {velocity} m/s when it collides with a spring, and ends up 
            compressing the spring at the bottom by {compression:.2f} meters.
            \n The {noun} lost {thermal} Joules due to friction / heat along the way. 
            \n How strong is the spring?"""
            answer = spring_constant
            unit = "Spring Strength (N/m)"
        elif flip == 2:
            # give the initial and the loss, find final info
            question = f"""A {mass} kg {noun} is moving at {velocity} m/s when it collides with a spring 
            that has a strength of {spring_constant} N/m.
            \n The {noun} lost {thermal} Joules due to friction / heat along the way. 
            \n How much does the spring compress?"""
            answer = compression
            unit = "Compression Distance (meters)"
        elif flip == 3:
            # give final and loss, find initial
            question = f"""A {noun} is moving at {velocity} m/s, and ends up compressing a
            spring that has a strength of {spring_constant} N/m by {compression:.2f} meters.
            \n The {noun} loses {thermal} Joules due to friction / heat along the way. 
            \n How much mass does the {noun} have?"""
            answer = mass
            unit = "Mass (kilograms)"
        elif flip == 4:
            question = f"""A {mass} kg {noun} collides with a spring that has a strength of {spring_constant} N/m,
            compressing it by {compression:.2f} meters.
            \n The {noun} loses {thermal} Joules due to friction / heat along the way. 
            \n How fast was it moving?"""
            answer = velocity
            unit = "Velocity (m/s)"
        return question, [answer], [unit]

    def thermal_quant_problems(self, difficulty):
        noun = random_noun()
        flip = ri(0,2)
        if flip == 0:
            #grav -> Kin
            question, answer, unit = self.grav_kin_thermal(difficulty)
        elif flip == 1:
            #grav -> elastic
            question, answer, unit = self.grav_elastic_thermal(difficulty)
        elif flip == 2:
            #kinetic -> elastic
            question, answer, unit = self.kinetic_elastic_thermal(difficulty)

        return question, answer, unit




    def grav_kinetic_friction_distance_q(self, difficulty):
        
        mass, height, velocity, thermal = self.grav_kin_thermal_nums()
        distance = height + ri(int(height//2 + 1),int(2*height + 1))
        friction = thermal / distance

        noun = random_noun()
        if difficulty == "Easy":
            flip = ri(0,2)
            if flip == 0: 
                question = f"""A {mass} kg {noun} is released from rest and slides down a {height} meter tall ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how fast is it moving at the bottom?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = velocity
                unit2 = "Final Velocity (m/s)"
            elif flip == 1:
                question = f"""A {mass} kg {noun} is released from rest and slides down a ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how tall is the ramp?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = height
                unit2 = "Ramp Height (meters)"
            else:
                question = f"""A {noun} is released from rest and slides down a {height} meter tall ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much mass does the {noun} have?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = mass
                unit2 = "Mass (kilograms)"
            return question, answer1, answer2, unit1, unit2
        else:
            flip = ri(0,4)
            if flip == 0: 
                question = f"""A {mass} kg {noun} is released from rest and slides down a {height} meter tall ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How fast is it moving at the bottom?"""
                answer = velocity
                unit = "Final Velocity (m/s)"
            elif flip == 1:
                question = f"""A {mass} kg {noun} is released from rest and slides down a ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How tall is the ramp?"""
                answer = height
                unit = "Ramp Height (meters)"
            elif flip == 2:
                question = f"""A {noun} is released from rest and slides down a {height} meter tall ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much mass does the {noun} have?"""
                answer = mass
                unit = "Mass (kilograms)"
            elif flip == 3:
                question = f"""A {mass} kg {noun} is released from rest and slides down a {height} meter tall ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force. 
                \n What is the length of the ramp?"""
                answer = distance
                unit = "Ramp Length (meters)"
            else:
                question = f"""A {mass} kg {noun} is released from rest and slides down a {height} meter tall ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n If the ramp is {distance} meters long, how strong was the force of friction?"""
                answer = friction
                unit = "Force of Friction (Newtons)"
            return question, answer, unit
        

    def friction_and_distance_problems(self,difficulty):
        flip = ri(0,2)
        if flip == 0:
            pass
        elif flip == 1:
            mass, height, spring_constant, compression, thermal = self.grav_elastic_thermal_nums()
        else:
            mass, height, velocity, thermal = self.grav_kin_thermal_nums()
        

        if difficulty == "Easy":
            pass


        return


    def choose_problem(self,problem_type, difficulty):
        if problem_type == "Elastic Potential Energy":
            question, answer, unit = self.elastic_problem(difficulty)
        elif problem_type == "Kinetic Energy":
            question, answer, unit = self.kinetic_problem(difficulty)
        elif problem_type == "Gravitational Potential Energy":
            question, answer, unit = self.gravitational_problem(difficulty)
        elif problem_type == "Work":
            question, answer, unit = self.work_problem(difficulty)

        elif problem_type == "Elastic <--> Kinetic":
            question, answer, unit = self.elastic_kinetic_problem(difficulty)
        elif problem_type == "Gravitational <--> Kinetic":
            question, answer, unit = self.kinetic_gravitational_problem(difficulty)
        elif problem_type == "Gravitational <--> Elastic":
              question, answer, unit = self.elastic_gravitational_problem(difficulty)

        elif problem_type == "Quantifying Thermal Energy":
            question, answer, unit = self.thermal_quant_problems(difficulty)
        else:
            pass
        
        return question, answer, unit
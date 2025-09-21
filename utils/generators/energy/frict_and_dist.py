from random import randint as ri
from utils.generators.base_generator import BaseGenerator
from utils.word_lists import random_noun
from utils.generators.energy.thermal_loss import ThermalLossGenerator
TLG = ThermalLossGenerator()

class ThermalWithFrictionGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="thermal_w_fric_")


    # # # F R I C T I 0 N   A N D   D I S T A N C E   P R 0 B L E M S # # # 
    def grav_to_kinetic_friction_distance_q(self, difficulty):
        
        mass, height, velocity, thermal = TLG.grav_to_kin_thermal_nums()
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
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how tall is the ramp?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = height
                unit2 = "Ramp Height (meters)"
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
            else:
                question = f"""A {noun} is released from rest and slides down a {height:.2f} meter tall ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much mass does the {noun} have?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = mass
                unit2 = "Mass (kilograms)"
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]

        else:
            flip = ri(0,4)
            if flip == 0: 
                question = f"""A {mass:.2f} kg {noun} is released from rest and 
                slides down a {height:.2f} meter tall ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How fast is it moving at the bottom?"""
                answer = [velocity]
                unit = ["Final Velocity (m/s)"]
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How tall is the ramp?"""
                answer = [height]
                unit = ["Ramp Height (meters)"]
            elif flip == 2:
                question = f"""A {noun} is released from rest and slides down a {height:.2f} meter tall ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much mass does the {noun} have?"""
                answer = [mass]
                unit = ["Mass (kilograms)"]
            elif flip == 3:
                question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a {height:.2f} meter tall ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n It experiences {friction:.2f} N of frictional force. 
                \n What is the length of the ramp?"""
                answer = [distance]
                unit = ["Ramp Length (meters)"]
            else:
                question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a {height:.2f} meter tall ramp, 
                reaching a velocity of {velocity:.2f} m/s at the bottom.
                \n If the ramp is {distance:.2f} meters long, how strong was the force of friction?"""
                answer = [friction]
                unit = ["Force of Friction (Newtons)"]
        return {"question": question, "answers": answer, "units": unit}
        
    def kinetic_to_grav_friction_distance_q(self, difficulty):
        
        mass, height, velocity, thermal = TLG.kin_to_grav_thermal_nums()
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
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} initially moving at {velocity:.2f} m/s slides up a ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much does the height of the {noun} increase?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = height
                unit2 = "Ramp Height (meters)"
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
            else:
                question = f"""A {noun} is initially moving at {velocity:.2f} m/s 
                increases its height by {height:.2f} meters by sliding up a ramp before coming to rest.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much mass does the {noun} have?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = mass
                unit2 = "Mass (kilograms)"
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]

        else:
            flip = ri(0,4)
            if flip == 0: 
                question = f"""A {mass:.2f} kg {noun} increases its height by {height:.2f} meters
                 by sliding up a ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How fast was it moving initially?"""
                answer = [velocity]
                unit = ["Final Velocity (m/s)"]
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} initially moving at {velocity:.2f} m/s slides up a ramp. 
                \n It reaches rest after it experiences {friction:.2f} N of frictional force 
                over the {distance:.2f} m ramp length. 
                \n How high up on the ramp did the {noun} get?"""
                answer = [height]
                unit = ["Ramp Height (meters)"]
            elif flip == 2:
                question = f"""A {mass:.2f} kg {noun} initially moving at {velocity:.2f} m/s 
                slides up a ramp, increasing its height by {height:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length.
                \n How much mass does the {noun} have?"""
                answer =[ mass]
                unit = ["Mass (kilograms)"]
            elif flip == 3:
                question = f"""A {mass:.2f} kg {noun} initially moving at {velocity:.2f} m/s
                slides {height:.2f} meters tall ramp, 
                reaching a velocity of  at the bottom.
                \n It experiences {friction:.2f} N of frictional force. 
                \n What is the length of the ramp?"""
                answer = [distance]
                unit = ["Ramp Length (meters)"]
            else:
                question = f"""A {mass:.2f} kg {noun} initially moving at {velocity:.2f} m/s 
                slides up a ramp, increasing its height by {height:.2f} meters.
                \n If the ramp is {distance:.2f} meters long, how strong was the force of friction?"""
                answer = [friction]
                unit = ["Force of Friction (Newtons)"]
        return {"question": question, "answers": answer, "units": unit}

    def grav_to_elastic_friction_distance_q(self, difficulty):
        mass, height, spring_constant, compression, thermal = TLG.grav_to_elastic_thermal_nums()        
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
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
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
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
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
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
            else:
                question = f"""A {noun} is released from rest and slides down a {height:.2f} meter tall ramp, 
                and compresses a spring of strength {spring_constant:.2f} N/m by {compression:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much mass does the {noun} have?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = mass
                unit2 = "Mass (kilograms)"
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
        else:
            flip = ri(0,5)
            if flip == 0: 
                question = f"""A {mass:.2f} kg {noun} is released from rest and 
                slides down a {height:.2f} meter tall ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length, 
                and compresses a spring of strength {spring_constant:.2f} N/m at the bottom.
                \n How much does the spring compress?"""
                answer = [compression]
                unit = ["Spring Compression (meters)"]
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} is released from rest and 
                slides down a {height:.2f} meter tall ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length, 
                and compresses a spring by {compression:.2f} meters at the bottom.
                \n How strong is the spring?"""
                answer = [spring_constant]
                unit = ["Spring Constant (N/m)"]
            elif flip == 2:
                question = f"""A {noun} is released from rest and slides down a {height:.2f} meter tall ramp, 
                and compresses a spring of strength {spring_constant:.2f} N/m by {compression:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much mass does the {noun} have?"""
                answer = [mass]
                unit = ["Mass (kilograms)"]
            elif flip == 3:
                question = f"""A {mass:.2f} kg {noun} is released from rest 
                and slides down a {height:.2f} meter tall ramp, 
                and compresses a spring of strength {spring_constant:.2f} N/m by {compression:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force.
                \n What is the length of the ramp?"""
                answer = [distance]
                unit = ["Ramp Length (meters)"]
            elif flip == 4:
                question = f"""A {mass:.2f} kg {noun} is released from rest and slides down a ramp.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length, 
                and compresses a spring with strength {spring_constant:.2f} by 
                {compression:.2f} meters at the bottom.
                \n How high up was the {noun} initially?"""
                answer = [height]
                unit = ["Ramp Height (meters)"]
            else:
                question = f"""A {mass:.2f} kg {noun} is released from rest 
                and slides down a {height:.2f} meter tall ramp, 
                and compresses a spring of strength {spring_constant:.2f} N/m by {compression:.2f} meters.
                \n If the ramp is {distance:.2f} meters long, how strong was the force of friction?"""
                answer = [friction]
                unit = ["Force of Friction (Newtons)"]
        return {"question": question, "answers": answer, "units": unit}

    def elastic_to_grav_friction_distance_q(self, difficulty):
        mass, height, spring_constant, compression, thermal = TLG.elastic_to_grav_thermal_nums()        
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
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
            elif flip == 1:
                question = f"""A spring of strength {spring_constant:.2f} N/m 
                launches a {mass:.2f} kg {noun} up a ramp to a height of {height:.2f} meters.
                \n The {noun} experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much was the spring compressed?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = compression
                unit2 = "Spring Compression (meters)"
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
            elif flip == 2:
                question = f"""A {mass:.2f} kg {noun} is launched to a height of {height:.2f} meters up a ramp 
                by a spring compressed by {compression:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length.
                \n How much energy was lost as heat, and how strong is the spring?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = spring_constant
                unit2 = "Spring Constant (N/m)"
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
            else:
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by {compression:.2f} meters 
                and launches a {noun} up a ramp to a height of {height:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much energy was lost as heat, and how much mass does the {noun} have?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = mass
                unit2 = "Mass (kilograms)"
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]

        else:
            flip = ri(0,5)
            if flip == 0: 
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by {compression:.2f} meters 
                and launches a {mass:.2f} kg {noun} up a ramp.
                \n The {noun} experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How high does the {noun} reach?"""
                answer = [height]
                unit = ["Height (meters)"]
            elif flip == 1:
                question = f"""A spring of strength {spring_constant:.2f} N/m launches a {mass:.2f} kg {noun} 
                up a ramp to a height of {height:.2f} meters.
                \n The {noun} experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length.
                \n By how much was the spring compressed?"""
                answer = [compression]
                unit = ["Spring Compression (meters)"]
            elif flip == 2:
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by {compression:.2f} meters 
                and launches a {noun} up a ramp to a height of {height:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length. 
                \n How much mass does the {noun} have?"""
                answer = [mass]
                unit = ["Mass (kilograms)"]
            elif flip == 3:
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by {compression:.2f} meters 
                and launches a {mass:.2f} kg {noun} up a ramp to a height of {height:.2f} meters.
                \n The {noun} experiences {friction:.2f} N of frictional force.
                \n What is the length of the ramp?"""
                answer = [distance]
                unit = ["Ramp Length (meters)"]
            elif flip == 4:
                question = f"""A {mass:.2f} kg {noun} is launched to a height of {height:.2f} meters up a ramp 
                by a spring compressed by {compression:.2f} meters.
                \n It experiences {friction:.2f} N of frictional force over the {distance:.2f} m ramp length.
                \n How strong is the spring?"""
                answer = [spring_constant]
                unit = ["Spring Constant (N/m)"]
            else:
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by {compression:.2f} meters 
                and launches a {mass:.2f} kg {noun} up a ramp to a height of {height:.2f} meters.
                \n If the ramp is {distance:.2f} meters long, how strong was the force of friction?"""
                answer = [friction]
                unit = ["Force of Friction (Newtons)"]
        return {"question": question, "answers": answer, "units": unit}

    def kinetic_to_elastic_friction_distance_q(self, difficulty):
        mass, velocity, spring_constant, compression, thermal = TLG.kinetic_to_elastic_thermal_nums()
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
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} moving at {velocity:.2f} m/s slides along a surface
                with {friction:.2f} N of friction over {distance:.2f} m 
                before compressing a spring by {compression:.2f} m.
                \n How much energy was lost to heat, and what is the spring constant?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = spring_constant
                unit2 = "Spring Constant (N/m)"
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
            elif flip == 2:
                question = f"""A {mass:.2f} kg {noun} enters a section of rough surface
                with {friction:.2f} N of friction over {distance:.2f} m. 
                It then compresses a spring of strength {spring_constant:.2f} by {compression:.2f} m.
                \n How much energy was lost to heat, and how fast was the {noun} initially moving?"""
                answer1 = thermal
                unit1 = "Thermal Energy (Joules)"
                answer2 = velocity
                unit2 = "Initial Velocity (m/s)"
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
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
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]

        else:
            flip = ri(0,5)
            if flip == 0: 
                question = f"""A {mass:.2f} kg {noun} moving at 
                {velocity:.2f} m/s slides along a surface
                with {friction:.2f} N of friction over {distance:.2f} m before hitting a spring 
                with spring constant {spring_constant:.2f} N/m.
                \n How much does the spring compress?"""
                answer = [compression]
                unit = ["Spring Compression (meters)"]
            elif flip == 1:
                question = f"""A {mass:.2f} kg {noun} moving at {velocity:.2f} m/s slides along a surface
                with {friction:.2f} N of friction over {distance:.2f} m before 
                compressing a spring by {compression:.2f} m.
                \n What is the spring constant?"""
                answer = [spring_constant]
                unit = ["Spring Constant (N/m)"]
            elif flip == 2:
                question = f"""A {noun} moving at {velocity:.2f} m/s slides along a surface 
                with {friction:.2f} N of friction
                over {distance:.2f} m before hitting a spring 
                with spring constant {spring_constant:.2f} N/m, 
                compressing it by {compression:.2f} m.
                \n What is the mass of the {noun}?"""
                answer =[ mass]
                unit = ["Mass (kilograms)"]
            elif flip == 3:
                question = f"""A {mass:.2f} kg {noun} moving at {velocity:.2f} m/s slides along a surface 
                with {friction:.2f} N of friction
                before hitting a spring with spring constant {spring_constant:.2f} N/m, 
                compressing it by {compression:.2f} m.
                \n How far did the {noun} slide before hitting the spring?"""
                answer = [distance]
                unit = ["Distance (meters)"]
            elif flip == 4:
                question = f"""A {mass:.2f} kg {noun} enters a section of rough surface
                with {friction:.2f} N of friction over {distance:.2f} m. 
                It then compresses a spring of strength {spring_constant:.2f} by {compression:.2f} m.
                \n How fast was the {noun} initially moving?"""
                answer = [velocity]
                unit = ["Initial Velocity (m/s)"]
            else:
                question = f"""A {mass:.2f} kg {noun} moving at {velocity:.2f} m/s slides along a surface 
                for {distance:.2f} m
                before hitting a spring with spring constant {spring_constant:.2f} N/m, 
                compressing it by {compression:.2f} m.
                \n What was the force of friction?"""
                answer = [friction]
                unit = ["Force of Friction (Newtons)"]
        return {"question": question, "answers": answer, "units": unit}

    def elastic_to_kinetic_friction_distance_q(self, difficulty):
        mass, velocity, spring_constant, compression, thermal = TLG.elastic_to_kinetic_thermal_nums()
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
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
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
                answer = [answer1, answer2]
                unit = [f"{unit1}", f"{unit2}"]
            elif flip == 2:
                question = f"""A spring is compressed by {compression:.2f} m and launches a {mass:.2f} kg {noun}.
                \n After the {noun} slides along a surface with {friction:.2f} N of friction over {distance:.2f} m,
                the {noun} is moving at a velocity of {velocity:.2f} m/s
                \n How much energy was lost to heat, and what is the strength of the spring?"""
                answer = [thermal,spring_constant]
                unit = ["Thermal Energy (Joules)", "Spring Constant (N/m)"]
                
            else:
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed by {compression:.2f} m
                and launches a {noun} along a surface with {friction:.2f} N of friction over {distance:.2f} m.
                \n The {noun} reaches a velocity of {velocity:.2f} m/s.
                \n How much energy was lost to heat, and what is the mass of the {noun}?"""
                answer = [thermal,mass]
                unit = ["Thermal Energy (Joules)","Mass (kilograms)"]
                
        else:
            flip = ri(0,5)
            if flip == 0: 
                question = f"""A spring of strength {spring_constant:.2f} N/m 
                is compressed by {compression:.2f} m
                and launches a {mass:.2f} kg {noun} along a surface with 
                {friction:.2f} N of friction over {distance:.2f} m.
                \n What is the final velocity of the {noun}?"""
                answer = [velocity]
                unit = ["Velocity (m/s)"]
            elif flip == 1:
                question = f"""A spring with strength {spring_constant:.2f} N/m 
                launches a {mass:.2f} kg {noun}.
                \n After the {noun} slides along a surface with {friction:.2f} N of friction over {distance:.2f} m,
                the {noun} is moving at a velocity of {velocity:.2f} m/s.
                \n By how much was the spring compressed?"""
                answer = [compression]
                unit = ["Spring Compression (meters)"]
            elif flip == 2:
                question = f"""A spring of strength {spring_constant:.2f} N/m 
                is compressed by {compression:.2f} m
                and launches a {noun} along a surface with {friction:.2f} N of friction over {distance:.2f} m.
                \n The {noun} reaches a velocity of {velocity:.2f} m/s.
                \n What is the mass of the {noun}?"""
                answer = [mass]
                unit = ["Mass (kilograms)"]
            elif flip == 3:
                question = f"""A spring of strength {spring_constant:.2f} N/m is compressed 
                by {compression:.2f} m
                and launches a {mass:.2f} kg {noun} along a surface with {friction:.2f} N of friction.
                \n The {noun} reaches a velocity of {velocity:.2f} m/s.
                \n How far was the rough section that the {noun} travelled through?"""
                answer = [distance]
                unit = ["Distance (meters)"]
            elif flip == 4:
                question = f"""A spring is compressed by {compression:.2f} m and launches a {mass:.2f} kg {noun}.
                \n After the {noun} slides along a surface with 
                {friction:.2f} N of friction over {distance:.2f} m,
                the {noun} is moving at a velocity of {velocity:.2f} m/s
                \n What is the strength of the spring?"""
                answer = [spring_constant]
                unit = ["Spring Constant (N/m)"]
            else:
                question = f"""A spring of strength {spring_constant:.2f} N/m 
                is compressed by {compression:.2f} m
                and launches a {mass:.2f} kg {noun} along a surface for {distance:.2f} m.
                \n The {noun} reaches a velocity of {velocity:.2f} m/s.
                \n What was the force of friction experienced by the {noun}?"""
                answer = [friction]
                unit = ["Force of Friction (Newtons)"]
        return {"question": question, "answers": answer, "units": unit}




    # # # I N T E R F A C E  W I T H   R E N D E R E R # # # 
    def choose_problem_dict(self,problem_type, difficulty):
        flip = ri(0,1)
        if problem_type == "Elastic <--> Kinetic":
            if flip == 0:
              return self.elastic_to_kinetic_friction_distance_q(difficulty)
            elif flip == 1:
              return self.kinetic_to_elastic_friction_distance_q(difficulty)
            
        elif problem_type == "Gravitational <--> Kinetic":
            if flip == 0:
              return self.grav_to_kinetic_friction_distance_q(difficulty)
            elif flip == 1:
              return self.kinetic_to_grav_friction_distance_q(difficulty)
        elif problem_type == "Gravitational <--> Elastic":
              if flip == 0:
                return self.grav_to_elastic_friction_distance_q(difficulty)
              elif flip == 1:
                return self.elastic_to_grav_friction_distance_q(difficulty)
        else:
            pass

    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return  {
            "Elastic <--> Kinetic": {
                "honors": r"""W_f = F_f \; x
                \newline ~ \newline ~ \newline
                EPE = \frac{1}{2} k \Delta x^2 \quad ,
                \quad KE = \frac{1}{2} m v^2
                """,

                "conceptual": r"""W_f = F_f \; x \;\;,
                 \;\ x = \frac{W_f}{F_f} \;\;
                 \;\; F_f = \frac{W_f}{x}
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
                "honors": r"""W_f = F_f \; x
                \newline ~ \newline ~ \newline
                GPE = mgh \quad ,
                \quad KE = \frac{1}{2} m v^2
                """,

                "conceptual": r"""W_f = F_f \; x \;\;,
                 \;\ x = \frac{W_f}{F_f} \;\;
                 \;\; F_f = \frac{W_f}{x}
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
                "honors": r"""W_f = F_f \; x
                \newline ~ \newline ~ \newline
                GPE = mgh \quad , \quad
                EPE = \frac{1}{2} k \Delta x^2
                """,
                "conceptual": r"""W_f = F_f \; x \;\;,
                 \;\ x = \frac{W_f}{F_f} \;\;
                 \;\; F_f = \frac{W_f}{x}
                \newline ~ \newline ~ \newline
                GPE = mgh\;\; ,
                \;\; m = \frac{GPE}{gh} \;\; ,
                \;\; h = \frac{GPE}{mg}
                \newline ~ \newline ~ \newline
                EPE = \frac{1}{2} k \Delta x^2 \;\; , 
                \;\; k = \frac{2 \cdot EPE}{\Delta x^2} \;\; , 
                \;\; \Delta x = \sqrt{\frac{2 \cdot EPE}{k}}
                """
                },
        }

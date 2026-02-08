from random import randint as ri
import random

from utils.generators.base_generator import BaseGenerator

from utils.word_lists import random_noun

class RelativeMotionGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="rel_motion_")
    

    def tailwind(self):
        """Returns a tuple of base speed, a modifier, and their sum"""
        object_speed = ri(10,100)
        wind_speed = ri(5,50)
        net_speed = object_speed + wind_speed
        return object_speed, wind_speed, net_speed


    def headwind(self):
        """Returns a tuple of base speed, a modifier, and their difference. \n
        Difference is always positive 
        (tailwind does not fully cancel
        or reverse the direction of the object)"""
        object_speed = ri(20,100)
        wind_speed = -1*ri(5,object_speed - 1)
        net_speed = object_speed + wind_speed
        return object_speed, wind_speed, net_speed
    
    def tailwind_q(self,difficulty,solve_for = None):
        noun = random_noun()
        if solve_for is None:
            solve_for = random.choice([
                "Object Speed",
                "Wind Speed",
                "Net Speed"
            ])
        obj_s, wind_s, net_s = self.tailwind()
        if difficulty == "Easy":
            solve_for = "Net Speed"
            answer = [net_s]
            unit = ["Net Speed (m/s)"]
            question = f"""
            A {noun} is flying at {obj_s} m/s when a 
            {wind_s} m/s wind starts blowing, helping it along.
            What is the overall speed of the {noun}?
            """
        

        return {"question": question, "answers": answer, "unit": unit}

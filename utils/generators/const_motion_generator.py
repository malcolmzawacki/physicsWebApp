from random import randint as ri
import random
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

class ConstantMotionGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="const_motion_")
    
    def choose_problem(self, problem_type: str, difficulty: str
                       ) -> tuple[
        str,list[float],list[str],list[tuple[str,float]]]:
        if problem_type == "Constant Speed":
            return self.inst_speed_question()
        if problem_type == "Average Speed":
            return self.average_speed_question(difficulty)
        if problem_type == "Average Velocity":
            return self.average_velocity_question(difficulty)
        if problem_type == "Combined Constant Motion":
            return self.combined_constant_question(difficulty)

    def choose_problem_dict(self, problem_type: str, difficulty: str):
        if problem_type == "Constant Speed":
            return self.inst_speed_question()
        if problem_type == "Average Speed":
            return self.average_speed_question(difficulty)
        if problem_type == "Average Velocity":
            return self.average_velocity_question(difficulty)
        if problem_type == "Combined Constant Motion":
            return self.combined_constant_question(difficulty)

    def inst_speed(self):
        time = ri(10, 50)
        speed = ri(10, 50)
        dist = speed*time
        return dist, time, speed
    
    def inst_speed_question(self):
        dist, time, speed = self.inst_speed()
        noun = random_noun()
        p = ri(0,2)
        if p == 0:
            answer = dist
            unit = "Distance (m)"
            question = f"""A {noun} spends {time} seconds moving at {speed} m/s. 
            \n\nHow much distance was travelled?"""
        if p == 1:
            answer = time
            unit = "Time (sec)"
            question = f"""A {noun} moves at {speed} m/s, covering {dist} meters of distance. 
            \n\nHow long did it take to do this?"""
        if p == 2:
            answer = speed
            unit = "Speed (m/s)"
            question = f"""A {noun} moves {dist} meters over {time} seconds. 
            \n\nHow fast was the {noun} moving?"""
        return {"question": question, "answers": [answer], "units": [unit]}
    
    def average_speed_question(self, difficulty):
        d1,t1,s1 = self.inst_speed()
        d2,t2,s2 = self.inst_speed()
        
        noun = random_noun()
        if difficulty == "Easy":
            # gives the distances and time, just average them
            answer = round((d1+d2)/(t1+t2),3)
            unit = "Average Speed (m/s)"
            question = f"""A {noun} travels {d1} meters in {t1} seconds,
             \n\n then {d2} meters in {t2} seconds.
              \n\n What is the average speed of the {noun}? """
        if difficulty == "Medium":
            # gives speed and d, t, have to calculate
            answer = round((d1+d2)/(t1+t2),3)
            unit = "Average Speed (m/s)"
            question = f"""A {noun} travels at {s1} m/s for {t1} seconds,
             \n\n then {s2} m/s over {d2} meters.
              \n\n What is the average speed of the {noun}? """
        if difficulty == "Hard":
            # three segments ****can vary order/combination later
            d3,t3,s3 = self.inst_speed()
            answer = round((d1+d2+d3)/(t1+t2+t3),3)
            unit = "Average Speed (m/s)"
            question = f"""A {noun} travels at {s1} m/s for {t1} seconds,
             \n\n then {s2} m/s over {d2} meters,
             \n\n and finally {d3} meters in {t3} seconds.
              \n\n What is the average speed of the {noun}? """
        
        return {"question": question, "answers": [answer], "units": [unit]}
    

    def average_velocity_question(self, difficulty):
        d1,t1,s1 = self.inst_speed()
        d2,t2,s2 = self.inst_speed()
        noun = random_noun()

        sign_change = ri(0,1)
        if sign_change == 0:
            d1*=-1
            direct1 = "to the left"
            direct2 = "to the right"
        else:
            d2*=-1
            direct1 = "to the right"
            direct2 = "to the left"

        if difficulty == "Easy":
            # gives the distances and time, just average them
            answer = round((d1+d2)/(t1+t2),3)
            d1, d2 = abs(d1), abs(d2)
            unit = "Average Velocity (m/s)"
            question = f"""A {noun} travels {d1} meters {direct1} in {t1} seconds,
             \n\n then {d2} meters {direct2} in {t2} seconds.
              \n\n What is the average velocity of the {noun}? """
        if difficulty == "Medium":
            # gives speed and d, t, have to calculate
            answer = round((d1+d2)/(t1+t2),3)
            d1, d2 = abs(d1), abs(d2)
            unit = "Average Velocity (m/s)"
            question = f"""A {noun} travels at {s1} m/s {direct1} for {t1} seconds,
             \n\n then {s2} m/s {direct2} over {d2} meters.
              \n\n What is the average velocity of the {noun}? """
        if difficulty == "Hard":
            # three segments ****can vary order/combination later
            d3,t3,s3 = self.inst_speed()
            sign_change2 = ri(0,1)
            if sign_change == 0:
                d3*=-1
                direct3 = "to the left"
            else:
                direct3 = "to the right"
            answer = round((d1+d2+d3)/(t1+t2+t3),3)
            d1, d2, d3 = abs(d1), abs(d2), abs(d3)
            unit = "Average Velocity (m/s)"
            question = f"""A {noun} travels at {s1} m/s {direct1} for {t1} seconds,
             \n\n then {s2} m/s {direct2} for {d2} meters,
             \n\n and finally {d3} meters {direct3} in {t3} seconds.
              \n\n What is the average velocity of the {noun}? """
        
        return {"question": question, "answers": [answer], "units": [unit]}
    


    
    def combined_constant_question(self, difficulty):
        d1,t1,s1 = self.inst_speed()
        d2,t2,s2 = self.inst_speed()
        noun = random_noun()

        sign_change = ri(0,1)
        if sign_change == 0:
            d1*=-1
            direct1 = "to the left"
            direct2 = "to the right"
        else:
            d2*=-1
            direct1 = "to the right"
            direct2 = "to the left"

        if difficulty == "Easy":
            # asks for speed and velocity
            velocity = round((d1+d2)/(t1+t2),3)
            d1, d2 = abs(d1), abs(d2)
            speed  = round((d1+d2)/(t1+t2),3)
            answer = [speed, velocity]
            unit = ["Average Speed (m/s)", "Average Velocity (m/s)"]
            question = f"""A {noun} travels {d1} meters {direct1} in {t1} seconds,
             \n\n then {d2} meters {direct2} in {t2} seconds.
              \n\n What is the average speed of the {noun}? The average velocity?"""
        if difficulty == "Medium":
            # asks for distance, displacement, speed, and velocity
            disp = d1 + d2
            velocity = round(disp/(t1+t2),3)
            d1, d2 = abs(d1), abs(d2)
            dist = d1 + d2
            speed  = round((dist)/(t1+t2),3)
            answer = [dist, disp, speed, velocity]
            unit = ["Total Distance (m)","Net Displacement (m)","Average Speed (m/s)", "Average Velocity (m/s)"]
            question = f"""A {noun} travels at {s1} m/s {direct1} for {t1} seconds,
             \n\n then {s2} m/s {direct2} over {d2} meters.
             \n\n What is the total distance travelled by the {noun}? What is the net displacement?
              \n\n What is the average speed of the {noun}? The average velocity?"""
        if difficulty == "Hard":
            # asks for distance, displacement, speed, and velocity
            d3,t3,s3 = self.inst_speed()
            sign_change2 = ri(0,1)
            if sign_change2 == 0:
                d3*=-1
                direct3 = "to the left"
            else:
                direct3 = "to the right"
            disp = d1 + d2 + d3
            velocity = round(disp/(t1+t2+t3),3)
            d1, d2, d3 = abs(d1), abs(d2), abs(d3)
            dist = d1 + d2 + d3
            speed  = round((dist)/(t1+t2+t3),3)
            answer = [dist, disp, speed, velocity]
            unit = ["Total Distance (m)","Net Displacement (m)","Average Speed (m/s)", "Average Velocity (m/s)"]
            question = f"""A {noun} travels at {s1} m/s {direct1} for {t1} seconds,
             \n\n then {s2} m/s {direct2} for {d2} meters,
             \n\n and finally {d3} meters {direct3} in {t3} seconds.
              \n\n What is the total distance travelled by the {noun}? What is the net displacement?
              \n\n What is the average speed of the {noun}? The average velocity?"""
        
        return {"question": question, "answers": answer, "units": unit}
import random
import sys
from pathlib import Path
from random import randint as ri

sys.path.append(str(Path(__file__).parent.parent.parent))
try:
    from .base_generator import BaseGenerator
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from utils.generators.base_generator import BaseGenerator

from utils.word_lists import random_noun

class LinearMotionGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="linear_")

    def get_difficulty_range(self, difficulty):
        if difficulty == "Easy":
            return 5
        elif difficulty == "Hard":
            return 20
        return 10

    def no_time_eq_nums(self, difficulty): # v_f,v_i,a,x 
        max_val = self.get_difficulty_range(difficulty)

        """
        changing direction is not worth scrutinizing over,
        (at least for initial launch) 
        """
        m = random.randint(3,max_val)
        if difficulty in ["Easy", "Medium"]: # v_i = 0
            n = m
            "this covers starting or ending at zero"
            """stopping (or slowing) can be handled at 
            word problem level as swapping vf, vi, a*= -1"""
        elif difficulty == "Hard":
            n = random.randint(1,m-1)
        v_i = m**2 - n**2
        v_f = m**2 + n**2
        a_x = 2* m**2 * n**2
        temp_list = []
        for i in range(2,a_x + 1):
            if a_x % i == 0:
                temp_list.append((i,a_x//i))
        list_choice = random.randint(0,len(temp_list)-1)
        a = temp_list[list_choice][0]
        x = temp_list[list_choice][1]
        return v_f,v_i,a,x
    
    def no_dist_eq_nums(self,difficulty):
        max_val = self.get_difficulty_range(difficulty)
        t = random.randint(2,max_val)
        if difficulty == "Easy":
            """easy means no initial velocity
            (or final in case of swap)"""
            v_i = 0
            a = random.randint(1,max_val)
        elif difficulty == "Medium":
            """in medium, non-zero velocities, but same dirn"""
            v_i = random.randint(1,max_val)
            a = random.randint(1,max_val)
        else: # Hard"
            """in HARD, deliberately switching direction"""
            v_i = random.randint(1,max_val)
            a = -1*random.randint((v_i//t)+1,(3*(v_i//t +2)))
            # different range of a ensures a*t is larger than v_i
            # but not unreasonably large once multiplied by t
            # somewhat balanced final velocity
            # default is v_i to right, a to left, but can be swapped
        v_f = v_i + a*t
        return v_f,v_i,a,t
    
    def no_acc_eq_nums(self,difficulty):
        max_val = self.get_difficulty_range(difficulty)
        "case of zero not currently handled here"
        "avoid by differentiating more by difficulty"
        if difficulty == "Easy":
            "so clearly, for easy, one of the velocities should be zero"
            "and the other should be positive"
            v_i = 0
            v_f = random.randint(1,max_val)
        elif difficulty == "Medium":
            "maybe both non-zero, but positive? no negatives here, no reason"
            v_i = random.randint(1,max_val)
            v_f = random.randint(v_i+1,v_i+max_val)
        else: # hard
            "change in direction, default is pos -> neg, can be swapped"
            v_i = random.randint(3,max_val)
            "need to make sure NOT equal and opposite"
            coin = random.randint(0,1)
            if coin == 0:
                v_f = -1*random.randint(1,v_i-1)
            else:
                v_f = -1*random.randint(v_i+1,v_i+max_val)
        if (v_f + v_i)%2 == 0:
            t = random.randint(2,max_val)
        else: # odd sum, needs factor of 2
            t = 2 * random.randint(1,max_val//2)
        x = (v_f + v_i)*t//2
        return x, v_f,v_i,t
    
    def no_vf_eq_nums(self,difficulty):
        max_val = self.get_difficulty_range(difficulty)
        t = random.randint(2,max_val)
        "easy: v_i = 0, a > 0"
        if t%2 == 0:
            a_mult = 1
        else:
            a_mult = 2
        if difficulty == "Easy":
            v_i = 0
            a = random.randint(1,max_val)
        elif difficulty == "Medium":
            "non-zero vi but still all positive"
            v_i = random.randint(1,max_val)
            a = random.randint(1,max_val)
        else: # hard
            "mis-matched velocity and acceleration"
            "slowed, but not reversed hmmmm"
            "2vi/t > a"
            v_i = random.randint(1,max_val)
            a = -1*random.randint(1,(2*v_i//t)+2)
        a*=a_mult # ensures divisibility if t is odd
        v_i*=a_mult # ensures directionality is preserved
        x = v_i*t + 0.5*a*t**2
        return x, v_i,t,a

    def get_step_num(self,difficulty):
        if difficulty == "Easy":
            return 2
        elif difficulty == "Medium":
            return 4
        else: #hard
            return 6

    def distance_and_displacement_1D(self,difficulty):
        noun = random_noun()
        directions = [
            ["right","left"],
            ["up","down"],
            ["North","South"],
            ["East","West"]
            ]
        # note that the positive direction is listed first 
        problem_directions = random.choice(directions)
        distance = 0
        displacement = 0
        movements =[]
        max_val = 2*self.get_difficulty_range(difficulty)
        label_set = [
            "Total Distance (meters)", 
            "Net Displacement (meters)", 
            "Direction (Say 'None' for zero)"
            ]
        question = f"A {noun} goes on a walk, and makes the following movements: \n"

        steps = self.get_step_num(difficulty)

        for i in range(steps):
            dirn = ri(0,1)
            step = ri(1,max_val)
            distance += step
            if dirn == 0:
                displacement += step
            else: 
                displacement -= step
            step_dirn = problem_directions[dirn]
            movements.append((step_dirn, step))

            question += f"{i+1}. {step} meters {step_dirn} \n"
        question += f"\nWhat is the total distance and net displacment of the {noun}?"
        if displacement > 0:
            direction = problem_directions[0]
        elif displacement < 0:
            direction = problem_directions[1]
        else:
            direction = "None"
        displacement = abs(displacement)
        return question, [distance, displacement, direction], label_set, movements
    

    def distance_and_displacement_2D(self,difficulty):
        noun = random_noun()
        problem_directions = [["East","West"],["North","South"]]
        # note that the positive direction is listed first, x and y
        distance = 0
        disp_x = 0
        disp_y = 0
        max_val = 20
        movements = []
        label_set = [
            "Total Distance (meters)", 
            "Net Displacement (meters)", 
            "Direction (Say 'None' for zero)"]
        question = f"A {noun} goes on a walk, and makes the following movements: \n"
        steps = int(self.get_step_num(difficulty) / 2)
        for i in range(steps):
            dirn_x = ri(0,1)
            dirn_y = ri(0,1)
            step_x = ri(1,max_val)
            step_y = ri(1,max_val)
            distance += step_x + step_y
            if dirn_x == 0:
                disp_x += step_x
            else: 
                disp_x -= step_x
            if dirn_y == 0:
                disp_y += step_y
            else: 
                disp_y -= step_y
            step_dirn_x = problem_directions[0][dirn_x]
            step_dirn_y = problem_directions[1][dirn_y]
            movements.append((step_dirn_x, step_x))
            movements.append((step_dirn_y, step_y))
            question += f"{2*i+1}. {step_x} meters {step_dirn_x} \n"
            question += f"{2*i+2}. {step_y} meters {step_dirn_y} \n"
        if disp_x > 0:
            dirn_x_final = "East"
        elif disp_x < 0:
            dirn_x_final = "West"
        else:
            dirn_x_final = ""
        if disp_y > 0:
            dirn_y_final = "North"
        elif disp_y < 0:
            dirn_y_final = "South"
        else:
            dirn_y_final = ""
        dirn_final = dirn_y_final + dirn_x_final
        dirn_final = "None" if len(dirn_final) < 4 else dirn_final
        displacement = (disp_x**2  + disp_y**2)**(1/2)

        return question, [distance, displacement, dirn_final], label_set, movements
    


    "E X T R A   S P A C E   F O R   Q U E S T I O N   F U N C T I O N S"


    def no_time_question(self, difficulty):
        """has acceleration problems, needs x, vf, vi"""
        noun = random_noun()
        coin = random.randint(0,1)  # determines speeding up or slowing down
        var_dice = random.randint(0, 3)  # roll for variable to solve for
        v_f, v_i, a, x = self.no_time_eq_nums(difficulty)
        if coin == 0:
            verb = "speeds up"
        else:
            a *= -1
            verb = "slows down"

        if difficulty in ["Easy", "Medium"]:
            if var_dice == 0:  # Solve for acceleration
                unit = "Acceleration (m/s²)"
                answer = a
                if verb == "speeds up":
                    question = f"""What acceleration would a {noun} at rest need to experience \
                    for it to reach a velocity of {v_f} m/s over a distance of {x} meters?"""
                else:
                    question = f"""How much deceleration would a {noun} moving at {v_f} m/s \
                    need in order to come to rest over a distance of {x} meters?"""
            elif var_dice in [1,2]:  # Solve for final velocity, swap for 'initial' if slowing
                
                answer = v_f
                if verb == "speeds up":
                    question = f"""If a {noun} starts from rest and accelerates at {a} m/s² \
                    over a distance of {x} meters, what velocity does it reach?"""
                    unit = "Final Velocity (m/s)"
                else:
                    question = f"""If a {noun} decelerates at {-1*a} m/s² to rest \
                    over {x} meters, what was its initial velocity?"""
                    unit = "Initial Velocity (m/s)"
            elif var_dice == 3:  # Solve for distance
                unit = "Distance (meters)"
                answer = x
                if verb == "speeds up":
                    question = f"""A {noun} at rest accelerates at {a} m/s² to a velocity of {v_f} m/s. \
                    How far did it travel during this time?"""
                else:
                    question = f"""A {noun} decelerates at {-1*a} m/s² from {v_f} m/s to rest. \
                    How far did it travel during this time?"""
        else:  # HARD difficulty
            if var_dice == 0:  # Solve for acceleration
                unit = "Acceleration (m/s²)"
                answer = a
                if verb == "speeds up":
                    question = f"""What acceleration would a {noun} moving at {v_i} m/s need to experience \
                    for it to speed up to {v_f} m/s over a distance of {x} meters?"""
                else:
                    question = f"""What deceleration would a {noun} moving at {v_f} m/s need to experience \
                    to slow down to {v_i} m/s over a distance of {x} meters?"""
            elif var_dice == 1:  # Solve for final velocity
                unit = "Final Velocity (m/s)"
                answer = v_f
                if verb == "speeds up":
                    question = f"""If a {noun} starts at {v_i} m/s and accelerates at {a} m/s² \
                    over {x} meters, what velocity does it reach?"""
                else:
                    question = f"""If a {noun} decelerates at {-1*a} m/s² from {v_f} m/s \
                    to {v_i} m/s over {x} meters, what is the final velocity?"""
            elif var_dice == 2:  # Solve for initial velocity
                unit = "Initial Velocity (m/s)"
                answer = v_i
                if verb == "speeds up":
                    question = f"""If a {noun} accelerates at {a} m/s² to {v_f} m/s \
                    over {x} meters, what was its initial velocity?"""
                else:
                    question = f"""If a {noun} decelerates at {-1*a} m/s² to {v_f} m/s \
                    over {x} meters, what was its initial velocity?"""
            elif var_dice == 3:  # Solve for distance
                unit = "Distance (meters)"
                answer = x
                if verb == "speeds up":
                    question = f"""A {noun} accelerates from {v_i} m/s to {v_f} m/s at {a} m/s². \
                    How far did it travel?"""
                else:
                    question = f"""A {noun} decelerates from {v_f} m/s to {v_i} m/s at {-1*a} m/s². \
                    How far did it travel?"""

        return question, [answer], [unit]
            
    "Formatting on HARD here could be improved to state direction textually. still includes negative signs. gotta ship something tho"
    def no_dist_question(self, difficulty):
        """has a, needs t, vf, vi"""
        v_f, v_i, a, t = self.no_dist_eq_nums(difficulty)
        noun = random_noun()
        coin = random.randint(0, 1)  # determines speeding up or slowing down
        var_dice = random.randint(0, 3)  # roll for variable to solve for
        if coin == 0:
            verb = "speeds up"
        else:
            a *= -1
            verb = "slows down"
        if difficulty == "Easy":
            if var_dice == 0:  # Solve for acceleration
                unit = "Acceleration (m/s²)"
                answer = a
                if coin == 0: # speeding up
                    question = f"""What acceleration would a {noun} initially at rest need to \
                    experience to get to {v_f} m/s in {t} seconds?"""
                else: # slowing down
                    question = f"""What deceleration would a {noun} initally moving at {v_f} m/s need to \
                    experience to get to rest in {t} seconds?"""
            elif var_dice in [1,2]:  # Solve for final velocity since initial is zero in easy
                answer = v_f
                if coin == 0:
                    question = f"""If a {noun} starts at rest and accelerates at {a} m/s² for \
                    {t} seconds, what velocity does it reach?"""
                    unit = "Final Velocity (m/s)"
                else:
                    question = f"""If a {noun} decelerates at {-1*a} m/s² for \
                    {t} seconds in order to come to rest, what velocity did it start with?"""
                    unit = "Initial Velocity (m/s)"
            elif var_dice == 3:  # Solve for time
                unit = "Time (seconds)"
                answer = t
                if coin == 0: #speeding up
                    question = f"""A {noun} accelerates from rest at {a} m/s², reaching {v_f} m/s. \
                    How long does it take?"""
                else:
                    question = f"""A {noun} decelerates from {v_f} m/s to rest at a rate of {-1*a}  m/s². \
                    How long does it take?"""
        elif difficulty == "Medium":
            if var_dice == 0:  # Solve for acceleration
                unit = "Acceleration (m/s²)"
                answer = a
                if coin == 0:
                    question = f"""Determine the acceleration required for a {noun} moving at {v_i} m/s \
                    to speed up to {v_f} m/s in {t} seconds."""
                else:
                    question = f"""Determine the deceleration required for a {noun} moving at {v_f} m/s \
                    to slow to {v_i} m/s in {t} seconds."""
            elif var_dice in [1,2]:  # Solve for final velocity, they are reversible
                if coin == 0:
                    question = f"""A {noun} starts at {v_i} m/s and accelerates at {a} m/s² for {t} seconds. \
                    What is its final velocity?"""
                    unit = "Final Velocity (m/s)"
                else:
                    question = f"""A {noun} slows to {v_i} m/s after decelerating at {-1*a} m/s² for {t} seconds. \
                    What was its initial velocity?"""
                    unit = "Initial Velocity (m/s)"
            elif var_dice == 3:  # Solve for time
                unit = "Time (seconds)"
                answer = t
                if coin == 0:
                    question = f"""A {noun} accelerates from {v_i} m/s to {v_f} m/s with an acceleration of {a} m/s². \
                    How much time does it take?"""
                else:
                    question = f"""A {noun} decelerates from {v_f} m/s to {v_i} m/s at a rate of {a} m/s². \
                    How much time does it take?"""
        else:  # HARD difficulty
            if var_dice == 0:  # Solve for acceleration
                unit = "Acceleration (m/s²)"
                answer = a
                question = f"""What acceleration would a {noun} moving at {v_i} m/s need to experience \
                to {verb} to {v_f} m/s in {t} seconds?"""
            elif var_dice == 1:  # Solve for final velocity
                unit = "Final Velocity (m/s)"
                answer = v_f
                question = f"""If a {noun} starts at {v_i} m/s and {verb} at {a} m/s² for {t} seconds, \
                what velocity does it reach?"""
            elif var_dice == 2:  # Solve for initial velocity
                unit = "Initial Velocity (m/s)"
                answer = v_i
                question = f"""If a {noun} {verb} at {a} m/s² to reach {v_f} m/s in {t} seconds, \
                what was its initial velocity?"""
            elif var_dice == 3:  # Solve for time
                unit = "Time (seconds)"
                answer = t
                question = f"""A {noun} {verb} at {a} m/s² from {v_i} m/s to {v_f} m/s. \
                How long does it take?"""

        return question, [answer], [unit]

    
    def no_acc_question(self,difficulty):
        "has t,x, needs vf, vi"
        x, v_f,v_i,t = self.no_acc_eq_nums(difficulty)
        noun = random_noun()
        coin = random.randint(0,1)
        var_dice = random.randint(0,1)
        if difficulty == "Easy":
            "so clearly, for easy, one of the velocities should be zero"
            "and the other should be positive. default is speeding up"
            if var_dice == 0: # time
                unit = "Time (seconds)"
                answer = t
                if coin == 0: # speeding up
                    question = f"""A {noun} initially at rest accelerates at a constant rate over a distance of {x} meters. 
                    If it reached a velocity of {v_f} m/s, how much time did it take to get up to that speed?"""
                else:
                    question = f"""A {noun} initially moving at a velocity of {v_f} m/s decelerates at a constant rate 
                    until it is at a full stop. If this occurred over a distance of {x} meters, how much time did it take?"""
            elif var_dice == 1: # x
                unit = "Distance (meters)"
                answer = x
                if coin == 0: # speeding up
                    question = f"""A {noun} initially at rest accelerates at a constant rate for {t} seconds. 
                    If it reached a velocity of {v_f} m/s, how much distance did it cover during that time?"""
                else:
                    question = f"""A {noun} initially moving at a velocity of {v_f} m/s decelerates at a constant rate 
                    until it is at a full stop. If this occurred over {t} seconds, how much distance did it cover?"""
            elif var_dice in [2,3]: # velocity, reversible
                answer = v_f
                if coin == 0: # speeding up
                    question = f"""A {noun} initially at rest accelerates at a constant rate for {t} seconds. \
                    If this occurred over {x} meters, what velocity did the {noun} reach?"""
                    unit = "Final Velocity (m/s)"
                else:
                    question = f"""A noun reaches rest after decelerating at a constant rate for {t} seconds. \ 
                    If this occurred over {x} meters, what velocity did {noun} start with?"""
                    unit = "Initial Velocity (m/s)"

        elif difficulty == "Medium":
            "maybe both non-zero, but positive? no negatives here, no reason"
            if var_dice == 0: # time
                unit = "Time (seconds)"
                answer = t
                if coin == 0: # speeding up
                    question = f"""A {noun} initially moving at {v_i} m/s accelerates at a constant rate over a distance of {x} meters. 
                    If it reaches a final velocity of {v_f} m/s, how much time did it take to get up to that speed?"""
                else:
                    question = f"""A {noun} initially moving at a velocity of {v_f} m/s decelerates at a constant rate 
                    until it is at a new velocity of {v_i} m/s. If this occurred over a distance of {x} meters, how much time did it take?"""
            elif var_dice == 1: # x
                unit = "Distance (meters)"
                answer = x
                if coin == 0: # speeding up
                    question = f"""A {noun} initially moving at {v_i} m/s accelerates at a constant rate for {t} seconds. 
                    If it reaches a final velocity of {v_f} m/s, how much distance did it cover during that time?"""
                else:
                    question = f"""A {noun} initially moving at a velocity of {v_f} m/s decelerates at a constant rate 
                    until it is at a new velocity of {v_i} m/s. If this occurred over {t} seconds, how much distance did it cover?"""
            elif var_dice in [2,3]: # v_f,vi
                unit = "Final Velocity (m/s)"
                if coin == 0:
                    answer = v_f
                    question = f"""A {noun} initially moving at {v_i} m/s accelerates at a constant rate for {t} seconds.\
                        If this occurred over a distance of {x} meters, what velocity did it reach?""" 
                else:
                    answer = v_i
                    question = f"""A {noun} initially moving at {v_f} m/s decelerates at a constant rate for {t} seconds.\
                        If this occurred over a distance of {x} meters, what velocity did it reach?"""
            
        else: # hard
            "change in direction, default is pos -> neg, can be swapped"
            if x > 0:
                direction_phrase = "to the right"
            else:
                direction_phrase = "to the left"
            if var_dice == 0: # time
                unit = "Time (seconds)"
                answer = t
                if coin == 0: # vi>0, vf<0
                    question = f"""A {noun}, initially moving at {v_i} m/s to the right, slows all the way down,
                    and gets back up to {-1*v_f} m/s to the left. 
                    The {noun} travels {abs(x)} meters {direction_phrase} in the process. 
                    How much time did this take?"""
                else: # vi<0, a>0
                    question = f"""A {noun}, initially moving at {-1*v_f} m/s to the left, 
                    slows all the way down, and gets back up to {v_i} m/s to the right.  
                    The {noun} travels {abs(x)} meters {direction_phrase} in the process. 
                    How much time did this take?"""
            elif var_dice == 1: # x
                unit = "Distance (meters)"
                answer = x
                if coin == 0: # vi>0, vf<0
                    question = f"""A {noun}, initially moving at {v_i} m/s to the right,  
                    slows all the way down, and gets back up to {-1*v_f} m/s to the left in {t} seconds.  
                    What is the {noun}'s displacement?"""
                else: # vi<0, a>0
                    question = f"""A {noun}, initially moving at {-1*v_f} m/s to the left,  
                    slows all the way down, and gets back up to {v_i} m/s to the right in {t} seconds.  
                    What is the {noun}'s displacement?"""
            elif var_dice in [2,3]:
                unit = "Final Velocity (m/s)"
                if coin == 0:
                    answer = v_f
                    question = f"""A {noun}, initially moving at {v_i} m/s to the right, experiences a constant acceleration that 
                    slows it all the way down, and speeds it back up to the left. 
                    The acceleration was applied for {t} seconds, and resulted in the {noun} 
                    traveling {abs(x)} meters {direction_phrase}.
                    What is the final velocity of the {noun}?"""
                else:
                    answer = v_i
                    question = f"""A {noun}, initially moving at {-1*v_f} m/s to the left, experiences a constant acceleration that 
                    slows it all the way down, and speeds it back up to the right. 
                    The acceleration was applied for {t} seconds, and resulted in the {noun} 
                    traveling {abs(x)} meters {direction_phrase}.
                    What is the final velocity of the {noun}?"""

        return question, [answer], [unit]
    
    def no_vf_question(self,difficulty):
        "has x, needs a, vi, t -> (for easy, hard only)"
        x, v_i,t,a = self.no_vf_eq_nums(difficulty)
        noun = random_noun()
        if difficulty == "Easy":
            "vi = 0, find only x a t"
            var_dice = random.randint(0,2)
            if var_dice == 0: # x
                question = f"""A {noun}, initially at rest, accelerates at a rate of {a} m/s² for {t} seconds.
                How far does it go during this time?"""
                answer = x
                unit = "Distance (meters)"
            elif var_dice == 1: # time
                answer = t
                unit = "Time (seconds)"
                question = f"""A {noun}, initially at rest, accelerates at a rate of {a} m/s² over {x} meters.
                How long does this take?"""
            else:
                answer = a
                unit = "Acceleration (m/s²)"
                question = f"""A {noun}, initially at rest, accelerates at a constant rate for {t} seconds over {x} meters.
                How big was the acceleration?"""
        elif difficulty == "Medium":
            "non-zero vi but still all positive. find x , vi, a (NOT t)"
            var_dice = random.randint(0,2)
            if var_dice == 0: # x
                question = f"""A {noun}, initially moving at {v_i} m/s, accelerates at a rate of {a} m/s² for {t} seconds.
                How far does it go during this time?"""
                answer = x
                unit = "Distance (meters)"
            elif var_dice == 1: # vi
                question = f"""A {noun}, initially moving to the right, accelerates at a rate of {a} m/s² for {t} seconds.
                The {noun} covers {x} meters. How fast was it initially moving?"""
                answer = v_i
                unit = "m/s"
            else: # a
                answer = a
                unit = "Acceleration (m/s²)"
                question = f"""A {noun}, initially moving at {v_i} m/s, accelerates at a constant rate for {t} seconds over {x} meters.
                How big was the acceleration?"""
        else: # hard
            "mis-matched velocity and acceleration, sometimes?? somehow re-loop in medium?"
            "one in three chance, maybe"
            medium_chance = random.randint(0,2)
            if medium_chance == 0:
                question, answer, unit = self.no_vf_question("Medium")
            else:
                "find all four"
                var_dice = random.randint(0,3)
                if var_dice == 0: # x
                    question = f"""A {noun} is initially moving at {v_i} m/s to the right, 
                    but is slowed by an acceleration of {-1*a} m/s² for {t} seconds.
                    How far does it go during this time?"""
                    answer = x
                    unit = "Distance (meters)"
                elif var_dice == 1: #v_i
                    question = f"""A {noun}, initially moving to the right, is slowed at a rate of {-1*a} m/s² for {t} seconds.
                    Despite this, {noun} covers {x} meters. How fast was it initially moving?"""
                    answer = v_i
                    unit = "Initial Velovity (m/s)"
                elif var_dice == 2: # a
                    answer = a
                    unit = "Acceleration (m/s²)"
                    question = f"""A {noun}, initially moving at {v_i} m/s to the right, is slowed at a constant rate for {t} seconds over {x} meters.
                    What was the acceleration?"""
                else: # time
                    answer = t
                    unit = "Time (seconds)"
                    question = f"""A {noun}, initially moving at {v_i} m/s to the right, is slowed at a constant rate {-1*a} m/s².
                    How much time does this take for the {noun} to cover {x} meters?"""



        return question, [answer], [unit]
    
    def mixed_question(self,difficulty):
        dice = random.randint(0,3)
        if dice == 0:
            question, answer, unit = self.no_time_question(difficulty)
        elif dice == 1:
            question, answer, unit = self.no_dist_question(difficulty)
        elif dice == 2:
            question, answer, unit = self.no_acc_question(difficulty)
        else:
            if difficulty == "Hard":
                coin = random.randint(0,1)
                if coin == 0:
                    question, answer, unit = self.no_vf_question("Medium")
                else:
                    question, answer, unit = self.no_vf_question(difficulty)
            else:
                question, answer, unit = self.no_vf_question(difficulty)

        return question, answer, unit
    
    def choose_problem(self,problem_type, difficulty):
        if problem_type == "No Time":
            question, answer, unit = self.no_time_question(difficulty)
        elif problem_type == "No Distance":
            question, answer, unit = self.no_dist_question(difficulty)
        elif problem_type == "No Acceleration":
            question, answer, unit = self.no_acc_question(difficulty)
        elif problem_type == "No Final Velocity":
            question, answer, unit = self.no_vf_question(difficulty)
        elif problem_type == "One Dimensional":
            question, answer, unit, movements = self.distance_and_displacement_1D(difficulty)
            return question, answer, unit, movements
        elif problem_type == "Two Dimensional":
            question, answer, unit, movements = self.distance_and_displacement_2D(difficulty)
            return question, answer, unit, movements
        else:  # Mixed
            question, answer, unit = self.mixed_question(difficulty)
        return question, answer, unit


    def generate_movement_diagram(self,movements: list, problem_type: str, difficulty: str):
        """
        Generate a diagram showing the movement path
        
        Parameters:
        movements: list of tuples (direction, distance)
        problem_type: "1D" or "2D"
        
        Returns:
        matplotlib figure
        """
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(4, 4))
        
        # Set up the plot
        if problem_type == "One Dimensional":
            # For 1D, we'll draw on a horizontal line
            horizontal_directions = {"left","right","East", "West"}
            if movements[0][0] in horizontal_directions:
                ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
                steps = self.get_step_num(difficulty)
                ax.set_ylim(0, steps+2)
                # Start at origin
                current_x = 0
                current_y = 1
                points_x = [current_x]
                points_y = [current_y]
                step_count = 0
                positive_directions = {"right","East"}
                # Plot each movement
                for i in range(len(movements)):
                    if movements[i][0] in positive_directions:
                        current_x += movements[i][1]
                    else:
                        current_x -= movements[i][1]
                    
                    points_x.append(current_x)
                    points_y.append(current_y)
                    current_y+=1
                    if i < len(movements) - 1:
                        points_x.append(current_x)
                        points_y.append(current_y)
                    
                # Plot the path
                #ax.plot(points_x, points_y, 'o-', color='yellow')
                
                # Add arrows to show direction
                for i in range(len(points_x) - 1):
                    if i % 2 == 1:
                    
                        ax.arrow(points_x[i], points_y[i],0, 0.8,
                            head_width=0.1, head_length=0.2, 
                            fc='yellow', ec='yellow',linestyle=':')

                    dx = points_x[i+1] - points_x[i]
                    
                    ax.arrow(points_x[i], points_y[i], dx * 0.8, 0, 
                            head_width=0.1, head_length=abs(dx) * 0.2, 
                            fc='cyan', ec='cyan')
                
                # Add displacement vector
                ax.arrow(
                    points_x[0], steps+1, 
                    (points_x[-1] - points_x[0])*0.9, 0,
                    head_width=0.1, 
                    head_length=abs(points_x[-1] - points_x[0]) * 0.1,
                    fc='red', ec='red', linewidth=2
                    )
                
                # Add grid
                ax.grid(True, linestyle='--', alpha=0.3)

                # Add labels
                ax.set_xlabel('Position (meters)')
                ax.set_ylabel('Movement Number')
                ax.set_title(
                    """1D Movement Diagram\npath in blue, step in yellow,\ndisplacement in red"""
                             )
            else: # vertical Stuff
                ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
                steps = self.get_step_num(difficulty)
                ax.set_xlim(0, steps+2)
                # Start at origin
                current_y = 0
                current_x = 1
                points_y = [current_y]
                points_x = [current_x]
                step_count = 0
                positive_directions = {"North","up"}
                # Plot each movement
                for i in range(len(movements)):
                    if movements[i][0] in positive_directions:
                        current_y += movements[i][1]
                    else:
                        current_y -= movements[i][1]
                    
                    points_x.append(current_x)
                    points_y.append(current_y)
                    current_x+=1
                    if i < len(movements) - 1:
                        points_x.append(current_x)
                        points_y.append(current_y)
                    
                # Plot the path
                #ax.plot(points_x, points_y, 'o-', color='yellow')
                
                # Add arrows to show direction
                for i in range(len(points_x) - 1):
                    dy = points_y[i+1] - points_y[i]
                    
                    ax.arrow(points_x[i], points_y[i], 0, dy * 0.8, 
                            head_width=0.1, head_length=abs(dy) * 0.2, 
                            fc='cyan', ec='cyan')
                    if i % 2 == 1:
                    
                        ax.arrow(points_x[i], points_y[i],0.8, 0,
                            head_width=0.1, head_length=0.2, 
                            fc='yellow', ec='yellow',linestyle=':')
                
                # Add displacement vector
                ax.arrow(
                    steps+1,points_y[0], 0,
                    (points_y[-1] - points_y[0])*0.9,
                    head_width=0.1, 
                    head_length=abs(points_y[-1] - points_y[0]) * 0.1,
                    fc='red', ec='red', linewidth=2
                    )
                
                # Add grid
                ax.grid(True, linestyle='--', alpha=0.3)

                # Add labels
                ax.set_ylabel('Position (meters)')
                ax.set_xlabel('Movement Number')
                ax.set_title(
                    """1D Movement Diagram\npath in blue, step in yellow,\ndisplacement in red"""
                             )

            
        else:  # 2D
            # Start at origin
            current_x, current_y = 0, 0
            points_x = [current_x]
            points_y = [current_y]
            
            # Plot each movement
            for direction, distance in movements:
                if direction == "East":
                    current_x += distance
                elif direction == "West":
                    current_x -= distance
                elif direction == "North":
                    current_y += distance
                elif direction == "South":
                    current_y -= distance
                
                points_x.append(current_x)
                points_y.append(current_y)
            
            # Plot the path
            #ax.plot(points_x, points_y, 'o-', color='cyan')
            
            # Add arrows to show direction
            for i in range(len(points_x) - 1):
                dx = points_x[i+1] - points_x[i]
                dy = points_y[i+1] - points_y[i]
                dx = 0.8*dx if dx != 0 else dx
                dy = 0.8*dy if dy != 0 else dy
                x_arrow = abs(0.2*dx) if dx != 0 else 1
                y_arrow = abs(0.2*dy) if dy != 0 else 1
                ax.arrow(points_x[i], points_y[i], dx, dy, 
                        head_width=0.3, head_length=x_arrow*y_arrow, 
                        fc='cyan', ec='cyan')
            
            # Add displacement vector
            disp_x = (points_x[-1] - points_x[0])
            disp_y = (points_y[-1] - points_y[0])
            arrowhead_length =abs((disp_x**2 + disp_y**2)**(1/2))
            disp_x *= 0.8
            disp_y *= 0.8
            arrowhead_length *= 0.2
            ax.arrow(points_x[0], points_y[0],
                    disp_x, 
                    disp_y,
                    head_width=0.3, head_length=arrowhead_length,
                    fc='red', ec='red', linewidth=1)
            
            # Add grid
            ax.grid(True, linestyle='--', alpha=0.3)
            
            # Add labels
            ax.set_xlabel('X Position (meters)')
            ax.set_ylabel('Y Position (meters)')
            ax.set_title('2D Movement Diagram \n path in blue \n displacement in red')
            
            # Make axes equal scale
            ax.set_aspect('auto')
        
        # Make the plot clean
        plt.tight_layout()
        plt.style.use("dark_background")
        
        return fig
        
import random
from random import randint as ri


from utils.generators.base_generator import BaseGenerator

from utils.word_lists import random_noun

class LinearMotionGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="linear_")


    def choose_problem_dict(self, problem_type, difficulty, solve_for=None):
        """Return a problem dictionary for the requested kinematics case."""
        if problem_type == "No Time":
            return self.no_time_question(difficulty, solve_for=solve_for)
        elif problem_type == "No Distance":
            return self.no_dist_question(difficulty, solve_for=solve_for)
        elif problem_type == "No Acceleration":
            return self.no_acc_question(difficulty, solve_for=solve_for)
        elif problem_type == "No Final Velocity":
            return self.no_vf_question(difficulty, solve_for=solve_for)
        elif problem_type == "Mixed":
            return self.mixed_question(difficulty, solve_for=solve_for)
        else:
            raise ValueError(f"Unknown problem type '{problem_type}'")


    def get_difficulty_range(self, difficulty):
        if difficulty == "Easy":
            return 5
        elif difficulty == "Hard":
            return 20
        return 10
    

    # region get numbers for equations

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
            a = a_mult*random.randint(1,max_val)
        elif difficulty == "Medium":
            "non-zero vi but still all positive"
            v_i = random.randint(1,max_val)
            a = a_mult*random.randint(1,max_val)
        else: # hard
           "needs to change direction in order for there to be a unique answer"
           "I mean I could also set the net displacement equal to zero but where's the variety in that?"
           a = random.randint(2,max_val)
           t = random.randint(2,max_val)
           v_i = ri(1, a*t - 1)
           t*=2 # now the change in velocity is more than twice the size of the initial
           if random.choice([True,False]):
               a*=-1
           else:
               v_i*=-1

        x = v_i*t + 0.5*a*t**2
        return x, v_i,t,a


    # endregion






    # region question phrasing and formatting

    def _select_solve_for(self, solve_for, allowed_map, context_label):
        """Normalize a solve_for string and validate it against supported options."""
        options = list(allowed_map.keys())
        if solve_for is None:
            return random.choice(options)

        normalized = str(solve_for).strip().lower()
        for canonical, aliases in allowed_map.items():
            alias_values = {canonical}
            alias_values.update(aliases)
            if normalized in alias_values:
                return canonical

        readable = "', '".join(options)
        raise ValueError(
            f"Unsupported solve_for '{solve_for}' for {context_label}. Choose from '{readable}'."
        )

    def _direction_label(self, value):
        if value > 0:
            return "to the right"
        if value < 0:
            return "to the left"
        return None

    def _velocity_value_str(self, value):
        direction = self._direction_label(value)
        base = f"{value} m/s"
        if direction:
            return f"{base} ({direction})"
        return base

    def _describe_velocity(self, value):
        direction = self._direction_label(value)
        speed = abs(value)
        if speed == 0:
            return "at rest"
        if direction:
            return f"{speed} m/s {direction}"
        return f"{speed} m/s"

    def _format_acceleration(self, value):
        direction = self._direction_label(value)
        base = f"{value} m/s^2"
        if direction and value != 0:
            return f"{base} ({direction})"
        return base

    def _motion_phrases(self, initial, final, scenario):
        start_inf = "start from rest" if initial == 0 else f"start by moving at {self._velocity_value_str(initial)}"
        start_ind = "it starts from rest" if initial == 0 else f"it starts by moving at {self._velocity_value_str(initial)}"

        if final == 0:
            end_inf = "come to rest"
            end_ind = "it comes to rest"
        elif scenario == "reversal":
            end_inf = f"reach {self._velocity_value_str(final)} after changing direction"
            end_ind = f"it reaches {self._velocity_value_str(final)} after changing direction"
        else:
            end_inf = f"reach {self._velocity_value_str(final)}"
            end_ind = f"it reaches {self._velocity_value_str(final)}"

        start_stmt = start_ind[3:] if start_ind.startswith("it ") else start_ind
        end_stmt = end_ind[3:] if end_ind.startswith("it ") else end_ind

        return {
            "start_inf": start_inf,
            "start_ind": start_ind,
            "start_stmt": start_stmt,
            "end_inf": end_inf,
            "end_ind": end_ind,
            "end_stmt": end_stmt,
        }

    def _motion_context(self, initial, final, accel):
        """Analyze motion parameters and derive narrative details without altering values."""
        speed_initial = abs(initial)
        speed_final = abs(final)
        reverses = initial * final < 0

        if speed_initial == 0 and speed_final == 0:
            scenario = "stationary"
        elif reverses:
            scenario = "reversal"
        elif speed_initial == 0:
            scenario = "starting"
        elif speed_final == 0:
            scenario = "stopping"
        elif speed_final > speed_initial:
            scenario = "increasing"
        elif speed_final < speed_initial:
            scenario = "decreasing"
        else:
            scenario = "steady"

        verb_map = {
            "starting": "speeds up",
            "increasing": "speeds up",
            "stopping": "slows down",
            "decreasing": "slows down",
            "reversal": "changes direction",
            "steady": "maintains speed",
            "stationary": "remains at rest",
        }

        return {
            "initial": initial,
            "final": final,
            "accel": accel,
            "accel_mag": abs(accel),
            "initial_direction": self._direction_label(initial),
            "final_direction": self._direction_label(final),
            "accel_direction": self._direction_label(accel),
            "initial_desc": self._describe_velocity(initial),
            "final_desc": self._describe_velocity(final),
            "initial_value_str": self._velocity_value_str(initial),
            "final_value_str": self._velocity_value_str(final),
            "accel_value_str": self._format_acceleration(accel),
            "scenario": scenario,
            "verb": verb_map.get(scenario, "changes speed"),
            "speed_initial": speed_initial,
            "speed_final": speed_final,
            "reverses": reverses,
        }


    # endregion






    # region question and answer functions

    def no_time_question(self, difficulty, solve_for=None):
        """Build a no-time kinematics question."""
        target = self._select_solve_for(
            solve_for,
            {
                "a": ("acceleration",),
                "vf": ("final", "final_velocity"),
                "vi": ("initial", "initial_velocity"),
                "x": ("distance", "displacement"),
            },
            "No Time",
        )

        v_f, v_i, base_a, x = self.no_time_eq_nums(difficulty)
        if random.choice([True, False]):
            v_i, v_f, base_a, x = -v_i, -v_f, -base_a, -x
        context = self._motion_context(v_i, v_f, base_a)
        phrases = self._motion_phrases(v_i, v_f, context["scenario"])
        noun = random_noun()

        accel_phrase = context["accel_value_str"]
        start_inf = phrases["start_inf"]
        start_ind = phrases["start_ind"]
        start_stmt = phrases["start_stmt"]
        end_inf = phrases["end_inf"]
        end_ind = phrases["end_ind"]
        end_stmt = phrases["end_stmt"]

        if target == "a":
            unit = "Acceleration (m/s^2)"
            answer = base_a
            question = (
                f"What constant acceleration would allow a {noun} to {start_inf} and {end_inf} over {x} meters?"
            )
        elif target == "vf":
            unit = "Final Velocity (m/s)"
            answer = v_f
            question = (
                f"A {noun} experiences a constant acceleration of {accel_phrase} while traveling {x} meters. "
                f"If {start_ind}, what velocity does it reach?"
            )
        elif target == "vi":
            unit = "Initial Velocity (m/s)"
            answer = v_i
            question = (
                f"A {noun} experiences a constant acceleration of {accel_phrase} while traveling {x} meters. "
                f"If {end_ind}, what was its initial velocity?"
            )
        else:  # target == "x"
            unit = "Distance (meters)"
            answer = x
            question = (
                f"How far does a {noun} travel if it experiences a constant acceleration of {accel_phrase}, "
                f"{start_stmt}, and {end_stmt}?"
            )

        return {"question": question, "answers": [answer], "units": [unit]}


    def no_dist_question(self, difficulty, solve_for=None):
        """Build a no-distance (v_f = v_i + at) kinematics question."""
        target = self._select_solve_for(
            solve_for,
            {
                "a": ("acceleration",),
                "vf": ("final", "final_velocity"),
                "vi": ("initial", "initial_velocity"),
                "t": ("time", "delta_t"),
            },
            "No Distance",
        )

        v_f, v_i, base_a, t = self.no_dist_eq_nums(difficulty)
        if random.choice([True, False]):
            v_i, v_f, base_a = -v_i, -v_f, -base_a
        context = self._motion_context(v_i, v_f, base_a)
        phrases = self._motion_phrases(v_i, v_f, context["scenario"])
        noun = random_noun()

        accel_phrase = context["accel_value_str"]
        start_inf = phrases["start_inf"]
        start_ind = phrases["start_ind"]
        start_stmt = phrases["start_stmt"]
        end_inf = phrases["end_inf"]
        end_ind = phrases["end_ind"]
        end_stmt = phrases["end_stmt"]
        time_phrase = f"{t} seconds"

        if target == "a":
            unit = "Acceleration (m/s^2)"
            answer = base_a
            question = (
                f"What constant acceleration would allow a {noun} to {start_inf} and {end_inf} in {time_phrase}?"
            )
        elif target == "vf":
            unit = "Final Velocity (m/s)"
            answer = v_f
            question = (
                f"A {noun} experiences a constant acceleration of {accel_phrase} for {time_phrase}. "
                f"If {start_ind}, what velocity does it reach?"
            )
        elif target == "vi":
            unit = "Initial Velocity (m/s)"
            answer = v_i
            question = (
                f"A {noun} experiences a constant acceleration of {accel_phrase} for {time_phrase}. "
                f"If {end_ind}, what was its initial velocity?"
            )
        else:  # target == "t"
            unit = "Time (seconds)"
            answer = t
            question = (
                f"How long would it take for a {noun} to {start_inf} and {end_inf} if it experiences a constant "
                f"acceleration of {accel_phrase}?"
            )

        return {"question": question, "answers": [answer], "units": [unit]}


    def no_acc_question(self, difficulty, solve_for=None):
        """Build a no-acceleration (x = (v_f + v_i)/2 * t) kinematics question."""
        target = self._select_solve_for(
            solve_for,
            {
                "t": ("time",),
                "x": ("distance", "displacement"),
                "vf": ("final", "final_velocity"),
                "vi": ("initial", "initial_velocity"),
            },
            "No Acceleration",
        )

        x, v_f, v_i, t = self.no_acc_eq_nums(difficulty)
        if random.choice([True, False]):
            v_i, v_f, x = -v_i, -v_f, -x

        effective_accel = (v_f - v_i) / t if t != 0 else 0
        context = self._motion_context(v_i, v_f, effective_accel)
        phrases = self._motion_phrases(v_i, v_f, context["scenario"])
        noun = random_noun()

        start_ind = phrases["start_ind"]
        start_stmt = phrases["start_stmt"]
        end_ind = phrases["end_ind"]
        end_stmt = phrases["end_stmt"]

        if target == "t":
            unit = "Time (seconds)"
            answer = t
            question = (
                f"A {noun} {start_stmt} and {end_stmt} while covering {x} meters. How long does this motion take?"
            )
        elif target == "x":
            unit = "Distance (meters)"
            answer = x
            question = (
                f"A {noun} {start_stmt} and {end_stmt} over {t} seconds. How much distance does it cover?"
            )
        elif target == "vf":
            unit = "Final Velocity (m/s)"
            answer = v_f
            question = (
                f"A {noun} {start_stmt} for {t} seconds while covering {x} meters. What is its final velocity?"
            )
        else:  # target == "vi"
            unit = "Initial Velocity (m/s)"
            answer = v_i
            question = (
                f"A {noun} {end_stmt} after traveling {x} meters in {t} seconds. What was its initial velocity?"
            )

        return {"question": question, "answers": [answer], "units": [unit]}


    def no_vf_question(self, difficulty, solve_for=None):
        """Build a no-final-velocity (x = v_i t + 1/2 a t^2) kinematics question."""
        target = self._select_solve_for(
            solve_for,
            {
                "x": ("distance", "displacement"),
                "t": ("time",),
                "vi": ("initial", "initial_velocity"),
                "a": ("acceleration",),
            },
            "No Final Velocity",
        )

        x, v_i, t, a = self.no_vf_eq_nums(difficulty)
        if random.choice([True, False]):
            v_i, a, x = -v_i, -a, -x
        v_f = v_i + a * t
        context = self._motion_context(v_i, v_f, a)
        phrases = self._motion_phrases(v_i, v_f, context["scenario"])
        noun = random_noun()

        accel_phrase = context["accel_value_str"]
        start_inf = phrases["start_inf"]
        start_ind = phrases["start_ind"]
        start_stmt = phrases["start_stmt"]
        end_inf = phrases["end_inf"]
        end_ind = phrases["end_ind"]
        end_stmt = phrases["end_stmt"]
        time_phrase = f"{t} seconds"

        if target == "x":
            unit = "Distance (meters)"
            answer = x
            question = (
                f"A {noun} experiences a constant acceleration of {accel_phrase} for {time_phrase}. "
                f"If {start_ind}, how far does it travel?"
            )
        elif target == "t":
            unit = "Time (seconds)"
            answer = t
            question = (
                f"How long would it take for a {noun} to {start_inf} and {end_inf} over {x} meters if it experiences "
                f"a constant acceleration of {accel_phrase}?"
            )
        elif target == "vi":
            unit = "Initial Velocity (m/s)"
            answer = v_i
            question = (
                f"A {noun} experiences a constant acceleration of {accel_phrase} for {time_phrase} and covers {x} meters. "
                f"What was its initial velocity?"
            )
        else:  # target == "a"
            unit = "Acceleration (m/s^2)"
            answer = a
            question = (
                f"What constant acceleration would allow a {noun} to {start_inf}, {end_inf}, and cover {x} meters in "
                f"{time_phrase}?"
            )

        return {"question": question, "answers": [answer], "units": [unit]}

    def mixed_question(self, difficulty, solve_for=None):
        """Return a problem from a randomly selected no-kinematics case.

        Mixed questions rotate between the specific generators. Provide a concrete
        problem type if you need to lock the variable being solved for.
        """
        if solve_for is not None:
            raise ValueError(
                "Mixed questions do not support a solve_for override; invoke a specific problem type instead."
            )

        dice = random.randint(0,3)
        if dice == 0:
            return self.no_time_question(difficulty)
        elif dice == 1:
            return self.no_dist_question(difficulty)
        elif dice == 2:
            return self.no_acc_question(difficulty)
        else:
            if difficulty == "Hard":
                coin = random.randint(0,1)
                if coin == 0:
                    return self.no_vf_question("Medium")
                else:
                    return self.no_vf_question(difficulty)
            else:
                return self.no_vf_question(difficulty)


    # endregion
    




    # region metadata
    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "No Time": {
                "honors_equation": r"v_f^2 = v_i^2 + 2ax",
                "conceptual_equation": r"v_f = \sqrt{v_i^2 + 2ax}  \quad , \quad v_i = \sqrt{2ax - v_f^2}  \quad , \quad  x = \frac{v_f^2 - v_i^2}{2a}  \quad, \quad  a = \frac{v_f^2 - v_i^2}{2x}",
                "tags": ["kinematics", "no time"],
            },
            "No Distance": {
                "honors_equation": r"v_f = v_i + at",
                "conceptual_equation": r"v_f = v_i +at  \quad , \quad v_i =  v_f - at  \quad , \quad a = \frac{v_f - v_i}{t}  \quad, \quad t = \frac{v_f - v_i}{a}",
                "tags": ["kinematics", "no distance"],
            },
            "No Acceleration": {
                "honors_equation": r"x = \frac{v_f + v_i}{2} t",
                "conceptual_equation": r"x = \frac{v_f + v_i}{2} t  \quad , \quad t = \frac{2x}{v_f + v_i}  \quad , \quad v_f = \frac{2x}{t} - v_i  \quad , \quad v_i = \frac{2x}{t} - v_f",
                "tags": ["kinematics", "no acceleration"],
            },
            "No Final Velocity": {
                "honors_equation": r"x = v_i t + \frac{1}{2} at^2",
                "conceptual_equation": r"x = v_i t + \frac{1}{2} at^2  \quad , \quad a = 2 \left( \frac{x - v_i t}{t^2} \right)\quad , \quad t = \frac{\sqrt{v_i^2 + 2ax} - v_i}{a}",
                "tags": ["kinematics", "no v_f"],
            },
            "Mixed": {
                "honors_equation": r"v_f^2 = v_i^2 + 2ax \quad , \quad v_f = v_i +at  \quad , \quad x = \frac{v_f + v_i}{2} t  \quad , \quad x = v_i t + \frac{1}{2} at^2",
                "conceptual_equation": r"""
                x = \frac{v_f + v_i}{2} t  \quad , \quad 
                x = v_i t + \frac{1}{2} at^2  \quad , \quad 
                x = \frac{v_f^2 - v_i^2}{2a}  
                \newline ~ \newline ~ \newline 
                t = \frac{2x}{v_f + v_i}  \quad , \quad 
                t = \frac{v_f - v_i}{a}  \quad , \quad 
                t = \frac{\sqrt{v_i^2 + 2ax} - v_i}{a}   
                \newline ~ \newline ~ \newline 
                v_i = \sqrt{2ax - v_f^2}  \quad , \quad
                v_i = v_f - at  \quad , \quad 
                v_i = \frac{2x}{t} - v_f  \quad , \quad 
                v_i = \frac{x}{t} - \frac{1}{2} at 
                \newline ~ \newline ~ \newline 
                v_f = \frac{2x}{t} - v_i  \quad , \quad 
                v_f = \sqrt{v_i^2 + 2ax}  \quad , \quad 
                v_f = v_i + at  \quad  
                \newline ~ \newline ~ \newline 
                a = 2 \left( \frac{x - v_i t}{t^2} \right)\quad  , \quad 
                a = \frac{v_f - v_i}{t}  \quad , \quad 
                a = \frac{v_f^2 - v_i^2}{2x}""",
                "tags": ["kinematics", "mixed"],
            },
        }


import random
from random import randint as ri


from utils.generators.base_generator import BaseGenerator

from utils.word_lists import random_noun

class LinearMotionGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="linear_")

        self.INFO_CLAUSES = {
            "vi": "{start_stmt}",
            "vf": "{end_stmt}",
            "a": "experiences {accel_phrase}",
            "t": "for {time_phrase}",
            "x": "over {dist_phrase}",
        }
        
        self.QUESTION_CLAUSES = {
            "vi": "What was its initial velocity?",
            "vf": "What is its final velocity?",
            "a": "What is its acceleration?",
            "t": "How much time did this take?",
            "x": "What is its overall displacement?",
        }

        self.UNIT_LABELS = {
            "vi": "Initial Velocity (m/s)",
            "vf": "Final Velocity (m/s)",
            "a": "Acceleration (m/s^2)",
            "t": "Time (seconds)",
            "x": "Distance (meters)",
        }


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

    def combined_eq_nums(self, difficulty):
        """Calculates a consistent, integer-based set of all 5 kinematics variables."""
        max_val = self.get_difficulty_range(difficulty)
        
        # 1. Choose a and t, ensuring one is even for an integer 'x'
        a = ri(2, max_val)
        t = ri(2, max_val) # both have min of 2 to avoid edge case errors in reversal scenarios
        
        if a % 2 != 0 and t % 2 != 0:
            # If both are odd, make one even
            if random.choice([True, False]):
                t += 1 # A simple way to make it even
            else:
                a += 1
                
        # 2. Determine v_i and sign of 'a' based on difficulty
        if difficulty == "Easy":
            v_i = 0
            # Keep 'a' positive for simplicity
        
        elif difficulty == "Medium":
            # "Medium" = No reversal. v_i and a have the same sign
            v_i = ri(1, max_val)
            if random.choice([True, False]): # 50/50 chance to make it a "slowing down" problem
                # Make v_i and a have opposite signs, but don't reverse
                a *= -1 # Make 'a' negative
                # Ensure |v_i| > |a*t| so it just slows down, no reversal
                v_i = ri(abs(a * t) + 1, abs(a * t) + max_val//2) 
            
        else: # "Hard"
            # "Hard" = Guaranteed reversal. v_i and a have opposite signs.
            if random.choice([True, False]):
                a *= -1 # Make 'a' negative
            
            # Ensure |v_i| < |a*t| to guarantee reversal
            max_vi = abs(a * t) - 1
            
            # This is the one v_i magnitude that results in x = 0
            critical_vi_mag = 0.5 * abs(a * t) 
            v_i_mag = ri(1, max_vi)
            # Re-roll if we hit the one bad value
            while v_i_mag == critical_vi_mag:
                v_i_mag = ri(1, max_vi)
                
            v_i = v_i_mag

            if a > 0: # If 'a' is positive, 'v_i' must be negative
                v_i *= -1

        # 3. Calculate the remaining variables
        v_f = v_i + a * t
        x = int(v_i * t + 0.5 * a * t**2) # Cast to int to avoid 0.0

        return {
            "vi": v_i,
            "vf": v_f,
            "a": a,
            "t": t,
            "x": x
        }


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

    def _motion_state_details(self, value, role):
        """Return semantic data describing a motion state."""
        direction = self._direction_label(value)
        description = self._describe_velocity(value)
        return {
            "value": value,
            "speed": abs(value),
            "direction": direction,
            "is_rest": value == 0,
            "velocity_value": self._velocity_value_str(value),
            "velocity_desc": description,
            "role": role,
            "label": "initial" if role == "start" else "final",
        }

    def _state_phrases(self, state, *, scenario):
        """Build reusable phrase fragments for a motion state."""
        subject = "it"
        role = state["role"]
        is_rest = state["is_rest"]
        velocity_value = state["velocity_value"]

        if role == "start":
            if is_rest:
                infinitive = "start from rest"
                indicative_subjectless = "is at rest initially"
                indicative_it = f"{subject} is at rest initially"
            else:
                infinitive = f"begin with an initial velocity of {velocity_value}"
                indicative_subjectless = f"has an initial velocity of {velocity_value}"
                indicative_it = f"{subject} has an initial velocity of {velocity_value}"
        else:
            if is_rest:
                infinitive = "come to rest"
                indicative_subjectless = "comes to rest"
                indicative_it = f"{subject} comes to rest"
            else:
                if scenario == "reversal":
                    infinitive = f"change direction and reach {velocity_value}"
                    indicative_subjectless = f"changes direction and reaches {velocity_value}"
                    indicative_it = f"{subject} changes direction and reaches {velocity_value}"
                elif scenario == "steady":
                    infinitive = f"continue moving at {velocity_value}"
                    indicative_subjectless = f"continues moving at {velocity_value}"
                    indicative_it = f"{subject} continues moving at {velocity_value}"
                else:
                    infinitive = f"reach {velocity_value}"
                    indicative_subjectless = f"reaches {velocity_value}"
                    indicative_it = f"{subject} reaches {velocity_value}"

        return {
            "infinitive": infinitive,
            "indicative_subjectless": indicative_subjectless,
            "indicative_it": indicative_it,
        }

    def _motion_phrases(self, initial, final, scenario):
        """Return semantic state data and phrase fragments for the motion."""
        start_state = self._motion_state_details(initial, role="start")
        end_state = self._motion_state_details(final, role="end")

        return {
            "start": {
                "state": start_state,
                "phrases": self._state_phrases(start_state, scenario=scenario),
            },
            "end": {
                "state": end_state,
                "phrases": self._state_phrases(end_state, scenario=scenario),
            },
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


    def _build_question(self, eq_nums, target, noun, info_keys):
        """Assemble a question dict using clause templates and shared motion phrasing."""
        context = self._motion_context(eq_nums["vi"], eq_nums["vf"], eq_nums["a"])
        motion = self._motion_phrases(eq_nums["vi"], eq_nums["vf"], context["scenario"])

        start_phrases = motion["start"]["phrases"]
        end_phrases = motion["end"]["phrases"]

        format_vars = {
            "noun": noun,
            "x": eq_nums["x"],
            "t": eq_nums["t"],
            "accel_phrase": context["accel_value_str"],
            "time_phrase": f"{eq_nums['t']} seconds",
            "dist_phrase": f"{eq_nums['x']} meters",
            "start_stmt": start_phrases["indicative_subjectless"],
            "end_stmt": end_phrases["indicative_subjectless"],
        }

        info_parts = [
            self.INFO_CLAUSES[key].format(**format_vars)
            for key in info_keys
            if key != target
        ]
        info_sentence = ", ".join(info_parts)
        question = f"A {noun} {info_sentence}. {self.QUESTION_CLAUSES[target]}"
        answer = eq_nums[target]
        unit = self.UNIT_LABELS[target]

        return {"question": question, "answers": [answer], "units": [unit]}

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

        eq_nums = self.combined_eq_nums(difficulty)
        noun = random_noun()

        info_keys = ["vi", "vf", "a", "x"]
        return self._build_question(eq_nums, target, noun, info_keys)


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

        eq_nums = self.combined_eq_nums(difficulty)
        noun = random_noun()

        info_keys = ["vi", "vf", "a", "t"]
        return self._build_question(eq_nums, target, noun, info_keys)


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

        eq_nums = self.combined_eq_nums(difficulty)
        noun = random_noun()

        info_keys = ["vi", "vf", "t", "x"]
        return self._build_question(eq_nums, target, noun, info_keys)


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

        eq_nums = self.combined_eq_nums(difficulty)
        noun = random_noun()

        info_keys = ["vi", "a", "t", "x"]
        return self._build_question(eq_nums, target, noun, info_keys)

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


import random
import math
from random import randint as ri

from utils.generators.base_generator import BaseGenerator
from utils.word_lists import random_noun


class RotationalMotionGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="rotational_")

        self.INFO_CLAUSES = {
            "vi": "has an initial angular velocity of {vi} rad/s",
            "vf": "reaches a final angular velocity of {vf} rad/s",
            "a": "experiences an angular acceleration of {a} rad/s^2",
            "t": "for {t} seconds",
            "theta": "rotates through {theta} radians",
        }

        self.QUESTION_CLAUSES = {
            "vi": "What was its initial angular velocity?",
            "vf": "What is its final angular velocity?",
            "a": "What is its angular acceleration?",
            "t": "How much time did this take?",
            "theta": "What is its angular displacement?",
        }

        self.UNIT_LABELS = {
            "vi": "Initial Angular Velocity (rad/s)",
            "vf": "Final Angular Velocity (rad/s)",
            "a": "Angular Acceleration (rad/s^2)",
            "t": "Time (seconds)",
            "theta": "Angular Displacement (radians)",
        }
        self.CONVERSION_PROBABILITY = 0.35
        self.CONVERSION_OPTIONS = ("rev/s", "rev/min")

    def choose_problem_dict(self, problem_type, difficulty, solve_for=None):
        """Return a problem dictionary for the requested rotational kinematics case."""
        if problem_type == "No Time":
            return self.no_time_question(difficulty, solve_for=solve_for)
        if problem_type == "No Distance":
            return self.no_dist_question(difficulty, solve_for=solve_for)
        if problem_type == "No Acceleration":
            return self.no_acc_question(difficulty, solve_for=solve_for)
        if problem_type == "No Final Velocity":
            return self.no_vf_question(difficulty, solve_for=solve_for)
        if problem_type == "Mixed":
            return self.mixed_question(difficulty, solve_for=solve_for)
        raise ValueError(f"Unknown problem type '{problem_type}'")

    def get_difficulty_range(self, difficulty):
        if difficulty == "Easy":
            return 5
        if difficulty == "Hard":
            return 20
        return 10

    def combined_eq_nums(self, difficulty):
        """Calculates a consistent, integer-based set of rotational variables."""
        max_val = self.get_difficulty_range(difficulty)

        a = ri(2, max_val)
        t = ri(2, max_val)

        if a % 2 != 0 and t % 2 != 0:
            if random.choice([True, False]):
                t += 1
            else:
                a += 1

        if difficulty == "Easy":
            v_i = 0
        elif difficulty == "Medium":
            v_i = ri(1, max_val)
        else:
            v_i = ri(max_val // 2, max_val * 2)

        v_f = v_i + a * t
        theta = int(v_i * t + 0.5 * a * t**2)

        return {
            "vi": v_i,
            "vf": v_f,
            "a": a,
            "t": t,
            "theta": theta,
        }

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

    def _build_question(self, eq_nums, target, noun, info_keys):
        """Assemble a question dict using clause templates."""
        format_vars = {
            "noun": noun,
            "vi": eq_nums["vi"],
            "vf": eq_nums["vf"],
            "a": eq_nums["a"],
            "t": eq_nums["t"],
            "theta": eq_nums["theta"],
        }

        info_parts = [
            self.INFO_CLAUSES[key].format(**format_vars)
            for key in info_keys
            if key != target
        ]
        info_sentence = ", ".join(info_parts)
        question = f"A {noun} {info_sentence}. {self.QUESTION_CLAUSES[target]}"
        answers = [eq_nums[target]]
        units = [self.UNIT_LABELS[target]]

        conversion = self._build_conversion_prompt(target, eq_nums[target])
        if conversion is not None:
            question = f"{question} {conversion['prompt']}"
            answers.append(conversion["answer"])
            units.append(conversion["unit"])

        return {"question": question, "answers": answers, "units": units}

    def _build_conversion_prompt(self, target, value):
        """Optionally add a unit-conversion follow-up for angular velocity."""
        if target not in ("vi", "vf"):
            return None
        if random.random() > self.CONVERSION_PROBABILITY:
            return None

        unit = random.choice(self.CONVERSION_OPTIONS)
        if unit == "rev/s":
            converted = value / math.tau
            prompt = "Also give that angular velocity in revolutions per second."
        else:
            converted = value / math.tau * 60
            prompt = "Also give that angular velocity in revolutions per minute."

        return {
            "prompt": prompt,
            "answer": converted,
            "unit": f"Angular Velocity ({unit})",
        }

    def no_time_question(self, difficulty, solve_for=None):
        """Build a no-time rotational kinematics question."""
        target = self._select_solve_for(
            solve_for,
            {
                "a": ("acceleration",),
                "vf": ("final", "final_velocity"),
                "vi": ("initial", "initial_velocity"),
                "theta": ("distance", "displacement", "angle"),
            },
            "No Time",
        )

        eq_nums = self.combined_eq_nums(difficulty)
        noun = random_noun()

        info_keys = ["vi", "vf", "a", "theta"]
        return self._build_question(eq_nums, target, noun, info_keys)

    def no_dist_question(self, difficulty, solve_for=None):
        """Build a no-angle (omega_f = omega_i + alpha t) question."""
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
        """Build a no-acceleration (theta = (omega_f + omega_i)/2 * t) question."""
        target = self._select_solve_for(
            solve_for,
            {
                "t": ("time",),
                "theta": ("distance", "displacement", "angle"),
                "vf": ("final", "final_velocity"),
                "vi": ("initial", "initial_velocity"),
            },
            "No Acceleration",
        )

        eq_nums = self.combined_eq_nums(difficulty)
        noun = random_noun()

        info_keys = ["vi", "vf", "t", "theta"]
        return self._build_question(eq_nums, target, noun, info_keys)

    def no_vf_question(self, difficulty, solve_for=None):
        """Build a no-final-velocity (theta = omega_i t + 1/2 alpha t^2) question."""
        target = self._select_solve_for(
            solve_for,
            {
                "theta": ("distance", "displacement", "angle"),
                "t": ("time",),
                "vi": ("initial", "initial_velocity"),
                "a": ("acceleration",),
            },
            "No Final Velocity",
        )

        eq_nums = self.combined_eq_nums(difficulty)
        noun = random_noun()

        info_keys = ["vi", "a", "t", "theta"]
        return self._build_question(eq_nums, target, noun, info_keys)

    def mixed_question(self, difficulty, solve_for=None):
        """Return a problem from a randomly selected rotational kinematics case."""
        if solve_for is not None:
            raise ValueError(
                "Mixed questions do not support a solve_for override; invoke a specific problem type instead."
            )

        dice = random.randint(0, 3)
        if dice == 0:
            return self.no_time_question(difficulty)
        if dice == 1:
            return self.no_dist_question(difficulty)
        if dice == 2:
            return self.no_acc_question(difficulty)
        return self.no_vf_question(difficulty)

    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "No Time": {
                "honors_equation": r"\omega_f^2 = \omega_i^2 + 2\alpha\theta",
                "conceptual_equation": (
                    r"\omega_f = \sqrt{\omega_i^2 + 2\alpha\theta}  \quad , \quad "
                    r"\omega_i = \sqrt{2\alpha\theta - \omega_f^2}  \quad , \quad  "
                    r"\theta = \frac{\omega_f^2 - \omega_i^2}{2\alpha}  \quad, \quad  "
                    r"\alpha = \frac{\omega_f^2 - \omega_i^2}{2\theta}"
                ),
                "tags": ["kinematics", "rotational", "no time"],
            },
            "No Distance": {
                "honors_equation": r"\omega_f = \omega_i + \alpha t",
                "conceptual_equation": (
                    r"\omega_f = \omega_i + \alpha t  \quad , \quad "
                    r"\omega_i =  \omega_f - \alpha t  \quad , \quad "
                    r"\alpha = \frac{\omega_f - \omega_i}{t}  \quad, \quad "
                    r"t = \frac{\omega_f - \omega_i}{\alpha}"
                ),
                "tags": ["kinematics", "rotational", "no distance"],
            },
            "No Acceleration": {
                "honors_equation": r"\theta = \frac{\omega_f + \omega_i}{2} t",
                "conceptual_equation": (
                    r"\theta = \frac{\omega_f + \omega_i}{2} t  \quad , \quad "
                    r"t = \frac{2\theta}{\omega_f + \omega_i}  \quad , \quad "
                    r"\omega_f = \frac{2\theta}{t} - \omega_i  \quad , \quad "
                    r"\omega_i = \frac{2\theta}{t} - \omega_f"
                ),
                "tags": ["kinematics", "rotational", "no acceleration"],
            },
            "No Final Velocity": {
                "honors_equation": r"\theta = \omega_i t + \frac{1}{2} \alpha t^2",
                "conceptual_equation": (
                    r"\theta = \omega_i t + \frac{1}{2} \alpha t^2  \quad , \quad "
                    r"\alpha = 2 \left( \frac{\theta - \omega_i t}{t^2} \right)\quad , \quad "
                    r"t = \frac{\sqrt{\omega_i^2 + 2\alpha\theta} - \omega_i}{\alpha}"
                ),
                "tags": ["kinematics", "rotational", "no omega_f"],
            },
            "Mixed": {
                "honors_equation": (
                    r"\omega_f^2 = \omega_i^2 + 2\alpha\theta \quad , \quad "
                    r"\omega_f = \omega_i + \alpha t  \quad , \quad "
                    r"\theta = \frac{\omega_f + \omega_i}{2} t  \quad , \quad "
                    r"\theta = \omega_i t + \frac{1}{2} \alpha t^2"
                ),
                "conceptual_equation": r"""
                \theta = \frac{\omega_f + \omega_i}{2} t  \quad , \quad 
                \theta = \omega_i t + \frac{1}{2} \alpha t^2  \quad , \quad 
                \theta = \frac{\omega_f^2 - \omega_i^2}{2\alpha}  
                \newline ~ \newline ~ \newline 
                t = \frac{2\theta}{\omega_f + \omega_i}  \quad , \quad 
                t = \frac{\omega_f - \omega_i}{\alpha}  \quad , \quad 
                t = \frac{\sqrt{\omega_i^2 + 2\alpha\theta} - \omega_i}{\alpha}   
                \newline ~ \newline ~ \newline 
                \omega_i = \sqrt{2\alpha\theta - \omega_f^2}  \quad , \quad
                \omega_i = \omega_f - \alpha t  \quad , \quad 
                \omega_i = \frac{2\theta}{t} - \omega_f  \quad , \quad 
                \omega_i = \frac{\theta}{t} - \frac{1}{2} \alpha t 
                \newline ~ \newline ~ \newline 
                \omega_f = \frac{2\theta}{t} - \omega_i  \quad , \quad 
                \omega_f = \sqrt{\omega_i^2 + 2\alpha\theta}  \quad , \quad 
                \omega_f = \omega_i + \alpha t  
                \newline ~ \newline ~ \newline 
                \alpha = 2 \left( \frac{\theta - \omega_i t}{t^2} \right)\quad  , \quad 
                \alpha = \frac{\omega_f - \omega_i}{t}  \quad , \quad 
                \alpha = \frac{\omega_f^2 - \omega_i^2}{2\theta}""",
                "tags": ["kinematics", "rotational", "mixed"],
            },
        }

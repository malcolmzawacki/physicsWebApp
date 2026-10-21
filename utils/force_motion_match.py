"""C2: one-dimensional constant forces and multiple compatible motion histories."""
from dataclasses import dataclass
from io import BytesIO
import random

from utils.force_diagram_match import DIRECTIONS, ForceArrow

PRACTICE_SETS = ("All situations", "Balanced forces", "Horizontal net force", "Vertical net force")


@dataclass(frozen=True)
class ForceMotionCase:
    id: str
    title: str
    axis: str
    arrows: tuple[ForceArrow, ...]
    prompt: str

    @property
    def acceleration_sign(self):
        i = 0 if self.axis == "horizontal" else 1
        net = sum(DIRECTIONS[a.direction][i] * a.size for a in self.arrows)
        return (net > 0) - (net < 0)

    @property
    def category(self):
        return "Balanced forces" if self.acceleration_sign == 0 else "Horizontal net force" if self.axis == "horizontal" else "Vertical net force"


G = ForceArrow("gravity", "down")
N = ForceArrow("normal", "up")
CASES = (
    ForceMotionCase("cart_balance", "Cart on a smooth track", "horizontal", (G, N),
        "A cart stays on a horizontal, frictionless track. Air resistance is neglected. Its initial velocity is not supplied."),
    ForceMotionCase("cart_right", "Cart pushed right", "horizontal", (G, N, ForceArrow("applied", "right")),
        "A cart stays on a horizontal, frictionless track while a steady horizontal push acts to the right. Air resistance is neglected. Its initial velocity is not supplied."),
    ForceMotionCase("cart_left", "Cart pushed left", "horizontal", (G, N, ForceArrow("applied", "left")),
        "A cart stays on a horizontal, frictionless track while a steady horizontal push acts to the left. Air resistance is neglected. Its initial velocity is not supplied."),
    ForceMotionCase("load_balance", "Load on a cable", "vertical", (G, ForceArrow("tension", "up")),
        "A winch keeps a vertical cable taut and pulls a load with constant tension equal to its weight. It stays clear of the floor and ceiling. Its initial velocity is not supplied."),
    ForceMotionCase("load_up", "Stronger cable pull", "vertical", (G, ForceArrow("tension", "up", 2)),
        "A winch keeps a vertical cable taut and pulls a load with constant tension greater than its weight. It stays clear of the floor and ceiling. Its initial velocity is not supplied."),
    ForceMotionCase("load_down", "Weaker cable pull", "vertical", (ForceArrow("gravity", "down", 2), ForceArrow("tension", "up")),
        "A winch keeps a vertical cable taut and pulls a load with constant tension smaller than its weight. It stays clear of the floor and ceiling. Its initial velocity is not supplied."),
    ForceMotionCase("ball_gravity", "Ball in flight", "vertical", (G,),
        "A ball is in flight near Earth after leaving the hand. Neglect air resistance. It remains above the ground throughout the shown interval. Its initial velocity is not supplied."),
)
CASE_BY_ID = {c.id: c for c in CASES}


@dataclass(frozen=True)
class MotionHistory:
    id: str
    v0: int
    acceleration: int

    @property
    def positions(self):
        return tuple(self.v0 * t + .5 * self.acceleration * t * t for t in range(4))

    def description(self, axis):
        positive, negative = ("right", "left") if axis == "horizontal" else ("upward", "downward")
        if self.v0 == self.acceleration == 0:
            return "Remains at rest"
        direction = positive if (self.v0 or self.acceleration) > 0 else negative
        if self.acceleration == 0:
            return f"Moves {direction} at constant speed"
        if self.v0 == 0:
            return f"Starts from rest, then speeds up {direction}"
        return f"Moves {direction}, {'speeding up' if self.v0 * self.acceleration > 0 else 'slowing down'}"


MOTIONS = (
    MotionHistory("rest", 0, 0), MotionHistory("coast_positive", 2, 0), MotionHistory("coast_negative", -2, 0),
    MotionHistory("speed_positive", 1, 1), MotionHistory("slow_negative", -5, 1), MotionHistory("start_positive", 0, 1),
    MotionHistory("speed_negative", -1, -1), MotionHistory("slow_positive", 5, -1), MotionHistory("start_negative", 0, -1),
)


def compatible(case, motion):
    return ((motion.acceleration > 0) - (motion.acceleration < 0)) == case.acceleration_sign


def available_cases(context):
    if context not in PRACTICE_SETS:
        raise ValueError("Unknown context")
    return tuple(c for c in CASES if context == "All situations" or c.category == context)


def make_options(case, rng=None):
    rng = rng or random
    correct = [m for m in MOTIONS if compatible(case, m)]
    wrong = [m for m in MOTIONS if not compatible(case, m)]
    result = correct + rng.sample(wrong, 1)
    rng.shuffle(result)
    return result


def check_motion_set(case, options, selected):
    selected = tuple(sorted(selected))
    if len(selected) != len(set(selected)) or any(type(i) is not int or not 0 <= i < len(options) for i in selected):
        raise ValueError("Invalid motion selection")
    expected = {i for i, m in enumerate(options) if compatible(case, m)}
    return {"correct": set(selected) == expected, "selected": selected,
            "missing": tuple(sorted(expected - set(selected))), "extra": tuple(sorted(set(selected) - expected))}


def new_attempt(case_id):
    if case_id not in CASE_BY_ID:
        raise ValueError("Unknown case")
    return {"case_id": case_id, "options": make_options(CASE_BY_ID[case_id]), "selection": (),
            "checks": [], "completed": False, "hint_used": False, "outcome": None}


def submit_attempt(attempt):
    if attempt["completed"]:
        return False
    result = check_motion_set(CASE_BY_ID[attempt["case_id"]], attempt["options"], attempt["selection"])
    if attempt["checks"] and result["selected"] == attempt["checks"][-1]["selected"]:
        return False
    attempt["checks"].append(result)
    if result["correct"]:
        attempt["completed"] = True
        attempt["outcome"] = ("Completed with help" if attempt["hint_used"] else
                              "First try" if len(attempt["checks"]) == 1 else "Corrected after feedback")
    return True


def explanation(case):
    direction = ("right" if case.axis == "horizontal" else "upward") if case.acceleration_sign > 0 else ("left" if case.axis == "horizontal" else "downward")
    if case.acceleration_sign == 0:
        return "The forces balance, so acceleration is zero. Rest and constant velocity in either direction are all possible."
    return f"The net force and acceleration point {direction}. The object could speed up in that direction, slow down while moving the opposite way, or start from rest. Force does not uniquely determine velocity."


def render_motion(motion, axis):
    from matplotlib.figure import Figure
    fig = Figure(figsize=(3.4, 2.6), dpi=130)
    ax = fig.subplots()
    try:
        positions = motion.positions
        lo, hi = min(positions), max(positions)
        span = max(2, hi - lo)
        ax.axis("off")
        vertical = axis == "vertical"
        if vertical:
            ax.set(xlim=(-1, 1), ylim=(lo - span * .24, hi + span * .24))
        else:
            ax.set(xlim=(lo - span * .14, hi + span * .14), ylim=(-1, 1))
        if len(set(positions)) == 1:
            ax.plot(0, 0, "o", color="#176b9b", markersize=10)
            ax.annotate("1–4: same position", (0, 0), xytext=(0, -22), textcoords="offset points", ha="center", fontsize=9)
        else:
            for i, p in enumerate(positions, 1):
                xy = (0, p) if vertical else (p, 0)
                ax.plot(*xy, "o", color="#176b9b", markersize=8)
                ax.annotate(str(i), xy, xytext=(12, 0) if vertical else (0, -16),
                            textcoords="offset points", ha="left" if vertical else "center", va="center", fontsize=10)
        ax.set_title(motion.description(axis), fontsize=10, color="#173f56", wrap=True)
        fig.text(.02, .015, "Up ↑" if vertical else "Left ←                         → Right", fontsize=9, color="#173f56")
        fig.subplots_adjust(left=.05, right=.95, bottom=.16, top=.78)
        buffer = BytesIO()
        fig.savefig(buffer, format="png", facecolor="white")
        return buffer.getvalue()
    finally:
        fig.clear()

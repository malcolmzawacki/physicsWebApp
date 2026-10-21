"""C3: change one horizontal interaction to achieve a requested motion change."""
from dataclasses import dataclass
from io import BytesIO
import random

PRACTICE_SETS = ("All situations", "Start moving", "Change speed", "Change acceleration")


@dataclass(frozen=True)
class ForceState:
    push: int
    pull: int

    def __post_init__(self):
        if any(type(v) is not int or v not in range(4) for v in (self.push, self.pull)):
            raise ValueError("Force levels must be integers from zero to three")

    @property
    def net(self):
        return 10 * (self.push - self.pull)

    @property
    def description(self):
        return f"Push: {self.push * 10} N right; rope pull: {self.pull * 10} N left; weight: 20 N down; normal: 20 N up. Zero means that horizontal interaction is absent."


@dataclass(frozen=True)
class ChangeCase:
    id: str
    title: str
    category: str
    initial: ForceState
    motion: str
    request: str
    target: str


CASES = (
    ChangeCase("start_right", "Start right from balanced pushes", "Start moving", ForceState(1, 1), "The cart is at rest.", "Make the cart begin moving right.", "positive"),
    ChangeCase("start_left", "Start left from balanced pushes", "Start moving", ForceState(1, 1), "The cart is at rest.", "Make the cart begin moving left.", "negative"),
    ChangeCase("add_push", "Add a push", "Start moving", ForceState(0, 0), "The cart is at rest with no horizontal forces.", "Make the cart begin moving right by adding one interaction.", "positive"),
    ChangeCase("add_rope", "Add a rope pull", "Start moving", ForceState(0, 0), "The cart is at rest with no horizontal forces.", "Make the cart begin moving left by adding one interaction.", "negative"),
    ChangeCase("coast_right", "Keep moving right without speeding up", "Change speed", ForceState(2, 1), "The cart is moving right and speeding up.", "Make the cart continue right at constant speed.", "zero"),
    ChangeCase("coast_left", "Keep moving left without speeding up", "Change speed", ForceState(1, 2), "The cart is moving left and speeding up.", "Make the cart continue left at constant speed.", "zero"),
    ChangeCase("slow_right", "Slow the rightward cart", "Change speed", ForceState(2, 1), "The cart is moving right and speeding up.", "Make the cart slow down while it is still moving right.", "negative"),
    ChangeCase("slow_left", "Slow the leftward cart", "Change speed", ForceState(1, 2), "The cart is moving left and speeding up.", "Make the cart slow down while it is still moving left.", "positive"),
    ChangeCase("faster_right", "Increase rightward acceleration", "Change acceleration", ForceState(2, 1), "The cart is moving right and speeding up.", "Make the cart speed up rightward at a greater rate than before.", "more_positive"),
    ChangeCase("faster_left", "Increase leftward acceleration", "Change acceleration", ForceState(1, 2), "The cart is moving left and speeding up.", "Make the cart speed up leftward at a greater rate than before.", "more_negative"),
)
CASE_BY_ID = {c.id: c for c in CASES}


def available_cases(context):
    if context not in PRACTICE_SETS:
        raise ValueError("Unknown practice set")
    return tuple(c for c in CASES if context == "All situations" or c.category == context)


def change_description(before, after):
    changed = [f for f in ("push", "pull") if getattr(before, f) != getattr(after, f)]
    if len(changed) != 1:
        raise ValueError("Exactly one interaction must change")
    force = changed[0]
    old, new = getattr(before, force), getattr(after, force)
    name = "rightward push" if force == "push" else "leftward rope pull"
    if not new:
        return f"Remove the {name} ({old * 10} N to 0 N)."
    if not old:
        return f"Add a {new * 10} N {name}."
    return f"{'Increase' if new > old else 'Reduce'} the {name} from {old * 10} N to {new * 10} N."


def accepted(case, after):
    changed = sum(getattr(case.initial, f) != getattr(after, f) for f in ("push", "pull"))
    if changed != 1:
        return False
    return {"positive": after.net > 0, "negative": after.net < 0, "zero": after.net == 0,
            "more_positive": after.net > case.initial.net,
            "more_negative": after.net < case.initial.net}[case.target]


def make_options(case, rng=None):
    options = [ForceState(level, case.initial.pull) for level in range(4) if level != case.initial.push]
    options += [ForceState(case.initial.push, level) for level in range(4) if level != case.initial.pull]
    rng = rng or random
    correct = [option for option in options if accepted(case, option)]
    wrong = [option for option in options if not accepted(case, option)]
    result = correct + rng.sample(wrong, 4 - len(correct))
    rng.shuffle(result)
    return result


def check_changes(case, options, selected):
    selected = tuple(sorted(selected))
    if len(selected) != len(set(selected)) or any(type(i) is not int or not 0 <= i < len(options) for i in selected):
        raise ValueError("Invalid selection")
    expected = {i for i, after in enumerate(options) if accepted(case, after)}
    return {"correct": set(selected) == expected, "selected": selected,
            "missing": tuple(sorted(expected - set(selected))), "extra": tuple(sorted(set(selected) - expected))}


def new_attempt(case_id):
    case = CASE_BY_ID[case_id]
    return {"case_id": case_id, "options": make_options(case), "selection": (),
            "checks": [], "hint_used": False, "completed": False, "outcome": None}


def submit_attempt(attempt):
    if attempt["completed"]:
        return False
    result = check_changes(CASE_BY_ID[attempt["case_id"]], attempt["options"], attempt["selection"])
    if attempt["checks"] and result["selected"] == attempt["checks"][-1]["selected"]:
        return False
    attempt["checks"].append(result)
    if result["correct"]:
        attempt["completed"] = True
        attempt["outcome"] = ("Completed with help" if attempt["hint_used"] else
                              "First try" if len(attempt["checks"]) == 1 else "Corrected after feedback")
    return True


def explanation(case):
    return {"positive": "Beginning rightward motion or slowing a leftward cart requires net force to the right.",
            "negative": "Beginning leftward motion or slowing a rightward cart requires net force to the left.",
            "zero": "Constant velocity requires balanced forces. Removing acceleration does not instantly remove velocity.",
            "more_positive": "With unchanged mass, greater rightward net force produces greater rightward acceleration.",
            "more_negative": "With unchanged mass, greater leftward net force produces greater leftward acceleration."}[case.target]


def render_change_diagram(state):
    from matplotlib.figure import Figure
    from matplotlib.patches import Circle
    fig = Figure(figsize=(3.5, 3), dpi=130)
    ax = fig.subplots()
    try:
        ax.set(xlim=(-3.2, 3.2), ylim=(-2.4, 2.4), aspect="equal")
        ax.axis("off")
        arrows = [(0, 1.4, "Normal 20 N"), (0, -1.4, "Weight 20 N")]
        if state.push:
            arrows.append((state.push * .7, 0, f"Push {state.push * 10} N"))
        if state.pull:
            arrows.append((-state.pull * .7, 0, f"Rope {state.pull * 10} N"))
        for x, y, label in arrows:
            ax.annotate("", xy=(x, y), xytext=(0, 0),
                        arrowprops={"arrowstyle":"-|>", "color":"#176b9b", "lw":2.7, "mutation_scale":17})
            if y:
                ax.text(.17, y, label, va="center", fontsize=10, color="#173f56")
            else:
                ax.text(.25 if x > 0 else -.25, .28 if x > 0 else -.28, label, ha="left" if x > 0 else "right",
                        va="bottom" if x > 0 else "top", fontsize=10, color="#173f56")
        ax.add_patch(Circle((0, 0), .14, color="#173f56"))
        fig.subplots_adjust(left=.01, right=.99, bottom=.04, top=.98)
        buffer = BytesIO()
        fig.savefig(buffer, format="png", facecolor="white")
        return buffer.getvalue()
    finally:
        fig.clear()

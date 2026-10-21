"""C10 exact force/acceleration values, controlled boards, and tied ranking."""
from dataclasses import dataclass
from fractions import Fraction
from io import BytesIO
import random

QUANTITIES = ("Net force", "Acceleration")
COMPARISONS = ("Magnitude (size only)", "Signed horizontal value")
MASS_PATTERNS = ("Equal masses", "Different masses")


@dataclass(frozen=True)
class RankCase:
    push: int
    pull: int
    mass: int

    def __post_init__(self):
        if any(type(v) is not int or v < 0 or v > 60 or v % 10 for v in (self.push, self.pull)):
            raise ValueError("Horizontal forces must be 0–60 N in 10 N steps")
        if type(self.mass) is not int or self.mass not in range(1, 5):
            raise ValueError("Mass must be 1–4 kg")

    @property
    def net(self):
        return self.push - self.pull

    @property
    def acceleration(self):
        return Fraction(self.net, self.mass)

    @property
    def description(self):
        return f"Mass {self.mass} kg; push {self.push} N right; rope {self.pull} N left; weight {10*self.mass} N down; normal {10*self.mass} N up."


def ranking_value(case, quantity, comparison):
    if quantity not in QUANTITIES or comparison not in COMPARISONS:
        raise ValueError("Unknown ranking mode")
    value = Fraction(case.net) if quantity == "Net force" else case.acceleration
    return abs(value) if comparison == COMPARISONS[0] else value


def make_board(quantity, comparison, masses, ties, rng=None):
    """Four distinct physical cases; optional ties and mass variation are guaranteed."""
    if masses not in MASS_PATTERNS or type(ties) is not bool:
        raise ValueError("Unknown mass/tie setting")
    rng = rng or random
    mass_values = (rng.randint(1,4),) if masses == MASS_PATTERNS[0] else range(1,5)
    groups = {}
    for mass in mass_values:
        for push in range(0,61,10):
            for pull in range(0,61,10):
                case = RankCase(push,pull,mass)
                groups.setdefault(ranking_value(case,quantity,comparison),[]).append(case)
    if masses == MASS_PATTERNS[1]:
        # Every available value can be realized with two masses, so a varied board
        # can be constructed directly without retries or an unbounded rejection loop.
        groups = {v: cases for v,cases in groups.items() if len({c.mass for c in cases}) >= 2}
    if ties:
        tied_value = rng.choice([v for v,cases in groups.items() if len(cases) >= 2])
        first = rng.choice(groups[tied_value])
        second = rng.choice([c for c in groups[tied_value] if c != first and
                             (masses == MASS_PATTERNS[0] or c.mass != first.mass)])
        values = rng.sample([v for v in groups if v != tied_value], 2)
        cases = [first, second, *[rng.choice(groups[v]) for v in values]]
    else:
        values = rng.sample(list(groups),4)
        cases = []
        for i,v in enumerate(values):
            choices = groups[v]
            if i == 1 and masses == MASS_PATTERNS[1]:
                choices = [c for c in choices if c.mass != cases[0].mass]
            cases.append(rng.choice(choices))
    rng.shuffle(cases)
    return tuple(cases)


def expected_groups(cases, quantity, comparison):
    groups = {}
    for i,case in enumerate(cases):
        groups.setdefault(ranking_value(case,quantity,comparison),[]).append(i)
    return tuple(tuple(groups[v]) for v in sorted(groups,reverse=True))


def ranking_text(groups):
    return " > ".join(" = ".join(chr(65+i) for i in group) for group in groups)


def check_ranking(cases, ranks, quantity, comparison):
    if len(ranks) != len(cases) or any(type(r) is not int or not 1 <= r <= len(cases) for r in ranks):
        raise ValueError("Choose one rank from 1 to the number of cases for each case")
    values = [ranking_value(c,quantity,comparison) for c in cases]
    feedback = []
    if min(ranks) != 1:
        feedback.append("Start the greatest value or tied group at rank 1.")
    for i in range(len(cases)):
        for j in range(i+1,len(cases)):
            correct_relation = (values[i] > values[j]) - (values[i] < values[j])
            entered_relation = (ranks[i] < ranks[j]) - (ranks[i] > ranks[j])
            if correct_relation != entered_relation:
                a,b = chr(65+i),chr(65+j)
                relation = "equal to" if correct_relation == 0 else "greater than" if correct_relation > 0 else "less than"
                feedback.append(f"{a}'s {quantity.lower()} value should be {relation} {b}'s.")
    return {"correct": not feedback, "ranks": tuple(ranks), "feedback": tuple(feedback),
            "groups": expected_groups(cases,quantity,comparison)}


def new_attempt(quantity, comparison, masses, ties):
    return {"settings": (quantity,comparison,masses,ties), "cases": make_board(quantity,comparison,masses,ties),
            "draft": (None,)*4, "checks": [], "hint_used": False, "completed": False, "outcome": None}


def submit_attempt(attempt, ranks):
    if attempt["completed"]:
        return False
    quantity,comparison,_,_ = attempt["settings"]
    result = check_ranking(attempt["cases"],ranks,quantity,comparison)
    if attempt["checks"] and attempt["checks"][-1]["ranks"] == result["ranks"]:
        return False
    attempt["draft"] = tuple(ranks)
    attempt["checks"].append(result)
    if result["correct"]:
        attempt["completed"] = True
        attempt["outcome"] = ("Completed with help" if attempt["hint_used"] else
                              "First try" if len(attempt["checks"]) == 1 else "Corrected after feedback")
    return True


def render_rank_diagram(case, scale):
    from matplotlib.figure import Figure
    from matplotlib.patches import Circle
    if scale < max(case.push,case.pull,10*case.mass) or scale <= 0:
        raise ValueError("Use a shared scale large enough for every force")
    fig = Figure(figsize=(3.4,2.8),dpi=130)
    ax = fig.subplots()
    try:
        ax.set(xlim=(-2.7,2.7),ylim=(-2.7,2.7),aspect="equal")
        ax.axis("off")
        forces=[(case.push,1,0,"P"),(case.pull,-1,0,"T"),(10*case.mass,0,1,"N"),(10*case.mass,0,-1,"W")]
        for force,dx,dy,symbol in forces:
            if force == 0:
                continue
            x,y=2.05*force/scale*dx,2.05*force/scale*dy
            ax.annotate("",xy=(x,y),xytext=(0,0),arrowprops={"arrowstyle":"-|>","color":"#176b9b","lw":2.5,"mutation_scale":14})
            ax.text(x+.19*dx+(0 if dx else .15),y+.19*dy,symbol,
                    ha="left" if dx >= 0 else "right",va="center",fontsize=11,color="#173f56",weight="bold")
        ax.add_patch(Circle((0,0),.11,color="#173f56"))
        fig.text(.5,.05,f"P = {case.push} N right     T = {case.pull} N left",ha="center",fontsize=9,color="#173f56")
        fig.text(.5,.95,f"Mass: {case.mass} kg",ha="center",va="top",fontsize=12,color="#173f56")
        fig.subplots_adjust(left=.02,right=.98,bottom=.17,top=.86)
        buffer=BytesIO();fig.savefig(buffer,format="png",facecolor="white")
        return buffer.getvalue()
    finally:
        fig.clear()

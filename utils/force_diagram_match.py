"""Original C5 cases, qualitative diagram equivalence, and shared force artwork."""
from dataclasses import dataclass, replace
from io import BytesIO
import random

from utils.recognizing_forces import FORCE_LABELS, SCENARIO_BY_ID


@dataclass(frozen=True)
class ForceArrow:
    force: str
    direction: str
    size: int = 1


@dataclass(frozen=True)
class DiagramCase:
    id: str
    arrows: tuple[ForceArrow, ...]
    explanation: str
    clarification: str = ""

    @property
    def scenario(self):
        return SCENARIO_BY_ID[self.id]

    @property
    def prompt(self):
        return self.scenario.situation + (" " + self.clarification if self.clarification else "")


G = ForceArrow("gravity", "down")
N = ForceArrow("normal", "up")
CASES = (
    DiagramCase("book_rest", (G, N), "The desk's normal force balances the book's weight. Rest does not mean no forces."),
    DiagramCase("book_push", (G, N, ForceArrow("applied", "right"), ForceArrow("friction", "left")),
        "At rest, the horizontal push and static friction balance; normal force and weight also balance.",
        "The hand pushes to the right. Compare opposing forces along each axis; vertical and horizontal force sizes need not match."),
    DiagramCase("puck_coast", (G, N), "The puck coasts with balanced vertical forces and no horizontal force. The stick no longer acts on it."),
    DiagramCase("crate_slide", (G, N, ForceArrow("friction", "left")),
        "Weight and normal force balance vertically. Friction points left, opposing the rightward sliding motion."),
    DiagramCase("lamp_hang", (G, ForceArrow("tension", "up")),
        "The cable pulls upward with tension equal to the lamp's downward weight."),
    DiagramCase("bucket_lift", (G, ForceArrow("tension", "up", 2)),
        "Upward acceleration requires upward tension greater than downward weight. The person's hand does not directly touch the bucket.",
        "At this instant the rope is vertical and the bucket is speeding up as it moves upward."),
    DiagramCase("spring_hang", (G, ForceArrow("spring", "up")),
        "The stretched spring pulls upward, balancing weight. This is spring force, not rope tension."),
    DiagramCase("spring_cart", (G, N, ForceArrow("spring", "left")),
        "Normal force balances weight; the stretched spring pulls toward its anchor on the left. The hand has released the cart.",
        "The spring's fixed anchor is to the left of the cart."),
    DiagramCase("ball_rise", (G,),
        "After release, gravity points downward even while the ball travels upward. There is no continuing force from the hand."),
    DiagramCase("skydiver", (G, ForceArrow("drag", "up")),
        "Constant downward speed means zero acceleration: upward drag balances downward weight."),
)
CASE_BY_ID = {case.id: case for case in CASES}
DIRECTIONS = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}
OPPOSITE = {"up": "down", "down": "up", "left": "right", "right": "left"}
SHORT_LABELS = {"gravity": "Weight", "normal": "Normal", "friction": "Friction",
                "applied": "Applied", "tension": "Tension", "spring": "Spring", "drag": "Drag"}


def available_cases(context):
    from utils.recognizing_forces import PRACTICE_SETS
    if context not in PRACTICE_SETS:
        raise ValueError("Unknown context")
    return tuple(c for c in CASES if context == "All contexts" or c.scenario.context == context)


def diagram_signature(arrows):
    """Compare identity/direction and relative sizes on one axis, not pixel lengths.

    No case promises an exact numeric ratio or a comparison between axes.
    """
    by_force = {a.force: a for a in arrows}
    if len(by_force) != len(arrows):
        raise ValueError("Repeated force type")
    if any(a.force not in FORCE_LABELS or a.direction not in DIRECTIONS or a.size <= 0 for a in arrows):
        raise ValueError("Invalid force arrow")
    ordering = []
    ordered = sorted(arrows, key=lambda a: a.force)
    for i, a in enumerate(ordered):
        for b in ordered[i + 1:]:
            if (DIRECTIONS[a.direction][0] == 0) == (DIRECTIONS[b.direction][0] == 0):
                ordering.append((a.force, b.force, (a.size > b.size) - (a.size < b.size)))
    return tuple((a.force, a.direction) for a in ordered), tuple(ordering)


def diagram_matches(case, arrows):
    return diagram_signature(case.arrows) == diagram_signature(arrows)


def make_options(case, rng=None):
    """One defensible answer, shuffled with three deliberate misconception choices."""
    arrows = case.arrows
    missing = tuple(a for a in arrows if a.force != "gravity")
    pivot = next((a for a in arrows if a.force != "gravity"), G)
    reversed_arrow = tuple(replace(a, direction=OPPOSITE[a.direction]) if a == pivot else a for a in arrows)
    if len(arrows) == 1:
        changed_size = (*arrows, ForceArrow("applied", "up"))
        size_feedback = "The hand has lost contact. Upward motion does not imply an upward applied force."
    else:
        pivot = next((a for a in arrows if a.force == "applied"),
                     next(a for a in arrows if a.direction == "up"))
        changed_size = tuple(replace(a, size=1 if a.size == 2 else 2) if a == pivot else a for a in arrows)
        size_feedback = "Compare the opposing arrow lengths with the stated acceleration or state of rest. " + case.explanation
    options = [
        {"arrows": arrows, "feedback": case.explanation},
        {"arrows": missing, "feedback": "Gravity still acts on this object near Earth. The diagram is missing its downward weight."},
        {"arrows": reversed_arrow, "feedback": "One force points in the wrong direction. " + case.explanation},
        {"arrows": changed_size, "feedback": size_feedback},
    ]
    (rng or random).shuffle(options)
    return options


def describe_diagram(arrows):
    if not arrows:
        return "No force arrows."
    forces = "; ".join(f"{SHORT_LABELS[a.force]} {a.direction}, length {a.size}" for a in arrows)
    return forces + ". Lengths are relative, not measurements."


def render_force_diagram(arrows):
    """Return a closed, white-background PNG; no external image assets needed."""
    from matplotlib.figure import Figure
    from matplotlib.patches import Circle
    fig = Figure(figsize=(3.2, 2.7), dpi=180)
    ax = fig.subplots()
    try:
        ax.set(xlim=(-2.6, 2.6), ylim=(-2.35, 2.35), aspect="equal")
        ax.axis("off")
        for arrow in arrows:
            dx, dy = DIRECTIONS[arrow.direction]
            parallel = [a for a in arrows if a.direction == arrow.direction]
            offset = (parallel.index(arrow) - (len(parallel) - 1) / 2) * .28
            ox, oy = (offset, 0) if dy else (0, offset)
            length = 1.05 if arrow.size == 1 else 1.75
            x, y = dx * length + ox, dy * length + oy
            ax.annotate("", xy=(x, y), xytext=(ox, oy),
                        arrowprops={"arrowstyle": "-|>", "color": "#176b9b", "lw": 2.7, "mutation_scale": 17})
            if dx:
                ax.text(x / 2, -.33, SHORT_LABELS[arrow.force], ha="center", va="top", fontsize=11, color="#152f41")
            else:
                label_x = -.34 if ox < 0 else .34
                ax.text(label_x, y, SHORT_LABELS[arrow.force], ha="right" if ox < 0 else "left", va="center", fontsize=11, color="#152f41")
        ax.add_patch(Circle((0, 0), .16, color="#152f41"))
        if not arrows:
            ax.text(0, -.55, "No forces", ha="center", fontsize=10, color="#152f41")
        fig.subplots_adjust(left=.02, right=.98, top=.98, bottom=.02)
        buffer = BytesIO()
        fig.savefig(buffer, format="png", facecolor="white")
        return buffer.getvalue()
    finally:
        fig.clear()

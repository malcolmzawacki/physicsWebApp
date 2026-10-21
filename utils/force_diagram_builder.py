"""I2 qualitative diagram construction and category-specific physical feedback."""
from dataclasses import asdict
from io import BytesIO

from utils.force_diagram_match import CASE_BY_ID, DIRECTIONS, ForceArrow, OPPOSITE
from utils.recognizing_forces import FORCE_LABELS, check_forces

SIZE_LABELS = {1: "Short", 2: "Medium", 3: "Long"}
SYMBOLS = {"gravity": "W", "normal": "N", "friction": "f", "tension": "T",
           "applied": "P", "spring": "S", "drag": "D"}


def validate_arrows(arrows):
    if len({a.force for a in arrows}) != len(arrows):
        raise ValueError("Use one arrow per force type")
    if any(a.force not in FORCE_LABELS or a.direction not in DIRECTIONS
           or type(a.size) is not int or a.size not in SIZE_LABELS for a in arrows):
        raise ValueError("Invalid force, direction, or relative size")


def check_builder(case, arrows):
    """Check interactions first, then directions and compatible size relations.

    Relations only compare opposite expected forces along one axis. Arrow lengths
    on different axes and exact ratios are never constraints in this pilot.
    """
    validate_arrows(arrows)
    presence = check_forces(case.scenario, [a.force for a in arrows])
    actual = {a.force: a for a in arrows}
    wrong_directions = tuple(
        f"{FORCE_LABELS[a.force]} should point {a.direction}."
        for a in case.arrows if a.force in actual and actual[a.force].direction != a.direction)
    relations = []
    deferred = False
    for i, a in enumerate(case.arrows):
        for b in case.arrows[i + 1:]:
            if OPPOSITE[a.direction] != b.direction:
                continue
            if any(c.force not in actual or actual[c.force].direction != c.direction for c in (a, b)):
                deferred = True
                continue
            compare = lambda x, y: (x > y) - (x < y)
            if compare(a.size, b.size) != compare(actual[a.force].size, actual[b.force].size):
                relationship = "the same length as" if a.size == b.size else "longer than" if a.size > b.size else "shorter than"
                relations.append(f"The {FORCE_LABELS[a.force]} arrow should be {relationship} the {FORCE_LABELS[b.force]} arrow.")
    return {"correct": presence["correct"] and not wrong_directions and not relations,
            "forces_ok": presence["correct"], "force_feedback": presence["feedback"],
            "direction_feedback": wrong_directions, "size_feedback": tuple(relations),
            "size_deferred": deferred,
            "arrows": tuple(sorted(arrows, key=lambda a: a.force))}


def new_builder_attempt(case_id):
    if case_id not in CASE_BY_ID:
        raise ValueError("Unknown case")
    return {"case_id": case_id, "draft": [], "checks": [], "hint_used": False,
            "completed": False, "outcome": None}


def submit_builder(attempt, arrows):
    if attempt["completed"]:
        return False
    result = check_builder(CASE_BY_ID[attempt["case_id"]], arrows)
    if attempt["checks"] and attempt["checks"][-1]["arrows"] == result["arrows"]:
        return False
    attempt["checks"].append({**result, "hint_used": attempt["hint_used"]})
    attempt["draft"] = [asdict(a) for a in arrows]
    if result["correct"]:
        attempt["completed"] = True
        attempt["outcome"] = ("Completed with help" if attempt["hint_used"] else
                              "First try" if len(attempt["checks"]) == 1 else "Corrected after feedback")
    return True


def describe_builder(arrows):
    if not arrows:
        return "No force arrows."
    return "; ".join(f"{FORCE_LABELS[a.force]}: {a.direction}, {SIZE_LABELS[a.size].lower()}" for a in arrows)


def render_builder_diagram(arrows):
    """Render up to seven independently labeled cardinal arrows without overlaps.

    The central box expands only to give same-direction arrows distinct attachment
    points; its size has no physical meaning. Relative arrow lengths remain fixed.
    """
    from matplotlib.figure import Figure
    from matplotlib.patches import Rectangle
    validate_arrows(arrows)
    groups = {d: [a for a in arrows if a.direction == d] for d in DIRECTIONS}
    width = .48 + .34 * (max(1, len(groups["up"]), len(groups["down"])) - 1)
    height = .36 + .34 * (max(1, len(groups["left"]), len(groups["right"])) - 1)
    extent = max(width / 2, height / 2) + 2.25
    fig = Figure(figsize=(4.6, 4.0), dpi=130)
    ax = fig.subplots()
    try:
        ax.set(xlim=(-extent, extent), ylim=(-extent, extent), aspect="equal")
        ax.axis("off")
        ax.add_patch(Rectangle((-width / 2, -height / 2), width, height,
                               facecolor="#dce9f1", edgecolor="#173f56", lw=1.5))
        for arrow in arrows:
            dx, dy = DIRECTIONS[arrow.direction]
            group = groups[arrow.direction]
            offset = (group.index(arrow) - (len(group) - 1) / 2) * .34
            ox, oy = (offset, dy * height / 2) if dy else (dx * width / 2, offset)
            length = {1: .75, 2: 1.25, 3: 1.75}[arrow.size]
            x, y = ox + dx * length, oy + dy * length
            ax.annotate("", xy=(x, y), xytext=(ox, oy),
                        arrowprops={"arrowstyle": "-|>", "color": "#176b9b", "lw": 3, "mutation_scale": 18})
            ax.text(x + dx * .16, y + dy * .16, SYMBOLS[arrow.force],
                    ha="center" if dy else "left" if dx > 0 else "right",
                    va="bottom" if dy > 0 else "top" if dy < 0 else "center",
                    fontsize=13, weight="bold", color="#173f56")
        if not arrows:
            ax.text(0, -.65, "Add forces to build your diagram", ha="center", fontsize=11, color="#173f56")
        fig.subplots_adjust(left=.01, right=.99, top=.99, bottom=.01)
        buffer = BytesIO()
        fig.savefig(buffer, format="png", facecolor="white")
        return buffer.getvalue()
    finally:
        fig.clear()

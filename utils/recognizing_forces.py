"""Original, bounded force-identification content and retryable set checking.

This is conceptual content, not a numerical generator or a dynamics solver.
Each interaction names an agent exerting a force on the target object.
"""
from dataclasses import dataclass


FORCE_LABELS = {
    "gravity": "Gravity (weight)",
    "normal": "Normal force (surface support)",
    "friction": "Friction (along a solid surface)",
    "tension": "Tension (rope or cable)",
    "applied": "Applied force (direct push or pull)",
    "spring": "Spring force",
    "drag": "Drag (air resistance)",
}
ABSENT_REASONS = {
    "gravity": "We ignore gravity in this model.",
    "normal": "No solid surface is pressing on the object.",
    "friction": "There is no rough solid contact producing friction in this situation.",
    "tension": "No taut rope or cable is pulling on the object.",
    "applied": "No person or device is directly pushing or pulling on the object now.",
    "spring": "No stretched or compressed spring is acting on the object.",
    "drag": "Air resistance is ignored or there is no relative motion through air.",
}
PRACTICE_SETS = ("All contexts", "Surfaces", "Ropes", "Springs", "Flight")


@dataclass(frozen=True)
class ForceScenario:
    id: str
    title: str
    context: str
    target: str
    situation: str
    interactions: tuple[tuple[str, str], ...]
    hint: str
    related: str

    @property
    def forces(self) -> frozenset[str]:
        return frozenset(force for force, _ in self.interactions)


SCENARIOS = (
    ForceScenario("book_rest", "Book on a desk", "Surfaces", "the book",
        "A book rests on a horizontal desk near Earth's surface. Nothing pushes or pulls it sideways. Ignore air forces.",
        (("gravity", "Earth pulls the book downward."), ("normal", "The desk presses upward on the book.")),
        "An object at rest can still interact with Earth and a supporting surface.", "book_push"),
    ForceScenario("book_push", "Book held in place", "Surfaces", "the book",
        "A hand pushes a book horizontally on a rough, horizontal desk near Earth's surface. The book stays at rest because static friction opposes the push. Ignore air forces.",
        (("gravity", "Earth pulls the book downward."), ("normal", "The desk presses upward on the book."),
         ("applied", "The hand pushes directly on the book."), ("friction", "Static friction from the desk opposes the hand's push, even though the book is at rest.")),
        "List the agents touching the book. Static friction can act without sliding.", "book_rest"),
    ForceScenario("puck_coast", "Puck coasting", "Surfaces", "the puck",
        "After a stick has lost contact, a puck glides right on horizontal ice near Earth's surface. Model the ice as frictionless and ignore air resistance. No rope or spring is attached.",
        (("gravity", "Earth pulls the puck downward."), ("normal", "The ice presses upward on the puck.")),
        "The stick no longer touches the puck. Motion does not require a continuing forward force.", "crate_slide"),
    ForceScenario("crate_slide", "Crate slowing down", "Surfaces", "the crate",
        "A crate slides right on a rough, horizontal floor near Earth's surface after a person lets go. Kinetic friction slows it. Ignore air resistance; no rope or spring is attached.",
        (("gravity", "Earth pulls the crate downward."), ("normal", "The floor presses upward on the crate."),
         ("friction", "The rough floor exerts kinetic friction on the sliding crate.")),
        "The person has let go. Which interactions continue while the crate slides?", "puck_coast"),
    ForceScenario("lamp_hang", "Hanging lamp", "Ropes", "the lamp",
        "A lamp hangs at rest from a taut cable near Earth's surface. It touches no wall or floor. Ignore air forces.",
        (("gravity", "Earth pulls the lamp downward."), ("tension", "The taut cable pulls upward on the lamp.")),
        "A cable supports by pulling. It is not a supporting surface underneath the lamp.", "bucket_lift"),
    ForceScenario("bucket_lift", "Bucket being lifted", "Ropes", "the bucket",
        "A person lifts a bucket using a taut rope near Earth's surface. The bucket is above the ground and the person touches only the rope. Ignore air resistance.",
        (("gravity", "Earth pulls the bucket downward."), ("tension", "The rope pulls on the bucket. The person's hand acts on the rope, not directly on the bucket.")),
        "Focus on the bucket: the hand touches the rope, and the rope touches the bucket.", "lamp_hang"),
    ForceScenario("spring_hang", "Mass on a spring", "Springs", "the mass",
        "A mass hangs at rest directly from a stretched vertical spring near Earth's surface. It touches no other objects. Ignore air forces.",
        (("gravity", "Earth pulls the mass downward."), ("spring", "The stretched spring pulls upward on the mass; classify this as spring force rather than rope tension.")),
        "Identify the elastic object supporting the mass. Use the most specific force label.", "spring_cart"),
    ForceScenario("spring_cart", "Cart released from a spring", "Springs", "the cart",
        "A cart on a frictionless horizontal track near Earth's surface is attached directly to a stretched horizontal spring. A hand has just released the cart; the spring is still stretched. Ignore air resistance.",
        (("gravity", "Earth pulls the cart downward."), ("normal", "The track presses upward on the cart."),
         ("spring", "The stretched spring pulls on the cart.")),
        "The spring still touches the cart, but the hand no longer does.", "spring_hang"),
    ForceScenario("ball_rise", "Ball after release", "Flight", "the ball",
        "A ball travels upward after leaving a thrower's hand near Earth's surface. It touches nothing. Ignore air resistance.",
        (("gravity", "Earth pulls the ball downward even while the ball moves upward."),),
        "The hand no longer touches the ball. Upward velocity is not an upward force.", "ball_drag"),
    ForceScenario("ball_drag", "Ball rising through air", "Flight", "the ball",
        "A ball travels upward through still air after leaving a thrower's hand near Earth's surface. Include air resistance. It touches no solid object.",
        (("gravity", "Earth pulls the ball downward."), ("drag", "Air pushes against the ball's upward motion, producing downward drag.")),
        "Compare this with a no-air model. The ball interacts with both Earth and moving air.", "ball_rise"),
    ForceScenario("skydiver", "Steady descent", "Flight", "the skydiver and equipment together",
        "A skydiver and equipment descend together at constant speed through still air near Earth's surface before the parachute opens. Include air resistance. Treat the person and equipment as one object; there is no external rope.",
        (("gravity", "Earth pulls the skydiver and equipment downward."), ("drag", "Air exerts upward drag. Constant speed means the forces balance, not that they disappear.")),
        "Zero net force can result from two nonzero forces that balance.", "ball_drag"),
    ForceScenario("probe_coast", "Probe coasting in space", "Flight", "the probe",
        "A probe coasts in empty space with its engine off. In this idealized model it is far enough from massive bodies to ignore gravity. There is no gas, contact, rope, or spring.",
        (), "Check for interactions, not motion. A coasting object can have no modeled forces.", "ball_rise"),
)
SCENARIO_BY_ID = {scenario.id: scenario for scenario in SCENARIOS}


def available_scenarios(context: str) -> tuple[ForceScenario, ...]:
    if context not in PRACTICE_SETS:
        raise ValueError(f"Unknown practice set: {context}")
    return tuple(s for s in SCENARIOS if context == "All contexts" or s.context == context)


def check_forces(scenario: ForceScenario, selected) -> dict:
    selected = frozenset(selected)
    if selected - FORCE_LABELS.keys():
        raise ValueError("Unknown force type")
    missing = scenario.forces - selected
    extra = selected - scenario.forces
    reasons = dict(scenario.interactions)
    return {"correct": not (missing or extra), "selected": tuple(sorted(selected)),
            "missing": tuple(f for f in FORCE_LABELS if f in missing),
            "extra": tuple(f for f in FORCE_LABELS if f in extra),
            "feedback": tuple(
                f"{FORCE_LABELS[f]}: {reasons[f] if f in missing else ABSENT_REASONS[f]}"
                for f in FORCE_LABELS if f in missing or f in extra)}


def new_attempt(scenario_id: str) -> dict:
    if scenario_id not in SCENARIO_BY_ID:
        raise ValueError("Unknown scenario")
    return {"scenario_id": scenario_id, "checks": [], "hint_used": False,
            "completed": False, "outcome": None, "last_result": None, "selection": ()}


def submit_attempt(attempt: dict, selected) -> dict:
    """Identical repeated checks and checks after completion cannot inflate scores."""
    if attempt["completed"]:
        return attempt
    result = check_forces(SCENARIO_BY_ID[attempt["scenario_id"]], selected)
    attempt["selection"] = result["selected"]
    if attempt["last_result"] == result:
        return attempt
    attempt["checks"].append({**result, "hint_used": attempt["hint_used"]})
    attempt["last_result"] = result
    if result["correct"]:
        attempt["completed"] = True
        attempt["outcome"] = (
            "Completed with help" if attempt["hint_used"] else
            "First try" if len(attempt["checks"]) == 1 else "Corrected after feedback")
    return attempt

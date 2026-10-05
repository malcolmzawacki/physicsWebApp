"""Rebuild a route-complete inventory without treating discovery as review.

Review decisions live separately in docs/organizing_help_reviews.json.
Run with --check to detect drift in the committed inventory.
"""
import ast
import inspect
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.validate_payloads import discover_generators

GENERATORS = {
    "Arithmetic": "ArithmeticGenerator", "Vector Practice": "VectorGenerator",
    "Relative Motion": "RelativeMotionGenerator", "Distance & Displacement": "DistDispGenerator",
    "Constant Motion": "ConstantMotionGenerator", "Accelerated Motion": "LinearMotionGenerator",
    "Types of Motion Graphs": "MotionGraphGenerator", "Projectiles": "ProjectileGenerator",
    "Rotational Kinematics": "RotationalMotionGenerator", "Torque": "TorqueGenerator",
    "Newton's Second Law": "ForceGenerator", "Center of Mass": "CenterOfMassGenerator",
    "Tension": "TensionGenerator", "Atwood Machines": "AtwoodGenerator", "Inclined Planes": "InclineGenerator",
    "Momentum": "MomentumGenerator", "Impulse": "ImpulseGenerator", "Collisions": "CollisionGenerator",
    "Types of Energy": "EnergyBasicsGenerator", "Conservation of Energy": "EnergyConservationGenerator",
    "Thermal Energy": "ThermalLossGenerator", "Friction and Distance": "ThermalWithFrictionGenerator",
    "Wave Properties": "WaveGenerator", "Harmonics": "WaveGenerator", "deciBel Scale": "WaveGenerator",
}
CUSTOM = {
    "Algebra": ["Step-by-step equation rearrangement (easy / medium / hard / extra_hard)"],
    "Scientific Notation": ["Scientific-notation expressions (easy / medium / hard)"],
    "Matching Motion Graphs": ["Position-Time First", "Velocity-Time First"],
    "Charging by Friction": ["Explorer", "Comparison Practice", "Ranking Logic Puzzle"],
    "Charging by Conduction": ["Contact charging (Easy: signs)", "Contact charging (Medium: signs and mechanism)", "Contact charging (Hard: signs, mechanism, and amounts)"],
    "Charging by Induction": ["Induction (Easy)", "Induction (Medium)", "Induction (Hard)"],
    "Compound Names Practice": ["Ionic naming", "Covalent naming", "Polyatomic naming (optional)"],
    "Compound Formula Explorer": ["Covalent Compound", "Ionic Compound (Monatomic)", "Ionic Compound (with Polyatomic Ion)"],
    "Stoichiometry Practice": ["Random", "Combustion", "Decomposition", "Synthesis", "Single Replacement", "Double Replacement"],
    "Stoichiometry Explorer": ["Molar Mass Calculator", "Balancing Equations", "Limiting Reagent"],
    "Roulette": ["Simulation (no problem-type selector)"],
    "Reverse Engineering": ["Planner (no problem-type selector)"],
}


def routes():
    tree = ast.parse((ROOT / "Home.py").read_text(encoding="utf-8-sig"))
    catalog = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "ACTIVITIES" for t in n.targets)))
    def walk(items, trail):
        for name, entry in items.items():
            if "items" in entry:
                yield from walk(entry["items"], trail + [name])
            else:
                yield trail + [name], entry
    for section, items in catalog.items():
        yield from walk(items, [section])


def inventory():
    generators = {type(g).__name__: g for g in discover_generators()}
    from utils.generators.current_electricity.ohms_law_model import PROBLEM_TYPES
    from utils.generators.current_electricity.series_parallel_model import SERIES_PARALLEL_PROBLEM_TYPES
    from utils.worksheet_ui import UNIT_ACTIVITIES, ACTIVITIES
    custom = {**CUSTOM, "Circuit Ohm's Law": list(PROBLEM_TYPES),
              "Series and Parallel Circuits": list(SERIES_PARALLEL_PROBLEM_TYPES)}
    rows = []
    for trail, entry in routes():
        activity = trail[-1]
        handler = entry["handler"]
        source = handler.removeprefix("file:").split("::")[0] if handler.startswith("file:") else handler.split(":")[0].replace(".", "/") + ".py"
        if activity == "Create a worksheet":
            unit = "Forces" if trail[0] == "Dynamics" else "Kinematics"
            types = [(f"{name} / {kind}", "worksheet catalog")
                     for name in UNIT_ACTIVITIES[unit]
                     for kind in ACTIVITIES[name]().stored_metadata()]
        elif activity in GENERATORS:
            gen = generators[GENERATORS[activity]]
            kinds = list(gen.stored_metadata())
            if activity == "Wave Properties": kinds = [k for k in kinds if k == "Wave Properties"]
            if activity == "Harmonics": kinds = [k for k in kinds if "Harmonics" in k]
            if activity == "deciBel Scale": kinds = [k for k in kinds if k == "deciBel Scale"]
            source = Path(inspect.getfile(type(gen))).relative_to(ROOT).as_posix()
            types = [(kind, "generator metadata") for kind in kinds]
        elif activity in custom:
            types = [(kind, "custom mode/task") for kind in custom[activity]]
        else:
            # Never omit a new route just because no adapter knows its subtypes.
            types = [("[Problem types not yet inventoried]", "UNRESOLVED")]
        for kind, discovery in types:
            rows.append({"id": " / ".join(trail + [kind]), "route": " / ".join(trail),
                         "activity": activity, "problem_type": kind, "level": entry.get("min_level", "high"),
                         "handler": handler, "source": source, "discovery": discovery})
    return rows


def main():
    rows = inventory()
    reviews_path = ROOT / "docs/organizing_help_reviews.json"
    reviews = json.loads(reviews_path.read_text(encoding="utf-8")) if reviews_path.exists() else {}
    ids = {row["id"] for row in rows}
    if len(ids) != len(rows): raise ValueError("Duplicate inventory identity")
    stale = set(reviews) - ids
    if stale: raise ValueError(f"Review records no longer match inventory: {sorted(stale)}")
    route_count = len({row["route"] for row in rows})
    text = f"""# Organizing-help activity and problem-type inventory

Generated from the current route catalog and generator/worksheet metadata, with
explicit adapters for custom pages. **{route_count} routes; {len(rows)} problem-type/mode rows.**

A blank **Review** or **Findings / next work** cell means **not yet evaluated for
organizing help**. Discovery is not review, migration, or proof of readiness.
Previously passing solve-for and payload tests do not fill these review cells.
Recorded assessments are limited to the migrated families listed below.

Scope: every routed activity, including Advanced routes, custom pages, explorers,
labs, and both worksheet builders. Rows represent selectable problem types or
named modes; custom activities without such a selector use a descriptive task row.
Difficulty/solve-for combinations, randomized scenario branches, and individual
worksheet recipes are future review dimensions, not all separately enumerated here.
Stoichiometry reaction-type rows each include all available difficulties/conversions.
Worksheet rows remain unreviewed even when the underlying practice generator was
migrated: export scaffolding is a separate question.

Maintain decisions in [organizing_help_reviews.json](organizing_help_reviews.json).
Rebuild with `python tools/build_organizing_inventory.py`; verify drift with
`python tools/build_organizing_inventory.py --check`. New unmapped routes receive an
UNRESOLVED placeholder rather than disappearing. Generator type changes are picked
up automatically; custom selector changes require updating the explicit adapter.

See [architecture and migration requirements](organizing_help_architecture.md).

"""
    section = None
    for row in rows:
        if row["route"] != section:
            section = row["route"]
            source = row["handler"].removeprefix("file:").split("::")[0] if row["handler"].startswith("file:") else row["handler"].split(":")[0].replace(".", "/") + ".py"
            text += f"\n## {section}\n\nRoute: `{row['handler']}` ([page](../{source})); minimum level: {row['level']}.\n\n"
            text += "| Problem type / mode | Discovery source | Review | Findings / next work |\n|---|---|---|---|\n"
        review = reviews.get(row["id"], {})
        cells = [row["problem_type"], f"[{row['discovery']}](../{row['source']})", review.get("status", ""), review.get("notes", "")]
        text += "| " + " | ".join(cell.replace("|", "\\|").replace("\n", " ") for cell in cells) + " |\n"
    output = ROOT / "docs/organizing_help_inventory.md"
    if "--check" in sys.argv:
        if not output.exists() or output.read_text(encoding="utf-8") != text:
            raise SystemExit("Inventory drift: run tools/build_organizing_inventory.py")
    else:
        output.write_text(text, encoding="utf-8")
    unresolved = [row["id"] for row in rows if row["discovery"] == "UNRESOLVED"]
    print(f"{route_count} routes, {len(rows)} rows, {len(reviews)} reviewed rows, {len(unresolved)} unresolved routes.")
    if unresolved: raise SystemExit("Missing type discovery adapters: " + str(unresolved))

if __name__ == "__main__":
    main()

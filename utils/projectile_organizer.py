"""Projectile facts and supporting calculations, using the printed givens."""
import math


LABELS = {
    "vx": "Horizontal velocity, vₓ (m/s)", "vyi": "Initial vertical velocity, vᵧᵢ (m/s)",
    "vyf": "Landing vertical velocity, vᵧf (m/s)", "vi": "Launch speed (m/s)",
    "vf": "Landing speed (m/s)", "ai": "Launch angle (°)", "af": "Landing angle (°)",
    "h": "Cliff height (m)", "x": "Horizontal displacement, Δx (m)",
    "dy": "Vertical displacement, Δy (m)", "hmax": "Maximum height above launch (m)",
    "back": "Distance behind cliff edge (m)", "inroad": "Landing distance beyond edge (m)",
    "tfirst": "First time at cliff height (s)", "t": "Total flight time (s)",
    "tpeak": "Time to maximum height (s)", "tlevel": "Time back at launch height (s)",
}
HINTS = {
    "vx": "Horizontal velocity stays constant. Resolve a speed using v cos θ, or use Δx / t.",
    "vyi": "Resolve launch speed using v sin θ. A horizontal launch has no initial vertical velocity.",
    "vyf": "Up is positive: vᵧf = vᵧᵢ − 10t. Downward velocity is negative.",
    "dy": "Landing position minus launch position. A landing below launch gives a negative change; cliff height is a positive distance.",
    "t": "Both axes share the same flight time. For an elevated landing, use the later crossing on the way down.",
    "tpeak": "At maximum height the vertical velocity is zero. This is not generally half the flight time.",
    "af": "Give the positive angle below horizontal at landing.",
    "tlevel": "The nonzero time when vertical displacement from launch is zero.",
}


def projectile_payload(kind, difficulty, choice, raw, question, units):
    r = lambda key: round(raw[key], 2 if kind != 3 else 4)
    facts = {}
    if kind == 1:
        mapping = {"x": (["h", "vx"], ["x"]), "h": (["vx", "x"], ["h"]),
                   "v_i": (["h", "x"], ["vi"]), "v_i and h": (["vf", "af"], ["vi", "h"]),
                   "v_f and theta": (["vx", "x"], ["vf", "af"]),
                   "v_f and x": (["h", "af"], ["vf", "x"])}
        available = {"h": r("d_y"), "vx": r("v_x"), "x": r("d_x"), "vf": r("v_r"), "af": r("theta")}
        given, targets = mapping[choice]
        facts = {key: available[key] for key in given}
        if "vf" in facts:
            vx = facts["vf"] * math.cos(math.radians(facts["af"]))
            t = facts["vf"] * math.sin(math.radians(facts["af"])) / 10
        elif "vx" in facts:
            vx = facts["vx"]
            t = facts["x"] / vx if "x" in facts else math.sqrt(facts["h"] / 5)
        else:
            t = math.sqrt(facts["h"] / 5)
            vx = facts["x"] / t if "x" in facts else 10*t / math.tan(math.radians(facts["af"]))
        vyi, dy = 0, -5*t*t
        values = {"vi": vx, "h": -dy, "x": vx*t}
    elif kind == 2:
        mapping = {"x and y_max": (["vi", "ai"], ["x", "hmax"]),
                   "v_i and theta": (["hmax", "x"], ["vi", "ai"]),
                   "v_i and x": (["ai", "hmax"], ["vi", "x"]),
                   "theta and x": (["vi", "hmax"], ["ai", "x"])}
        available = {"vi": r("v_r"), "ai": r("theta"), "hmax": r("d_y"), "x": r("d_x")}
        given, targets = mapping[choice]
        facts = {key: available[key] for key in given}
        vyi = facts["vi"]*math.sin(math.radians(facts["ai"])) if "hmax" not in facts else math.sqrt(20*facts["hmax"])
        t = vyi/5
        vx = (facts["x"]/t if "x" in facts else vyi/math.tan(math.radians(facts["ai"])) if "ai" in facts else math.sqrt(facts["vi"]**2-vyi**2))
        dy = 0
        values = {"vi": math.hypot(vx,vyi), "ai": math.degrees(math.atan2(vyi,vx)), "x": vx*t, "hmax": vyi*vyi/20}
        question += " It lands at the same height it was launched from."
    else:
        high_low = raw["direction_choice"] == 1
        if high_low:
            given, targets = (["h", "vi", "ai"], ["x", "vf"]) if difficulty == "Easy" else (["h", "vi", "ai", "x"], ["back", "tlevel"])
        elif difficulty == "Easy":
            given, targets = (["h", "vi", "ai"], ["x", "af"]) if choice == 1 else (["vi", "ai", "x"], ["h", "vf"])
        else:
            given, targets = ["h", "vi", "tfirst", "inroad"], ["ai", "x"]
        available = {"h": raw["d_y"], "vi": raw["v_r"], "ai": raw["theta_i"], "x": raw["d_x"], "tfirst": raw.get("t_1"), "inroad": raw["x_back"]}
        facts = {key: available[key] for key in given}
        vyi = (facts["h"] + 5*facts["tfirst"]**2)/facts["tfirst"] if "tfirst" in facts else facts["vi"]*math.sin(math.radians(facts["ai"]))
        vx = math.sqrt(facts["vi"]**2-vyi**2)
        if "h" in facts:
            dy = -facts["h"] if high_low else facts["h"]
            t = (vyi + math.sqrt(max(0, vyi*vyi-20*dy)))/10
        else:
            t = facts["x"]/vx
            dy = vyi*t-5*t*t
        values = {"x": vx*t-facts.get("inroad",0), "h": abs(dy), "back": vx*t-facts.get("x",0), "ai": math.degrees(math.atan2(vyi,vx))}
        if not high_low:
            question += " It lands while descending."
    vyf = vyi-10*t
    values.update(vx=vx, vyi=vyi, vyf=vyf, dy=dy, t=t, tpeak=vyi/10,
                  tlevel=vyi/5, vf=math.hypot(vx,vyf), af=math.degrees(math.atan2(abs(vyf),vx)))
    steps = ["vx", "vyi", "t", "vyf"]
    if kind == 2:
        steps.insert(3, "tpeak")
    # Supporting values may overlap earlier requested answers, but exclude the last.
    steps = [key for key in steps if key not in facts and key != targets[-1]]
    def field(key, value):
        label = LABELS[key]
        if key == "dy":
            label = "Launch to ground, Δy (m)" if kind == 1 else "Launch to landing, Δy (m)"
        return {"id": key, "label": label, "value": value, "help": HINTS.get(key, "Use the information in the question and the projectile equations.")}
    # Only printed facts and wording cues enter the diagram contract. The
    # renderer may reconstruct proportions, but never labels solved values.
    scene = "horizontal" if kind == 1 else "level" if kind == 2 else "down" if high_low else "up"
    diagram = {"scene": scene, "givens": dict(facts),
               "launch_behind_edge": kind == 3 and high_low and difficulty != "Easy"}
    return {"question": question, "answers": [values[key] for key in targets], "units": units,
            "diagram_data": diagram,
            "extras": {"projectile_plan": {"kind": kind, "givens": facts, "targets": targets,
                      "fields": [field(key,value) for key,value in facts.items()],
                      "steps": [field(key,values[key]) for key in steps], "values": values}}}

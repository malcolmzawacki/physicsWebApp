"""Constant-velocity cases with explicit reference frames and reversible unknowns."""
import random
from utils.generators.base_generator import BaseGenerator


class RelativeMotionGenerator(BaseGenerator):
    TYPES = ("Independent motion", "Nested reference frames", "Combined")
    DIFFICULTIES = ("Easy", "Medium", "Hard")
    TARGETS = ("Result", "Missing velocity", "Mixed practice")

    def __init__(self):
        super().__init__(state_prefix="rel_motion_")

    def stored_metadata(self):
        relative = r"v_{A/B}=v_{A/S}-v_{B/S}"
        chain = r"v_{P/S}=v_{P/B}+v_{B/W}+v_{W/S}"
        metadata = {
            self.TYPES[0]: {
                "honors": [relative, r"d(t)=d_0+(v_{B/S}-v_{A/S})t"],
                "conceptual": [relative, r"d(t)=d_0-v_{A/B}t", r"t_{meet}=\frac{d_0}{v_{A/S}-v_{B/S}}", r"v_{A/S}=v_{A/B}+v_{B/S}"],
            },
            self.TYPES[1]: {
                "honors": [chain],
                "conceptual": [chain, r"v_{W/S}=v_{P/S}-v_{P/B}-v_{B/W}", r"v_{P/B}=v_{P/S}-v_{B/W}-v_{W/S}"],
            },
            self.TYPES[2]: {
                "honors": [relative, chain],
                "conceptual": [relative, chain, r"v_{P/Q}=(v_{P/B_1}+v_{B_1/W}+v_{W/S})-(v_{Q/B_2}+v_{B_2/W}+v_{W/S})"],
            },
        }
        identities = {
            "Independent motion": "relative-motion.independent",
            "Nested reference frames": "relative-motion.nested-frames",
            "Combined": "relative-motion.combined",
        }
        return {kind: {"id": identities[kind], "aliases": [kind],
                       **{level: r"\begin{gathered}" + r"\\".join(equations) + r"\end{gathered}"
                          for level, equations in levels.items()}} for kind, levels in metadata.items()}

    @staticmethod
    def _link(subject, reference, velocity, coefficient=1):
        return dict(subject=subject, reference=reference, velocity=velocity, coefficient=coefficient)

    def build_case(self, problem_type, difficulty):
        if problem_type not in self.TYPES or difficulty not in self.DIFFICULTIES:
            raise ValueError("Unsupported relative-motion type or difficulty")
        tier = self.DIFFICULTIES.index(difficulty)
        def signed():
            return random.choice((-1, 1)) * random.randint(1, 6)
        case = dict(problem_type=problem_type, difficulty=difficulty, kind="velocity")
        if problem_type == self.TYPES[0]:
            a, b = signed(), signed()
            if tier == 0:
                a, b = random.randint(1, 6), -random.randint(1, 6)
                if random.choice((True, False)):
                    a, b = -a, -b
            if tier == 2:
                # A starts behind B; positive closing velocity guarantees a future meeting.
                a, b = random.randint(2, 6), random.randint(-5, 1)
            case["links"] = [self._link("Object A", "ground", a), self._link("Object B", "ground", b, -1)]
            case["context"] = "Two objects move along the same straight track. Take right as positive."
            case["result_label"] = "Velocity of A relative to B"
            if tier == 1:
                elapsed = random.randint(2, 8)
                gap = abs(a - b) * elapsed + random.randint(10, 30)
                case.update(kind="separation", time=elapsed, gap=gap, result_label="Separation after the stated time")
            elif tier == 2:
                case.update(kind="meeting", gap=(a - b) * random.randint(2, 12), result_label="Time until the objects meet")
        elif problem_type == self.TYPES[1]:
            frames = ["Person", "boat", "shore"] if tier == 0 else ["Person", "boat", "water", "shore"]
            if tier == 2:
                frames.insert(1, "moving walkway")
            case["links"] = [self._link(x, y, random.randint(1, 6) if x == "water" else signed())
                             for x, y in zip(frames, frames[1:])]
            case["context"] = "A person moves on a boat. All motion is along the river; take downstream as positive."
            if tier == 2:
                case["context"] += " The boat has a moving walkway along its deck."
            case["result_label"] = "Person's velocity relative to the shore"
        else:
            frames_a = ["Person A", "boat A", "shore"]
            frames_b = ["Person B", "boat B", "shore"]
            if tier >= 1:
                frames_a.insert(-1, "water")
                frames_b.insert(-1, "water")
            if tier == 2:
                frames_a.insert(1, "walkway A")
                frames_b.insert(1, "walkway B")
            links, current = [], random.randint(1, 6)
            for frames, coefficient in ((frames_a, 1), (frames_b, -1)):
                for x, y in zip(frames, frames[1:]):
                    links.append(self._link(x, y, current if x == "water" else signed(), coefficient))
            case["links"] = links
            case["context"] = "Two people move on separate boats along the same river. Take downstream as positive."
            if tier >= 1:
                case["context"] += " Both boats experience the same uniform water current."
            if tier == 2:
                case["context"] += " Each boat has a moving walkway along its deck."
            case["result_label"] = "Velocity of Person A relative to Person B"
        relative = sum(link["velocity"] * link["coefficient"] for link in case["links"])
        case.update(relative_velocity=relative, result=relative)
        if case["kind"] == "separation":
            case["result"] = case["gap"] - relative * case["time"]
        elif case["kind"] == "meeting":
            case["result"] = case["gap"] / relative
        return case

    def eligible_unknowns(self, case):
        # A shared current cancels; relative velocity cannot determine its value.
        return [i for i, link in enumerate(case["links"]) if not (
            case["problem_type"] == "Combined" and link["subject"] == "water")]

    def render_case(self, case, solve_for="result"):
        links = case["links"]
        if solve_for != "result" and solve_for not in self.eligible_unknowns(case):
            raise ValueError("Unknown must be 'result' or an identifiable velocity-link index")
        missing = solve_for != "result"
        question = [case["context"], "Assume all velocities are constant. Use negative velocities for motion opposite the positive direction."]
        displayed, seen = [], set()
        for i, link in enumerate(links):
            label = f"{link['subject']} relative to {link['reference']}"
            value = None if i == solve_for else link["velocity"]
            if label not in seen:
                question.append(f"- {label}: **{'?' if value is None else f'{value:+g}'} m/s**")
                displayed.append(dict(label=label, value=value))
                seen.add(label)
        if case["kind"] != "velocity":
            question.append(f"Initially B is **{case['gap']:g} m to the right of A**.")
        if case["kind"] == "separation":
            question.append(f"Consider the separation after **{case['time']:g} s**. The objects have not passed each other.")
        result_unit = dict(velocity="m/s", separation="m", meeting="s")[case["kind"]]
        if missing:
            question.append(f"{case['result_label']}: **{case['result']:g} {result_unit}**.")
            target = links[solve_for]
            label = f"Velocity of {target['subject']} relative to {target['reference']}"
            answer, unit = target["velocity"], "m/s"
        else:
            label, answer, unit = case["result_label"], case["result"], result_unit
        question.append(f"**Find: {label.lower()}.**")
        terms = " ".join(f"{'+' if link['coefficient'] > 0 else '-'} ({link['velocity']:g})" for link in links)
        equations = []
        if missing:
            if case["kind"] == "separation":
                equations.append(rf"v_{{rel}}=\frac{{{case['gap']:g}-{case['result']:g}}}{{{case['time']:g}}}={case['relative_velocity']:g}\;\mathrm{{m/s}}")
            elif case["kind"] == "meeting":
                equations.append(rf"v_{{rel}}=\frac{{{case['gap']:g}}}{{{case['result']:g}}}={case['relative_velocity']:g}\;\mathrm{{m/s}}")
            known = sum(link["velocity"] * link["coefficient"] for i, link in enumerate(links) if i != solve_for)
            equations.append(rf"v_{{unknown}}=\frac{{{case['relative_velocity']:g}-({known:g})}}{{{links[solve_for]['coefficient']}}}={answer:g}\;\mathrm{{m/s}}")
        equations.append(rf"v_{{rel}}={terms}={case['relative_velocity']:g}\;\mathrm{{m/s}}")
        if not missing and case["kind"] == "separation":
            equations.append(rf"d={case['gap']:g}-({case['relative_velocity']:g})({case['time']:g})={case['result']:g}\;\mathrm{{m}}")
        elif not missing and case["kind"] == "meeting":
            equations.append(rf"t=\frac{{{case['gap']:g}}}{{{case['relative_velocity']:g}}}={case['result']:g}\;\mathrm{{s}}")
        explanation = "Add velocities along each frame chain. For two objects, subtract B's ground/shore velocity from A's."
        if case["problem_type"] == "Combined" and case["difficulty"] != "Easy":
            explanation += " The shared water current cancels in the subtraction."
        if missing:
            explanation += " Isolate the missing term; its sign is part of the answer."
        return dict(question="\n\n".join(question), answers=[answer], units=[f"{label} ({unit})"],
                    problem_type=case["problem_type"], difficulty=case["difficulty"], diagram_data=displayed,
                    hints=["Keep each velocity paired with its observer. Add along a chain; subtract between objects."],
                    extras=dict(case=case, solve_for=solve_for, solution_equations=equations, explanation=explanation))

    def selected_question(self, problem_type, difficulty, target):
        """Render one declared unknown, identified by its named reference frames."""
        case = self.build_case(problem_type, difficulty)
        if target == "result":
            return self.render_case(case, "result")
        for index in self.eligible_unknowns(case):
            link = case["links"][index]
            if target == link["subject"] + "|" + link["reference"]:
                return self.render_case(case, index)
        raise ValueError(f"Target {target!r} is not identifiable in this case")

    def choose_problem_dict(self, problem_type, difficulty, solve_for=None):
        case = self.build_case(problem_type, difficulty)
        if solve_for is None:
            solve_for = "Mixed practice"
        if solve_for in ("Missing velocity", "Mixed practice"):
            choices = self.eligible_unknowns(case)
            if solve_for == "Mixed practice":
                choices = choices + ["result"]
            solve_for = random.choice(choices)
        elif solve_for == "Result":
            solve_for = "result"
        return self.render_case(case, solve_for)

    def example(self):
        case = dict(problem_type="Nested reference frames", difficulty="Medium", kind="velocity",
                    context="A person walks upstream on a boat moving downstream through the water. Take downstream as positive.",
                    links=[self._link("Person", "boat", -1), self._link("boat", "water", 3), self._link("water", "shore", 2)],
                    result_label="Person's velocity relative to the shore", result=4, relative_velocity=4)
        return self.render_case(case, 2)

    def generate_diagram(self, diagram_data, problem_type, difficulty):
        from matplotlib.figure import Figure
        fig = Figure(figsize=(7, max(2.5, len(diagram_data) * .7)))
        ax = fig.subplots()
        ax.set(xlim=(-7, 7), ylim=(-.6, len(diagram_data)))
        ax.axis("off")
        ax.set_title("Velocities (m/s) in their named frames | positive to the right", fontsize=11)
        for index, row in enumerate(diagram_data):
            y, value = len(diagram_data) - index - 1, row["value"]
            ax.text(-6.8, y + .27, row["label"], fontsize=10)
            if value is None:
                ax.text(0, y, "? m/s", ha="center", color="#b45309")
            elif value == 0:
                ax.plot(0, y, "o", color="#2563eb")
                ax.text(.3, y, "0 m/s")
            else:
                ax.annotate("", xy=(value, y), xytext=(0, y), arrowprops=dict(arrowstyle="->", color="#2563eb", lw=2))
                ax.text(value + (.2 if value > 0 else -.2), y, f"{value:+g}", ha="left" if value > 0 else "right", va="center")
        fig.tight_layout()
        return fig

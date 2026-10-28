"""Paper versions of conceptual Dynamics activities using their existing case models.

Specs retain selected cases/options, never practice attempts. Essential diagrams
are part of the question and are not governed by the optional-sketch checkbox.
"""
import io
import random
from dataclasses import asdict
from utils.generators.base_generator import BaseGenerator
from utils import recognizing_forces as recognize
from utils import force_diagram_match as diagrams
from utils import force_motion_match as motion
from utils import force_change as change
from utils import force_ranking as ranking

LETTERS = "ABCD"


def _panels(spec, problem_type=None, difficulty=None):
    from matplotlib.figure import Figure
    from matplotlib import rc_context, rcParamsDefault
    import matplotlib.image as mpimg
    from xtrct_docs.motion_graph_adapter import _render_lock
    with _render_lock, rc_context(rcParamsDefault):
        panels = spec["panels"]
        columns = spec.get("columns", 1 if len(panels) == 1 else 2)
        rows = (len(panels)+columns-1)//columns
        figure = Figure(figsize=(3 if columns == 1 else 6, (1.65 if columns == 4 else 2.0)*rows), facecolor="white")
        for i, panel in enumerate(panels):
            ax = figure.add_subplot(rows, columns, i+1)
            kind, data = panel["kind"], panel["data"]
            if kind == "blank":
                ax.plot(0, 0, "ko", markersize=5)
                ax.set(xlim=(-2,2), ylim=(-2,2), aspect="equal")
            elif kind == "forces" and columns == 4:
                # Draw at final print size so labels stay readable in four-across rows.
                ax.set(xlim=(-2.6,2.6),ylim=(-2.5,2.5),aspect="equal")
                for item in data:
                    dx,dy = diagrams.DIRECTIONS[item["direction"]]
                    length = 1.05 if item["size"] == 1 else 1.75
                    x,y = dx*length,dy*length
                    ax.annotate("",xy=(x,y),xytext=(0,0),
                        arrowprops=dict(arrowstyle="-|>",color="black",lw=1,mutation_scale=9))
                    ax.text(.18 if dy else x/2, y if dy else (.35 if dx>0 else -.35),
                        diagrams.SHORT_LABELS[item["force"]],fontsize=7.5,color="black",
                        ha="left" if dy else "center",va="center")
                ax.plot(0,0,"ko",markersize=3)
                if not data:
                    ax.text(0,-.7,"No forces",fontsize=7.5,ha="center")
            else:
                if kind == "forces":
                    png = diagrams.render_force_diagram(tuple(diagrams.ForceArrow(**a) for a in data))
                elif kind == "change":
                    png = change.render_change_diagram(change.ForceState(**data))
                elif kind == "rank":
                    png = ranking.render_rank_diagram(ranking.RankCase(**data), spec["scale"])
                else:
                    history = next(m for m in motion.MOTIONS if m.id == data["id"])
                    png = motion.render_motion(history, data["axis"]) if kind == "dots" else motion.render_motion_graph(history, data["graph"])
                pixels = mpimg.imread(io.BytesIO(png))
                ax.imshow(pixels[:,:,:3].mean(axis=2), cmap="gray", vmin=0, vmax=1)
            ax.axis("off")
            ax.set_title(panel["label"], color="black", fontsize=11)
        figure.tight_layout(pad=.5)
        return figure


class ConceptualWorksheet(BaseGenerator):
    DIFFICULTIES = ("Standard",)
    WORKSHEET_NOTE = "Conceptual practice; no difficulty tiers."
    family = ""

    def __init__(self):
        super().__init__("worksheet_dynamics_" + self.family)
        self._bags = {}
        self._last = {}

    def get_problem_types(self):
        if self.family in ("recognize", "match", "builder"):
            return list(recognize.PRACTICE_SETS)
        if self.family == "motion":
            return [f"{context} / {display}" for context in motion.PRACTICE_SETS for display in motion.MOTION_DISPLAYS]
        if self.family == "change":
            return list(change.PRACTICE_SETS)
        return [f"{q} / {c} / {m} / {t}" for q in ranking.QUANTITIES for c in ranking.COMPARISONS
                for m in ranking.MASS_PATTERNS for t in ("With ties", "Without ties")]

    def _pick(self, key, candidates):
        bag = self._bags.setdefault(key, [])
        if not bag:
            bag.extend(candidates)
        available = [c for c in bag if c.id != self._last.get(key)] or bag
        selected = random.choice(available)
        bag.remove(selected)
        self._last[key] = selected.id
        return selected

    def generate_diagram(self, diagram_data, problem_type=None, difficulty=None):
        return _panels(diagram_data)

    def choose_problem_dict(self, problem_type, difficulty):
        if problem_type not in self.get_problem_types() or difficulty != "Standard":
            raise ValueError("Unsupported conceptual worksheet request")
        panels, spec, case_id = [], {}, None
        if self.family == "recognize":
            case = self._pick(problem_type, recognize.available_scenarios(problem_type))
            case_id = case.id
            prompt = case.situation + f"\nWhich forces act on {case.target}? Select all that apply, or write none."

            answer = "; ".join(f"{chr(65+i)}: {label}" for i,(key,label) in enumerate(recognize.FORCE_LABELS.items()) if key in case.forces) or "None"
        elif self.family in ("match", "builder"):
            case = self._pick(problem_type, diagrams.available_cases(problem_type))
            case_id = case.id
            prompt = case.prompt + f"\n{'Choose' if self.family == 'match' else 'Draw and label'} the free-body diagram for {case.scenario.target}. Compare opposing lengths along the same axis; exact ratios are not required."
            if self.family == "match":
                spec["columns"] = 4
                options = diagrams.make_options(case)
                panels = [dict(kind="forces", data=[asdict(a) for a in o["arrows"]], label=LETTERS[i]) for i,o in enumerate(options)]
                answer = next(LETTERS[i] for i,o in enumerate(options) if diagrams.diagram_matches(case, o["arrows"])) + ": " + case.explanation
            else:
                panels = [dict(kind="blank", data=None, label="Draw forces on this object")]
                answer = diagrams.describe_diagram(case.arrows) + " " + case.explanation
        elif self.family == "motion":
            context, display = problem_type.split(" / ")
            case = self._pick(problem_type, motion.available_cases(context))
            case_id = case.id
            options = motion.make_options(case)
            spec["options"] = [m.id for m in options]
            prompt = case.prompt + "\nSelect ALL motion histories compatible with the forces. Arrow lengths are relative; compare forces on the same axis."
            panels = [dict(kind="forces", data=[asdict(a) for a in case.arrows], label="Given forces")]
            if display == "Written descriptions":
                prompt += "\n" + "\n".join(f"{LETTERS[i]}. {m.description(case.axis)}" for i,m in enumerate(options))
            else:
                prompt += "\nDots mark equal time intervals." if display == "Dot diagrams" else "\nGraphs use positive right/up."
                for i,m in enumerate(options):
                    panels.append(dict(kind="dots" if display == "Dot diagrams" else "graph",
                        data=dict(id=m.id,axis=case.axis,graph=None if display == "Dot diagrams" else motion.graph_kind(display,i,0)), label=LETTERS[i]))
            answer = "; ".join(f"{LETTERS[i]}: {m.description(case.axis)}" for i,m in enumerate(options) if motion.compatible(case,m))
        elif self.family == "change":
            case = self._pick(problem_type, change.available_cases(problem_type))
            case_id = case.id
            options = change.make_options(case)
            spec["options"] = [asdict(o) for o in options]
            prompt = "A cart stays on a level frictionless track; air resistance is ignored. " + case.motion + " " + case.request
            prompt += " Change exactly one interaction. Select ALL valid changes.\n" + "\n".join(f"{LETTERS[i]}. {change.change_description(case.initial,o)}" for i,o in enumerate(options))
            panels = [dict(kind="change",data=asdict(case.initial),label="Before the change")]
            answer = "; ".join(LETTERS[i] for i,o in enumerate(options) if change.accepted(case,o)) + ": " + change.explanation(case)
        else:
            quantity, comparison, masses, ties = problem_type.split(" / ")
            cases = ranking.make_board(quantity,comparison,masses,ties == "With ties")
            prompt = f"Rank {quantity.lower()} by {comparison.lower()}, greatest to least. Equal values tie. Right is positive. The carts stay on level frictionless tracks; air resistance is ignored. P is a rightward push; T is a leftward rope pull; N and W balance vertically. All panels share one arrow scale."
            panels = [dict(kind="rank",data=asdict(c),label=LETTERS[i]) for i,c in enumerate(cases)]
            spec["scale"] = max(max(c.push,c.pull,10*c.mass) for c in cases)
            answer = ranking.ranking_text(ranking.expected_groups(cases,quantity,comparison))
        spec.update(panels=panels, case_id=case_id)
        result = dict(question=prompt.replace("\n", "  \n"), answers=[answer], units=["Answer"], worksheet_case=spec)
        if self.family == "recognize":
            result["print_option_columns"] = [[f"{chr(65+i)}. {label}" for i,label in enumerate(recognize.FORCE_LABELS.values())][:4],
                                              [f"{chr(65+i)}. {label}" for i,label in enumerate(recognize.FORCE_LABELS.values())][4:]]
        if panels:
            result["diagram_data"] = spec
            result["graph_doc_width"] = 2.7 if len(panels) == 1 else 5.7
        return result


class WorksheetRecognizingForces(ConceptualWorksheet):
    family = "recognize"

class WorksheetForceDiagramMatch(ConceptualWorksheet):
    family = "match"

class WorksheetForceDiagramBuilder(ConceptualWorksheet):
    family = "builder"

class WorksheetForceMotion(ConceptualWorksheet):
    family = "motion"

class WorksheetForceChange(ConceptualWorksheet):
    family = "change"

class WorksheetForceRanking(ConceptualWorksheet):
    family = "ranking"

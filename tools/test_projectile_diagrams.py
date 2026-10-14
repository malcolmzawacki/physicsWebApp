"""Check physical proportions, bounded extremes and given-only labels."""
import copy
import math
import random
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from utils.generators.kinematics.projectile_generator import ProjectileGenerator
from utils.projectile_diagrams import diagram_geometry, projectile_figure
from utils.solve_for import target_options, generate_selected
from xtrct_docs.payload_adapter import DocumentGenerator


def signature(figure):
    ax = figure.axes[0]
    return ([t.get_text() for t in list(ax.texts)+list(figure.texts)],
            [line.get_xydata().tolist() for line in ax.lines])


def main():
    generator = ProjectileGenerator()
    cases = []
    for difficulty in ("Easy", "Medium", "Hard"):
        for kind in generator.stored_metadata():
            for option in target_options(generator, kind, difficulty):
                cases.append(generate_selected(generator, kind, difficulty, option["id"]))
        for direction, variants in ((1, (1,)), (2, (1, 2) if difficulty == "Easy" else (1,))):
            for variant in variants:
                cases.append(generator._generate_type3_question(difficulty, direction=direction, variant=variant))
    scenes = set()
    modes = set()
    for payload in cases:
        data = payload["diagram_data"]
        scenes.add(data["scene"])
        assert data["givens"] == payload["extras"]["projectile_plan"]["givens"]
        baseline = signature(generator.generate_diagram(data, "", ""))
        geo = diagram_geometry(data)
        modes.add(geo["mode"])
        motion = geo["motion"]
        plan = payload["extras"]["projectile_plan"]
        # Independently stored organizer calculations agree with reconstruction.
        for key in ("vx", "vy", "time"):
            expected_key = {"vy": "vyi", "time": "t"}.get(key, key)
            assert math.isclose(motion[key], plan["values"][expected_key], rel_tol=1e-9)
        extent = (motion["peak_y"]-min(motion["y0"], motion["y1"]))*geo["y_scale"]
        assert .64-1e-9 <= extent <= 8.+1e-9
        if geo["mode"] == "equal":
            assert geo["x_scale"] == geo["y_scale"]
        changed = copy.deepcopy(payload)
        changed["answers"] = [987654321] * len(payload["answers"])
        changed["extras"]["projectile_plan"]["values"] = {"vx": 987654321}
        changed["extras"]["projectile_plan"]["steps"] = []
        assert signature(generator.generate_diagram(changed["diagram_data"], "", "")) == baseline
        assert all(np.isfinite(line).all() for line in baseline[1])
    assert scenes == {"horizontal", "level", "down", "up"}
    # Known h/range cases provide independent scale and endpoint checks.
    for height, distance, mode in ((100., 400., "equal"), (100., 1e6, "adjusted"),
                                   (1e6, 100., "adjusted"), (1e12, 4e12, "equal")):
        data = dict(scene="horizontal", givens=dict(h=height, x=distance), launch_behind_edge=False)
        geo = diagram_geometry(data)
        assert geo["mode"] == mode
        assert math.isclose(geo["motion"]["range"], distance)
        assert math.isclose(geo["motion"]["y0"], height)
        fig = projectile_figure(data)
        # Verify actual pixel scale after Matplotlib lays out the axes.
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        FigureCanvasAgg(fig).draw()
        ax = fig.axes[0]
        origin = ax.transData.transform((0, 0))
        x_pixel = ax.transData.transform((geo["x_scale"], 0))[0]-origin[0]
        y_pixel = ax.transData.transform((0, geo["y_scale"]))[1]-origin[1]
        assert math.isclose(y_pixel/x_pixel, geo["vertical_factor"], rel_tol=1e-3)
        assert any("angles are not to scale" in t.get_text() for t in fig.texts) == (mode == "adjusted")
        if distance == 1e6:
            assert math.isclose(geo["vertical_factor"], 800.)
    # Broad sampling covers rounding, zero setbacks/inroads and later crossings.
    for seed in range(100):
        random.seed(seed)
        for difficulty in ("Easy", "Medium", "Hard"):
            for kind in generator.stored_metadata():
                payload = generator.choose_problem_dict(kind, difficulty)
                geo = diagram_geometry(payload["diagram_data"])
                assert all(math.isfinite(v) for v in geo["motion"].values())
    assert modes == {"equal", "adjusted"}
    exported = DocumentGenerator(generator).question("Type 1", "Easy")
    assert exported["diagram_renderer"](exported["diagram_data"]) is not None
    print(f"Projectile diagrams: {len(cases)} branches, 900 sampled flights, physical/pixel scales, extreme ratios, hidden-data isolation and export rendering passed.")


if __name__ == "__main__":
    main()

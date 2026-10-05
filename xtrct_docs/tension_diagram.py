"""Compact print-only suspension schematic; never displays solved tensions."""
import math
from matplotlib.figure import Figure
from matplotlib.patches import Arc, Rectangle


def tension_inset(spec):
    """Draw numbered wires and given angles from the horizontal in black ink."""
    fig = Figure(figsize=(2.0, 1.05), facecolor="white")
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], facecolor="white")
    ax.plot([-1.15, 1.15], [0, 0], color="0.5", linestyle="--", linewidth=0.7)
    for i, (quadrant, theta) in enumerate(zip(spec["scenario"], (spec["theta1"], spec["theta2"])), 1):
        angle = {1: theta, 2: 180-theta, 3: 180+theta, 4: 360-theta}[quadrant]
        radians = math.radians(angle)
        x, y = math.cos(radians), math.sin(radians)
        ax.plot([0, x], [0, y], color="black", linewidth=1.4)
        ax.text(1.12*x + (0.08 if x > 0 else -0.08), 1.12*y, f"Wire {i}", ha="left" if x > 0 else "right", va="bottom" if y > 0 else "top", fontsize=8.5, color="black")
        start, end = {1: (0, theta), 2: (180-theta, 180), 3: (180, 180+theta), 4: (360-theta, 360)}[quadrant]
        ax.add_patch(Arc((0, 0), 0.72, 0.72, theta1=start, theta2=end, color="black", linewidth=0.7))
        mid = math.radians((start+end)/2)
        ax.text(0.62*math.cos(mid), 0.62*math.sin(mid), f"{theta}°", ha="center", va="center", fontsize=9, color="black", bbox=dict(facecolor="white", edgecolor="none", pad=0.2))
    ax.add_patch(Rectangle((-0.10, -0.10), 0.20, 0.20, facecolor="white", edgecolor="black", zorder=5))
    ax.set(xlim=(-2.1, 2.1), ylim=(-1.25, 1.25), aspect="equal")
    # Fixed physical canvas bounds the worst-case height. Equal aspect scales
    # wire geometry to fit the vertical extent while labels retain their point
    # size. Opposing wires need more height than two upward wires with the same
    # angle sum, so use actual vertical extent rather than the angle sum.
    ys = [math.sin(math.radians({1: t, 2: 180-t, 3: 180+t, 4: 360-t}[q]))
          for q, t in zip(spec["scenario"], (spec["theta1"], spec["theta2"]))]
    ax.set_ylim(min(-0.35, min(ys)*1.12-0.45), max(0.35, max(ys)*1.12+0.45))
    ax.axis("off")
    _fit_labels(fig, ax)
    return fig


def _fit_labels(fig, ax):
    """Measure actual print glyphs, leaving a safety margin inside the canvas.

    Expanding data limits shrinks geometry without shrinking label fonts or
    changing the physical inset size. Measure at the export resolution.
    """
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    fig.set_dpi(200)
    canvas = FigureCanvasAgg(fig)
    margin = 0.06 * fig.dpi
    for _ in range(24):
        canvas.draw()
        renderer = canvas.get_renderer()
        bounds = [text.get_window_extent(renderer) for text in ax.texts]
        if all(b.x0 >= margin and b.y0 >= margin and
               b.x1 <= fig.bbox.width - margin and
               b.y1 <= fig.bbox.height - margin for b in bounds):
            return
        for getter, setter in ((ax.get_xlim, ax.set_xlim), (ax.get_ylim, ax.set_ylim)):
            low, high = getter()
            middle = (low + high) / 2
            half = (high - low) * 0.56
            setter(middle - half, middle + half)
    raise ValueError("Could not fit tension labels inside the print canvas")


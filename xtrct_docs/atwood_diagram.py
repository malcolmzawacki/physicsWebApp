"""Compact print schematic accepting only explicitly disclosed givens."""
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Circle
from xtrct_docs.tension_diagram import _fit_labels


def atwood_inset(spec):
    fig = Figure(figsize=(2, 1.05), facecolor="white")
    ax = fig.add_axes([.02, .02, .96, .96], facecolor="white")
    ax.plot([.1, 2.4, 2.4], [.9, .9, -.15], color="black", linewidth=1)
    ax.add_patch(Rectangle((.55, .9), .65, .4, facecolor="white", edgecolor="black"))
    ax.add_patch(Circle((2.45, 1.1), .16, facecolor="white", edgecolor="black"))
    ax.plot([1.2, 2.45], [1.26, 1.26], color="black")
    ax.plot([2.61, 2.61], [1.1, .25], color="black")
    ax.add_patch(Rectangle((2.38, -.15), .46, .4, facecolor="white", edgecolor="black"))
    for key, symbol, x, y in (("m1", "m₁", .85, 1.55), ("m2", "m₂", 2.65, -.4)):
        value = spec.get(key)
        label = symbol if value is None else f"{symbol} = {value:g} kg"
        ax.text(x, y, label, ha="center", va="center", fontsize=8.5, color="black")
    coefficient = next((key for key in ("mu_s", "mu_k") if key in spec), None)
    if coefficient:
        symbol = r"$\mu_s$" if coefficient == "mu_s" else r"$\mu_k$"
        value = spec[coefficient]
        label = symbol if value is None else f"{symbol} = {value:.4f}"
    else:
        label = "Frictionless"
    ax.text(.9, .45, label, ha="center", va="center", fontsize=8.5, color="black")
    ax.set(xlim=(-.15, 3.35), ylim=(-.65, 1.85), aspect="equal")
    ax.axis("off")
    _fit_labels(fig, ax)
    return fig

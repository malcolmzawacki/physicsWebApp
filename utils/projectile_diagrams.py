"""Scale-aware trajectories reconstructed only from printed givens.

Unknowns have no numeric labels or coordinate ticks, but their approximate
proportions are visible. Extreme aspect ratios receive an explicit scale note.
"""
import math

import numpy as np
from matplotlib.figure import Figure


# Practical vertical extent / horizontal range. Apply the smallest adjustment
# outside this band; inside it a metre has the same length in both directions.
MIN_HEIGHT_RATIO = .08
MAX_HEIGHT_RATIO = 1.0


def trajectory_from_givens(data):
    """Reconstruct motion without reading organizer/answer data (g=10).

    Elevated landings use the later crossing. The first crossing, when given,
    is a separate event on the ascending trajectory.
    """
    g, scene = data["givens"], data["scene"]
    if scene == "horizontal":
        vy = 0.
        if "vf" in g:
            vx = g["vf"] * math.cos(math.radians(g["af"]))
            time = g["vf"] * math.sin(math.radians(g["af"])) / 10
        elif "vx" in g:
            vx = g["vx"]
            time = g["x"] / vx if "x" in g else math.sqrt(g["h"] / 5)
        else:
            time = math.sqrt(g["h"] / 5)
            vx = g["x"] / time if "x" in g else 10*time / math.tan(math.radians(g["af"]))
        y0 = 5*time*time
    elif scene == "level":
        vy = math.sqrt(20*g["hmax"]) if "hmax" in g else g["vi"]*math.sin(math.radians(g["ai"]))
        time = vy / 5
        vx = (g["x"] / time if "x" in g else
              vy / math.tan(math.radians(g["ai"])) if "ai" in g else
              math.sqrt(g["vi"]**2-vy**2))
        y0 = 0.
    else:
        vy = ((g["h"]+5*g["tfirst"]**2)/g["tfirst"] if "tfirst" in g else
              g["vi"]*math.sin(math.radians(g["ai"])))
        vx = math.sqrt(g["vi"]**2-vy**2)
        if "h" in g:
            change = -g["h"] if scene == "down" else g["h"]
            time = (vy+math.sqrt(max(0., vy*vy-20*change))) / 10
        else:
            time = g["x"] / vx
            change = vy*time-5*time*time
        y0 = -change if scene == "down" else 0.
    total_x = vx*time
    y1 = y0+vy*time-5*time*time
    peak_time = min(time, max(0., vy/10))
    peak_y = y0+vy*peak_time-5*peak_time**2
    edge_x = (total_x-g["x"] if data["launch_behind_edge"] else
              total_x-g.get("inroad", 0.) if scene == "up" else 0.)
    # Rounding printed angles can put a nominally zero setback below zero.
    edge_x = min(total_x, max(0., edge_x))
    if not all(math.isfinite(v) for v in (vx, vy, time, total_x, peak_y)) or total_x <= 0 or time <= 0:
        raise ValueError("Projectile givens must describe a finite forward flight.")
    return dict(vx=vx, vy=vy, time=time, range=total_x, y0=y0, y1=y1,
                peak_time=peak_time, peak_y=peak_y, edge_x=edge_x)


def diagram_geometry(data):
    """Normalize absolute size, then bound aspect ratio without cropping flight."""
    motion = trajectory_from_givens(data)
    height = motion["peak_y"]-min(motion["y0"], motion["y1"])
    ratio = height/motion["range"]
    if not math.isfinite(ratio) or ratio <= 0:
        raise ValueError("Projectile flight must have a positive vertical extent.")
    displayed_ratio = min(MAX_HEIGHT_RATIO, max(MIN_HEIGHT_RATIO, ratio))
    stretch = displayed_ratio/ratio
    return dict(motion=motion, vertical_factor=stretch,
                mode="equal" if MIN_HEIGHT_RATIO <= ratio <= MAX_HEIGHT_RATIO else "adjusted",
                x_scale=8/motion["range"], y_scale=8/motion["range"]*stretch)


def projectile_figure(data):
    geometry = diagram_geometry(data)
    m = geometry["motion"]
    sx, sy = geometry["x_scale"], geometry["y_scale"]
    g, scene = data["givens"], data["scene"]
    ink, blue, teal = "#243247", "#2563a6", "#087f8c"
    figure = Figure(figsize=(11, 5.7), facecolor="white")
    ax = figure.add_axes((.04, .22, .66, .60))
    ax.set_facecolor("white")
    y0, y1, peak_y = m["y0"]*sy, m["y1"]*sy, m["peak_y"]*sy
    edge = m["edge_x"]*sx
    ax.set(xlim=(-1., 10.), ylim=(-1.25, peak_y+1.25), aspect="equal")
    ax.set_axis_off()
    t = np.linspace(0, m["time"], 201)
    ax.plot(m["vx"]*t*sx, (m["y0"]+m["vy"]*t-5*t*t)*sy,
            color=blue, lw=2.3, linestyle=(0, (4, 3)))
    if scene in ("horizontal", "down", "up"):
        ground_x, ground_y = [-.65, edge, edge, 8.6], [y0, y0, y1, y1]
    else:
        ground_x, ground_y = [-.65, 8.6], [y0, y1]
    ax.plot(ground_x, ground_y, color=ink, lw=2)
    ax.fill_between(ground_x, ground_y, -.12, color="#e5eaf0", zorder=0)

    def number(key):
        return f"{g[key]:.4f}".rstrip("0").rstrip(".")

    def text(x, y, label, **kwargs):
        return ax.text(x, y, label, fontsize=10, color=ink,
                       bbox=dict(facecolor="white", edgecolor="none", alpha=.94, pad=2), **kwargs)

    def dimension(a, z, label):
        vertical = a[0] == z[0]
        if math.dist(a, z) < .3:
            # Arrowheads would overlap on very short distances. Use end caps.
            ax.plot([a[0], z[0]], [a[1], z[1]], color=teal, lw=1.4)
            for px, py in (a, z):
                ax.plot([px-.06, px+.06] if vertical else [px, px],
                        [py, py] if vertical else [py-.06, py+.06], color=teal, lw=1.4)
        else:
            ax.annotate("", xy=z, xytext=a,
                        arrowprops=dict(arrowstyle="<->", color=teal, lw=1.4))
        text((a[0]+z[0])/2+(.12 if vertical else 0),
             (a[1]+z[1])/2+(0 if vertical else -.14), label,
             ha="left" if vertical else "center", va="center" if vertical else "top")

    for px, py, label in ((0., y0, "Launch"), (8., y1, "Landing")):
        ax.scatter([px], [py], s=40, color=blue, zorder=5)
        if px == 0:
            text(px, py+.23, label, ha="right", va="bottom")
        else:
            text(px-.12, py+.18, label, ha="right", va="bottom")
    if "h" in g:
        dimension((8.9, min(y0, y1)), (8.9, max(y0, y1)), f"h = {number('h')} m")
    if "x" in g:
        a, z = (edge, 8.) if scene in ("horizontal", "down") else (0., edge) if scene == "up" else (0., 8.)
        dimension((a, -.55), (z, -.55), f"Horizontal distance\nx = {number('x')} m")
    if "inroad" in g:
        dimension((edge, y1-.55), (8., y1-.55), f"Beyond edge\n{number('inroad')} m")
    if "hmax" in g:
        peak_x = m["vx"]*m["peak_time"]*sx
        dimension((peak_x, y0), (peak_x, peak_y), f"hₘₐₓ = {number('hmax')} m")

    def velocity_arrow(px, py, vy):
        dx, dy = m["vx"]*sx, vy*sy
        length = math.hypot(dx, dy)
        ax.annotate("", xy=(px+.95*dx/length, py+.95*dy/length), xytext=(px, py),
                    arrowprops=dict(arrowstyle="->", color=teal, lw=2))

    if any(key in g for key in ("vi", "vx", "ai")):
        velocity_arrow(0., y0, m["vy"])
    if any(key in g for key in ("vf", "af")):
        velocity_arrow(8., y1, m["vy"]-10*m["time"])
    if "tfirst" in g:
        point = (m["vx"]*g["tfirst"]*sx, y1)
        ax.scatter(*point, s=35, facecolors="white", edgecolors=teal, zorder=5)
        ax.annotate("First at cliff height", xy=point, xytext=(.06, .96),
                    textcoords="axes fraction", fontsize=9, color=ink,
                    arrowprops=dict(arrowstyle="->", color=teal),
                    bbox=dict(facecolor="white", edgecolor="none", pad=2))

    # Fixed figure coordinates keep labels clear of the path as its shape changes.
    labels = []
    names = {"vi": ("Speed", "m/s"), "vx": ("Horizontal speed", "m/s"),
             "ai": ("Angle above horizontal", "°"), "vf": ("Speed", "m/s"),
             "af": ("Angle below horizontal", "°"), "tfirst": ("Time", "s")}
    for keys, heading in ((("vi", "vx", "ai"), "At launch"), (("vf", "af"), "At landing"),
                          (("tfirst",), "First at cliff height")):
        lines = [f"{names[key][0]}\n{number(key)} {names[key][1]}" for key in keys if key in g]
        if lines:
            labels.append(heading+"\n"+"\n\n".join(lines))
    figure.text(.75, .78, "\n\n".join(labels), fontsize=10, color=ink, va="top", linespacing=1.4)
    figure.text(.06, .94, "Projectile motion · given information", color=ink, fontsize=14)
    if geometry["mode"] == "equal":
        note = "Same scale horizontally and vertically · proportions preserved"
        detail = "Only given values are labeled. The drawing is approximate; use the given values for calculations."
    else:
        factor = geometry["vertical_factor"]
        action = "enlarged" if factor > 1 else "compressed"
        amount = factor if factor > 1 else 1/factor
        note = f"Vertical distances {action} ×{amount:,.1f} to keep the flight visible"
        detail = "Horizontal and vertical scales differ; angles are not to scale. Only given values are labeled."
    figure.text(.06, .105, note, color=ink, fontsize=10, weight="bold")
    figure.text(.06, .055, detail, color="#526174", fontsize=9)
    return figure

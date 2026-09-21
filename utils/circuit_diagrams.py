"""Shared circuit geometry for interactive and printable diagrams."""

def draw_series(drawing, elm, diagram: dict) -> None:
    battery_cls = getattr(elm, "BatteryCell", getattr(elm, "Battery", None))
    if battery_cls is None:
        raise RuntimeError("schemdraw battery element was not available")
    battery = drawing.add(battery_cls().up().label(diagram["source_label"], loc="left"))
    top_wire = elm.Line().right().length(0.9)
    if diagram["wire_label"]:
        top_wire = top_wire.label(diagram["wire_label"], loc="top")
    drawing.add(top_wire)
    for resistor_label in diagram["resistor_labels"]:
        drawing.add(elm.Resistor().right().label(resistor_label))
        drawing.add(elm.Line().right().length(0.9))
    drawing.add(elm.Line().down().length(2.0))
    drawing.add(elm.Line().tox(battery.start))
    drawing.add(elm.Line().toy(battery.start))


def draw_parallel(drawing, elm, diagram: dict) -> None:
    battery_cls = getattr(elm, "BatteryCell", getattr(elm, "Battery", None))
    if battery_cls is None:
        raise RuntimeError("schemdraw battery element was not available")
    battery = drawing.add(battery_cls().up().label(diagram["source_label"], loc="left"))
    drawing.add(elm.Line().right().length(2.6))
    drawing.push()
    r1 = drawing.add(elm.Resistor().down().label(diagram["resistor_labels"][0], loc="left"))
    drawing.add(elm.Line().to(battery.start))
    drawing.pop()
    drawing.add(elm.Line().right().length(3.0))
    drawing.add(elm.Resistor().down().label(diagram["resistor_labels"][1], loc="right"))
    drawing.add(elm.Line().to(r1.end))



def circuit_figure(diagram):
    import schemdraw
    import schemdraw.elements as elm
    from matplotlib.figure import Figure
    figure = Figure(figsize=(7, 4), facecolor="white")
    axes = figure.add_subplot(111, facecolor="white")
    drawing = schemdraw.Drawing(canvas=axes, show=False, color="black", bgcolor="white")
    if diagram.get("kind") == "parallel":
        draw_parallel(drawing, elm, diagram)
    else:
        draw_series(drawing, elm, diagram)
    drawing.draw(show=False)
    bounds = drawing.get_bbox()
    axes.set_xlim(bounds.xmin - .3, bounds.xmax + .3)
    axes.set_ylim(bounds.ymin - .3, bounds.ymax + .3)
    axes.set_aspect("equal")
    axes.axis("off")
    return figure

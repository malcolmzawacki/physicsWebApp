"""Explicit bridges from custom activity cases to the shared payload contract."""
from functools import partial
from utils.problem_payload import payload_from_dict


def with_diagram_renderer(problem, generator, problem_type, difficulty="Medium"):
    result = dict(problem)
    result["problem_type"] = problem_type
    result["difficulty"] = difficulty
    result["diagram_renderer"] = partial(generator.generate_diagram,
        problem_type=problem_type, difficulty=difficulty)
    payload_from_dict(result)
    return result


def circuit_payload(case):
    from utils.circuit_diagrams import circuit_figure
    from utils.grading import CIRCUIT_POLICY
    question = case["prompt"] + "\n\n" + "\n".join(f"- {label}: {value}" for label, value in case["givens"])
    result = dict(question=question, answers=[case["answer"]],
        units=[f"{case['answer_label']} ({case['unit']})"],
        problem_type=case["problem_type"], difficulty=case["difficulty"],
        diagram_data=case["diagram"], diagram_renderer=circuit_figure,
        explanation=case["explanation"], grading=dict(CIRCUIT_POLICY))
    payload_from_dict(result)
    return result


def matching_payload(case):
    """Combine primary and labeled option diagrams for standard UI/export."""
    import io
    import matplotlib.image as mpimg
    from matplotlib.figure import Figure
    options = case["option_diagrams"]
    labels = case.get("choice_labels") or [chr(65 + i) for i in range(len(options))]
    if not options or len(labels) != len(options) or not 0 <= case["correct_index"] < len(options):
        raise ValueError("Matching cases require options, matching labels and a valid correct index")
    figure = Figure(figsize=(max(6, len(options) * 2.5), 5))
    grid = figure.add_gridspec(2, len(options))
    sources = [(case["primary_diagram"], figure.add_subplot(grid[0, :]), "Question")]
    sources += [(source, figure.add_subplot(grid[1, i]), f"Option {labels[i]}") for i, source in enumerate(options)]
    for source, ax, title in sources:
        buffer = io.BytesIO()
        source.savefig(buffer, format="png", bbox_inches="tight")
        buffer.seek(0)
        ax.imshow(mpimg.imread(buffer))
        ax.axis("off")
        ax.set_title(title)
    figure.tight_layout()
    return dict(question=case.get("prompt", "Select the matching diagram."),
        answers=[labels[case["correct_index"]]], units=["Option"],
        button_options={0: labels}, diagram_data=figure)

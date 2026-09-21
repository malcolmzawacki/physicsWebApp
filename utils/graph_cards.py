"""Local clickable graph board, compatible with Streamlit components v1."""
import base64
import io
from pathlib import Path
import streamlit.components.v1 as components

_board = components.declare_component("graph_cards", path=str(Path(__file__).with_name("graph_cards_frontend")))


def prepare_images(payload):
    """Encode once per question, keeping original figures available for export."""
    import matplotlib.pyplot as plt
    images = []
    for figure in [payload['primary_diagram'], *payload['option_diagrams']]:
        buffer = io.BytesIO()
        figure.savefig(buffer, format="png", dpi=130, bbox_inches="tight", facecolor="white")
        images.append("data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii"))
        plt.close(figure)
    return images


def selected_index(event, question_id, count):
    """Ignore stale or malformed browser values instead of scoring another question."""
    if not isinstance(event, dict) or event.get("question_id") != question_id:
        return None
    index = event.get("index")
    return index if type(index) is int and 0 <= index < count else None


def graph_cards(images, labels, question_id, selection, locked, layout, key, correct_index=None):
    return _board(images=images, labels=labels, question_id=question_id,
                  selection=selection, locked=locked, layout=layout,
                  correct_index=correct_index if locked else None, key=key, default=None)

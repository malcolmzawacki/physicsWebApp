import matplotlib.pyplot as plt
from docx.shared import Inches
import io


def embed_graph_in_doc(target, fig, width_inches=5):
    """Generic function to embed any matplotlib figure in a Word doc or cell."""
    image = io.BytesIO()
    fig.savefig(image, format="png", dpi=200, bbox_inches='tight')
    plt.close(fig)
    image.seek(0)

    if hasattr(target, "add_picture"):
        target.add_picture(image, width=Inches(width_inches))
    else:
        paragraph = target.add_paragraph()
        run = paragraph.add_run()
        run.add_picture(image, width=Inches(width_inches))

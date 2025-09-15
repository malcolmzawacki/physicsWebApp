import matplotlib.pyplot as plt
from docx.shared import Inches
import os
import uuid


def embed_graph_in_doc(doc, fig, width_inches=5):
    """Generic function to embed any matplotlib figure in a Word doc"""
    # Generate unique filename to avoid conflicts
    filename = f"temp_graph_{uuid.uuid4().hex[:8]}.png"
    
    # Save the figure
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)  # Close to free memory
    
    # Add to document
    doc.add_picture(filename, width=Inches(width_inches))
    
    # Clean up
    os.remove(filename)
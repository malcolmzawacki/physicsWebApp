"""Compact question headings and optional instructions for force activities."""
import re

import streamlit as st
from utils.ui_components import render_header


def force_activity_header(title, stars):
    st.html("""<style>
        [data-testid="stMainBlockContainer"]:has(.st-key-force_activity_header) {
            padding-top: 3.5rem;
        }
        [data-testid="stMainBlockContainer"]:has(.st-key-force_activity_header) > [data-testid="stVerticalBlock"] {
            gap: .65rem;
        }
        .st-key-force_activity_header h1 {
            padding-block: .25rem .5rem;
        }
        .st-key-force_activity_reference [data-testid="stImage"] {
            max-width: 170px;
        }
    </style>""")
    with st.container(key="force_activity_header"):
        render_header(title, stars)


def question_title(title, *help_paragraphs):
    """Use Streamlit's small hover-help icon beside the scenario title."""
    help_text = "\n\n".join(paragraph for paragraph in help_paragraphs if paragraph)
    st.markdown(f"**{title}**", help=help_text or None, width="content")


def separate_assumptions(prompt):
    """Move standalone modeling notes, retaining the physical situation verbatim."""
    main, notes = [], []
    for sentence in re.split(r"(?<=[.!?])\s+", prompt):
        if sentence.startswith(("Ignore ", "Air resistance is ignored.",
                                "Its initial velocity is not supplied.")):
            notes.append(sentence)
        else:
            main.append(sentence)
    return " ".join(main), " ".join(notes)

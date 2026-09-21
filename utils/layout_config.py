"""Shared layout adjusters. Values are relative shares, not pixel widths.

Increase DIFFICULTY_WIDTH to give Medium more room on all question control rows.
The other shares determine how much of the remaining row each selector receives.
Streamlit handles stacking at narrow viewport widths.
"""
PROBLEM_TYPE_WIDTH = 3
DIFFICULTY_WIDTH = 1.2
SOLVE_FOR_WIDTH = 4
CONTROL_GAP = "small"

EQUATION_EXPANDER_WIDTH = 5
EQUATION_TOGGLE_WIDTH = 1.5


def question_columns():
    import streamlit as st
    return st.columns([PROBLEM_TYPE_WIDTH, DIFFICULTY_WIDTH, SOLVE_FOR_WIDTH],
                      gap=CONTROL_GAP, vertical_alignment="bottom")

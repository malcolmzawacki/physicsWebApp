import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.ui import ui
from utils.generators.energy_generator import EnergyGenerator
from utils.generators.linear_motion_generator import LinearMotionGenerator


def input_plot(start = 2.8,end = 4,accuracy=0.001,reps=600,numtoplot=200):
    interval = (start, end)  # start, end
    lims = np.zeros(reps)
    numtoplot = reps - 1
    fig, biax = plt.subplots()
    fig.set_size_inches(16, 9)

    lims[0] = np.random.rand()
    size_of_marker =0.02
    for r in np.arange(interval[0], interval[1], accuracy):
        for i in range(reps - 1):
            lims[i + 1] = r * lims[i] * (1 - lims[i])

        biax.plot([r] * numtoplot, lims[reps - numtoplot :], "y.", markersize=size_of_marker)

    biax.set(xlabel="r", ylabel="x", title="logistic map")
    plt.style.use("dark_background")
    return fig

def main():
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        start = st.number_input("start value",-2.0,3.9,-1.0,0.1)
    with col2:
        end = st.number_input("end value",-2.0,4.0,1.0,0.1)
    with col3:
        accuracy = st.number_input("accuracy",0.001,0.1,0.001,0.001)
    with col4:
        reps = st.number_input("reps",200,1000,800,10)
    with col5:
        numtoplot = st.number_input("number to plot",10,500,300,10)
    fig = input_plot(start,end,accuracy,reps,numtoplot)
    st.pyplot(fig)

class energy_basics:

    @staticmethod
    def question_parameters():
        """Holds current options for questions for centralized updating"""
        problem_type_dict = {
                "One Dimensional": {
                      "honors": r"""
                      \textrm{distance } =\; d_1 + d_2 + ... \newline ~ \newline
                      \textrm{displacement } =\; d_{final} - d_{initial} \; \textrm{(with direction)}
                      """,

                      "conceptual": r"""
                      \textrm{distance } =\; d_1 + d_2 + ... 
                      
                     \newline ~ \newline \textrm{"Positive" directions are right, East, up, and North}
                     \newline ~ \newline \textrm{"Negative" directions are left, West, down, and South}
                     \newline ~ \newline \textrm{displacement } =\; d_{final} - d_{initial} \; \textrm{(with direction)}
                      """},
                "Two Dimensional": {
                      "honors": r"""
                      \textrm{distance } =\; d_1 + d_2 + ... \newline ~ \newline
                    \textrm{displacement } =\; \sqrt{d_{horizontal}^2 + d_{vertical}^2} \;\; \textrm{(with direction)}
                      """,

                      "conceptual": r"""
                      \textrm{distance } =\; d_1 + d_2 + ... \newline ~ \newline
                      \textrm{Horizontal Displacement } =\; D_{East} - D_{West} \newline ~ \newline
                      \textrm{Vertical Displacement } =\; D_{North} - D_{South} \newline ~ \newline
                    \textrm{Net Displacement } =\; \sqrt{D_{horizontal}^{\;2} + D_{vertical}^2} \;\; \textrm{(with direction)}
                      """},
                
                }
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, difficulties
    
    @staticmethod
    def main():
        prefix = "energy_basics"
        title = "Types of Energy"
        problem_type_dict, difficulties = energy_basics.question_parameters()
        generator = LinearMotionGenerator()
        ui = ui(prefix,title,generator,problem_type_dict,difficulties)
        ui.diagram_layout()

if __name__ == "__main__":
    energy_basics.main()
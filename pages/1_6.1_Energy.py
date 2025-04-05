import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))
from utils.generators.energy_generator import EnergyGenerator
from utils.rendering import rendering
from utils.word_lists import random_error_message
from utils.word_lists import random_correct_message



class energy_basics:

    @staticmethod
    def question_parameters():
        """Holds current options for questions for centralized updating"""
        problem_type_dict = {
            "Elastic Potential Energy": {
                "honors" : r"EPE = \frac{1}{2} k \Delta x^2", 
                "conceptual": r"""EPE = \frac{1}{2} k \Delta x^2 \;\; , 
                \;\; k = \frac{2 \cdot EPE}{\Delta x^2} \;\; , 
                \;\; \Delta x = \sqrt{\frac{2 \cdot EPE}{k}}"""
                },
            "Kinetic Energy": {
                "honors": r"KE = \frac{1}{2} m v^2",
                "conceptual": r"""KE = \frac{1}{2} m v^2\;\; ,
                \;\; m = \frac{2KE}{v^2} \;\; ,
                \;\; v = \sqrt{\frac{2KE}{m}}"""
            },               
            "Gravitational Potential Energy" : {
                "honors": r"GPE = mgh",
                "conceptual": r"""GPE = mgh\;\; ,
                \;\; m = \frac{GPE}{gh} \;\; ,
                \;\; h = \frac{GPE}{mg}"""
            },
            "Work": {
                "honors": r"W = Fd",
                "conceptual": r"""W = Fd\;\; ,
                \;\; F = \frac{W}{d} \;\; ,
                \;\; d = \frac{W}{F}"""
            },
            }
        problem_types = list(problem_type_dict.keys())
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, problem_types, difficulties
    @staticmethod
    def main():
        prefix = "energy_basics"
        problem_type_dict, problem_types, difficulties = energy_basics.question_parameters()
        render = rendering()
        generator = EnergyGenerator()
        
        render.initialize_session_state(prefix, problem_types, difficulties)
        render.header(prefix,"Types of Energy")
        performance = st.session_state[f"{prefix}_performance"]
        render.question_options_1(prefix,problem_type_dict,difficulties,generator)
        render.question_ui_4(prefix, problem_type_dict, problem_types ,difficulties, generator)
        render.footer_1(prefix,generator,performance)



class energy_conservation:

    @staticmethod
    def question_parameters():
        """Holds current options for questions for centralized updating"""
        problem_type_dict = {
            "Elastic <--> Kinetic": {
                "honors": r"\frac{1}{2} m v^2 = \frac{1}{2} k \Delta x^2",
                "conceptual": r""" m = k \cdot \left( \frac{ \Delta x}{v} \right)^2 \;\; ,
                \;\; v = \Delta x \cdot \sqrt{\frac{k}{m}} \;\; ,
                \;\; k = m \cdot \left( \frac{v}{ \Delta x} \right)^2 \;\; ,
                \;\; \Delta x = v \cdot \sqrt{\frac{m}{k}}"""
                },
            "Gravitational <--> Kinetic": {
                "honors": r"mgh = \frac{1}{2} m v^2",
                "conceptual": r"""h = \frac{v^2}{2g} \;\;,
                 \;\; v = \sqrt{2gh}"""
                },
            "Gravitational <--> Elastic" : {
                "honors": r"mgh = \frac{1}{2} k \Delta x^2",
                "conceptual": r"""m = \frac{k \Delta x^2}{2gh}\;\;,
                \;\; h = \frac{k \Delta x^2}{2mg} \;\;,
                \;\; k = \frac{2mgh}{\Delta x^2}\;\;,
                \;\; \Delta x = \sqrt{\frac{2mgh}{k}}"""
                                            }
            }
        problem_types = list(problem_type_dict.keys())
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, problem_types, difficulties
    
    @staticmethod
    def main():
        prefix = "energy_conservation"
        problem_type_dict, problem_types, difficulties = energy_conservation.question_parameters()
        render = rendering()
        generator = EnergyGenerator()
        render.initialize_session_state(prefix, problem_types, difficulties)
        performance = st.session_state[f"{prefix}_performance"]
        render.subheader_ui(prefix,performance)
        render.question_ui_3(prefix, problem_type_dict, problem_types ,difficulties, generator)

# for updating thermal as backend is completed
def question_parameters():
        """Holds current options for questions for centralized updating"""
        problem_type_dict = {
            "Quantifying Thermal Energy": {
                "honors": r"\Delta E = W_f",
                "conceptual": r"""\Delta E = W_f \;\; ,
                \;\; E_i = E_f + W_f \;\; ,
                \;\; E_f = E_i - W_f \;\;
                """
                },
            "Friction and Distance": {
                "honors": r"W_f = F_f \; x",
                "conceptual": r"""W_f = F_f \; x \;\;,
                 \;\ x = \frac{W_f}{F_f} \;\;
                 \;\; F_f = \frac{W_f}{x}"""
                },
            "Coefficient of Friction" : {
                "honors": r"F_f = \mu F_n",
                "conceptual": r"""F_f = \mu m g\;\;,
                \;\; m = \frac{F_f}{\mu g} \;\;,
                \;\; \mu = \frac{F_f}{mg}
                """
                                            }
            }
        problem_types = list(problem_type_dict.keys())
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, problem_types, difficulties


class thermal:
    @staticmethod
    def question_parameters():
        """Holds current options for questions for centralized updating"""
        problem_type_dict = {
            "Quantifying Thermal Energy": {
                "honors": r"\Delta E = W_f",
                "conceptual": r"""W_f = E_f - E_i\;\;
                \newline ~ \newline ~ \newline
                EPE = \frac{1}{2} k \Delta x^2 \quad ,
                \quad KE = \frac{1}{2} m v^2 \quad ,
                \quad GPE = mgh
                """
                },
                "Friction and Distance": {
                "honors": r"W_f = F_f \; x",
                "conceptual": r"""W_f = F_f \; x \;\;,
                 \;\ x = \frac{W_f}{F_f} \;\;
                 \;\; F_f = \frac{W_f}{x}"""
                },
            }
        problem_types = list(problem_type_dict.keys())
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, problem_types, difficulties

    @staticmethod
    def main():
        st.title("Thermal Energy")
        prefix = "thermal"
        problem_type_dict, problem_types, difficulties = thermal.question_parameters()
        render = rendering()
        generator = EnergyGenerator()
        render.initialize_session_state(prefix, problem_types, difficulties)
        performance = st.session_state[f"{prefix}_performance"]
        render.subheader_ui(prefix,performance)
        render.question_ui_3(prefix, problem_type_dict, problem_types ,difficulties, generator)


def main():
    # Add tabs for quiz and explorer modes
    tab1, tab2, tab3 = st.tabs(["Types of Energy", "Conservation of Energy","Thermal Energy"])  
    
    with tab1:
        energy_basics.main()
    with tab2:
        energy_conservation.main()
    with tab3:
        thermal.main()

if __name__ == "__main__":
    main()
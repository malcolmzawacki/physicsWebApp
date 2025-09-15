import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))
from utils.generators.energy_generator import EnergyGenerator
from utils.ui import interface



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
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, difficulties
    @staticmethod
    def main():
        title = "Types of Energy"
        prefix = "energy_basics"
        problem_type_dict, difficulties = energy_basics.question_parameters()
        generator = EnergyGenerator()
        ui = interface(prefix,title,generator,problem_type_dict,difficulties)
        ui.unified_smart_layout()



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
       
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, difficulties
    
    @staticmethod
    def main():
        title = "Conservation of Energy"
        prefix = "energy_conservation"
        problem_type_dict, difficulties = energy_conservation.question_parameters()
        generator = EnergyGenerator()
        
        ui = interface(prefix,title,generator,problem_type_dict,difficulties)
        ui.unified_smart_layout()

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
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, difficulties


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
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, difficulties

    @staticmethod
    def main():
        title = "Thermal Energy"
        prefix = "thermal"
        problem_type_dict, difficulties = thermal.question_parameters()
        generator = EnergyGenerator()
        ui = interface(prefix,title,generator,problem_type_dict,difficulties)
        ui.unified_smart_layout()

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
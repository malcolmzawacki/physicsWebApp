import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.ui import interface

def wave_properties():
        
    problem_type_dict = {
        "Wave Properties": {
                "honors": r"""v \;=\; \lambda f
                \quad , \quad T \;=\; \frac{1}{f}""",

                "conceptual": r"""v \;=\; \lambda f \quad , \quad
                \lambda \;=\; \frac{v}{f} \quad , \quad
                f \;=\; \frac{v}{\lambda}
                \newline ~ \newline
                T \;=\; \frac{1}{f}
                \quad , \quad f \;=\; \frac{1}{T}
                """},
        "deciBel Scale": {
            "honors": r"""\textrm{Multplying the intensity by 10 adds 10 on the deciBel scale}""",
            "conceptual": r"""\textrm{Multplying the intensity by 10 adds 10 on the deciBel scale}"""
        }
        }
    
    difficulties = ["Easy"]

    from utils.generators.waves_generator import WaveGenerator
    title = "Wave Properties"
    prefix = "wave_properties"
    ui = interface(prefix,title,WaveGenerator(),
                    problem_type_dict,difficulties,True)
    ui.default_layout()


def Harmonics():
        
    problem_type_dict = {
        "String Harmonics": {
                "honors": r"""v \;=\; \lambda f
                \quad , \quad \lambda \;=\; \frac{2L}{m}
                \quad , \quad m = 1, 2, 3 ...
                \newline ~ \newline
                \textrm{speed of sound } \approx 343 \frac{m}{s}""",

                "conceptual": r"""v \;=\; \lambda f \quad , \quad
                \lambda \;=\; \frac{v}{f} \quad , \quad
                f \;=\; \frac{v}{\lambda}
                \newline ~ \newline
                \lambda \;=\; \frac{2L}{m}
                \quad , \quad f = \frac{vm}{2L}
                \quad , \quad L = \frac{vm}{2f}
                \quad , \quad L = \frac{m \lambda}{2}
                \quad , \quad m = 1, 2, 3 ...
                \newline ~ \newline
                \textrm{speed of sound }\approx 343 \frac{m}{s}
                """},
        "Open Ended Column Harmonics": {
                "honors": r"""v \;=\; \lambda f
                \quad , \quad \lambda \;=\; \frac{2L}{m}
                \quad , \quad m = 1, 2, 3 ...
                \newline ~ \newline
                \textrm{speed of sound } \approx 343 \frac{m}{s}""",

                "conceptual": r"""v \;=\; \lambda f \quad , \quad
                \lambda \;=\; \frac{v}{f} \quad , \quad
                f \;=\; \frac{v}{\lambda}
                \newline ~ \newline
                \lambda \;=\; \frac{2L}{m}
                \quad , \quad f = \frac{vm}{2L}
                \quad , \quad L = \frac{vm}{2f}
                \quad , \quad L = \frac{m \lambda}{2}
                \quad , \quad m = 1, 2, 3 ...
                \newline ~ \newline
                \textrm{speed of sound }\approx 343 \frac{m}{s}
                """},
        "Closed End Column Harmonics": {
                "honors": r"""v \;=\; \lambda f
                \quad , \quad \lambda \;=\; \frac{4L}{m}
                \quad , \quad m = 1, 3, 5 ...
                \newline ~ \newline
                \textrm{speed of sound } \approx 343 \frac{m}{s}""",

                "conceptual": r"""v \;=\; \lambda f \quad , \quad
                \lambda \;=\; \frac{v}{f} \quad , \quad
                f \;=\; \frac{v}{\lambda}
                \newline ~ \newline
                \lambda \;=\; \frac{4L}{m}
                \quad , \quad f = \frac{vm}{2L}
                \quad , \quad L = \frac{vm}{2f}
                \quad , \quad L = \frac{m \lambda}{2}
                \quad , \quad m = 1, 3, 5 ...
                \newline ~ \newline
                \textrm{speed of sound }\approx 343 \frac{m}{s}
                """},
        }
    
    difficulties = ["Easy","Medium","Hard"]

    from utils.generators.waves_generator import WaveGenerator
    title = "Harmonics"
    prefix = "harmonics"
    ui = interface(prefix,title,WaveGenerator(),
                    problem_type_dict,difficulties,True)
    ui.default_layout()

def main():
    tab1,tab2 = st.tabs(["Wave Properties","Harmonics"])
    with tab1:
        wave_properties()
    with tab2:
        Harmonics()

if __name__ == "__main__":
    main()
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
        }
    
    difficulties = ["Easy"]

    from utils.generators.waves_generator import WaveGenerator
    title = "Wave Properties"
    prefix = "wave_properties"
    ui = interface(prefix,title,WaveGenerator(),
                    problem_type_dict,difficulties,True)
    ui.default_layout()

def main():
    tab1,tab2 = st.tabs(["Wave Properties","TBD"])
    with tab1:
        wave_properties()
    with tab2:
        pass

if __name__ == "__main__":
    main()
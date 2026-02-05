from utils.ui import interface
from tools.loading import lazy_tabs

# region older layout

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
    ui.unified_smart_layout()


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
                \quad , \quad f = \frac{vm}{4L}
                \quad , \quad L = \frac{vm}{4f}
                \quad , \quad L = \frac{m \lambda}{4}
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
    ui.unified_smart_layout()

def deciBel_practice():
        
    problem_type_dict = {
        "deciBel Scale": {
            "honors": r"""\textrm{Multplying the intensity by 10 adds 10 on the deciBel scale}
            \newline ~ \newline
            \textrm{Intensity changes with the distance SQUARED, not just distance}""",
            "conceptual": r"""\textrm{Multplying the intensity by 10 adds 10 on the deciBel scale}
            \newline ~ \newline
            \textrm{Intensity changes with the distance SQUARED, not just distance}"""
        }
        }
    
    difficulties = ["Easy","Medium"]

    from utils.generators.waves_generator import WaveGenerator
    title = "deciBel Scale"
    prefix = "deciBels_"
    ui = interface(prefix,title,WaveGenerator(),
                    problem_type_dict,difficulties,True)
    ui.unified_smart_layout()


def main():
    tab_specs = [
        ("Wave Properties", wave_properties),
        ("Harmonics", Harmonics),
        ("deciBel Scale", deciBel_practice),
    ]

    lazy_tabs(tab_specs, state_key="waves_tabs", auto_load_first=True)
# endregion


def main2():
    from utils.generators.waves_generator import WaveGenerator
    prefix ="waves_"
    title = "Waves"
    generator = WaveGenerator()
    metadata = generator.stored_metadata()
    difficulties = ["Easy","Medium","Hard"]

    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()
    

if __name__ == "__main__":
    main()

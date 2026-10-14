from random import randint as ri
from utils.generators.base_generator import BaseGenerator
from utils.quantities import PROFILES, QUANTITIES, equation
from utils.setup_schema import make_setup

class WaveGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="waves_")
    
    
    def choose_problem_dict(self, problem_type: str, difficulty: str):
        if problem_type == "Wave Properties":
            return self.properties_of_waves(difficulty)
        elif problem_type == "String Harmonics":
            return self.string_harmonics(difficulty)
        elif problem_type == "Open Ended Column Harmonics":
            return self.open_column_harmonics(difficulty)
        elif problem_type == "Closed End Column Harmonics":
            return self.closed_column_harmonics(difficulty)
        elif problem_type == "deciBel Scale":
            return self.decibel_scale(difficulty)
        else:
            pass

    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "Wave Properties": {
                "id": "wave.wave-properties",
                "aliases": ["Wave Properties"],
                "honors": equation("wave_properties", r"""${v} = ${wavelength} ${f}
                    \quad , \quad ${T} = \frac{1}{${f}}
                    \quad , \quad ${v} = \frac{${wavelength}}{${T}}"""),
                "conceptual": equation("wave_properties", r"""
                    \begin{gathered}
                    ${v} = ${wavelength} ${f} \quad , \quad
                    ${wavelength} = \frac{${v}}{${f}} \quad , \quad
                    ${f} = \frac{${v}}{${wavelength}} \\
                    ${T} = \frac{1}{${f}} \quad , \quad ${f} = \frac{1}{${T}} \\
                    ${v} = \frac{${wavelength}}{${T}} \quad , \quad
                    ${wavelength} = ${v}${T} \quad , \quad
                    ${T} = \frac{${wavelength}}{${v}}
                    \end{gathered}""")},
            "String Harmonics": {
                "id": "wave.string-harmonics",
                "aliases": ["String Harmonics"],
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
                "id": "wave.open-ended-column-harmonics",
                "aliases": ["Open Ended Column Harmonics"],
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
                "id": "wave.closed-end-column-harmonics",
                "aliases": ["Closed End Column Harmonics"],
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
            "deciBel Scale": {
            "id": "wave.decibel-scale",
            "aliases": ["deciBel Scale"],
            "honors": r"""\textrm{Multplying the intensity by 10 adds 10 on the deciBel scale}
            \newline ~ \newline
            \textrm{Intensity changes with the distance SQUARED, not just distance}""",
            "conceptual": r"""\textrm{Multplying the intensity by 10 adds 10 on the deciBel scale}
            \newline ~ \newline
            \textrm{Intensity changes with the distance SQUARED, not just distance}""",
            },
        }


    
    def properties_of_waves(self, difficulty, *, variant=None):
        """Eight independent given/target forms; difficulty is compatibility-only.

        Mixed practice samples each form equally. Given periods are rounded to
        three decimal places *before* calculating an answer, so the displayed
        information is sufficient and the organizer checks the printed number.
        """
        if variant is not None and (type(variant) is not int or not 0 <= variant < 8):
            raise ValueError("Wave Properties variant must be an integer from 0 to 7")
        frequency = ri(2,100)
        wavelength = ri(2,100)
        speed = wavelength*frequency
        period = round(1 / frequency, 3)
        q_type = ri(0,7) if variant is None else variant
        values = {"v": speed, "wavelength": wavelength, "f": frequency, "T": period}
        if q_type == 0:
            given, target, answer = ("f", "wavelength"), "v", wavelength * frequency
        elif q_type == 1:
            given, target, answer = ("v", "f"), "wavelength", speed / frequency
        elif q_type == 2:
            given, target, answer = ("v", "wavelength"), "f", speed / wavelength
        elif q_type == 3:
            given, target, answer = ("T", "wavelength"), "v", wavelength / period
        elif q_type == 4:
            given, target, answer = ("v", "T"), "wavelength", speed * period
        elif q_type == 5:
            given, target, answer = ("v", "wavelength"), "T", wavelength / speed
        elif q_type == 6:
            given, target, answer = ("f",), "T", 1 / frequency
        else:
            given, target, answer = ("T",), "f", 1 / period

        roles = PROFILES["wave_properties"]
        def label(key):
            return roles[key].name.lower()
        def unit(key):
            return QUANTITIES[roles[key].quantity].unit
        def displayed(key):
            return f"{values[key]:.3f}".rstrip("0").rstrip(".") if key == "T" else str(values[key])
        facts = [f"a {label(key)} of {displayed(key)} {unit(key)}" for key in given]
        question = "A wave has " + " and ".join(facts) + f".\n\nWhat is its {label(target)}?"
        setup = make_setup("wave_properties", values, given, [target])
        return {"question": question, "answers": [answer],
                "units": [f"{roles[target].name} ({unit(target)})"],
                "extras": {"setup": setup, "wave_variant": q_type}}
    
    def string_harmonics(self,difficulty, *, variant=None):
        fundamental_frequency = ri(20,5000)
        velocity = 343
        wavelength = velocity / fundamental_frequency
        string_length = wavelength / 2
        
        if difficulty == "Easy":
            # only working forwards
            q_type = ri(0,3) if variant is None else variant
            if q_type == 0:
                question = f"""What is the wavelength of the first harmonic of a {string_length:.3f} meter long string?"""
                answer = [wavelength]
                unit = ["Wavelength (meters)"]

            elif q_type == 1:
                question = f"What is the fundamental frequency of a {string_length:.3f} meter long string?"
                answer = [fundamental_frequency]
                unit = ["Fundamental Frequency (Hz)"]

            elif q_type == 2:
                question = f"""A string resonates with a fundamental frequency of {fundamental_frequency} Hz.
                How long is the string?"""
                answer = [string_length]
                unit = ["String Length (meters)"]

            elif q_type == 3:
                question = f"""How long would a string have to be to produce a wavelength of {wavelength:.3f} meters for its first harmonic?"""
                answer = [string_length]
                unit = ["String Length (meters)"]

        elif difficulty == "Medium":
            # still forwards, multiple answers
            q_type = ri(0,1) if variant is None else variant
            if q_type == 0:
                question = f"""What are the wavelengths of the first three harmonics of a {string_length:.3f} meter long string?"""
                answer = [wavelength, wavelength/2, wavelength/3]
                unit = ["First Harmonic Wavelength (meters)","Second Harmonic Wavelength (meters)","Third Harmonic Wavelength (meters)"]

            elif q_type == 1:
                question = f"""What are the frequencies of the first three harmonics of a {string_length:.3f} meter long string?"""
                answer = [fundamental_frequency, 2*fundamental_frequency, 3*fundamental_frequency]
                unit = ["Fundamental Frequency (Hz)","Second Harmonic Frequency (Hz)","Third Harmonic Frequency (Hz)"]


        
        elif difficulty == "Hard":
            # lots of working backwards
            q_type = ri(0,1) if variant is None else variant
            if q_type == 0:
                question = f"""The third harmonic of a string is {3*fundamental_frequency:.3f} Hertz. 
                What is the wavelength of the first harmonic? What is the length of the string?"""
                answer = [wavelength, string_length]
                unit = ["Wavelength (meters)","String Length (meters)"]
            elif q_type == 1:
                question = f"""The third harmonic of a string has a wavelength of {wavelength/3:.3f} meters. 
                What is the fundamental frequency? What is the length of the string?"""
                answer = [fundamental_frequency, string_length]
                unit = ["Fundamental Frequency (Hz)","String Length (meters)"]
        question = "Assume a wave speed of 343 m/s. " + question
        return {"question": question, "answers": answer, "units": unit}


    
    def open_column_harmonics(self,difficulty, *, variant=None):
        fundamental_frequency = ri(20,5000)
        velocity = 343
        wavelength = velocity / fundamental_frequency
        open_column_length = wavelength / 2
        
        if difficulty == "Easy":
            # only working forwards
            q_type = ri(0,3) if variant is None else variant
            if q_type == 0:
                question = f"""What is the wavelength of the first harmonic of a {open_column_length:.3f} meter long open-ended column?"""
                answer = [wavelength]
                unit = ["Wavelength (meters)"]

            elif q_type == 1:
                question = f"What is the fundamental frequency of a {open_column_length:.3f} meter long open-ended column?"
                answer = [fundamental_frequency]
                unit = ["Fundamental Frequency (Hz)"]

            elif q_type == 2:
                question = f"""An open-ended column resonates with a fundamental frequency of {fundamental_frequency} Hz.
                How long is the column?"""
                answer = [open_column_length]
                unit = ["Column Length (meters)"]

            elif q_type == 3:
                question = f"""How long would an open-ended column have to be to produce a wavelength of {wavelength:.3f} meters for its first harmonic?"""
                answer = [open_column_length]
                unit = ["Column Length (meters)"]

        elif difficulty == "Medium":
            # still forwards, multiple answers
            q_type = ri(0,1) if variant is None else variant
            if q_type == 0:
                question = f"""What are the wavelengths of the first three harmonics of a {open_column_length:.3f} meter long open-ended column?"""
                answer = [wavelength, wavelength/2, wavelength/3]
                unit = ["First Harmonic Wavelength (meters)","Second Harmonic Wavelength (meters)","Third Harmonic Wavelength (meters)"]

            elif q_type == 1:
                question = f"""What are the frequencies of the first three harmonics of a {open_column_length:.3f} meter long open-ended column?"""
                answer = [fundamental_frequency, 2*fundamental_frequency, 3*fundamental_frequency]
                unit = ["Fundamental Frequency (Hz)","Second Harmonic Frequency (Hz)","Third Harmonic Frequency (Hz)"]


        
        elif difficulty == "Hard":
            # lots of working backwards
            q_type = ri(0,1) if variant is None else variant
            if q_type == 0:
                question = f"""The third harmonic of an open-ended column is {3*fundamental_frequency:.3f} Hertz. 
                What is the wavelength of the first harmonic? What is the length of the open-ended column?"""
                answer = [wavelength, open_column_length]
                unit = ["Wavelength (meters)","Column Length (meters)"]
            elif q_type == 1:
                question = f"""The third harmonic of an open-ended column has a wavelength of {wavelength/3:.3f} meters. 
                What is the fundamental frequency? What is the length of the open-ended column?"""
                answer = [fundamental_frequency, open_column_length]
                unit = ["Fundamental Frequency (Hz)","Column Length (meters)"]
        question = "Assume a wave speed of 343 m/s. " + question
        return {"question": question, "answers": answer, "units": unit}



    
    def closed_column_harmonics(self,difficulty, *, variant=None):
        fundamental_frequency = ri(20,5000)
        velocity = 343
        wavelength = velocity / fundamental_frequency
        closed_column_length = wavelength / 4
        
        if difficulty == "Easy":
            # only working forwards
            q_type = ri(0,3) if variant is None else variant
            if q_type == 0:
                question = f"""What is the wavelength of the first harmonic of a 
                {closed_column_length:.3f} meter long closed-end column?"""
                answer = [wavelength]
                unit = ["Wavelength (meters)"]

            elif q_type == 1:
                question = f"""What is the fundamental frequency of a 
                {closed_column_length:.3f} meter long closed-end column?"""
                answer = [fundamental_frequency]
                unit = ["Fundamental Frequency (Hz)"]

            elif q_type == 2:
                question = f"""An closed-end column resonates with 
                a fundamental frequency of {fundamental_frequency} Hz.
                How long is the column?"""
                answer = [closed_column_length]
                unit = ["Column Length (meters)"]

            elif q_type == 3:
                question = f"""How long would an closed-end column have to be to produce 
                a wavelength of {wavelength:.3f} meters for its first harmonic?"""
                answer = [closed_column_length]
                unit = ["Column Length (meters)"]

        elif difficulty == "Medium":
            # still forwards, multiple answers
            q_type = ri(0,1) if variant is None else variant
            if q_type == 0:
                question = f"""What are the wavelengths of the first three harmonics of a 
                {closed_column_length:.3f} meter long closed-end column?"""
                answer = [wavelength, wavelength/3, wavelength/5]
                unit = ["First Harmonic Wavelength (meters)","Third Harmonic Wavelength (meters)","Fifth Harmonic Wavelength (meters)"]

            elif q_type == 1:
                question = f"""What are the frequencies of the first three harmonics of a 
                {closed_column_length:.3f} meter long closed-end column?"""
                answer = [fundamental_frequency, 3*fundamental_frequency, 5*fundamental_frequency]
                unit = ["Fundamental Frequency (Hz)",
                        "Third Harmonic Frequency (Hz)","Fifth Harmonic Frequency (Hz)"]
        
        elif difficulty == "Hard":
            # lots of working backwards
            q_type = ri(0,1) if variant is None else variant
            if q_type == 0:
                question = f"""The fifth harmonic of an closed-end column is {5*fundamental_frequency:.3f} Hertz. 
                What is the wavelength of the first harmonic? What is the length of the closed-end column?"""
                answer = [wavelength, closed_column_length]
                unit = ["Wavelength (meters)","Column Length (meters)"]
            elif q_type == 1:
                question = f"""The fifth harmonic of an closed-end column has a wavelength of {wavelength/5:.3f} meters. 
                What is the fundamental frequency? What is the length of the closed-end column?"""
                answer = [fundamental_frequency, closed_column_length]
                unit = ["Fundamental Frequency (Hz)","Column Length (meters)"]
        question = "Assume a wave speed of 343 m/s. " + question
        return {"question": question, "answers": answer, "units": unit}
        
    
    def decibel_scale(self,difficulty):
        if difficulty == "Easy":
            #purely intensity, no distance. options are more or less intense
            more_or_less = ri(0,1)
            # 0 = more, 1 = less
            intensity_change = ri(1,5)
            initial_intensity = ri(0,7)
            final_intensity = initial_intensity + intensity_change
            if more_or_less == 0:
                question = f"""What sound is {10**intensity_change} 
                times more intense than a {initial_intensity*10} deciBel sound?"""
                answer = [final_intensity*10]
                unit = ["Volume (deciBels)"]
            else:
                # less intense
                question = f"""What sound is {10**intensity_change} 
                times less intense than a {final_intensity*10} deciBel sound?"""
                answer = [initial_intensity*10]
                unit = ["Volume (deciBels)"]
        else:
            # distance -> squaring distance = twice the change
            more_or_less = ri(0,1)
            # 0 = more, 1 = less, 2 = distance
            intensity_change = ri(1,3)
            initial_intensity = ri(0,7)
            final_intensity = initial_intensity + 2*intensity_change
            if more_or_less == 0:
                question = f"""How loud does a {initial_intensity*10} deciBel noise sound 
                 to someone {10**intensity_change} times closer to the source of the sound?"""
                answer = [final_intensity*10]
                unit = ["Volume (deciBels)"]
            elif more_or_less == 1:
                # less intense
                question = f"""How loud does a {final_intensity*10} deciBel noise sound 
                 to someone {10**intensity_change} times further away from the source of the sound?"""
                answer = [initial_intensity*10]
                unit = ["Volume (deciBels)"]
            else:
                question = f"""Person A and Person B both hear a sound. Person A hears a 
                {10*initial_intensity} sound, but person B hears a {10*final_intensity} sound. 
                \n\n How much closer to the source of the sound is Person B?"""
                answer = [intensity_change]
                unit = ["Distance Multiple"]
             
        return {"question": question, "answers": answer, "units": unit}


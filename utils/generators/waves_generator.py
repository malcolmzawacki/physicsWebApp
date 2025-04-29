from random import randint as ri
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
try:
    from .base_generator import BaseGenerator
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from utils.generators.base_generator import BaseGenerator

from utils.word_lists import random_noun

class WaveGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="waves_")
    
    
    def choose_problem(self, problem_type: str, difficulty: str):
        if problem_type == "Wave Properties":
            return self.properties_of_waves(difficulty)
        elif problem_type == "String Harmonics":
            return self.string_harmonics(difficulty)
        else:
            pass
    
    def properties_of_waves(self, difficulty):
        frequency = ri(2,100)
        wavelength = ri(2,100)
        speed = wavelength*frequency
        q_type = ri(0,2)
        if q_type == 0:
            question = f"""A wave has a frequency of {frequency} Hz
            and a wavelength of {wavelength} meters. \n\n How fast is it moving?"""
            answer = speed
            unit = "Wave Speed (m/s)"
        elif q_type == 1:
            # find wavelength
            question = f"""A wave moving at {speed} m/s has a frequency of {frequency} Hz. 
            \n\n What is its wavelength?"""
            answer = wavelength
            unit = "Wavelength (meters/cycle)"
        else:
            # find frequency
            question = f"""A wave is moving at {speed} m/s, and has a wavelength of 
            {wavelength} meters. \n\n What is the frequency of the wave?"""
            answer = frequency
            unit = "Frequency (Hz)"
            pass
        return question, [answer], [unit]
    
    def string_harmonics(self,difficulty):
        fundamental_frequency = ri(20,5000)
        velocity = 343
        wavelength = velocity / fundamental_frequency
        string_length = wavelength / 2
        
        if difficulty == "Easy":
            # only working forwards
            q_type = ri(0,3)
            if q_type == 0:
                question = f"""What is the wavelength of the first harmonic of a {string_length:.3f} meter long string?"""
                answer = wavelength
                unit = "Wavelength (meters)"

            elif q_type == 1:
                question = f"What is the fundamental frequency of a {string_length:.3f} meter long string?"
                answer = fundamental_frequency
                unit = "Fundamental Frequency (Hz)"

            elif q_type == 2:
                question = f"""A string resonates with a fundamental frequency of {fundamental_frequency} Hz.
                How long is the string?"""
                answer = string_length
                unit = "String Length (meters)"

            elif q_type == 3:
                question = f"""How long would a string have to be to produce a wavelength of {wavelength:.3f} meters for its first harmonic?"""
                answer = string_length
                unit = "String Length (meters)"
            return question, [answer],[unit]
        elif difficulty == "Medium":
            # still forwards, multiple answers
            q_type = ri(0,1)
            if q_type == 0:
                question = f"""What are the wavelengths of the first three harmonics of a {string_length:.3f} meter long string?"""
                answer = [wavelength, wavelength/2, wavelength/3]
                unit = ["First Harmonic Wavelength (meters)","Second Harmonic Wavelength (meters)","Third Harmonic Wavelength (meters)"]

            elif q_type == 1:
                question = f"""What are the frequencies of the first three harmonics of a {string_length:.3f} meter long string?"""
                answer = [fundamental_frequency, 2*fundamental_frequency, 3*fundamental_frequency]
                unit = ["Fundamental Frequency (Hz)","Second Harmonic Frequency (Hz)","Third Harmonic Frequency (Hz)"]

            return question, answer, unit
        
        elif difficulty == "Hard":
            # lots of working backwards
            q_type = ri(0,1)
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
            return question, answer, unit


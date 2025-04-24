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
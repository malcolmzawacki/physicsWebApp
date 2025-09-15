from random import randint as ri
from random import choice as rc
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
        elif problem_type == "Open Ended Column Harmonics":
            return self.open_column_harmonics(difficulty)
        elif problem_type == "Closed End Column Harmonics":
            return self.closed_column_harmonics(difficulty)
        elif problem_type == "deciBel Scale":
            return self.decibel_scale(difficulty)
        else:
            pass


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
        return {"question": question, "answers": [answer], "units": [unit]}
    
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
            return question, [answer],[unit], None
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

            return question, answer, unit, None
        
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
            return question, answer, unit, None


    
    def open_column_harmonics(self,difficulty):
        fundamental_frequency = ri(20,5000)
        velocity = 343
        wavelength = velocity / fundamental_frequency
        open_column_length = wavelength / 2
        
        if difficulty == "Easy":
            # only working forwards
            q_type = ri(0,3)
            if q_type == 0:
                question = f"""What is the wavelength of the first harmonic of a {open_column_length:.3f} meter long open-ended column?"""
                answer = wavelength
                unit = "Wavelength (meters)"

            elif q_type == 1:
                question = f"What is the fundamental frequency of a {open_column_length:.3f} meter long open-ended column?"
                answer = fundamental_frequency
                unit = "Fundamental Frequency (Hz)"

            elif q_type == 2:
                question = f"""An open-ended column resonates with a fundamental frequency of {fundamental_frequency} Hz.
                How long is the column?"""
                answer = open_column_length
                unit = "Column Length (meters)"

            elif q_type == 3:
                question = f"""How long would an open-ended column have to be to produce a wavelength of {wavelength:.3f} meters for its first harmonic?"""
                answer = open_column_length
                unit = "Column Length (meters)"
            return question, [answer],[unit], None
        elif difficulty == "Medium":
            # still forwards, multiple answers
            q_type = ri(0,1)
            if q_type == 0:
                question = f"""What are the wavelengths of the first three harmonics of a {open_column_length:.3f} meter long open-ended column?"""
                answer = [wavelength, wavelength/2, wavelength/3]
                unit = ["First Harmonic Wavelength (meters)","Second Harmonic Wavelength (meters)","Third Harmonic Wavelength (meters)"]

            elif q_type == 1:
                question = f"""What are the frequencies of the first three harmonics of a {open_column_length:.3f} meter long open-ended column?"""
                answer = [fundamental_frequency, 2*fundamental_frequency, 3*fundamental_frequency]
                unit = ["Fundamental Frequency (Hz)","Second Harmonic Frequency (Hz)","Third Harmonic Frequency (Hz)"]

            return question, answer, unit, None
        
        elif difficulty == "Hard":
            # lots of working backwards
            q_type = ri(0,1)
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
            return question, answer, unit, None



    
    def closed_column_harmonics(self,difficulty):
        fundamental_frequency = ri(20,5000)
        velocity = 343
        wavelength = velocity / fundamental_frequency
        closed_column_length = wavelength / 4
        
        if difficulty == "Easy":
            # only working forwards
            q_type = ri(0,3)
            if q_type == 0:
                question = f"""What is the wavelength of the first harmonic of a 
                {closed_column_length:.3f} meter long closed-end column?"""
                answer = wavelength
                unit = "Wavelength (meters)"

            elif q_type == 1:
                question = f"""What is the fundamental frequency of a 
                {closed_column_length:.3f} meter long closed-end column?"""
                answer = fundamental_frequency
                unit = "Fundamental Frequency (Hz)"

            elif q_type == 2:
                question = f"""An closed-end column resonates with 
                a fundamental frequency of {fundamental_frequency} Hz.
                How long is the column?"""
                answer = closed_column_length
                unit = "Column Length (meters)"

            elif q_type == 3:
                question = f"""How long would an closed-end column have to be to produce 
                a wavelength of {wavelength:.3f} meters for its first harmonic?"""
                answer = closed_column_length
                unit = "Column Length (meters)"
            return question, [answer],[unit], None
        elif difficulty == "Medium":
            # still forwards, multiple answers
            q_type = ri(0,1)
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

            return question, answer, unit, None
        
        elif difficulty == "Hard":
            # lots of working backwards
            q_type = ri(0,1)
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
            return question, answer, unit, None
        
    
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
                answer = final_intensity*10
                unit = "Volume (deciBels)"
            else:
                # less intense
                question = f"""What sound is {10**intensity_change} 
                times less intense than a {final_intensity*10} deciBel sound?"""
                answer = initial_intensity*10
                unit = "Volume (deciBels)"
        elif difficulty == "Medium":
            # distance -> squaring distance = twice the change
            more_or_less = ri(0,1)
            # 0 = more, 1 = less, 2 = distance
            intensity_change = ri(1,3)
            initial_intensity = ri(0,7)
            final_intensity = initial_intensity + 2*intensity_change
            if more_or_less == 0:
                question = f"""How loud does a {initial_intensity*10} deciBel noise sound 
                 to someone {10**intensity_change} times closer to the source of the sound?"""
                answer = final_intensity*10
                unit = "Volume (deciBels)"
            elif more_or_less == 1:
                # less intense
                question = f"""How loud does a {final_intensity*10} deciBel noise sound 
                 to someone {10**intensity_change} times further away from the source of the sound?"""
                answer = initial_intensity*10
                unit = "Volume (deciBels)"
            else:
                question = f"""Person A and Person B both hear a sound. Person A hears a 
                {10*initial_intensity} sound, but person B hears a {10*final_intensity} sound. 
                \n\n How much closer to the source of the sound is Person B?"""
                answer = intensity_change
                unit = "Distance Multiple"
             
        return question, [answer],[unit], None


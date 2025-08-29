import math
from random import randint as ri
import sys
from pathlib import Path

try:
    from .base_generator import BaseGenerator
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from utils.generators.base_generator import BaseGenerator


class VectorGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="_vect_")
    

    def create_vector(self) -> tuple:
        """
        Returns a tuple of the x, y, resultant, and angle of a vector
        """
        x = ri(1,100)
        y = ri(1,100)
        r = round((x**2 + y**2)**(0.5),3)
        theta = round(180*math.atan(y/x)/math.pi,3)

        return x, y, r, theta
    
    def component_problem(self) -> tuple:
        x, y, r, theta = self.create_vector()
        question = f"""
        A vector has a length of {r} and is at an angle of {theta}.
        What are its horizontal and vertical components?
        """
        answer = [x, y]
        unit = ["Horizontal (x) component", "Vertical (y) component"]
        return question, answer, unit

    def resultant_problem(self) -> tuple:
        x, y, r, theta = self.create_vector()
        question = f"""
        A vector has a horizontal component of {x} and 
        a vertical component of {y}.
        What is its overall magnitude, and its angle?
        """
        answer = [r, theta]
        unit = ["Magnitude", "Angle (degrees)"]
        return question, answer, unit

    def choose_problem(self, problem_type, difficulty):
        if problem_type == "Find Components":
            return self.component_problem()
        if problem_type == "Find Resultant":
            return self.resultant_problem()
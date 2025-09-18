import random
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

class ArithmeticGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="arithmetic_")


    def choose_problem_dict(self, problem_type: str, difficulty: str):
        if problem_type == "Multiplication":
            return self.multiplication_problem(difficulty)
        elif problem_type == "Division":
            return self.division_problem(difficulty)
        elif problem_type == "Subtraction":
            return self.subtraction_problem(difficulty)
        elif problem_type == "Addition":
            return self.addition_problem(difficulty)
        else: # mixed
            pass

    def difficulty_range(self, difficulty:str) -> tuple[int, int]:
        if difficulty == "Easy":
            first = random.randint(2,9)
            second = random.randint(2,9)
        elif difficulty == "Medium":
            first = random.randint(2,9)
            second = random.randint(2,9)
            coin = random.randint(0,1)
            if coin == 0:
                first+=-1
            else:
                second+=-1
        else:
            first = random.randint(11,19)
            second = random.randint(11,19)
        return first, second


    def multiplication_problem(self, difficulty: str):
        first, second = self.difficulty_range(difficulty)
        question = f"{first} X {second}"
        answer = first*second
        unit = "Product"
        return {"question": question, "answers": [answer], "units": [unit]}
    

    def division_problem(self, difficulty: str):
        first, second = self.difficulty_range(difficulty)
        third = first*second
        question = f"{third} ÷ {second}"
        answer = first
        unit = "Quotient"
        return {"question": question, "answers": [answer], "units": [unit]}
    
    
    def subtraction_problem(self,difficulty: str):
        first, second = self.difficulty_range(difficulty)
        third = first + second
        question = f"{third} - {second}"
        answer = first
        unit = "Difference"
        return {"question": question, "answers": [answer], "units": [unit]}
    

    def addition_problem(self, difficulty: str):
        first, second = self.difficulty_range(difficulty)
        question = f"{first} + {second}"
        answer = first+second
        unit = "Sum"
        return {"question": question, "answers": [answer], "units": [unit]}
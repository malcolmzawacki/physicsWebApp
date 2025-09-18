import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


from utils.generators.linear_motion_generator import LinearMotionGenerator
from utils.generators.const_motion_generator import ConstantMotionGenerator
from utils.generators.dist_disp_generator import DistDispGenerator
class Org:
    def __init__(self):
        self.AM = LinearMotionGenerator()
        self.CM = ConstantMotionGenerator()
        self.DDG = DistDispGenerator()

    def create_first_doc(self):
        def question_generator():
            return [
                {
                "heading": "No Acceleration Questions",
                "problems": [self.AM.no_acc_question(difficulty="Hard") for _ in range(3)],
                "gap": 2
                },
                {
                "heading": "No Distance Questions",
                "problems": [self.AM.no_dist_question("Hard") for _ in range(3)],
                "gap": 2
                },
                {
                "heading": "No Time Questions",
                "problems": [self.AM.no_time_question("Hard") for _ in range(3)],
                "gap": 2
                },
                {
                "heading": "",
                "problems": [self.AM.no_vf_question("Hard") for _ in range(3)],
                "gap": 2
                }
            ]
        return question_generator


    def unit1_practice_doc(self):
        def question_generator():

            return [
                {
                "heading": "No Acceleration Questions",
                "problems": [self.AM.no_acc_question("Hard") for _ in range(20)],
                "gap": 1
                },
                {
                "heading": "No Distance Questions",
                "problems": [self.AM.no_dist_question("Hard") for _ in range(20)],
                "gap": 1
                },
                {
                "heading": "No Time Questions",
                "problems": [self.AM.no_time_question("Hard") for _ in range(20)],
                "gap": 1
                },
                {
                "heading": "No Final Velocity Questions",
                "problems": [self.AM.no_vf_question("Hard") for _ in range(20)],
                "gap": 1
                },
                {
                "heading": "Mixed Questions",
                "problems": [self.AM.mixed_question("Hard") for _ in range(20)],
                "gap": 1
                }
            ]
        return question_generator()


    def constant_motion_quiz(self):
        def generate_questions():

             return [
                
                {
                "heading": "Constant Speed",
                "problems": [self.CM.inst_speed_question() for _ in range(5)],
                "gap": 2
                },
                {
                "heading": "Distance and Displacement",
                "problems": [self.DDG.distance_and_displacement_1D(difficulty="Easy") for _ in range(1)] +  [self.DDG.distance_and_displacement_1D(difficulty="Medium") for _ in range(1)] + [self.DDG.distance_and_displacement_1D(difficulty="Hard") for _ in range(1)],
                "gap": 2
                },
                {
                "heading": "Average Speed",
                "problems": [self.CM.average_speed_question("Easy") for _ in range(2)]+[self.CM.average_speed_question("Medium") for _ in range(2)],
                "gap": 2
                },
                {
                "heading": "Average Velocity",
                "problems": [self.CM.average_velocity_question("Easy") for _ in range(2)]+[self.CM.average_velocity_question("Medium") for _ in range(2)],
                "gap": 2
                },
                {
                "heading": "Combined Constant",
                "problems": [self.CM.combined_constant_question("Medium") for _ in range(2)]+[self.CM.combined_constant_question("Hard") for _ in range(1)],
                "gap": 2
                },
            ]
        return generate_questions





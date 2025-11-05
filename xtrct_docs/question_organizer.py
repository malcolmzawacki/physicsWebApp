import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import Any

from utils.generators.linear_motion_generator import LinearMotionGenerator
from utils.generators.const_motion_generator import ConstantMotionGenerator
from utils.generators.dist_disp_generator import DistDispGenerator
from utils.generators.projectile_generator import ProjectileGenerator
from utils.generators.motion_graph_generator import MotionGraphGenerator
class Org:
    def __init__(self):
        self.AM = LinearMotionGenerator()
        self.CM = ConstantMotionGenerator()
        self.DDG = DistDispGenerator()
        self.PG = ProjectileGenerator()
        self.MGG = MotionGraphGenerator()

    def motion_graph_section(self, difficulty: str = "Medium") -> dict[str, Any]:
        problems = self.MGG.unique_graph_problems_for_doc(
            "Position-Time Graph",
            difficulty,
            graph_doc_width=2.0,
            figsize=(2.2, 1.6),
            suppress_question_text=True,
        )
        instructions = (
            "For each graph below, determine the motion direction and motion state. Mark your choices using the buttons provided."
        )
        return {
            "heading": "Position-Time Graphs",
            "section_instructions": instructions,
            "problems": problems,
            "gap": 0,
        }


    def velocity_graph_section(self, difficulty: str = "Medium") -> dict[str, Any]:
        problems = self.MGG.unique_graph_problems_for_doc(
            "Velocity-Time Graph",
            difficulty,
            graph_doc_width=2.0,
            figsize=(2.2, 1.6),
            suppress_question_text=True,
        )
        instructions = (
            "For each velocity-time graph below, determine the direction of motion and whether the object is speeding up, slowing down, or moving at constant speed."
        )
        return {
            "heading": "Velocity-Time Graphs",
            "section_instructions": instructions,
            "problems": problems,
            "gap": 0,
        }

    def projectile_quiz_CP(self):
        def question_generator():
            return [
                {
                    "heading": "Type I Projectiles",
                    "problems": [
                        self.PG._generate_type1_question("Easy","x"),
                        self.PG._generate_type1_question("Easy","h"),
                        self.PG._generate_type1_question("Easy","v_i"),
                        self.PG._generate_type1_question("Medium","v_f and theta")
                        ],
                    "gap": 2
                },
                {
                    "heading": "Type II Projectiles",
                    "problems": [
                        self.PG._generate_type2_question("Easy"),
                        self.PG._generate_type2_question("Medium","v_i and x"),
                        self.PG._generate_type2_question("Easy")
                    ],
                    "gap": 2
                }
            ]
        return question_generator
    


    def projectile_quiz_H(self):
        def question_generator():
            return [
                {
                    "heading": "Type I Projectiles",
                    "problems": [
                        self.PG._generate_type1_question("Easy","x"),
                        self.PG._generate_type1_question("Easy","h"),
                        self.PG._generate_type1_question("Easy","v_i"),
                        self.PG._generate_type1_question("Medium","v_f and theta"),
                        self.PG._generate_type1_question("Medium","v_i and h")
                        ],
                    "gap": 2
                },
                {
                    "heading": "Type II Projectiles",
                    "problems": [
                        self.PG._generate_type2_question("Easy"),
                        self.PG._generate_type2_question("Medium","v_i and x"),
                        self.PG._generate_type2_question("Medium", "v_i and theta")
                    ],
                    "gap": 2
                }
            ]
        return question_generator
    

    
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
                "problems": [self.CM.combined_constant_question("Medium") for _ in range(2)]+[self.CM.combined_constant_question("Hard") for _ in range(5)],
                "gap": 1
                },
            ]
        return generate_questions


    def projectile_practice(self):
        def generate_question():
            return [
                {
                "heading": "Type 1 Projectiles (Easy)",
                "problems": [self.PG._generate_type1_question("Easy") for _ in range(10)],
                "gap": 1
                },
                {              
                "heading": "Type 1 Projectiles (Medium)",
                "problems": [self.PG._generate_type1_question("Medium") for _ in range(10)],
                "gap": 1
                },
                {              
                "heading": "Type 1 Projectiles (Hard)",
                "problems": [self.PG._generate_type1_question("Hard") for _ in range(10)],
                "gap": 1
                },
                {
                "heading": "Type 2 Projectiles (Easy)",
                "problems": [self.PG._generate_type2_question("Easy") for _ in range(10)],
                "gap": 1
                },
                {              
                "heading": "Type 2 Projectiles (Medium)",
                "problems": [self.PG._generate_type2_question("Medium") for _ in range(10)],
                "gap": 1
                },
                {              
                "heading": "Type 2 Projectiles (Hard)",
                "problems": [self.PG._generate_type2_question("Hard") for _ in range(10)],
                "gap": 1
                },
                {
                "heading": "Type 3 Projectiles (Easy)",
                "problems": [self.PG._generate_type3_question("Easy") for _ in range(10)],
                "gap": 1
                },
                {              
                "heading": "Type 3 Projectiles (Medium)",
                "problems": [self.PG._generate_type3_question("Medium") for _ in range(10)],
                "gap": 1
                },
                {              
                "heading": "Type 3 Projectiles (Hard)",
                "problems": [self.PG._generate_type3_question("Hard") for _ in range(10)],
                "gap": 1
                },

            ]
        return generate_question


    def motion_graph_test(self):
        def generate_question():
            return [
                self.motion_graph_section("Medium"),
                self.velocity_graph_section("Medium"),
            ]

        return generate_question


    def mixed_motion_with_graphs(self):
        def generate_question():
            return [
                self.motion_graph_section("Medium"),
                self.velocity_graph_section("Medium"),
                {
                    "heading": "Accelerated Motion Questions",
                    "problems": [
                        self.AM.no_acc_question("Easy", solve_for="t"), 
                        self.AM.no_dist_question("Easy",solve_for="vi"),
                        self.AM.no_vf_question("Easy", solve_for='x'),
                        self.AM.no_time_question("Easy",solve_for='vf'),

                        #self.AM.no_acc_question("Medium", solve_for="vi"), 
                        self.AM.no_dist_question("Medium",solve_for="a"),
                        #self.AM.no_vf_question("Medium", solve_for='x'),
                        self.AM.no_time_question("Medium",solve_for='vi'),

                        self.AM.no_acc_question("Medium", solve_for="t"), 
                        #self.AM.no_dist_question("Medium",solve_for="vf"),
                        self.AM.no_vf_question("Medium", solve_for='a'),
                        #self.AM.no_time_question("Medium",solve_for='x'),
                        ],
                    "gap": 2,
                },
            ]

        return generate_question
    
    def mixed_motion_with_graphs_H(self):
        def generate_question():
            return [
                self.motion_graph_section("Medium"),
                self.velocity_graph_section("Medium"),
                {
                    "heading": "Accelerated Motion Questions",
                    "problems": [
                        self.AM.no_acc_question("Easy", solve_for="t"), 
                        self.AM.no_dist_question("Easy",solve_for="vi"),
                        self.AM.no_vf_question("Easy", solve_for='x'),
                        self.AM.no_time_question("Easy",solve_for='vf'),

                        self.AM.no_acc_question("Medium", solve_for="vf"), 
                        self.AM.no_dist_question("Medium",solve_for="t"),
                        self.AM.no_vf_question("Medium", solve_for='x'),
                        self.AM.no_time_question("Medium",solve_for='vi'),

                        self.AM.no_acc_question("Medium", solve_for="t"), 
                        self.AM.no_dist_question("Medium",solve_for="vf"),
                        self.AM.no_vf_question("Medium", solve_for='a'),
                        self.AM.no_time_question("Medium",solve_for='x'),
                        ],
                    "gap": 2,
                },
            ]

        return generate_question




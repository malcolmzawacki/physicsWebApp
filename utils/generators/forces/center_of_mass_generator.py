import random
from random import randint as ri
import math
from utils.word_lists import random_noun
from utils.generators.base_generator import BaseGenerator


class CenterOfMassGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="COM_")
    
    def choose_problem_dict(self, problem_type, difficulty):
        if problem_type == "One Dimensional":
            return self.OneD_COM(difficulty)
        elif problem_type == "Two Dimensional":
            return self.TwoD_COM(difficulty)

    
    
    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "One Dimensional": {
                "honors": r"""
                      \Sigma F \;=\; ma""",

                "conceptual": r"""\Large{
                      \Sigma F \;=\; ma 
                      \quad\quad | \quad\quad
                      m \;=\; \frac{\Sigma F}{a}
                      \quad\quad | \quad\quad
                      a \;=\; \frac{\Sigma F}{m}
                      }"""
            },
            "Two Dimensional": {
                "honors": r"""
                      \Sigma F \;=\; ma""",

                "conceptual": r"""\Large{
                      \Sigma F \;=\; ma 
                      \quad\quad | \quad\quad
                      m \;=\; \frac{\Sigma F}{a}
                      \quad\quad | \quad\quad
                      a \;=\; \frac{\Sigma F}{m}
                      }"""
            },
       
        }
    
    def OneD_COM(self, difficulty):
        x1 = ri(0,25)
        m1 = ri(1,10)
        x2 = ri(0,25)
        m2 = ri(1,10)
        mass_list = [m1, m2]
        x_list = [x1, x2]
        if difficulty != "Easy":
            # at least 3 (medium)
            mass_list.append(ri(1,10))
            x_list.append(ri(0, 25))
        if difficulty == "Hard": # 4 masses
            mass_list.append(ri(1,10))
            x_list.append(ri(0, 25))
        center = sum(x*m for x,m in zip(x_list, mass_list))/sum(m for m in mass_list)
        info_str = ""
        for x, m in zip(x_list, mass_list):
            info_str += f" Mass {m} is located at {x} meters. "
        question = f"""A set of {len(mass_list)} masses are placed along a line.
        {info_str} Where is the center of mass?"""
        unit = "Center of Mass (meters)"
        diagram_data = {
            "masses": mass_list,
            "x_list": x_list
        }
        return {"question": question, "answers": [center], "units": [unit], "diagram_data": diagram_data}
    
    def TwoD_COM(self, difficulty):
        x1 = ri(0,25)
        y1 = ri(0,25)
        m1 = ri(1,10)
        x2 = ri(0,25)
        y2 = ri(0,25)
        m2 = ri(1,10)
        mass_list = [m1, m2]
        x_list = [x1, x2]
        y_list = [y1, y2]
        if difficulty != "Easy":
            # at least 3 (medium)
            mass_list.append(ri(1,10))
            x_list.append(ri(0, 25))
            y_list.append(ri(0, 25))
        if difficulty == "Hard": # 4 masses
            mass_list.append(ri(1,10))
            x_list.append(ri(0, 25))
            y_list.append(ri(0, 25))
        center_x = sum(x*m for x,m in zip(x_list, mass_list))/sum(m for m in mass_list)
        center_y = sum(y*m for y,m in zip(y_list, mass_list))/sum(m for m in mass_list)
        info_str = ""
        for m, x, y in zip(mass_list, x_list, y_list):
            info_str += f" Mass {m} is located at position ({x},{y}). "
        question = f"""A set of {len(mass_list)} masses are placed around a plane.
        {info_str} Where is the center of mass?"""
        answers = [center_x, center_y]
        units = ["X Coordinate (meters)","Y Coordinate (meters)"]
        diagram_data = {
            "masses": mass_list,
            "x_list": x_list,
            "y_list": y_list
        }
        return {"question": question, "answers": answers, "units": units, "diagram_data": diagram_data}
    



    def generate_diagram(self, diagram_data: dict, problem_type: str, difficulty: str):
        """
        Generate a Matplotlib figure.
        This method is called by the Interface's add_diagram_smart().
        """
        import matplotlib.pyplot as plt
        plt.tight_layout()
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(5, 5))

        mass_list = diagram_data["masses"]
        x_list = diagram_data.get("x_list")
        if len(diagram_data.keys()) == 3: # 2D
            y_list = diagram_data.get("y_list")
        else:
            y_list = []
            for _ in x_list:
                y_list.append(0)
    




        # scaling for circles (distance weighted by sum of masses)
        dist_1_2 = (((x_list[1] - x_list[0])**2 + (y_list[1] - y_list[0])**2)**(0.5)) / (mass_list[0] + mass_list[1])
        dist_list = [dist_1_2]
        if difficulty != "Easy":
            dist_1_3 = (((x_list[2] - x_list[0])**2 + (y_list[2] - y_list[0])**2)**(0.5)) / (mass_list[0] + mass_list[2])
            dist_2_3 = (((x_list[1] - x_list[2])**2 + (y_list[1] - y_list[2])**2)**(0.5)) / (mass_list[2] + mass_list[1])
            dist_list = [dist_1_2, dist_1_3, dist_2_3]
        if difficulty == "Hard":
            dist_1_4 = (((x_list[3] - x_list[0])**2 + (y_list[3] - y_list[0])**2)**(0.5)) / (mass_list[0] + mass_list[3])
            dist_2_4 = (((x_list[3] - x_list[1])**2 + (y_list[3] - y_list[1])**2)**(0.5)) / (mass_list[1] + mass_list[3])
            dist_3_4 = (((x_list[3] - x_list[2])**2 + (y_list[3] - y_list[2])**2)**(0.5)) / (mass_list[2] + mass_list[3])
            dist_list.append(dist_1_4)
            dist_list.append(dist_2_4)
            dist_list.append(dist_3_4)


        scale = round(min(dist_list)/(2) , 2)
    


        r1 = mass_list[0]*scale
        r2 = mass_list[1]*scale
        r_list = [r1, r2]
        circle1 = plt.Circle((x_list[0], y_list[0]), radius=r1, color='cyan', fill=True, zorder=5)
        ax.add_artist(circle1)
        ax.text(x_list[0], y_list[0], '$m_1$', color='black', ha='center', va='center', fontsize=12*r1, zorder=11)
        circle2 = plt.Circle((x_list[1], y_list[1]), radius=r2, color='green', fill=True, zorder=5)
        ax.add_artist(circle2)
        ax.text(x_list[1], y_list[1], '$m_2$', color='black', ha='center', va='center', fontsize=12*r2, zorder=11)

        if difficulty != "Easy":
            r3 = mass_list[2]*scale
            r_list.append(r3)
            circle3 = plt.Circle((x_list[2], y_list[2]), radius = r3, color='yellow', fill=True, zorder=5)
            ax.add_artist(circle3)
            ax.text(x_list[2], y_list[2], '$m_3$', color='black', ha='center', va='center', fontsize=12*r3, zorder=11)

        if difficulty == "Hard":
            r4 = mass_list[3]*scale
            r_list.append(r4)
            circle4 = plt.Circle((x_list[3], y_list[3]), radius= r4, color='magenta', fill=True, zorder=5)
            ax.add_artist(circle4)
            ax.text(x_list[3], y_list[3], '$m_4$', color='black', ha='center', va='center', fontsize=12*r4, zorder=11)

        # check for out of bounds circles
        x_min_list = []
        x_max_list = []
        y_min_list = []
        y_max_list = []
        for r, x, y in zip(r_list, x_list, y_list):
            x_min_list.append(x - r)
            x_max_list.append(r + x)
            y_min_list.append(y - r)
            y_max_list.append(y + r)
        max_x = max(x_max_list)
        min_x = min(x_min_list)
        x_center = (max_x + min_x) // 2
        x_range = max_x - min_x
        max_y = max(y_max_list)
        min_y = min(y_min_list)
        y_center = (max_y + min_y) // 2
        y_range = max_y - min_y

        axes_range = max(x_range, y_range) // 2  + 2
        x_axis_min = x_center - axes_range
        x_axis_max = x_center + axes_range
        y_axis_min = y_center - axes_range
        y_axis_max = y_center + axes_range


        ax.set_xlim(x_axis_min, x_axis_max)
        ax.set_ylim(y_axis_min, y_axis_max)
        return fig
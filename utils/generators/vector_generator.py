import math
from random import randint as ri

from utils.generators.base_generator import BaseGenerator


class VectorGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="_vect_")
    

    def create_vector(self) -> tuple[int, int, float, float, str]:
        """
        Returns a tuple of the x, y, resultant, reference angle, and angle descriptor str
        """
        x = ri(10,50)
        flip = ri(0,1)
        if flip == 1:
            x *= -1
        y = ri(10,50)
        flip2 = ri(0,1)
        if flip2 == 1:
            y *= -1
        r = round((x**2 + y**2)**(0.5),3)
        theta, theta_str = self.process_angle(x, y)

        return x, y, r, theta, theta_str
    
    def process_angle(self,
            x: int,
            y: int
            ) -> tuple[float, str]:
        if x != 0:
            side = "negative" if x < 0 else "positive"
            above_below = "below" if y < 0 else "above"

            theta_str = f"degrees {above_below} the {side} x axis"

            theta = round(180*math.atan(abs(y)/abs(x))/math.pi,3)
        elif x == 0 and y != 0:
            theta = 90.0
            above_below = "below" if y < 0 else "above"
            theta_str = f"degrees {above_below} the positive x axis"
        else: # both zero, exact opposites
            theta = 0
            theta_str = """wow this is like, a one in a million chance, just put zero for both answers i guess, or hit new problem. I really don't feel like taking care of this edge case, so instead I'm making this message so big that it'll hopefully be obvious enough that you read it."""

        return theta, theta_str


    def component_problem(self) -> tuple:
        x, y, r, theta, theta_str = self.create_vector()
        question = f"""
        A vector has a length of {r} and is at an angle of {theta} {theta_str}.
        What are its horizontal and vertical components?
        """
        answer = [x, y]
        unit = ["Horizontal (x) component", "Vertical (y) component"]
        return {"question": question, "answers": answer, "units": unit, "diagram_data": [x,y]}



    def resultant_problem(self) -> tuple:
        x, y, r, theta, theta_str = self.create_vector()
        question = f"""
        A vector has a horizontal component of {x} and 
        a vertical component of {y}.
        What is its overall magnitude, and its angle?
        """
        answer = [r, theta]
        unit = ["Magnitude", f"Angle ({theta_str}) "]
        return {"question": question, "answers": answer, "units": unit, "diagram_data": [x,y]}


    def vector_sum(self) -> tuple:
        x1, y1, r1, theta1, theta_str1 = self.create_vector()
        x2, y2, r2, theta2, theta_str2 = self.create_vector()
        x_r = x1 + x2
        y_r = y1 + y2
        r = round((x_r**2 + y_r**2)**(0.5),3)
        theta, theta_str = self.process_angle(x_r, y_r)
        question = f"""
        Vector A has a length of {r1} and an angle of {theta1} {theta_str1}. \n
        Vector B has a length of {r2} and an angle of {theta2} {theta_str2}. \n
        What is the magnitude and direction of Vector A + B?
        """
        answer = [r, theta]
        unit = ["Magnitude", f"Angle ({theta_str})"]
        data = [[x1, y1, r1], [x2, y2, r2], [x_r, y_r, r]]
        return {"question": question, "answers": answer, "units": unit, "diagram_data": data}


    def generate_diagram(
            self, data: list, 
            problem_type: str, 
            difficulty: str
            ):
        """Takes in data from a problem and creates a figure

        :param data: list of (ints?)
        problem_type: 
            str, for identification of what diagram to make
        difficulty: str,
            currently only to match with prior incarnations of generate_diagram in other classes, may have other useslater

        :returns: matplotlib figure
        :rtype: fig
        """
        import matplotlib.pyplot as plt
        plt.tight_layout()
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize = (4,4))
        try:
 
            # resultant arrow
            length = (data[0]**2 + data[1]**2)**(0.5)

            # define scale of figure
            if abs(data[0]) >= abs(data[1]):
                limit = 1.1*abs(data[0])
            else:
                limit = 1.1*abs(data[1])
            
            #identify quadrant
            if data[0] > 0 and data[1] > 0: # Q1
                ax.set_xlim(-1, limit)
                ax.set_ylim(-1, limit)

            elif data[0] > 0 and data[1] < 0: # Q4
                ax.set_xlim(-1, limit)
                ax.set_ylim(-1*limit, 1)

            elif data[0] < 0 and data[1] > 0: # Q2
                ax.set_xlim(-1*limit, 1)
                ax.set_ylim(-1, limit)

            else: # Q3
                ax.set_xlim(-1*limit, 1)
                ax.set_ylim(-1*limit, 1)

            # draw arrows
            ax.arrow(
                x = 0, y = 0, 
                dx = 0.9*data[0], dy = 0.9*data[1], 
                head_width = 0.5, head_length = 0.1*length, 
                fc = 'red', ec = 'red'
                )
            # horizontal arrow
            ax.arrow(
                x = 0, y = 0, 
                dx = 0.9*data[0], dy = 0, 
                head_width = 0.5, head_length = 0.1*abs(data[0]), 
                fc = 'cyan', ec = 'cyan'
                )
            # vertical arrow
            ax.arrow(
                x = data[0], y = 0, 
                dx = 0, dy = 0.9*data[1], 
                head_width = 0.5, head_length = 0.1*abs(data[1]), 
                fc = 'cyan', ec = 'cyan'
                )
        except:
            x1 = data[0][0]
            y1 = data[0][1]
            r1 = data[0][2]
            x2 = data[1][0]
            y2 = data[1][1]
            r2 = data[1][2]
            x_r = data[2][0]
            y_r = data[2][1]
            r = data[2][2]
            x_min = 1.1*min(x1, x2,x_r,-1)
            x_max = 1.1*max(x1, x2,x_r, 1)
            y_min = 1.1*min(y1, y2, y_r, -1)
            y_max = 1.1*max(y1, y2, y_r, 1)

            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)

            width = 0.1*min(r1, r2, r)
            # vector A
            ax.arrow(
                x = 0, y = 0,
                dx = 0.9*x1, dy = 0.9*y1,
                head_width = width, head_length = 0.1*r1, 
                fc = 'cyan', ec = 'cyan'
            )
            # vector B
            ax.arrow(
                x = x1, y = y1,
                dx = 0.9*x2, dy = 0.9*y2,
                head_width = width, head_length = 0.1*r2, 
                fc = 'yellow', ec = 'yellow'
            )
            # vector C
            ax.arrow(
                x = 0, y = 0,
                dx = 0.9*x_r, dy = 0.9*y_r,
                head_width = width, head_length = 0.1*r, 
                fc = 'green', ec = 'green'
            )
            ax.set_title("""Vector A in Blue, Vector B in Yellow \n Vector A+B in Green (get it? blue+yellow?)""")
        return fig


    def choose_problem_dict(self, problem_type, difficulty):
        if problem_type == "Find Components":
            return self.component_problem()
        if problem_type == "Find Resultant":
            return self.resultant_problem()
        if problem_type == "Summing Vectors":
            return self.vector_sum()

    def get_problem_metadata(self, problem_type: str) -> dict:
        meta = {
            "Find Components": {
                "honors_equation": r"x = r\cos(\theta) \quad , \quad y = r\sin(\theta)",
                "conceptual_equation": r"\text{Resolve the vector into horizontal (x) and vertical (y) components}",
                "tags": ["vectors", "components"],
            },
            "Find Resultant": {
                "honors_equation": r"r = \sqrt{x^2 + y^2} \quad , \quad \theta = \tan^{-1}\!\left(\frac{y}{x}\right)",
                "conceptual_equation": r"\text{Magnitude from Pythagorean theorem; angle from inverse tangent}",
                "tags": ["vectors", "resultant"],
            },
            "Summing Vectors": {
                "honors_equation": r"x_r = x_1 + x_2 \quad , \quad y_r = y_1 + y_2 \quad , \quad r = \sqrt{x_r^2 + y_r^2} \quad , \quad \theta = \tan^{-1}\!\left(\frac{y_r}{x_r}\right)",
                "conceptual_equation": r"\text{Add components, then convert to magnitude/angle}",
                "tags": ["vectors", "addition"],
            },
        }
        return meta.get(problem_type, {})

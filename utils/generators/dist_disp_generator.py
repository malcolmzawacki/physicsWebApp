from random import randint as ri
import random

from utils.generators.base_generator import BaseGenerator

from utils.word_lists import random_noun

class DistDispGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="disp_")
    


    def choose_problem_dict(self, problem_type: str, difficulty: str):
        if problem_type == "One Dimensional":
            return self.distance_and_displacement_1D(difficulty)
        elif problem_type == "Two Dimensional":
            return self.distance_and_displacement_2D(difficulty)
        
    
    def get_step_num(self,difficulty):
        if difficulty == "Easy":
            return 2
        elif difficulty == "Medium":
            return 4
        else: #hard
            return 6

    def distance_and_displacement_1D(self,difficulty):
        noun = random_noun()
        directions = [
            ["right","left"],
            ["up","down"],
            ["North","South"],
            ["East","West"]
            ]
        # note that the positive direction is listed first 
        problem_directions = random.choice(directions)
        distance = 0
        displacement = 0
        movements =[]
        max_val = 2*self.get_difficulty_range(difficulty)
        label_set = [
            "Total Distance (meters)", 
            "Net Displacement (meters)", 
            "Direction (Say 'None' for zero)"
            ]
        question = f"A {noun} goes on a walk, and makes the following movements: \n"

        steps = self.get_step_num(difficulty)

        for i in range(steps):
            dirn = ri(0,1)
            step = ri(1,max_val)
            distance += step
            if dirn == 0:
                displacement += step
            else: 
                displacement -= step
            step_dirn = problem_directions[dirn]
            movements.append((step_dirn, step))

            question += f"{i+1}. {step} meters {step_dirn} \n"
        question += f"\nWhat is the total distance and net displacment of the {noun}?"
        if displacement > 0:
            direction = problem_directions[0]
        elif displacement < 0:
            direction = problem_directions[1]
        else:
            direction = "None"
        displacement = abs(displacement)
        answers = [distance, displacement, direction]
        return {"question": question, "answers": answers, "units": label_set, "diagram_data": movements}
    

    def distance_and_displacement_2D(self,difficulty):
        noun = random_noun()
        problem_directions = [["East","West"],["North","South"]]
        # note that the positive direction is listed first, x and y
        distance = 0
        disp_x = 0
        disp_y = 0
        max_val = 20
        movements = []
        label_set = [
            "Total Distance (meters)", 
            "Net Displacement (meters)", 
            "Direction (Say 'None' for zero)"]
        question = f"A {noun} goes on a walk, and makes the following movements: \n"
        steps = int(self.get_step_num(difficulty) / 2)
        for i in range(steps):
            dirn_x = ri(0,1)
            dirn_y = ri(0,1)
            step_x = ri(1,max_val)
            step_y = ri(1,max_val)
            distance += step_x + step_y
            if dirn_x == 0:
                disp_x += step_x
            else: 
                disp_x -= step_x
            if dirn_y == 0:
                disp_y += step_y
            else: 
                disp_y -= step_y
            step_dirn_x = problem_directions[0][dirn_x]
            step_dirn_y = problem_directions[1][dirn_y]
            movements.append((step_dirn_x, step_x))
            movements.append((step_dirn_y, step_y))
            question += f"{2*i+1}. {step_x} meters {step_dirn_x} \n"
            question += f"{2*i+2}. {step_y} meters {step_dirn_y} \n"
        if disp_x > 0:
            dirn_x_final = "East"
        elif disp_x < 0:
            dirn_x_final = "West"
        else:
            dirn_x_final = ""
        if disp_y > 0:
            dirn_y_final = "North"
        elif disp_y < 0:
            dirn_y_final = "South"
        else:
            dirn_y_final = ""
        dirn_final = dirn_y_final + dirn_x_final
        dirn_final = "None" if len(dirn_final) < 4 else dirn_final
        displacement = (disp_x**2  + disp_y**2)**(1/2)

        return question, [distance, displacement, dirn_final], label_set, movements
    

    def generate_diagram(self,movements: list, problem_type: str, difficulty: str):
        """
        Generate a diagram showing the movement path
        
        Parameters:
        movements: list of tuples (direction, distance)
        problem_type: "1D" or "2D"
        
        Returns:
        matplotlib figure
        """

        if movements is None:
            return None
        
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(4, 4))
        
        # Set up the plot
        if problem_type == "One Dimensional":
            # For 1D, we'll draw on a horizontal line
            horizontal_directions = {"left","right","East", "West"}
            if movements[0][0] in horizontal_directions:
                ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
                steps = self.get_step_num(difficulty)
                ax.set_ylim(0, steps+2)
                # Start at origin
                current_x = 0
                current_y = 1
                points_x = [current_x]
                points_y = [current_y]
                step_count = 0
                positive_directions = {"right","East"}
                # Plot each movement
                for i in range(len(movements)):
                    if movements[i][0] in positive_directions:
                        current_x += movements[i][1]
                    else:
                        current_x -= movements[i][1]
                    
                    points_x.append(current_x)
                    points_y.append(current_y)
                    current_y+=1
                    if i < len(movements) - 1:
                        points_x.append(current_x)
                        points_y.append(current_y)
                    
                # Plot the path
                #ax.plot(points_x, points_y, 'o-', color='yellow')
                
                # Add arrows to show direction
                for i in range(len(points_x) - 1):
                    if i % 2 == 1:
                    
                        ax.arrow(points_x[i], points_y[i],0, 0.8,
                            head_width=0.1, head_length=0.2, 
                            fc='yellow', ec='yellow',linestyle=':')

                    dx = points_x[i+1] - points_x[i]
                    
                    ax.arrow(points_x[i], points_y[i], dx * 0.8, 0, 
                            head_width=0.1, head_length=abs(dx) * 0.2, 
                            fc='cyan', ec='cyan')
                
                # Add displacement vector
                ax.arrow(
                    points_x[0], steps+1, 
                    (points_x[-1] - points_x[0])*0.9, 0,
                    head_width=0.1, 
                    head_length=abs(points_x[-1] - points_x[0]) * 0.1,
                    fc='red', ec='red', linewidth=2
                    )
                
                # Add grid
                ax.grid(True, linestyle='--', alpha=0.3)

                # Add labels
                ax.set_xlabel('Position (meters)')
                ax.set_ylabel('Movement Number')
                ax.set_title(
                    """1D Movement Diagram\npath in blue, step in yellow,\ndisplacement in red"""
                             )
            else: # vertical Stuff
                ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
                steps = self.get_step_num(difficulty)
                ax.set_xlim(0, steps+2)
                # Start at origin
                current_y = 0
                current_x = 1
                points_y = [current_y]
                points_x = [current_x]
                step_count = 0
                positive_directions = {"North","up"}
                # Plot each movement
                for i in range(len(movements)):
                    if movements[i][0] in positive_directions:
                        current_y += movements[i][1]
                    else:
                        current_y -= movements[i][1]
                    
                    points_x.append(current_x)
                    points_y.append(current_y)
                    current_x+=1
                    if i < len(movements) - 1:
                        points_x.append(current_x)
                        points_y.append(current_y)
                    
                # Plot the path
                #ax.plot(points_x, points_y, 'o-', color='yellow')
                
                # Add arrows to show direction
                for i in range(len(points_x) - 1):
                    dy = points_y[i+1] - points_y[i]
                    
                    ax.arrow(points_x[i], points_y[i], 0, dy * 0.8, 
                            head_width=0.1, head_length=abs(dy) * 0.2, 
                            fc='cyan', ec='cyan')
                    if i % 2 == 1:
                    
                        ax.arrow(points_x[i], points_y[i],0.8, 0,
                            head_width=0.1, head_length=0.2, 
                            fc='yellow', ec='yellow',linestyle=':')
                
                # Add displacement vector
                ax.arrow(
                    steps+1,points_y[0], 0,
                    (points_y[-1] - points_y[0])*0.9,
                    head_width=0.1, 
                    head_length=abs(points_y[-1] - points_y[0]) * 0.1,
                    fc='red', ec='red', linewidth=2
                    )
                
                # Add grid
                ax.grid(True, linestyle='--', alpha=0.3)

                # Add labels
                ax.set_ylabel('Position (meters)')
                ax.set_xlabel('Movement Number')
                ax.set_title(
                    """1D Movement Diagram\npath in blue, step in yellow,\ndisplacement in red"""
                             )

            
        else:  # 2D
            # Start at origin
            current_x, current_y = 0, 0
            points_x = [current_x]
            points_y = [current_y]
            
            # Plot each movement
            for direction, distance in movements:
                if direction == "East":
                    current_x += distance
                elif direction == "West":
                    current_x -= distance
                elif direction == "North":
                    current_y += distance
                elif direction == "South":
                    current_y -= distance
                
                points_x.append(current_x)
                points_y.append(current_y)
            
            # Plot the path
            #ax.plot(points_x, points_y, 'o-', color='cyan')
            
            # Add arrows to show direction
            for i in range(len(points_x) - 1):
                dx = points_x[i+1] - points_x[i]
                dy = points_y[i+1] - points_y[i]
                dx = 0.8*dx if dx != 0 else dx
                dy = 0.8*dy if dy != 0 else dy
                x_arrow = abs(0.2*dx) if dx != 0 else 1
                y_arrow = abs(0.2*dy) if dy != 0 else 1
                ax.arrow(points_x[i], points_y[i], dx, dy, 
                        head_width=0.3, head_length=x_arrow*y_arrow, 
                        fc='cyan', ec='cyan')
            
            # Add displacement vector
            disp_x = (points_x[-1] - points_x[0])
            disp_y = (points_y[-1] - points_y[0])
            arrowhead_length =abs((disp_x**2 + disp_y**2)**(1/2))
            disp_x *= 0.8
            disp_y *= 0.8
            arrowhead_length *= 0.2
            ax.arrow(points_x[0], points_y[0],
                    disp_x, 
                    disp_y,
                    head_width=0.3, head_length=arrowhead_length,
                    fc='red', ec='red', linewidth=1)
            
            # Add grid
            ax.grid(True, linestyle='--', alpha=0.3)
            
            # Add labels
            ax.set_xlabel('X Position (meters)')
            ax.set_ylabel('Y Position (meters)')
            ax.set_title('2D Movement Diagram \n path in blue \n displacement in red')
            
            # Make axes equal scale
            ax.set_aspect('auto')
        
        # Make the plot clean
        plt.tight_layout()
        plt.style.use("dark_background")
        
        return fig
        
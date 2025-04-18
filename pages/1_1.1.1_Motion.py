import streamlit as st
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd

# Use a dark background for matplotlib so it fits a "dark mode" style
plt.style.use("dark_background")

sys.path.append(str(Path(__file__).parent.parent))
from utils.generators.linear_motion_generator import LinearMotionGenerator
from utils.generators.projectile_generator import ProjectileGenerator
from utils.ui import interface

class graphing:
    def generate_position_time_graph(graph_type: str):
        """
        Returns (fig, direction, motion_state, graph_label) for a randomly generated position-time graph
        """
        fig, ax = plt.subplots(figsize=(3, 2))  # Smaller figure size
        t = np.linspace(0, 5, 100)

        if graph_type == "linear_positive":
            position = 2 * t + 1    # slope > 0, constant velocity
            correct_direction = "Positive"
            correct_motion_state = "Constant Velocity"
        elif graph_type == "linear_negative":
            position = -1.5 * t + 5 # slope < 0, constant velocity
            correct_direction = "Negative"
            correct_motion_state = "Constant Velocity"
        elif graph_type == "accelerating_positive":
            position = t**2         # slope increasing over time
            correct_direction = "Positive"
            correct_motion_state = "Speeding Up"
        elif graph_type == "decelerating_positive":
            position = -t*(t-10) + 5
            correct_direction = "Positive"
            correct_motion_state = "Slowing Down"
        elif graph_type == "decelerating_negative":
            position = t*(t-10) - 5
            correct_direction = "Negative"
            correct_motion_state = "Slowing Down"
        else:  # "acceleration_negative"
            position = -t**2 + 5
            correct_direction = "Negative"
            correct_motion_state = "Speeding Up"

        ax.plot(t, position, color="cyan")
        ax.set_xlabel("Time (s)", color="white")
        ax.set_ylabel("Position (m)", color="white")
        ax.set_title("Position-Time Graph", color="white")
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        fig.tight_layout()

        return (fig, correct_direction, correct_motion_state)

    def generate_velocity_time_graph(graph_type: str):
        """
        Returns (fig, direction, motion_state) for a randomly generated velocity-time graph
        """
        fig, ax = plt.subplots(figsize=(3, 2))  # Smaller figure size
        t = np.linspace(0, 5, 100)

        # Randomly pick one of "types"

        if graph_type == "linear_positive":
            velocity = np.ones_like(t) * 2  # constant velocity > 0
            correct_direction = "Positive"
            correct_motion_state = "Constant Velocity"
        elif graph_type == "linear_negative":
            velocity = np.ones_like(t) * -2  # constant velocity < 0
            correct_direction = "Negative"
            correct_motion_state = "Constant Velocity"
        elif graph_type == "accelerating_positive":
            velocity = t  # starts at 0, increasing
            correct_direction = "Positive"
            correct_motion_state = "Speeding Up"
        elif graph_type == "decelerating_positive":
            velocity = -t + 5
            correct_direction = "Positive"
            correct_motion_state = "Slowing Down"
        elif graph_type == "decelerating_negative":
            velocity = t - 5
            correct_direction = "Negative"
            correct_motion_state = "Slowing Down"
        else:  # "increasing_negative"
            velocity = -t  # negative velocity, becomes more negative
            correct_direction = "Negative"
            correct_motion_state = "Speeding Up"

        ax.plot(t, velocity, color="orange")
        ax.set_xlabel("Time (s)", color="white")
        ax.set_ylabel("Velocity (m/s)", color="white")
        ax.set_title("Velocity-Time Graph", color="white")
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        fig.tight_layout()

        return (fig, correct_direction, correct_motion_state)

    def graphing_practice():
        st.title("Position & Velocity vs Time Graphs")
        # Use session state to store the current graph (so it doesn't regenerate on button press)
        if "pt_graph" not in st.session_state:
            st.session_state.pt_graph = None
        if "vt_graph" not in st.session_state:
            st.session_state.vt_graph = None

        # For matching mode, we'll store multiple graphs
        if "match_pt_graph" not in st.session_state:
            st.session_state.match_pt_graph = None
        if "match_vt_graph" not in st.session_state:
            st.session_state.match_vt_graph = None
        if "option_graphs" not in st.session_state:
            st.session_state.option_graphs = None

        mode = st.selectbox("Select a Practice Mode:", 
                        ["Position-Time Graph", "Velocity-Time Graph", "Match Graphs"])

        # --------------------------------------------
        # 1) POSITION-TIME GRAPH
        # --------------------------------------------
        if mode == "Position-Time Graph":
            # If there's no stored graph yet or user wants a new one, generate it
            if st.button("Generate New Graph"):
                graph_type = random.choice(["linear_positive", "linear_negative", 
                                    "accelerating_positive", "accelerating_negative",
                                    "decelerating_positive", "decelerating_negative"])
                st.session_state.pt_graph = graphing.generate_position_time_graph(graph_type)

            # If we have a stored graph, display it
            if st.session_state.pt_graph is not None:
                fig, correct_dir, correct_state = st.session_state.pt_graph
                probCol1, probCol2 = st.columns(2)
                with probCol1:
                    st.pyplot(fig)
                with probCol2:
                    # Let user pick answers
                    user_dir = st.selectbox(
                        "Select the direction of motion:", 
                        ["Positive", "Negative"]
                    )
                    user_state = st.selectbox(
                        "Select the state of motion:", 
                        ["Constant Velocity", "Speeding Up", "Slowing Down"]
                    )

                if st.button("Check Answers"):
                    # Compare to correct answers
                    direction_correct = (user_dir == correct_dir)
                    state_correct = (user_state == correct_state)

                    if direction_correct and state_correct:
                        st.success("Correct!")
                    else:
                        st.error(f"Incorrect. The correct direction is '{correct_dir}' and the motion state is '{correct_state}'.")
            else:
                st.info("Click 'Generate New Graph' to start.")

        # --------------------------------------------
        # 2) VELOCITY-TIME GRAPH
        # --------------------------------------------
        elif mode == "Velocity-Time Graph":
            # If there's no stored graph yet or user wants a new one, generate it
            if st.button("Generate New Graph"):
                graph_type = random.choice(["linear_positive", "linear_negative", 
                                    "accelerating_positive", "accelerating_negative",
                                    "decelerating_positive", "decelerating_negative"])
                st.session_state.vt_graph = graphing.generate_velocity_time_graph(graph_type)

            # If we have a stored graph, display it
            if st.session_state.vt_graph is not None:
                fig, correct_dir, correct_state = st.session_state.vt_graph
                probCol1, probCol2 = st.columns(2)
                with probCol1:
                    st.pyplot(fig)
                with probCol2:
                    # Let user pick answers
                    user_dir = st.selectbox(
                        "Select the direction of motion:", 
                        ["Positive", "Negative"]
                    )
                    user_state = st.selectbox(
                        "Select the state of motion:", 
                        ["Constant Velocity", "Speeding Up", "Slowing Down"]
                    )

                if st.button("Check Answers"):
                    direction_correct = (user_dir == correct_dir)
                    state_correct = (user_state == correct_state)

                    if direction_correct and state_correct:
                        st.success("Correct!")
                    else:
                        st.error(f"Incorrect. The correct direction is '{correct_dir}' and the motion state is '{correct_state}'.")
            else:
                st.info("Click 'Generate New Graph' to start.")

        # --------------------------------------------
        # 3) MATCH GRAPHS
        # --------------------------------------------
        else:
            st.write("You'll see either a position-time or velocity-time graph and try to match it among multiple options of the other type.")

            # decide which main graph to show (P-T or V-T)
            show_pt_first = st.selectbox("Which primary graph type?", 
                                    ["Position-Time First", "Velocity-Time First"])

            if show_pt_first == "Position-Time First":
                # If we don't have a stored graph or user wants a new scenario
                if st.button("Generate New Matching Set"):
                    graph_type = random.choice(["linear_positive", "linear_negative", 
                                    "accelerating_positive", "accelerating_negative",
                                    "decelerating_positive", "decelerating_negative"])
                    st.session_state.match_pt_graph = graphing.generate_position_time_graph(graph_type)
                    wrong_answers = ["linear_positive", "linear_negative", 
                                    "accelerating_positive", "accelerating_negative",
                                    "decelerating_positive", "decelerating_negative"]
                    wrong_answers.remove(graph_type)
                    wrong_1 = random.choice(wrong_answers)
                    wrong_answers.remove(wrong_1)
                    wrong_2 = random.choice(wrong_answers)
                    choice_list = [graph_type,wrong_1,wrong_2]
                    random.shuffle(choice_list)
                    # Generate 3 velocity-time option graphs
                    st.session_state.option_graphs = [
                        graphing.generate_velocity_time_graph(entry) for entry in choice_list
                    ]

                if st.session_state.match_pt_graph is not None:
                    fig_pt, dir_pt, state_pt = st.session_state.match_pt_graph
                    col1,col2,col3,col4 = st.columns(4)
                    with col1:
                        st.pyplot(fig_pt)
                        st.write("Match this Position-Time Graph to the correct Velocity-Time Graph")

                    # Display option graphs in columns
                    if st.session_state.option_graphs:
                        option_columns = col2,col3,col4
                        labels = ["A", "B", "C"]

                        for col, label, (fig_vt, dir_vt, state_vt) in zip(option_columns, labels, st.session_state.option_graphs):
                            with col:
                                st.pyplot(fig_vt)
                                st.write(f"Option {label}")
                                

                        # Let user pick which one is correct
                        user_choice = st.selectbox(
                            "Which Velocity-Time graph matches the Positon-Time graph above?", 
                            labels
                        )

                        if st.button("Check Match"):
                            chosen_index = labels.index(user_choice)
                            _, dir_vt_selected, state_vt_selected = st.session_state.option_graphs[chosen_index]

                            # Basic matching logic: compare direction & motion state
                            # (You might want more sophisticated logic in practice)
                            if (dir_pt == dir_vt_selected) and (state_pt == state_vt_selected):
                                st.success("Correct match!")
                            else:
                                st.error("Incorrect match. Try again or generate a new set.")
                    else:
                        st.info("Click 'Generate New Matching Set' to see the option graphs.")

            else:  # Velocity-Time First
                if st.button("Generate New Matching Set"):
                    graph_type = random.choice(["linear_positive", "linear_negative", 
                                    "accelerating_positive", "accelerating_negative",
                                    "decelerating_positive", "decelerating_negative"])
                    st.session_state.match_vt_graph = graphing.generate_velocity_time_graph(graph_type)
                    wrong_answers = ["linear_positive", "linear_negative", 
                                    "accelerating_positive", "accelerating_negative",
                                    "decelerating_positive", "decelerating_negative"]
                    wrong_answers.remove(graph_type)
                    wrong_1 = random.choice(wrong_answers)
                    wrong_answers.remove(wrong_1)
                    wrong_2 = random.choice(wrong_answers)
                    choice_list = [graph_type,wrong_1,wrong_2]
                    random.shuffle(choice_list)
                    # Generate 3 position-time option graphs
                    st.session_state.option_graphs = [
                        graphing.generate_position_time_graph(entry) for entry in choice_list
                    ]

                if st.session_state.match_vt_graph is not None:
                    fig_vt, dir_vt, state_vt = st.session_state.match_vt_graph
                    col1,col2,col3,col4 = st.columns(4)
                    with col1:
                        st.pyplot(fig_vt)
                        st.write("Match this Velocity-Time Graph to the correct Position-Time Graph below.")

                    if st.session_state.option_graphs:
                        option_columns = col2,col3,col4
                        labels = ["A", "B", "C"]

                        for col, label, (fig_pt, dir_pt, state_pt) in zip(option_columns, labels, st.session_state.option_graphs):
                            with col:
                                st.pyplot(fig_pt)
                                st.write(f"Option {label}")

                        user_choice = st.selectbox(
                            "Which Position-Time graph matches the V-T graph above?",
                            labels
                        )

                        if st.button("Check Match"):
                            chosen_index = labels.index(user_choice)
                            _, dir_pt_selected, state_pt_selected = st.session_state.option_graphs[chosen_index]

                            if (dir_pt_selected == dir_vt) and (state_pt_selected == state_vt):
                                st.success("Correct match!")
                            else:
                                st.error("Incorrect match. Try again or generate a new set.")
                    else:
                        st.info("Click 'Generate New Matching Set' to see the option graphs.")


class linear_fns:
    @ staticmethod
    def question_parameters():
        """Holds current options for questions for centralized updating"""

        problem_type_dict = {
                        "Mixed": {
                            "honors": r"""v_f^2 = v_i^2 + 2ax \quad ,
                            \quad v_f = v_i +at  \quad ,
                            \quad x = \frac{v_f + v_i}{2} t  \quad ,
                            \quad x = v_i t + \frac{1}{2} at^2""",

                            "conceptual": r"""
                            \quad x = \frac{v_f + v_i}{2} t  \quad
                            \quad x = \frac{1}{2} at^2  \quad
                            \quad x = \frac{v_f^2 - v_i^2}{2a}  \quad

                            \newline ~ \newline ~ \newline
                            \quad v_f = \frac{2x}{t} - v_i  \quad
                            \quad v_f = \sqrt{v_i^2 + 2ax}  \quad
                            \quad v_f = v_i + at  \quad
                            
                            \newline ~ \newline ~ \newline
                            \quad v_i = \sqrt{2ax - v_f^2}  \quad
                            \quad v_i = v_f - at  \quad
                            \quad v_i = \frac{2x}{t} - v_f  \quad
                            \newline ~ \newline ~ \newline
                            \quad t = \frac{2x}{v_f + v_i}  \quad 
                            \quad t = \sqrt{ \frac{2x}{a} }  \quad
                            \quad t = \frac{v_f - v_i}{a}  \quad
                            \newline ~ \newline ~ \newline
                                \quad a = \frac{2x}{t^2}  \quad 
                                \quad a = \frac{v_f - v_i}{t}  \quad
                                \quad a = \frac{v_f^2 - v_i^2}{2x}  \quad
                            
                            """},
                        "No Time": {
                            "honors" : r"v_f^2 = v_i^2 + 2ax", 
                            "conceptual": r"""v_f = \sqrt{v_i^2 + 2ax}  \quad , 
                            \quad v_i = \sqrt{2ax - v_f^2}  \quad , 
                            \quad  x = \frac{v_f^2 - v_i^2}{2a}  \quad,
                            \quad  a = \frac{v_f^2 - v_i^2}{2x}"""
                            },
                        "No Distance": {
                            "honors": r"v_f = v_i + at",
                            "conceptual": r"""v_f = v_i +at  \quad ,
                            \quad v_i =  v_f - at  \quad ,
                            \quad a = \frac{v_f - v_i}{t}  \quad,
                            \quad t = \frac{v_f - v_i}{a}"""
                        },               
                        "No Acceleration" : {
                            "honors": r"x = \frac{v_f + v_i}{2} t",
                            "conceptual": r"""x = \frac{v_f + v_i}{2} t  \quad ,
                            \quad t = \frac{2d}{v_f + v_i}  \quad ,
                            \quad v_f = \frac{2d}{t} - v_i  \quad , 
                            \quad v_i = \frac{2d}{t} - v_f  \quad """
                        },
                        "No Final Velocity": {
                            "honors": r"x = v_i t + \frac{1}{2} at^2",
                            "conceptual": r"""x = \frac{1}{2} at^2  \quad ,
                            \quad a = \frac{2x}{t^2}  \quad ,
                            \quad t = \sqrt{ \frac{2d}{a} }"""
                        },
                        }


        
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, difficulties

    @staticmethod
    def main():
        title = "Accelerated Motion"
        prefix = "accelerated_motion"
        problem_type_dict, difficulties = linear_fns.question_parameters()
        generator = LinearMotionGenerator()
        ui = interface(prefix,title,generator,problem_type_dict,difficulties)
        ui.default_layout()
    


class Projectile_fns:
     @ staticmethod
     def question_parameters():
            """Holds current options for questions for centralized updating"""

            problem_type_dict = {
                "Type 1": {
                      "honors": r"""currently under construction, ask your teacher to hurry up!""",

                      "conceptual": r"""currently under construction, ask your teacher to hurry up!
                      """},
                "Type 2": {
                    "honors" : r"currently under construction, ask your teacher to hurry up!", 
                    "conceptual": r"""currently under construction, ask your teacher to hurry up!"""
                    },
                "Type 3": {
                    "honors": r"currently under construction, ask your teacher to hurry up!",
                    "conceptual": r"""currently under construction, ask your teacher to hurry up!"""
                }
                }
            
            difficulties = ["Easy","Medium","Hard"]
            return problem_type_dict, difficulties

     @staticmethod
     def main():
        title = "Projectiles"
        prefix = "projectiles"
        problem_type_dict, difficulties = Projectile_fns.question_parameters()
        generator = ProjectileGenerator()
        
        ui = interface(prefix,title,generator,problem_type_dict,difficulties,True)
        ui.default_layout()

class constant_motion:
    @ staticmethod
    def question_parameters():
            """Holds current options for questions for centralized updating"""

            problem_type_dict = {
                "One Dimensional": {
                      "honors": r"""
                      \textrm{distance } =\; d_1 + d_2 + ... \newline ~ \newline
                      \textrm{displacement } =\; d_{final} - d_{initial} \; \textrm{(with direction)}
                      """,

                      "conceptual": r"""
                      \textrm{distance } =\; d_1 + d_2 + ... 
                      
                     \newline ~ \newline \textrm{"Positive" directions are right, East, up, and North}
                     \newline ~ \newline \textrm{"Negative" directions are left, West, down, and South}
                     \newline ~ \newline \textrm{displacement } =\; d_{final} - d_{initial} \; \textrm{(with direction)}
                      """},
                "Two Dimensional": {
                      "honors": r"""
                      \textrm{distance } =\; d_1 + d_2 + ... \newline ~ \newline
                    \textrm{displacement } =\; \sqrt{d_{horizontal}^2 + d_{vertical}^2} \;\; \textrm{(with direction)}
                      """,

                      "conceptual": r"""
                      \textrm{distance } =\; d_1 + d_2 + ... \newline ~ \newline
                      \textrm{Horizontal Displacement } =\; D_{East} - D_{West} \newline ~ \newline
                      \textrm{Vertical Displacement } =\; D_{North} - D_{South} \newline ~ \newline
                    \textrm{Net Displacement } =\; \sqrt{D_{horizontal}^{\;2} + D_{vertical}^2} \;\; \textrm{(with direction)}
                      """},
                
                }
    
            difficulties = ["Easy","Medium","Hard"]
            return problem_type_dict, difficulties

    @staticmethod
    def main():
        title = "Constant Motion"
        prefix = "constant"
        problem_type_dict, difficulties = constant_motion.question_parameters()
        generator = LinearMotionGenerator()
        
        ui = interface(prefix,title,generator,problem_type_dict,difficulties,True)
        ui.diagram_layout()

def main():
    # Add tabs for quiz and explorer modes
    tab1, tab2,tab3,tab4 = st.tabs(["Constant Motion","Accelerated Motion", "Graphing Practice","Projectile Practice"])
    
    with tab1:
        constant_motion.main()
    with tab2:
        linear_fns.main()
    with tab3:
        graphing.graphing_practice()
    with tab4:
        Projectile_fns.main()

if __name__ == "__main__":
    main()

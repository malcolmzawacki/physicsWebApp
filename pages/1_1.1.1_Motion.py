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
from utils.ui import interface

class motion_graphs:
    def graphing_practice():
        from utils.generators.motion_graph_generator import MotionGraphGenerator
        graph_types = ["linear_positive", "linear_negative", 
                                        "accelerating_positive", "accelerating_negative",
                                        "decelerating_positive", "decelerating_negative"]
        generator = MotionGraphGenerator(graph_types,prefix="_motion_graphs")
        generator.graphing_practice()


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


def linear_fns():
    problem_type_dict = {
                    
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
                        \quad t = \frac{2x}{v_f + v_i}  \quad ,
                        \quad v_f = \frac{2x}{t} - v_i  \quad , 
                        \quad v_i = \frac{2x}{t} - v_f  \quad """
                    },
                    "No Final Velocity": {
                        "honors": r"x = v_i t + \frac{1}{2} at^2",
                        "conceptual": r"""
                        x = v_i t + \frac{1}{2} at^2  \quad ,
                        \quad a = 2 \left( \frac{x - v_i t}{t^2} \right)\quad ,
                        \quad t = \frac{\sqrt{v_i^2 + 2ax} - v_i}{a}"""
                    },
                    "Mixed": {
                        "honors": r"""v_f^2 = v_i^2 + 2ax \quad ,
                        \quad v_f = v_i +at  \quad ,
                        \quad x = \frac{v_f + v_i}{2} t  \quad ,
                        \quad x = v_i t + \frac{1}{2} at^2""",

                        "conceptual": r"""
                        \quad x = \frac{v_f + v_i}{2} t  \quad
                        \quad x = v_i t + \frac{1}{2} at^2  \quad
                        \quad x = \frac{v_f^2 - v_i^2}{2a}  \quad

                        \newline ~ \newline ~ \newline
                        \quad t = \frac{2x}{v_f + v_i}  \quad 
                        \quad t = \frac{v_f - v_i}{a}  \quad
                        \quad t = \frac{\sqrt{v_i^2 + 2ax} - v_i}{a}  \quad
                        
                        \newline ~ \newline ~ \newline
                        \quad v_i = \sqrt{2ax - v_f^2}  \quad
                        \quad v_i = v_f - at  \quad
                        \quad v_i = \frac{2x}{t} - v_f  \quad
                        \quad v_i = \frac{x}{t} - \frac{1}{2} at \quad

                        \newline ~ \newline ~ \newline
                        \quad v_f = \frac{2x}{t} - v_i  \quad
                        \quad v_f = \sqrt{v_i^2 + 2ax}  \quad
                        \quad v_f = v_i + at  \quad

                        \newline ~ \newline ~ \newline
                        \quad a = 2 \left( \frac{x - v_i t}{t^2} \right)\quad 
                        \quad a = \frac{v_f - v_i}{t}  \quad
                        \quad a = \frac{v_f^2 - v_i^2}{2x}  \quad
                        
                        """},
                    }

    difficulties = ["Easy","Medium","Hard"]

    from utils.generators.linear_motion_generator import LinearMotionGenerator
    title = "Accelerated Motion"
    prefix = "accelerated_motion"

    ui = interface(prefix,title,
                    LinearMotionGenerator(),problem_type_dict,difficulties)
    ui.default_layout()


def projectile_fns():
        
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

    from utils.generators.projectile_generator import ProjectileGenerator
    title = "Projectiles"
    prefix = "projectiles"
    ui = interface(prefix,title,ProjectileGenerator(),
                    problem_type_dict,difficulties,True)
    ui.default_layout()


def distance_displacement():
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
    from utils.generators.dist_disp_generator import DistDispGenerator
    title = "Distance & Displacement"
    prefix = "constant"
    ui = interface(prefix,title,DistDispGenerator(),
                problem_type_dict,difficulties,True)
    ui.diagram_layout()

def position_and_velocity_graph_analysis():
    # Setup for standard interface
    problem_type_dict = {
        "Position-Time Graph": {
            "honors": r"\text{Direction and motion from position-time graphs}",
            "conceptual": r"""
            \text{Positive slope: moving in positive direction} \\
            \text{Negative slope: moving in negative direction} \\
            \text{Straight line: constant velocity} \\
            \text{Curved (increasing): speeding up} \\
            \text{Curved (decreasing): slowing down}
            """
        },
        "Velocity-Time Graph": {
            "honors": r"\text{Direction and motion from velocity-time graphs}",
            "conceptual": r"""
            \text{Above x-axis: moving in positive direction} \\
            \text{Below x-axis: moving in negative direction} \\
            \text{Horizontal line: constant velocity} \\
            \text{Sloped line (increasing): speeding up} \\
            \text{Sloped line (decreasing): slowing down}
            """
        },
    }
    from utils.generators.motion_graph_generator import MotionGraphGenerator
    difficulties = ["Easy", "Medium", "Hard"]
    generator = MotionGraphGenerator()
    ui = interface("motion_graph", "Graph Analysis", generator, problem_type_dict, difficulties)
    ui.button_layout(generator.display_current_graph)

def PvT_and_VvT_graph_matching():
    from utils.generators.motion_graph_generator import MotionGraphGenerator
    """Custom implementation for graph matching activity"""
    # Initialize state for the matching activity
    if "matching_initialized" not in st.session_state:
        st.session_state.matching_initialized = True
        st.session_state.match_graph = None
        st.session_state.option_graphs = None
        st.session_state.match_stars = 0
    
    # Display star count
    if st.session_state.match_stars > 0:
        st.write(f"⭐ x {st.session_state.match_stars}")
    
    # Setup graph types
    graph_types = ["linear_positive", "linear_negative", 
                  "accelerating_positive", "accelerating_negative",
                  "decelerating_positive", "decelerating_negative"]
    
    # Let user choose which graph type to show first
    show_pt_first = st.radio("Select primary graph type:", 
                         ["Position-Time First", "Velocity-Time First"],
                         horizontal=True)
    
    # Generate matching graphs button
    if st.button("Generate New Matching Set"):
        # Choose a random graph type
        graph_type = random.choice(graph_types)
        
        if show_pt_first == "Position-Time First":
            # Create main position-time graph
            generator = MotionGraphGenerator()
            fig_match, dir_match, state_match = generator.generate_position_time_graph(graph_type,rowsize=5,colsize=2)
            
            # Create incorrect options
            wrong_answers = graph_types.copy()
            wrong_answers.remove(graph_type)
            wrong_1 = random.choice(wrong_answers)
            wrong_answers.remove(wrong_1)
            wrong_2 = random.choice(wrong_answers)
            
            # Create option list with correct and incorrect answers
            choice_list = [graph_type, wrong_1, wrong_2]
            random.shuffle(choice_list)
            
            # Generate velocity graphs for options
            option_graphs = [
                generator.generate_velocity_time_graph(entry,rowsize=5,colsize=3) for entry in choice_list
            ]
            
            # Store in session state
            st.session_state.match_graph = (fig_match, dir_match, state_match)
            st.session_state.option_graphs = option_graphs
            st.session_state.correct_index = choice_list.index(graph_type)
        
        else:  # Velocity-Time First
            # Create main velocity-time graph
            generator = MotionGraphGenerator()
            fig_match, dir_match, state_match = generator.generate_velocity_time_graph(graph_type,rowsize=5,colsize=2)
            
            # Create incorrect options
            wrong_answers = graph_types.copy()
            wrong_answers.remove(graph_type)
            wrong_1 = random.choice(wrong_answers)
            wrong_answers.remove(wrong_1)
            wrong_2 = random.choice(wrong_answers)
            
            # Create option list with correct and incorrect answers
            choice_list = [graph_type, wrong_1, wrong_2]
            random.shuffle(choice_list)
            
            # Generate position graphs for options
            option_graphs = [
                generator.generate_position_time_graph(entry,rowsize=5,colsize=3) for entry in choice_list
            ]
            
            # Store in session state
            st.session_state.match_graph = (fig_match, dir_match, state_match)
            st.session_state.option_graphs = option_graphs
            st.session_state.correct_index = choice_list.index(graph_type)
    
    # Display the matching activity if we have graphs
    if st.session_state.match_graph is not None:
        fig_match, dir_match, state_match = st.session_state.match_graph
        
        # Determine graph titles based on order
        if show_pt_first == "Position-Time First":
            main_title = "Position-Time Graph"
            option_title = "Velocity-Time Graph"
        else:
            main_title = "Velocity-Time Graph"
            option_title = "Position-Time Graph"
        
        # Display main graph
        st.write(f"Match this {main_title} to the correct {option_title}:")
        st.pyplot(fig_match)
        
        # Display option graphs
        if st.session_state.option_graphs:
            # Create columns for options
            cols = st.columns(3)
            labels = ["A", "B", "C"]
            
            # Display each option
            for i, ((fig_opt, _, _), col, label) in enumerate(zip(st.session_state.option_graphs, cols, labels)):
                with col:
                    st.write(f"Option {label}")
                    st.pyplot(fig_opt)
            
            # Let user select an answer
            user_choice = st.radio("Which graph matches?", labels, horizontal=True)
            
            # Check answer button
            if st.button("Check Match"):
                chosen_index = labels.index(user_choice)
                correct_index = st.session_state.correct_index
                
                if chosen_index == correct_index:
                    st.success("Correct match! The graphs have matching direction and motion state.")
                    st.session_state.match_stars += 1
                else:
                    st.error("Incorrect match. Try again or generate a new set.")
        else:
            st.info("Click 'Generate New Matching Set' to see the options.")
    else:
        st.info("Click 'Generate New Matching Set' to start.")


def main():
    # Add tabs for quiz and explorer modes
    tab1, tab2,tab3,tab4,tab5 = st.tabs(["Distance & Displacement",
                                    "Accelerated Motion", 
                                    "Types of Motion Graphs",
                                    "Matching Motion Graphs",
                                    "Projectiles"])
    
    with tab1:
        distance_displacement()
    with tab2:
        linear_fns()
    with tab3:
        position_and_velocity_graph_analysis()
    with tab4:
        PvT_and_VvT_graph_matching()
    with tab5:
        projectile_fns()

if __name__ == "__main__":
    main()

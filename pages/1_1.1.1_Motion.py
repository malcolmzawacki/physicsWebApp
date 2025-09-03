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
    ui.button_layout()


def PvT_and_VvT_graph_matching():
    from utils.generators.motion_graph_generator import MotionGraphGenerator
    # Initialize state for the matching activity
    if "matching_initialized" not in st.session_state:
        st.session_state.matching_initialized = True
        st.session_state.match_graph = None
        st.session_state.option_graphs = None
        st.session_state.match_stars = 0
    
    col1,col2 = st.columns([3,1])
    with col1:
        st.title("Matching Motion Graphs")
    with col2:
    # Display star count
        if st.session_state.match_stars > 0:
            st.title(f"⭐ x {st.session_state.match_stars}")
    
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
    tab2,tab3,tab4,tab5 = st.tabs([
                                    "Accelerated Motion", 
                                    "Types of Motion Graphs",
                                    "Matching Motion Graphs",
                                    "Projectiles"
                                    ])
    
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

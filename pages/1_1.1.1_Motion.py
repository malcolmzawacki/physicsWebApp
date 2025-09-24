import streamlit as st
import matplotlib.pyplot as plt
import random

# Use a dark background for matplotlib so it fits a "dark mode" style
plt.style.use("dark_background")

from utils.ui import interface
from tools.loading import lazy_tabs
def linear_fns():
    # Lazy import - only load when this tab is actually accessed
    from utils.generators.linear_motion_generator import LinearMotionGenerator
    generator = LinearMotionGenerator()
    metadata = generator.stored_metadata()


    difficulties = ["Easy","Medium","Hard"]

    title = "Accelerated Motion"
    prefix = "accelerated_motion"

    ui = interface(prefix,title,
                    generator,metadata,difficulties)
    ui.unified_smart_layout()


def projectile_fns():
    # Lazy import - only load when this tab is actually accessed
    from utils.generators.projectile_generator import ProjectileGenerator

    generator = ProjectileGenerator()
    metadata = generator.stored_metadata()
    
    difficulties = ["Easy","Medium","Hard"]

    title = "Projectiles"
    prefix = "projectiles"
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def position_and_velocity_graph_analysis():
    # Lazy import - only load when this tab is actually accessed
    from utils.generators.motion_graph_generator import MotionGraphGenerator

    difficulties = ["Easy", "Medium", "Hard"]
    generator = MotionGraphGenerator()
    metadata = generator.stored_metadata()
    prefix = "motion_graph"
    title = "Analyzing Motion Graphs"
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout(side_by_side=True, equations=False, expanded=True)


def PvT_and_VvT_graph_matching():
    # Lazy import - only load when this tab is actually accessed
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


def constant_motion():
    # Lazy import - only load when this tab is actually accessed
    from utils.generators.const_motion_generator import ConstantMotionGenerator

    generator = ConstantMotionGenerator()
    metadata = generator.stored_metadata()
    difficulties = ["Easy","Medium","Hard"]
    title = "Constant Motion"
    prefix = "const_motion_"
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()

    
def main():
    tab_specs = [
        ("Constant Motion", constant_motion),
        ("Accelerated Motion", linear_fns),
        ("Types of Motion Graphs", position_and_velocity_graph_analysis),
        ("Matching Motion Graphs", PvT_and_VvT_graph_matching),
        ("Projectiles", projectile_fns),
    ]

    lazy_tabs(tab_specs, state_key="motion_tabs", auto_load_first=True)

if __name__ == "__main__":
    main()


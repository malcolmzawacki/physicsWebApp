import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# Use a dark background for matplotlib so it fits a "dark mode" style
plt.style.use("dark_background")
# Randomly pick one of four "types"
graph_type = random.choice(["at_rest","linear_positive", "linear_negative", 
    "acceleration_positive", "acceleration_negative","deceleration_positive","deceleration_negative"])
def state_of_motion_nums(graph_type):
    if graph_type == "at_rest":
        p_0 = random.randint(-5,5)
        v_0 = 0
        a = 0
    elif graph_type == "linear_positive":
        p_0 = random.randint(-5,5)
        v_0 = random.randint(1,5)
        a = 0
    elif graph_type == "linear_negative":
        p_0 = random.randint(-5,5)
        v_0 = random.randint(-5,-1)
        a = 0
    elif graph_type == "acceleration_positive":
        p_0 = random.randint(-5,5)
        v_0 = random.randint(0,2)
        a = random.randint(2,5)
    elif graph_type == "acceleration_negative":
        p_0 = random.randint(-5,5)
        v_0 = random.randint(-2,0)
        a = random.randint(-5,-2)
    elif graph_type == "deceleration_positive":
        p_0 = random.randint(-5,5)
        v_0 = random.randint(4,8)
        a = -1* (v_0/5) # prevents direction change
    else: #graph_type == "deceleration_negative"
        p_0 = random.randint(-5,5)
        v_0 = random.randint(-8,-4)
        a = -1* (v_0/5)
    
    return p_0, v_0, a
def generate_position_time_graph(graph_type,p_0, v_0, a):
    """
    Returns (fig, direction, motion_state, graph_label) for a randomly generated position-time graph
    """
    fig, ax = plt.subplots(figsize=(3, 2))  # Smaller figure size
    t = np.linspace(0, 5, 100)

    # Randomly pick "type"
    if graph_type == "at_rest":
        position = np.ones_like(t)*p_0
        correct_direction = "None"
        correct_motion_state = "At Rest"
    elif graph_type == "linear_positive":
        position = v_0 * t + p_0    # slope > 0, constant velocity
        correct_direction = "Forward (Positive)"
        correct_motion_state = "Constant Velocity"
    elif graph_type == "linear_negative":
        position = v_0 * t + p_0 # slope < 0, constant velocity
        correct_direction = "Backward (Negative)"
        correct_motion_state = "Constant Velocity"
    elif graph_type == "acceleration_positive":
        position = 0.5*a*t**2 + v_0*t + p_0       # slope increasing over time
        correct_direction = "Forward (Positive)"
        correct_motion_state = "Accelerating (Positive)"
    elif graph_type == "acceleration_negative":
        position = 0.5*a*t**2 + v_0*t + p_0
        correct_direction = "Backward (Negative)"
        correct_motion_state = "Accelerating (Negative)"
    elif graph_type == "deceleration_negative":
        position = 0.5*a*t**2 + v_0*t + p_0
        correct_direction = "Backward (Negative)"
        correct_motion_state = "Decelerating (Positive)"
    else:
        position = 0.5*a*t**2 + v_0*t + p_0
        correct_direction = "Forward (Positive)"
        correct_motion_state = "Decelerating (Negative)"
        



    ax.plot(t, position, color="cyan")
    ax.set_xlabel("Time (s)", color="white")
    ax.set_ylabel("Position (m)", color="white")
    ax.set_title("Position-Time Graph", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    fig.tight_layout()

    return (fig, correct_direction, correct_motion_state)


def generate_velocity_time_graph(graph_type, v_0, a):
    """
    Returns (fig, direction, motion_state) for a randomly generated velocity-time graph
    """
    fig, ax = plt.subplots(figsize=(3, 2))  # Smaller figure size
    t = np.linspace(0, 5, 100)

    # Randomly pick one of four "types"
    p_0, v_0, a = state_of_motion_nums(graph_type)
    if graph_type == "at_rest":
        velocity = np.ones_like(t) - 1
        correct_direction = "None"
        correct_motion_state = "At Rest"
    elif graph_type == "linear_positive":
        velocity = np.ones_like(t) * v_0
        correct_direction = "Forward (Positive)"
        correct_motion_state = "Constant Velocity"
    elif graph_type == "linear_negative":
        velocity = np.ones_like(t) * v_0
        correct_direction = "Backward (Negative)"
        correct_motion_state = "Constant Velocity"
    elif graph_type == "acceleration_positive":
        velocity = a*t + v_0      # slope increasing over time
        correct_direction = "Forward (Positive)"
        correct_motion_state = "Accelerating (Positive)"
    elif graph_type == "acceleration_negative":
        velocity = a*t + v_0
        correct_direction = "Backward (Negative)"
        correct_motion_state = "Accelerating (Negative)"
    elif graph_type == "deceleration_negative":
        velocity = a*t + v_0
        correct_direction = "Backward (Negative)"
        correct_motion_state = "Decelerating (Positive)"
    else:
        velocity = a*t + v_0
        correct_direction = "Forward (Positive)"
        correct_motion_state = "Decelerating (Negative)"

    ax.plot(t, velocity, color="orange")
    ax.set_xlabel("Time (s)", color="white")
    ax.set_ylabel("Velocity (m/s)", color="white")
    ax.set_title("Velocity-Time Graph", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    fig.tight_layout()

    return (fig, correct_direction, correct_motion_state)


def app():
    st.title("Motion Graphs")
    #st.write("Use this page to practice identifying direction and state of motion from different graphs.")
    type_list = ["at_rest","linear_positive", "linear_negative", 
    "acceleration_positive", "acceleration_negative","deceleration_positive","deceleration_negative"]

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
    main_col1, main_col2 = st.columns(2)
    with main_col1:
        mode = st.selectbox("Select a Practice Mode:", 
                    ["Position-Time Graph", "Velocity-Time Graph", "Match Graphs"])

    # --------------------------------------------
    # 1) POSITION-TIME GRAPH
    # --------------------------------------------
    if mode == "Position-Time Graph":
        # If there's no stored graph yet or user wants a new one, generate it
        with main_col2:
            st.write("")
            if st.button("Generate New Graph"):
                graph_type = random.choice(type_list)
                p_0, v_0, a = state_of_motion_nums(graph_type)
                st.session_state.pt_graph = generate_position_time_graph(graph_type,p_0, v_0, a)

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
                    ["None","Forward (Positive)", "Backward (Negative)"]
                )
                user_state = st.selectbox(
                    "Select the state of motion:", 
                    ["At Rest","Constant Velocity", "Accelerating (Positive)", "Accelerating (Negative)",
                     "Decelerating (Positive)","Decelerating (Negative)"]
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
        with main_col2:
            st.write("")
            if st.button("Generate New Graph"):
                graph_type = random.choice(type_list)
                _, v_0, a = state_of_motion_nums(graph_type)
                st.session_state.vt_graph = generate_velocity_time_graph(graph_type, v_0, a)

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
                    ["None","Forward (Positive)", "Backward (Negative)"]
                )
                user_state = st.selectbox(
                    "Select the state of motion:", 
                    ["At Rest","Constant Velocity", "Accelerating (Positive)", "Accelerating (Negative)",
                     "Decelerating (Positive)","Decelerating (Negative)"]
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
        with main_col1:
            st.write("You'll see either a position-time or velocity-time graph and try to match it among multiple options of the other type.")

        # We randomly decide which main graph to show (P-T or V-T)
        with main_col2:
            show_pt_first = st.selectbox("Which primary graph type?", 
                                 ["Position-Time First", "Velocity-Time First"])
        sample_col1, sample_col2 = st.columns(2)
        if show_pt_first == "Position-Time First":
            # If we don't have a stored graph or user wants a new scenario
            with main_col2:
                if st.button("Generate New Matching Set"):
                    graph_type = random.choice(type_list)
                    # Generate 2 incorrect options
                    remaining_choices = type_list.copy()
                    remaining_choices.pop(type_list.index(graph_type))
                    incorrect_1 = random.choice(remaining_choices)
                    remaining_choices.pop(remaining_choices.index(incorrect_1))
                    incorrect_2 = random.choice(remaining_choices)
                    p_0, v_0, a = state_of_motion_nums(graph_type)
                    _, v_01, a1 = state_of_motion_nums(incorrect_1)
                    _, v_02, a2 = state_of_motion_nums(incorrect_2)
                    st.session_state.match_pt_graph = generate_position_time_graph(graph_type,p_0, v_0, a)
                    st.session_state.option_graphs = [
                        generate_velocity_time_graph(graph_type,v_0,a),
                        generate_velocity_time_graph(incorrect_1,v_01,a1),
                        generate_velocity_time_graph(incorrect_2,v_02,a2)
                    ]
                    random.shuffle(st.session_state.option_graphs)

            if st.session_state.match_pt_graph is not None:
                fig_pt, dir_pt, state_pt = st.session_state.match_pt_graph
                
                with sample_col1:
                    st.pyplot(fig_pt)
                with sample_col2:
                    st.write(" ")
                    st.write(" ")
                    st.write("""Which of the Velocity-Time Graphs below match 
                             the Position-Time Graph on the left?""")
                    
                col1,col2,col3 = st.columns(3)
                    
                # Display option graphs in columns
                if st.session_state.option_graphs:
                    option_columns = col1,col2,col3
                    labels = ["A", "B", "C"]

                    for col, label, (fig_vt, dir_vt, state_vt) in zip(option_columns, labels, st.session_state.option_graphs):
                        with col:
                            st.pyplot(fig_vt)
                            #st.write(f"Option {label}")
                            st.markdown(
                                f"<p style='text-align: center; font-size:16px;'>{label}</p>",
                                unsafe_allow_html=True)
                            

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
            with main_col2:
                if st.button("Generate New Matching Set"):
                    graph_type = random.choice(type_list)
                    # Generate 2 incorrect options
                    remaining_choices = type_list.copy()
                    remaining_choices.pop(type_list.index(graph_type))
                    incorrect_1 = random.choice(remaining_choices)
                    remaining_choices.pop(remaining_choices.index(incorrect_1))
                    incorrect_2 = random.choice(remaining_choices)
                    p_0, v_0, a = state_of_motion_nums(graph_type)
                    p_01, v_01, a1 = state_of_motion_nums(incorrect_1)
                    p_02, v_02, a2 = state_of_motion_nums(incorrect_2)
                    st.session_state.match_vt_graph = generate_velocity_time_graph(graph_type, v_0, a)
                    st.session_state.option_graphs = [
                        generate_position_time_graph(graph_type,p_0,v_0,a),
                        generate_position_time_graph(incorrect_1,p_01,v_01,a1),
                        generate_position_time_graph(incorrect_2,p_02,v_02,a2)
                    ]
                    random.shuffle(st.session_state.option_graphs)

            if st.session_state.match_vt_graph is not None:
                fig_vt, dir_vt, state_vt = st.session_state.match_vt_graph
                with sample_col1:
                    st.pyplot(fig_vt)
                with sample_col2:
                    st.write(" ")
                    st.write(" ")
                    st.write("""Which of the Position-Time Graphs below match 
                             the Velocity-Time Graph on the left?""")
                col1,col2,col3 = st.columns(3)

                if st.session_state.option_graphs:
                    option_columns = col1,col2,col3
                    labels = ["A", "B", "C"]

                    for col, label, (fig_pt, dir_pt, state_pt) in zip(option_columns, labels, st.session_state.option_graphs):
                        with col:
                            st.pyplot(fig_pt)
                            st.markdown(
                                f"<p style='text-align: center; font-size:16px;'>{label}</p>",
                                unsafe_allow_html=True)

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

# If this page is run standalone, then start app()
if __name__ == "__main__":
    app()

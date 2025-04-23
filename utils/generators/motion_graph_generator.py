import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

class MotionGraphGenerator:
    def __init__(self, graph_types,prefix):
        #super().__init__(state_prefix="motion_graphs_")
        self.graph_types = graph_types
        self.prefix = prefix
    


    def generate_position_time_graph(self,graph_type: str):
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


    def generate_velocity_time_graph(self,graph_type: str):
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
    

    def generate_position_matches(self, graph_type: str):
        match = self.generate_position_time_graph(graph_type)
        wrong_answers = self.graph_types.copy()
        wrong_answers.remove(graph_type)
        wrong_1 = random.choice(wrong_answers)
        wrong_answers.remove(wrong_1)
        wrong_2 = random.choice(wrong_answers)
        choice_list = [graph_type,wrong_1,wrong_2]
        random.shuffle(choice_list)
        # Generate 3 velocity-time option graphs
        options = [
            self.generate_velocity_time_graph(entry) for entry in choice_list
        ]
        return match, options, None


    def generate_velocity_matches(self, graph_type: str):
        match = self.generate_velocity_time_graph(graph_type)
        wrong_answers = self.graph_types.copy()
        wrong_answers.remove(graph_type)
        wrong_1 = random.choice(wrong_answers)
        wrong_answers.remove(wrong_1)
        wrong_2 = random.choice(wrong_answers)
        choice_list = [graph_type,wrong_1,wrong_2]
        random.shuffle(choice_list)
        # Generate 3 position-time option graphs
        options = [
            self.generate_position_time_graph(entry) for entry in choice_list
        ]
        return match, options, None


    def choose_problem(self, graph_type: str, problem_type: str):
        if problem_type == "Position-Time Graph":
            return self.generate_position_time_graph(graph_type)
        elif problem_type == "Velocity-Time Graph":
            return self.generate_velocity_time_graph(graph_type)
        elif problem_type == "Match Graphs, Position-Time First":
            return self.generate_position_matches(graph_type)
        else:
            return self.generate_velocity_matches(graph_type)


    def initialize_session_state(self):
        if "pt_graph" not in st.session_state:
            st.session_state.pt_graph = None
        if "vt_graph" not in st.session_state:
            st.session_state.vt_graph = None
        
        # For matching mode, we'll store multiple graphs
        if "match_graph" not in st.session_state:
            st.session_state.match_graph = None
        if "option_graphs" not in st.session_state:
            st.session_state.option_graphs = None
        if "mode" not in st.session_state:
            st.session_state.mode = None
        if f"{self.prefix}_stars" not in st.session_state:
            st.session_state[f"{self.prefix}_stars"] = 0
    

    def graphing_practice(self):
        st.title("Position & Velocity vs Time Graphs")
        self.initialize_session_state()
        # Use session state to store the current graph (so it doesn't regenerate on button press)
        
        col1,col2 = st.columns(2)
        with col1:
            mode = st.selectbox("Select a Practice Mode:", 
                        ["Position-Time Graph", 
                         "Velocity-Time Graph", "Match Graphs"])
        with col2:
            if st.session_state[f"{self.prefix}_stars"] != 0:
                star_count = st.session_state[f"{self.prefix}_stars"]
                st.title(f"⭐ x {star_count}")
            else:
                st.write("")

        if mode != st.session_state.mode:
            st.session_state.mode = mode
            st.rerun()
        # --------------------------------------------
        # 1) POSITION-TIME GRAPH
        # --------------------------------------------
        if mode == "Position-Time Graph" or "Velocity-Time Graph":
            # If there's no stored graph yet or user wants a new one, generate it
            if st.button("Generate New Graph"):
                graph_type = random.choice(self.graph_types)
                st.session_state.pt_graph = self.choose_problem(graph_type,mode)
            # If we have a stored graph, display it
            if st.session_state.pt_graph is not None and mode == st.session_state.mode:
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
                            st.session_state[f"{self.prefix}_stars"] +=1
                        else:
                            st.error(f"Incorrect. The correct direction is '{correct_dir}' and the motion state is '{correct_state}'.")
            else:
                st.info("Click 'Generate New Graph' to start.")

        # --------------------------------------------
        # 3) MATCH GRAPHS
        # --------------------------------------------
        elif mode == "Match Graphs":
            st.rerun()
            st.write("You'll see either a position-time or velocity-time graph. Try to match it among multiple options of the other type.")

            # decide which main graph to show (P-T or V-T)
            show_pt_first = st.selectbox("Which primary graph type?", 
                                    ["Position-Time First", "Velocity-Time First"])
            problem_type = ", ".join([mode, show_pt_first])

            
            if st.button("Generate New Matching Set"):
                graph_type = random.choice(self.graph_types)
                st.session_state.match_graph, st.session_state.option_graphs, _ = self.choose_problem(graph_type,problem_type)

            if st.session_state.match_graph is not None:
                fig_match, dir_match, state_match = st.session_state.match_graph
                col1,col2,col3,col4 = st.columns(4)
                with col1:
                    st.pyplot(fig_match)
                    st.write("Match this Position-Time Graph to the correct Velocity-Time Graph")

                # Display option graphs in columns
                if st.session_state.option_graphs:
                    option_columns = col2,col3,col4
                    labels = ["A", "B", "C"]

                    for col, label, (fig_opt, _, _) in zip(option_columns, labels, st.session_state.option_graphs):
                        with col:
                            st.pyplot(fig_opt)
                            st.write(f"Option {label}")
                            

                    # Let user pick which one is correct
                    user_choice = st.selectbox(
                        "Which Velocity-Time graph matches the Positon-Time graph above?", 
                        labels
                    )

                    if st.button("Check Match"):
                        chosen_index = labels.index(user_choice)
                        _, dir_opt_selected, state_opt_selected = st.session_state.option_graphs[chosen_index]

                        # Basic matching logic: compare direction & motion state
                        # (You might want more sophisticated logic in practice)
                        if (dir_match == dir_opt_selected) and (state_match == state_opt_selected):
                            st.success("Correct match!")
                        else:
                            st.error("Incorrect match. Try again or generate a new set.")
                else:
                    st.info("Click 'Generate New Matching Set' to see the option graphs.")
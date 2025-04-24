# utils/generators/motion_graph_generator.py
import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
from utils.generators.base_generator import BaseGenerator

class MotionGraphGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="motion_graph_")
        self.graph_types = ["linear_positive", "linear_negative", 
                           "accelerating_positive", "accelerating_negative",
                           "decelerating_positive", "decelerating_negative"]
        plt.style.use("dark_background")
    
    def get_difficulty_range(self, difficulty):
        # Required by BaseGenerator
        if difficulty == "Easy":
            return 5
        elif difficulty == "Hard":
            return 20
        return 10

    def generate_position_time_graph(self, graph_type=None, rowsize = 3, colsize = 3):
        """Generate a position-time graph"""
        if graph_type is None:
            graph_type = random.choice(self.graph_types)
            
        fig, ax = plt.subplots(figsize=(rowsize,colsize))
        t = np.linspace(0, 5, 100)

        if graph_type == "linear_positive":
            position = 2 * t + 1
            correct_direction = "Positive"
            correct_motion_state = "Constant Velocity"
        elif graph_type == "linear_negative":
            position = -1.5 * t + 5
            correct_direction = "Negative"
            correct_motion_state = "Constant Velocity"
        elif graph_type == "accelerating_positive":
            position = t**2
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
        else:  # "accelerating_negative"
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

    def generate_velocity_time_graph(self, graph_type=None,rowsize = 3, colsize = 3):
        """Generate a velocity-time graph"""
        if graph_type is None:
            graph_type = random.choice(self.graph_types)
            
        fig, ax = plt.subplots(figsize=(rowsize, colsize))
        t = np.linspace(0, 5, 100)

        if graph_type == "linear_positive":
            velocity = np.ones_like(t) * 2
            correct_direction = "Positive"
            correct_motion_state = "Constant Velocity"
        elif graph_type == "linear_negative":
            velocity = np.ones_like(t) * -2
            correct_direction = "Negative"
            correct_motion_state = "Constant Velocity"
        elif graph_type == "accelerating_positive":
            velocity = t
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
        else:  # "accelerating_negative"
            velocity = -t
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

    def choose_problem(self, problem_type, difficulty):
        """Required method for BaseGenerator pattern"""
        # Store the graph_type chosen for this problem
        graph_type = random.choice(self.graph_types)
        
        if problem_type == "Position-Time Graph":
            fig, direction, motion_state = self.generate_position_time_graph(graph_type)
            # Store the graph in session state for display
            st.session_state[f"{self.state_prefix}current_graph"] = fig
            question = "Analyze the position-time graph shown above. What is the direction and state of motion?"
            return question, [direction, motion_state], ["Direction", "Motion State"]
        
        elif problem_type == "Velocity-Time Graph":
            fig, direction, motion_state = self.generate_velocity_time_graph(graph_type)
            # Store the graph in session state for display
            st.session_state[f"{self.state_prefix}current_graph"] = fig
            question = "Analyze the velocity-time graph shown above. What is the direction and state of motion?"
            return question, [direction, motion_state], ["Direction", "Motion State"]
        
        # For the matching activities, we'll handle differently
        else:
            # Return a placeholder - matching will be handled separately
            return "Matching activity requires a different interface", ["None"], ["None"]
    
    # Custom functions for displaying graphs
    def display_current_graph(self):
        """Display the current graph stored in session state"""
        if f"{self.state_prefix}current_graph" in st.session_state:
            st.pyplot(st.session_state[f"{self.state_prefix}current_graph"])
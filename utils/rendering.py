import streamlit as st
from utils.word_lists import random_correct_message
from utils.word_lists import random_error_message

class rendering:
    def __init__(self):
        super().__init__(state_prefix = "rendering_")

    
    def clear_performance_dataframe(self, prefix, problem_types, difficulties):
        """Reset the performance tracking dictionary"""
        _, problem_types, difficulties = self.question_parameters()
            
        performance_dict = {}
        for p_type in problem_types:
            performance_dict[p_type] = {}
            for diff in difficulties:
                performance_dict[p_type][diff] = {'attempts': 0, 'correct': 0}     
        st.session_state[f"{prefix}_performance"] = performance_dict
        return performance_dict


    def create_performance_dataframe(self, prefix):
        """Create a pandas DataFrame from the performance tracking dictionary"""
        performance = st.session_state[f"{prefix}_performance"]
        
        # Create lists to hold data
        rows = []
        
        # Format data for dataframe
        for problem_type, difficulties in performance.items():
            for difficulty, stats in difficulties.items():
                attempts = stats['attempts']
                correct = stats['correct']
                
                # Calculate percentage or display NA if no attempts
                if attempts > 0:
                    percentage = f"{(correct / attempts * 100):.1f}%"
                    display = f"{correct}/{attempts} ({percentage})"
                else:
                    display = "0/0 (0.0%)"
                    
                rows.append({
                    "Problem Type": problem_type,
                    "Difficulty": difficulty,
                    "Performance": display
                })

        
    def update_performance(self, prefix, problem_type, difficulty, is_correct):
            """Update the performance tracking dictionary when an answer is submitted"""
            performance = st.session_state[f"{prefix}_performance"]
            
            # Increment attempts
            performance[problem_type][difficulty]['attempts'] += 1
            
            # Increment correct if answer was correct
            if is_correct:
                performance[problem_type][difficulty]['correct'] += 1
            
            # Update session state
            st.session_state[f"{prefix}_performance"] = performance


    def render_submit(self, prefix, problem_type, difficulty, correct_answer):
        with st.form(f"{prefix}_form"):
            st.session_state[f"{prefix}user_answer"] = st.number_input(
                "Enter your answer:", 
                min_value=0.00, value=None, step=0.01,
                key=f"{prefix}_input")
            submitted = st.form_submit_button("Submit")
            if submitted:
                user_input = st.session_state[f"{prefix}user_answer"]
                correct_answer = st.session_state[f"{prefix}_correct_answer"]
                tolerance = correct_answer * 0.05
                is_correct = abs(user_input - correct_answer) < abs(tolerance)
                if not st.session_state[f"{prefix}_submitted"]:
                    self.update_performance(problem_type, difficulty, is_correct)
                    st.session_state[f"{prefix}_submitted"] = True 
                    if is_correct:
                        st.success(f"{random_correct_message()}")
                        st.session_state[f"{prefix}_stars"] += 1
                    else:
                        st.error(f"{random_error_message()} The correct answer is {correct_answer:.2f}.")

    def initialize_session_state(self,prefix):
   
        none_vars = [
        'current_question',
        'correct_answer',
        'unit',
        'user_answer',
        'submitted',
        'difficulty',
        'problem_type'
        ]

        zero_vars = ["_question_id","_stars"]



        # initialize all vars with prefix
        for var in none_vars:
            if f"{prefix}_{var}" not in st.session_state:
                st.session_state[f"{prefix}_{var}"] = 0

        for var in zero_vars:
            if f"{prefix}_{var}" not in st.session_state:
                st.session_state[f"{prefix}_{var}"] = None
    
        # Initialize performance tracking dictionary if it doesn't exist
        if f"{prefix}_performance" not in st.session_state:
            st.session_state[f"{prefix}_performance"] = self.clear_performance_dataframe()
        
        if f"{prefix}_level" not in st.session_state:
            st.session_state[f"{prefix}_level"] = False

    
    def subheader_ui(self,prefix):
        col1, col2 = st.columns(2)
        with col1:
            st.session_state[f"{prefix}_level"] = st.checkbox(
                "Need Re-Arrangements?", 
                value=False,
                key=f"{prefix}_level_check")
        with col2:
            if st.session_state[f"{prefix}_stars"] != 0:
                star_count = st.session_state[f"{prefix}_stars"]
                st.subheader(f"⭐ x {star_count}")
            else:
                st.write("")
        with st.expander("Your Performance", expanded=False):
            performance_df = self.create_performance_dataframe()
            st.dataframe(performance_df, use_container_width=True)
import streamlit as st
import pandas as pd
from utils.word_lists import random_correct_message
from utils.word_lists import random_error_message

class rendering:
    def __init__(self):
        pass

    
    def clear_performance_dataframe(self, prefix: str, problem_types: list, difficulties: list) -> dict:
        """Initialize/Reset the performance tracking dictionary"""
        performance_dict = {}
        for p_type in problem_types:
            performance_dict[p_type] = {}
            for diff in difficulties:
                performance_dict[p_type][diff] = {'attempts': 0, 'correct': 0}     
        st.session_state[f"{prefix}_performance"] = performance_dict
        return performance_dict



    def create_performance_dataframe(self, performance: dict) -> pd.DataFrame:
        """Create a pandas DataFrame from the performance tracking dictionary"""
        
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
        # Create DataFrame
        df = pd.DataFrame(rows)
        
        # Pivot the dataframe to get desired format
        pivot_df = df.pivot(index="Problem Type", columns="Difficulty", values="Performance")
        
        # Ensure all difficulty levels are present
        for col in difficulties:
            if col not in pivot_df.columns:
                pivot_df[col] = "0/0 (0.0%)"
        
        # Reorder columns
        pivot_df = pivot_df[list(difficulties.keys())]
        
        return pivot_df



    def update_performance(self, prefix: str, problem_type: str, difficulty: str, is_correct: bool) -> dict:
            """Update the performance tracking dictionary when an answer is submitted"""
            performance = st.session_state[f"{prefix}_performance"]
            
            # Increment attempts
            performance[problem_type][difficulty]['attempts'] += 1
            
            # Increment correct if answer was correct
            if is_correct:
                performance[problem_type][difficulty]['correct'] += 1
            
            # Update session state
            st.session_state[f"{prefix}_performance"] = performance



    def initialize_session_state(self, prefix: str, problem_types: list, difficulties: list) -> None:
        """takes commonly used streamlit state variables and initializes them for the page to use"""

        none_vars = [
        'current_question',
        'correct_answer',
        'unit',
        'user_answer',
        'submitted',
        'difficulty',
        'problem_type'
        ]

        zero_vars = ["question_id","stars"]

        # initialize all vars with prefix
        for var in none_vars:
            if f"{prefix}_{var}" not in st.session_state:
                st.session_state[f"{prefix}_{var}"] = None

        for var in zero_vars:
            if f"{prefix}_{var}" not in st.session_state:
                st.session_state[f"{prefix}_{var}"] = 0
    
        # Initialize performance tracking dictionary if it doesn't exist
        if f"{prefix}_performance" not in st.session_state:
            st.session_state[f"{prefix}_performance"] = self.clear_performance_dataframe(prefix, problem_types, difficulties)
        
        if f"{prefix}_level" not in st.session_state:
            st.session_state[f"{prefix}_level"] = False

    
    def subheader_ui(self,prefix:str, performance: dict) -> None:
        """renders a checkbox to look at the re-arrangements of equations, and displays stars earned"""
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
            performance_df = self.create_performance_dataframe(performance)
            st.dataframe(performance_df, use_container_width=True)
    
    def question_ui(self, prefix: str, problem_type_dict: dict, problem_types: list, difficulties: list, generator):
        """Produces questions with logic passed in from the generator class, and evaluates answers.
        **Requires the imported generator class to have a choose_problem(problem_type, difficulty) function"""
        # UI Controls
        col1, col2, col3,col4 = st.columns([10,5,2,5])
        with col1:

            selected_problem_type = st.selectbox(
                "Problem Type",
                options=list(problem_types),
                key=f"{prefix}_problem_type_select")
                
            problem_type = selected_problem_type

        with col2:
            difficulty = st.selectbox(
                "Difficulty",
                difficulties,
                key=f"{prefix}_difficulty_select"
            )
        with col3:
            st.write("")
        with col4:
            st.write("")
            st.write("")
            if st.button("New Question",key=f"{prefix}_new_question"):
                question, answer, unit = generator.choose_problem(problem_type, difficulty)
                st.session_state[f"{prefix}_question_id"] += 1
                st.session_state[f"{prefix}_current_question"] = question
                st.session_state[f"{prefix}_correct_answer"] = answer
                st.session_state[f"{prefix}_unit"] = unit
                st.session_state[f"{prefix}_submitted"] = False
                generator.clear_answers()
                st.rerun()  
        # Check if we need a new question
        if (problem_type != st.session_state[f"{prefix}_problem_type"] or 
            st.session_state[f"{prefix}_current_question"] is None):
            
            # Generate new question and store in session state
            question, answer, unit = generator.choose_problem(problem_type, difficulty)
            st.session_state[f"{prefix}_current_question"] = question
            st.session_state[f"{prefix}_correct_answer"] = answer
            st.session_state[f"{prefix}_unit"] = unit
            st.session_state[f"{prefix}_problem_type"] = problem_type
            st.session_state[f"{prefix}_submitted"] = False
            generator.clear_answers()

        with st.expander("equation(s)",expanded=True):
            if st.session_state[f"{prefix}_level"] == False:
                st.latex(problem_type_dict[st.session_state[f"{prefix}_problem_type"]]["honors"])
            else:
                st.latex(problem_type_dict[st.session_state[f"{prefix}_problem_type"]]["conceptual"])

        # Display current question
        st.subheader("Question:")
        st.write(st.session_state[f"{prefix}_current_question"])
        with st.form(f"{prefix}_form"):
                unit =  st.session_state[f"{prefix}_unit"]
                st.session_state[f"{prefix}user_answer"] = st.number_input(
                    f"Enter your answer (in {unit}):", 
                    min_value=0.00, value=None, step=0.01,
                    key=f"{prefix}_input")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    user_input = st.session_state[f"{prefix}user_answer"]
                    correct_answer = st.session_state[f"{prefix}_correct_answer"]
                    tolerance = correct_answer * 0.05
                    is_correct = abs(user_input - correct_answer) < abs(tolerance)
                    if not st.session_state[f"{prefix}_submitted"]:
                        self.update_performance( prefix, problem_type, difficulty, is_correct)
                        st.session_state[f"{prefix}_submitted"] = True 
                        if is_correct:
                            st.success(f"{random_correct_message()}")
                            st.session_state[f"{prefix}_stars"] += 1
                        else:
                            st.error(f"{random_error_message()} The correct answer is {correct_answer:.2f}.")
    

    def question_ui_2(self, prefix: str, problem_type_dict: dict, problem_types: list, 
                difficulties: list, generator):
        """Produces questions with logic passed in from the generator class, and evaluates answers.
            **Requires the imported generator class to have a choose_problem(problem_type, difficulty) function"""
        # UI Controls
        col1, col2, col3,col4 = st.columns([10,5,2,5])
        with col1:

            selected_problem_type = st.selectbox(
                "Problem Type",
                options=list(problem_types),
                key=f"{prefix}_problem_type_select")
                
            problem_type = selected_problem_type

        with col2:
            difficulty = st.selectbox(
                "Difficulty",
                difficulties,
                key=f"{prefix}_difficulty_select"
            )
        with col3:
            st.write("")
        with col4:
            st.write("")
            st.write("")
            if st.button("New Question",key=f"{prefix}_new_question"):
                question, answers, units = generator.choose_problem(problem_type, difficulty)
                st.session_state[f"{prefix}_question_id"] += 1
                st.session_state[f"{prefix}_current_question"] = question
                st.session_state[f"{prefix}_correct_answers"] = answers
                st.session_state[f"{prefix}_units"] = units
                st.session_state[f"{prefix}_submitted"] = False
                generator.clear_answers()
                st.rerun()  
        # Check if we need a new question
    
        # Generate questions - modified to handle multiple answers
        if (problem_type != st.session_state[f"{prefix}_problem_type"] or 
            st.session_state[f"{prefix}_current_question"] is None):
            question, answers, units = generator.choose_problem(problem_type, difficulty)
            num_inputs = len(answers)
            st.session_state[f"{prefix}_current_question"] = question
            st.session_state[f"{prefix}_correct_answers"] = answers  # Now a list
            st.session_state[f"{prefix}_units"] = units  # Now a list
            st.session_state[f"{prefix}_problem_type"] = problem_type
            st.session_state[f"{prefix}_submitted"] = False
            generator.clear_answers()
            # ... rest of your code ...
        
        with st.expander("equation(s)",expanded=True):
            if st.session_state[f"{prefix}_level"] == False:
                st.latex(problem_type_dict[st.session_state[f"{prefix}_problem_type"]]["honors"])
            else:
                st.latex(problem_type_dict[st.session_state[f"{prefix}_problem_type"]]["conceptual"])

        # Display current question
        st.subheader("Question:")
        st.write(st.session_state[f"{prefix}_current_question"])
        
        # Modified form to handle multiple inputs
        with st.form(f"{prefix}_form"):
            num_inputs = st.session_state[f"{prefix}_correct_answers"]
            num_inputs = len(num_inputs)
            if num_inputs > 1:
                cols = st.columns(num_inputs)
                user_answers = []
                
                for i, col in enumerate(cols):
                    unit = st.session_state[f"{prefix}_units"][i]
                    with col:
                        st.write(f"Answer {i+1}: {unit}")
                        input_value = st.number_input(
                            "Value:", 
                            min_value=0.00, value=None, step=0.01,
                            key=f"{prefix}_input_{i}_{st.session_state[f'{prefix}_question_id']}"
                        )
                        user_answers.append(input_value)
            else:
                # Single input case
                unit = st.session_state[f"{prefix}_units"][0]
                user_answers = [st.number_input(
                    f"{unit}:", 
                    min_value=0.00, value=None, step=0.01,
                    key=f"{prefix}_input_0_{st.session_state[f'{prefix}_question_id']}"
                )]
                
            submitted = st.form_submit_button("Submit")
            if submitted:
                correct_answers = st.session_state[f"{prefix}_correct_answers"]
                all_correct = True
                if None not in user_answers:
                    # Check all answers
                    for i, (user_input, correct_answer) in enumerate(zip(user_answers, correct_answers)):
                        tolerance = correct_answer * 0.05
                        is_correct = abs(user_input - correct_answer) < abs(tolerance)
                        all_correct = all_correct and is_correct
                    
                    # Update performance based on overall correctness
                    if not st.session_state[f"{prefix}_submitted"]:
                        self.update_performance(prefix, problem_type, difficulty, all_correct)
                        st.session_state[f"{prefix}_submitted"] = True 
                        
                        if all_correct:
                            st.success(f"{random_correct_message()}")
                            st.session_state[f"{prefix}_stars"] += 1
                        else:
                            answer_display = ", ".join([f"{ans:.2f}" for ans in correct_answers])
                            st.error(f"{random_error_message()} The correct answers are: {answer_display}.")
                else:
                    st.error("Please enter all answers before submitting")
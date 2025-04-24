import streamlit as st
import pandas as pd
from utils.word_lists import random_correct_message
from utils.word_lists import random_error_message
import time

class interface:
    def __init__(self, 
                 prefix: str, 
                 title: str, 
                 generator: None,
                 problem_type_dict: dict, 
                 difficulties: list,
                 type_weight = False,
                 ) -> None:
        self.prefix = prefix
        self.title = title
        self.generator = generator
        self.problem_type_dict = problem_type_dict
        self.problem_types = list(problem_type_dict.keys())
        self.difficulties = difficulties
        self.type_weight = type_weight

      
    def clear_performance_dataframe(self) -> dict:
        """Initialize/Reset the performance tracking dictionary"""
        performance_dict = {}
        for p_type in self.problem_types:
            performance_dict[p_type] = {}
            for diff in self.difficulties:
                performance_dict[p_type][diff] = {'attempts': 0, 'correct': 0}     
        st.session_state[f"{self.prefix}_performance"] = performance_dict
        return performance_dict
    

    def create_performance_dataframe(self) -> pd.DataFrame:
        """Create a pandas DataFrame from the performance tracking dictionary"""
        performance = st.session_state[f"{self.prefix}_performance"]
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


    def update_performance(self, problem_type: str, difficulty: str, is_correct: bool) -> dict:
            """Update the performance tracking dictionary when an answer is submitted"""
            performance = st.session_state[f"{self.prefix}_performance"]
            
            # Increment attempts
            performance[problem_type][difficulty]['attempts'] += 1
            
            # Increment correct if answer was correct
            if is_correct:
                performance[problem_type][difficulty]['correct'] += 1
            
            # Update session state
            st.session_state[f"{self.prefix}_performance"] = performance


    def initialize_session_state(self) -> None:
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
            if f"{self.prefix}_{var}" not in st.session_state:
                st.session_state[f"{self.prefix}_{var}"] = None

        for var in zero_vars:
            if f"{self.prefix}_{var}" not in st.session_state:
                st.session_state[f"{self.prefix}_{var}"] = 0
    
        # Initialize performance tracking dictionary if it doesn't exist
        if f"{self.prefix}_performance" not in st.session_state:
            st.session_state[f"{self.prefix}_performance"] = self.clear_performance_dataframe()
        
        if f"{self.prefix}_level" not in st.session_state:
            st.session_state[f"{self.prefix}_level"] = False


    def header(self) -> None:
        """Creates the page Title and displays stars"""
        col1,col2 = st.columns([10,4],vertical_alignment='top')
        with col1:
            st.title(f"{self.title}")
        with col2:
            if st.session_state[f"{self.prefix}_stars"] != 0:
                star_count = st.session_state[f"{self.prefix}_stars"]
                st.title(f"⭐ x {star_count}")
            else:
                st.write("")


    def performance_dropdown(self) -> None:
        """renders performance dataframe in dropdown menu"""
        with st.expander("Your Performance", expanded=False):
            performance_df = self.create_performance_dataframe()
            st.dataframe(performance_df, use_container_width=True)


    def generate_new_question(self, problem_type: str, difficulty: str) -> None:
        """reruns question generation routine
        **Requires the imported generator class to have a 
            choose_problem(problem_type, difficulty) function"""
        try:
            question, answers, units = self.generator.choose_problem(problem_type, 
                                                                     difficulty)
        except:
            question, answers, units, movements = self.generator.choose_problem(problem_type, 
                                                                     difficulty)
            st.session_state[f"{self.prefix}_movements"] = movements
        st.session_state[f"{self.prefix}_question_id"] += 1
        st.session_state[f"{self.prefix}_problem_type"] = problem_type
        st.session_state[f"{self.prefix}_difficulty"] = difficulty
        st.session_state[f"{self.prefix}_current_question"] = question
        st.session_state[f"{self.prefix}_correct_answers"] = answers
        st.session_state[f"{self.prefix}_units"] = units
        st.session_state[f"{self.prefix}_submitted"] = False
        self.generator.clear_answers()
        st.rerun() 


    def new_question(self, problem_type: str, difficulty: str) -> None:
        """module for new question button"""
        if st.button("New Question",key=f"{self.prefix}_new_question"):
                self.generate_new_question(problem_type, difficulty)
 

    def footer_1(self)-> None:
        """Organizes the new question button and the performance dataframe into 
        columns at the bottom of the page"""
        col1,col2 = st.columns([1,4],vertical_alignment='center')
        with col1:
            self.new_question(
                              st.session_state[f"{self.prefix}_problem_type"],
                              st.session_state[f"{self.prefix}_difficulty"])
        with col2:
            self.performance_dropdown()    


    def question_options_1(self, equations = True, ifDifficulty = True) -> None:
        # UI Controls
        col1, col2, col3 = st.columns([3,2,2],vertical_alignment='bottom',gap='medium')
        with col1:
            selected_problem_type = st.selectbox(
                "Problem Type",
                options=list(self.problem_types),
                key=f"{self.prefix}_problem_type_select")
                
            problem_type = selected_problem_type

        with col2:
            if ifDifficulty:
                difficulty = st.selectbox(
                    "Difficulty",
                    self.difficulties,
                    key=f"{self.prefix}_difficulty_select"
                )
            else:
                difficulty = "Easy"
        with col3:
            if equations:
                st.session_state[f"{self.prefix}_level"] = st.checkbox(
                    "More Equations", 
                    value=False,
                    key=f"{self.prefix}_levels_check")
            
        if (problem_type != st.session_state[f"{self.prefix}_problem_type"] or 
            st.session_state[f"{self.prefix}_current_question"] is None or 
            difficulty != st.session_state[f"{self.prefix}_difficulty"]):
                
                self.generate_new_question(problem_type, difficulty)
        if equations:
            with st.expander("equation(s)",expanded=True):
                if st.session_state[f"{self.prefix}_level"] == False:
                    st.latex(self.problem_type_dict[st.session_state[f"{self.prefix}_problem_type"]]["honors"])
                else:
                    st.latex(self.problem_type_dict[st.session_state[f"{self.prefix}_problem_type"]]["conceptual"])


    def question_ui_4(self,timer=3.0, big_font = False) -> None:
        """Displays questions passed in from the generator class, and evaluates answers."""
        # Display current question
        if big_font:
            st.title(st.session_state[f"{self.prefix}_current_question"])
        else:
            st.write(st.session_state[f"{self.prefix}_current_question"])
        # Modified form to handle multiple inputs
        with st.form(f"{self.prefix}_form",clear_on_submit=True):
            num_inputs = st.session_state[f"{self.prefix}_correct_answers"]
            num_inputs = len(num_inputs)
            if num_inputs > 1:
                cols = st.columns(num_inputs)
                user_answers = []
                
                for i, col in enumerate(cols):
                    unit = st.session_state[f"{self.prefix}_units"][i]
                    with col:
                        if type(st.session_state[f"{self.prefix}_correct_answers"][i]) == str:
                            input_value = st.text_input(f"{i+1}: {unit}", max_chars= 20,
                                key=f"{self.prefix}_input_{i}_{st.session_state[f'{self.prefix}_question_id']}"
                            )
                            user_answers.append(input_value)
                        else:
                            input_value = st.number_input(
                                f"{i+1}: {unit}", 
                                 value=None, step=0.01,
                                key=f"{self.prefix}_input_{i}_{st.session_state[f'{self.prefix}_question_id']}"
                            )
                            user_answers.append(input_value)
                            
            else:
                # Single input case
                unit = st.session_state[f"{self.prefix}_units"][0]
                user_answers = [st.number_input(
                    f"{unit}:", 
                    value=None, step=0.01,
                    key=f"{self.prefix}_input_0_{st.session_state[f'{self.prefix}_question_id']}"
                )]
                
            submitted = st.form_submit_button("Submit")
        if submitted:
            self.check_answers(user_answers,timer)
            

    def check_answers(self,user_answers: list, timer: float):
        correct_answers = st.session_state[f"{self.prefix}_correct_answers"]
        all_correct = True
        if None not in user_answers:
            # Check all answers
            for i, (user_input, correct_answer) in enumerate(zip(user_answers, correct_answers)):
                if type(user_input) == str:
                    is_correct == True if user_input.lower() == correct_answer.lower() else False
                else:
                    tolerance = correct_answer * 0.05
                    is_correct = abs(user_input - correct_answer) <= abs(tolerance)
                    all_correct = all_correct and is_correct
            
            # Update performance based on overall correctness
            if not st.session_state[f"{self.prefix}_submitted"]:
                problem_type = st.session_state[f"{self.prefix}_problem_type"]
                difficulty = st.session_state[f"{self.prefix}_difficulty"]
                self.update_performance(problem_type, difficulty, all_correct)
                st.session_state[f"{self.prefix}_submitted"] = True 
                
                if all_correct:
                    st.success(f"{random_correct_message()}")
                    st.session_state[f"{self.prefix}_stars"] += self.give_stars(difficulty,problem_type)
                    self.loading_question(timer)
                    
                else:
                    answer_display = ", ".join([f"{ans:.2f}" for ans in correct_answers])
                    st.error(f"{random_error_message()} The correct answers are: {answer_display}.")
                    self.loading_question(timer)
                
        else:
            st.error("Please enter all answers before submitting")



    def give_stars(self, difficulty: str, problem_type: str) -> None:
        """Weights stars given by difficulty and 
        how the problem type is categorized on the page, if applicable 
        (modulated by type_weight)
        """
        problem_type_bonus = self.problem_types.index(problem_type) + 1 if self.type_weight else 1
        difficulty_bonus = self.difficulties.index(difficulty) + 1
        return problem_type_bonus*difficulty_bonus
    

    def loading_question(self,timer: float) -> None:
        """
        Displays a loading bar to show the next question is coming up

        :param timer: the time (in seconds) that the next question takes to load
        :type timer: float
        """
        problem_type = st.session_state[f"{self.prefix}_problem_type"]
        difficulty = st.session_state[f"{self.prefix}_difficulty"]
        i = 0
        loading_text = "Next Question"
        timer*=100 # for smoother loading
        col1,col2=st.columns([5,2])
        with col1:
            loading_question = st.progress(0,loading_text)
                
        with col2:
            pause =st.checkbox("Cancel Next Question")

        while (i < timer and not pause):   
                time.sleep(0.01)
                loading_question.progress((i+1)/timer,loading_text)
                i+=1 
                
        if (i == timer and not pause):
            self.generate_new_question(problem_type,difficulty)


    def add_diagram(self) -> None:
        """currently over-specified for distance/displacement in linear fns class. 
        adds an expander with a diagram"""
        problem_type = st.session_state[f"{self.prefix}_problem_type"]
        difficulty = st.session_state[f"{self.prefix}_difficulty"]
        with st.expander("Diagram"):
            if f"{self.prefix}_movements" in st.session_state:
                movements = st.session_state[f"{self.prefix}_movements"]
                fig = self.generator.generate_movement_diagram(movements, problem_type, difficulty)
                st.pyplot(fig)


    def question_ui_buttons(self) -> None:
        """
        Displays questions with multiple-choice buttons instead of text input.
        
        Parameters:
        - timer: Time in seconds before loading the next question after submission
        """
        # Display current question
        st.write(st.session_state[f"{self.prefix}_current_question"])
        
        # Get the correct answers and their units
        correct_answers = st.session_state[f"{self.prefix}_correct_answers"]
        units = st.session_state[f"{self.prefix}_units"]
        
        # Define answer options based on units if not already in session state
        if f"{self.prefix}_answer_options" not in st.session_state:
            answer_options = {}
            for i, unit in enumerate(units):
                if unit == "Direction":
                    answer_options[i] = ["Positive", "Negative"]
                elif unit == "Motion State":
                    answer_options[i] = ["Constant Velocity", "Speeding Up", "Slowing Down"]
                else:
                    # Default option list if not recognized
                    answer_options[i] = []
            st.session_state[f"{self.prefix}_answer_options"] = answer_options
        
        # Initialize user answers in session state if not present
        if f"{self.prefix}_user_answers_selected" not in st.session_state:
            st.session_state[f"{self.prefix}_user_answers_selected"] = [None] * len(correct_answers)
        
        # Display each question with button options
        for i, unit in enumerate(units):
            st.write(f"**{unit}:**")
            
            # Get options for this question
            options = st.session_state[f"{self.prefix}_answer_options"].get(i, [])
            if not options:
                st.warning(f"No predefined options for {unit}. Please configure options.")
                continue
            
            # Create buttons in a row
            cols = st.columns(len(options))
            for j, (col, option) in enumerate(zip(cols, options)):
                with col:
                    # Determine if this button is selected
                    is_selected = st.session_state[f"{self.prefix}_user_answers_selected"][i] == option
                    button_type = "primary" if is_selected else "secondary"
                    
                    # Create the button
                    if st.button(option, key=f"{self.prefix}_option_{i}_{j}_{st.session_state[f'{self.prefix}_question_id']}", 
                                type=button_type, use_container_width=True):
                        # Update the selected answer
                        user_answers = st.session_state[f"{self.prefix}_user_answers_selected"]
                        user_answers[i] = option
                        st.session_state[f"{self.prefix}_user_answers_selected"] = user_answers
                        st.rerun()  # Rerun to update button states
        
        # Add a submit button
        if st.button("Submit Answers", key=f"{self.prefix}_submit_button_{st.session_state[f'{self.prefix}_question_id']}"):
            user_answers = st.session_state[f"{self.prefix}_user_answers_selected"]
            
            # Check if all questions have been answered
            if None in user_answers:
                st.error("Please answer all questions before submitting.")
            else:
                self.check_button_answers(user_answers)

    def check_button_answers(self, user_answers):
        """Check answers submitted via buttons."""
        correct_answers = st.session_state[f"{self.prefix}_correct_answers"]
        all_correct = True
        
        # Check each answer
        for user_input, correct_answer in zip(user_answers, correct_answers):
            is_correct = (user_input == correct_answer)
            all_correct = all_correct and is_correct
        
        # Update performance based on overall correctness
        if not st.session_state[f"{self.prefix}_submitted"]:
            problem_type = st.session_state[f"{self.prefix}_problem_type"]
            difficulty = st.session_state[f"{self.prefix}_difficulty"]
            self.update_performance(problem_type, difficulty, all_correct)
            st.session_state[f"{self.prefix}_submitted"] = True
            
            if all_correct:
                st.success(f"{random_correct_message()}")
                st.session_state[f"{self.prefix}_stars"] += self.give_stars(difficulty, problem_type)
                # Set a flag to show loading bar instead of directly calling loading_question
                st.session_state[f"{self.prefix}_show_loading"] = True
            else:
                answer_display = ", ".join([f"{ans}" for ans in correct_answers])
                st.error(f"{random_error_message()} The correct answers are: {answer_display}.")
                # Set a flag to show loading bar instead of directly calling loading_question
                st.session_state[f"{self.prefix}_show_loading"] = True
        
        # Reset selections for next question
        st.session_state[f"{self.prefix}_user_answers_selected"] = [None] * len(correct_answers)


    def button_layout(self, display_function=None, timer=3.0):
        """
        A custom layout that displays content in one column and buttons in another
        with a full-width loading bar when needed
        
        Parameters:
        - display_function: A function that displays content in the left column
        - timer: Time in seconds before loading the next question
        """
        self.initialize_session_state()
        
        # Initialize the loading flag if not present
        if f"{self.prefix}_show_loading" not in st.session_state:
            st.session_state[f"{self.prefix}_show_loading"] = False
        
        self.header()
        self.question_options_1(equations=False,ifDifficulty=False)
        
        # Display content and answer form in columns
        col1, col2 = st.columns([1, 1])
        with col1:
            if display_function:
                display_function()
        
        with col2:
            self.question_ui_buttons()  
        
        # Check if we should show the loading bar (full width, outside columns)
        if st.session_state[f"{self.prefix}_show_loading"]:
            problem_type = st.session_state[f"{self.prefix}_problem_type"]
            difficulty = st.session_state[f"{self.prefix}_difficulty"]
            
            i = 0
            loading_text = "Next Question"
            timer_steps = timer * 100  # for smoother loading
            loading_question = st.progress(0, loading_text)
                
            # Add a cancel button below the progress bar
            pause = st.checkbox("Cancel Next Question")

            while (i < timer_steps and not pause):   
                import time
                time.sleep(0.01)
                loading_question.progress((i+1)/timer_steps, loading_text)
                i += 1 
                
            if (i == timer_steps and not pause):
                # Reset the loading flag
                st.session_state[f"{self.prefix}_show_loading"] = False
                self.generate_new_question(problem_type, difficulty)
        
        self.footer_1()


    def default_layout(self) -> None:
        self.initialize_session_state()
        self.header()
        self.question_options_1()
        self.question_ui_4()
        self.footer_1()


    def diagram_layout(self) -> None:
        self.initialize_session_state()
        self.header()
        self.question_options_1()
        self.question_ui_4()
        self.add_diagram()
        self.footer_1()



    def rapid_layout(self) -> None:
        self.initialize_session_state()
        self.header()
        self.question_options_1(equations=False)
        self.question_ui_4(timer=0.1,big_font=True)
        self.footer_1()

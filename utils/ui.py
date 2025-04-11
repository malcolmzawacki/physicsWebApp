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
        col1,col2 = st.columns([10,4],vertical_alignment='center')
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


    def question_options_1(self, equations = True) -> None:
        # UI Controls
        col1, col2, col3 = st.columns([3,2,2],vertical_alignment='bottom',gap='medium')
        with col1:
            selected_problem_type = st.selectbox(
                "Problem Type",
                options=list(self.problem_types),
                key=f"{self.prefix}_problem_type_select")
                
            problem_type = selected_problem_type

        with col2:
            difficulty = st.selectbox(
                "Difficulty",
                self.difficulties,
                key=f"{self.prefix}_difficulty_select"
            )
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

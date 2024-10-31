import streamlit as st
import random
import sys
from pathlib import Path

# Add the project root directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Now you can import from utils
from utils.word_lists import random_noun

def challenge(difficulty): #test and adjust range
    if difficulty == "Easy":
        range = 10
    elif difficulty == "Hard":
        range = 30
    else:
        range = 20
    return range

def numbers(difficulty): #selects from list of triples and calculates vars
    coin = random.randint(0,1)
    m1 = random.randint(1,difficulty)
    g = random.randint(2,difficulty)
    h = random.randint(1,difficulty)
    j = random.randint(1,difficulty)
    if coin == 1:
        g *= -1
        h *= -1
        j *= -1
    
    m2 = m1*g*h
    v2 = j*(1+g*h)
    v1 = v2*g
    v1_p = g*j*(2*h - g*h + 1)
    v2_p = j*(2*g + g*h - 1)
    v3 = g*j*(h + 1)
   
    return m1, v1, m2, v2, v1_p, v2_p, v3



def generate_elastic_question(difficulty):
    m1, v1, m2, v2, v1_p, v2_p, v3 = numbers(challenge(difficulty))
    object1 = random_noun()
    object2 = random_noun()
    if v2 < 0:
        verb = "collides head on into"
    else:
        verb = "rear ends"
    if difficulty == "Easy":
        answer2 = 0
        unit2 = ""
        question = f"A {m1:.2f} kg {object1} moving at {v1:.2f} m/s {verb} a {m2:.2f} kg {object2} moving at {v2:.2f} m/s . The {object1} is moving at {v1_p:.2f} after the collision. How fast is the {object2} moving?"
        answer = v2_p
        unit = f"{object2} final velocity (m/s)"
    return question, answer, unit, answer2, unit2

def generate_inelastic_question(difficulty):
    m1, v1, m2, v2, v1_p, v2_p, v3 = numbers(challenge(difficulty))
    object1 = random_noun()
    object2 = random_noun()
    if v2 < 0:
        verb = "collides head on into"
    else:
        verb = "rear ends"
    if difficulty == "Easy":
        answer2 = 0
        unit2 = ""
        question = f"A {m1:.2f} kg {object1} moving at {v1:.2f} m/s {verb} a {m2:.2f} kg {object2} moving at {v2:.2f} m/s . They smush together. How fast are they moving together?"
        answer = v3
        unit = f"{object1} and {object2} combined final velocity (m/s)"
    return question, answer, unit, answer2, unit2


def generate_new_question(problem_type, difficulty):
    if problem_type == "Elastic Collision":
        st.session_state.current_question, st.session_state.correct_answer, st.session_state.unit, st.session_state.correct_answer2, st.session_state.unit2 = generate_elastic_question(difficulty)
    elif problem_type == "Inelastic Collision":
        st.session_state.current_question, st.session_state.correct_answer, st.session_state.unit, st.session_state.correct_answer2, st.session_state.unit2 = generate_inelastic_question(difficulty)
    st.session_state.problem_type = problem_type
    st.session_state.user_answer = None
    st.session_state.submitted = False
    st.session_state.question_id += 1  # Increment question ID for new input field key

# clears variables to prevent overlap with previous problem
def initialize_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'correct_answer' not in st.session_state:
        st.session_state.correct_answer = None
    if 'correct_answer2' not in st.session_state:
        st.session_state.correct_answer2 = None
    if 'unit' not in st.session_state:
        st.session_state.unit = None
    if 'unit2' not in st.session_state:
        st.session_state.unit2 = None
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = None
    if 'user_answer2' not in st.session_state:
        st.session_state.user_answer2 = None
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'question_id' not in st.session_state:
        st.session_state.question_id = 0
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = None
    if 'problem_type' not in st.session_state:
        st.session_state.problem_type = None

def main():
    st.title("Collisions")

    initialize_session_state()

    difficulty = st.selectbox(
        "Select Difficulty",
        ("Easy"),
        key="problem_difficulty_select"
    )

    problem_type = st.selectbox(
        "Select Problem Type",
        ("Elastic Collision", "Inelastic Collision"),
        key="problem_type_select"
    )

    if problem_type != st.session_state.problem_type:
        generate_new_question(problem_type, difficulty)


    if st.session_state.current_question:
        st.write(st.session_state.current_question)
        
        unit = st.session_state.unit
        user_input = st.number_input(
            f"{unit}:",
            value=None,
            step=None,  # Remove step to allow any decimal input
            format="%f",  # Use %f to allow flexible decimal places
            key=f"user_input_{st.session_state.question_id}"  # Unique key for each question
        )
        if difficulty == "Hard":
            unit2 = st.session_state.unit2
            user_input2 = st.number_input(
            f"{unit2}:",
            value=None,
            step=None,  # Remove step to allow any decimal input
            format="%f",  # Use %f to allow flexible decimal places
            key=f"user_input2_{st.session_state.question_id}"  # Unique key for each question
            )
        if st.button("Submit"): # this should not change from one thing to another
            st.session_state.submitted = True
            if user_input is not None:
                st.session_state.user_answer = user_input
                correct_answer = st.session_state.correct_answer
                tolerance = correct_answer * 0.05  # 5% tolerance
                correct_answer2 = st.session_state.correct_answer2
                tolerance2 = correct_answer2 * 0.05
                if difficulty == "Easy":
                    if abs(st.session_state.user_answer - correct_answer) < tolerance:
                        st.success("Correct!")
                    else:
                        st.error(f"Incorrect. The correct answer is {correct_answer:.2f}.")
                else: 
                    if abs(st.session_state.user_answer - correct_answer) < tolerance and abs(st.session_state.user_answer2 - correct_answer2) < tolerance2:
                        st.success("Correct!")
                    else:
                        st.error(f"Incorrect. The correct answer is {correct_answer:.2f} and {correct_answer2:.2f}.")
            else:
                st.error("Please enter an answer before submitting.")
        
        if st.button("New Question"):
            generate_new_question(problem_type,difficulty)
            st.rerun()

    # Reset submitted flag if problem type changes
    if problem_type != st.session_state.problem_type:
        st.session_state.submitted = False

if __name__ == "__main__":
    main()
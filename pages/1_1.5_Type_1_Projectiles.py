import streamlit as st
import random
import math
import sys
from pathlib import Path

# Add the project root directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Now you can import from utils
from utils.word_lists import random_noun, random_proj_verb

def challenge(difficulty): #test and adjust range
    if difficulty == "Easy":
        range = 10
    elif difficulty == "Hard":
        range = 50
    else:
        range = 20
    return range

def m_n_array(max): # generates pythagorean triples
    m = 5
    n = 1
    m_n_list = []
    while m <= max:
        if math.remainder(m,5) == 0 and n < m:
            m_n_list.append([m,n])
            n+=1
        elif n == m or math.remainder(m,5) != 0:
            m+=1
            if math.remainder(m,5) == 0:
                n = 1
                m_n_list.append([m,n])
                n+=1
            else:
                m_n_list.append([m,n])
    return m_n_list



def numbers(difficulty): #selects from list of triples and calculates vars
    m_n_list = m_n_array(challenge(difficulty))
    rowChoice = random.randint(0,len(m_n_list)-1)
    m = m_n_list[rowChoice][0]
    n = m_n_list[rowChoice][1]

    v_x = m**2 - n**2
    v_y_i = 2*m*n
    v_r = m**2 + n**2
    theta = round(math.degrees(math.atan(v_y_i / v_x)) , 4)
    d_x = v_x*v_y_i / 10
    d_y = v_y_i**2 / 20
    return v_x, v_r, theta, d_x, d_y

def generate_question(difficulty):
    v_x, v_r, theta, d_x, d_y = numbers(challenge(difficulty))
    object = random_noun()
    verb = random_proj_verb()
    if difficulty == "Easy":
        choice = random.randint(1,3)
        answer2 = 0
        unit2 = ""
        if choice == 1: # solve for distance
            question = f"If a {object} is {verb} horizontally off of a {d_y:.2f} m cliff with an initial velocity of {v_x:.2f} m/s, how far away from the base of the cliff does it land? (m)"
            answer = d_x
            unit = "Horizontal Distance (m)"
        elif choice == 2: # solve for height
            question = f"If a {object} is {verb} horizontally off of a cliff at {v_x:.2f} m/s, and lands {d_x:.2f} m away from the base of the cliff, what was the height of the cliff? (m)"
            answer = d_y
            unit = "Cliff Height (m)"
        elif choice == 3:
            question = f"If a {object} is {verb} horizontally off of a {d_y:.2f} m cliff, and lands {d_x:.2f} m away from the base of the cliff, how fast was it {verb}? (m/s)"
            answer = v_x
            unit = "Initial Velocity (m/s)"
    elif difficulty == "Hard":
        choice = random.randint(1,3)
        if choice == 1: # solve for initial velocity and height
            question = f"If a {object} was {verb} horizontally off of a cliff and lands at {v_r:.2f} m/s at a {theta:.2f} degree angle, how fast was it {verb}, and from how high?"
            answer = v_x
            unit = "Initial Velocity (m/s)"
            answer2 = d_y
            unit2 = "Cliff Height (m)"
        elif choice == 2: # solve for final velocity and angle
            question = f"If a {object} is {verb} horizontally off of a cliff at {v_x:.2f} m/s, and lands {d_x:.2f} m away from the base of the cliff, what speed and angle does it land with?"
            answer = v_r
            unit = "m/s"
            answer2 = theta
            unit2 = "degrees"
        elif choice == 3: # give only height and angle
            question = f"A {object} is {verb} horizontally off of a {d_y:.2f} m cliff, and lands at a {theta:.2f} degree angle, with what speed did it land, and how far from the base of the cliff?"
            answer = v_r
            unit = "Overall Final Velocity (m/s)"
            answer2 = d_x
            unit2 = "Horizontal Distance (m)"
    return question, answer, answer2, unit, unit2


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

def generate_new_question(difficulty):
    st.session_state.current_question, st.session_state.correct_answer, st.session_state.correct_answer2, st.session_state.unit, st.session_state.unit2 = generate_question(difficulty)
    st.session_state.difficulty = difficulty
    st.session_state.user_answer = None
    st.session_state.submitted = False
    st.session_state.question_id += 1  # Increment question ID for new input field key

def main():
    st.title("Type 1 Projectiles")

    initialize_session_state()

    difficulty = st.selectbox(
        "Select Difficulty",
        ("Easy", "Hard"),
        key="problem_difficulty_select"
    )

    if difficulty != st.session_state.difficulty:
        generate_new_question(difficulty)

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
            if user_input and user_input2 is not None:
                st.session_state.user_answer = user_input
                st.session_state.user_answer2 = user_input2
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
            generate_new_question(difficulty)
            st.rerun()

    # Reset submitted flag if problem type changes
    if difficulty != st.session_state.difficulty:
        st.session_state.submitted = False

if __name__ == "__main__":
    main()
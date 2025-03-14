import streamlit as st
import random
import math

class algebra:

    @staticmethod
    def generate_equation(difficulty):
        variables = ['x', 'y', 'z', 'a', 'b', 'c', 'm', 'n', 'p', 'q']
        operations = {
            'add': ('+', 'Subtract'),
            'sub': ('-', 'Add'),
            'mul': ('×', 'Divide by'),
            'div': ('÷', 'Multiply by'),
            'exp': ('^', 'Take the root'),
            'root': ('√', 'Square'),
        }

        if difficulty == 'easy':
            num_steps = 2
        elif difficulty == 'medium':
            num_steps = 3
        elif difficulty == 'hard':
            num_steps = 4
        elif difficulty == 'extra_hard':
            num_steps = 5

        var_target = random.choice(variables)
        var_solve = random.choice([v for v in variables if v != var_target])

        steps = []
        solution_steps = []
        prev_op = ''
        for _ in range(num_steps):
            op_name = random.choice(list(operations.keys()))
            while op_name == prev_op:
                op_name = random.choice(list(operations.keys()))
            prev_op = op_name

            value = random.randint(2, 5)

            symbol, inverse_text = operations[op_name]
            steps.append((op_name, symbol, value))
            solution_steps.append((inverse_text, value))

        right_side = var_target
        for op_name, symbol, value in steps:
            if op_name == 'mul':
                right_side = f"({right_side} · {value})"
            elif op_name == 'div':
                right_side = f"\\frac{{{right_side}}}{{{value}}}"
            elif op_name == 'add':
                right_side = f"({right_side} + {value})"
            elif op_name == 'sub':
                right_side = f"({right_side} - {value})"
            elif op_name == 'exp':
                right_side = f"({right_side} ^ {value})"
            elif op_name == 'root':
                right_side = f"\\sqrt[{value}]{{{right_side}}}"


        equation = f"{var_solve} = {right_side}"

        wrong_answers = []
        for _ in range(4):
            wrong = solution_steps.copy()
            change_idx = random.randrange(len(wrong))
            ops = list(operations.values())
            new_inverse = random.choice([op[1] for op in ops if op[1] != wrong[change_idx][0]])
            wrong[change_idx] = (new_inverse, wrong[change_idx][1])
            wrong_answers.append(wrong)

        all_answers = wrong_answers + [solution_steps]
        random.shuffle(all_answers)

        return {
            'equation': equation,
            'target_var': var_target,
            'solve_var': var_solve,
            'solution_steps': solution_steps,
            'choices': all_answers
        }

    @staticmethod
    def initialize_session_state():
        if 'problem' not in st.session_state:
            st.session_state.problem = None
        if 'submitted' not in st.session_state:
            st.session_state.submitted = False
        if 'question_id' not in st.session_state:
            st.session_state.question_id = 0

    @staticmethod
    def algebra_tab():
        st.title("Algebraic Manipulation Practice")

        algebra.initialize_session_state()

        difficulty = st.selectbox(
            "Select difficulty:",
            ['easy', 'medium', 'hard', 'extra_hard'],key="Algebra selectbox"
        )

        if st.button("New Question") or st.session_state.problem is None:
            st.session_state.problem = algebra.generate_equation(difficulty)
            st.session_state.submitted = False
            st.session_state.question_id += 1

        if st.session_state.problem:
            st.latex(st.session_state.problem['equation'])

            choices = []
            for i, steps in enumerate(st.session_state.problem['choices']):
                steps_text = " → ".join([f"{step[0]} {step[1]}" for step in reversed(steps)])
                choices.append(f"Option {i+1}: {steps_text}")

            answer = st.radio(
                f"Select the correct sequence of steps to solve for {st.session_state.problem['target_var']}",
                options=choices,
                key=f"choice_{st.session_state.question_id}"
            )

            if st.button("Submit"):
                selected_index = int(answer[7]) - 1
                if st.session_state.problem['choices'][selected_index] == st.session_state.problem['solution_steps']:
                    var_target = st.session_state.problem['target_var']
                    var_solve = st.session_state.problem['solve_var']
                    rearranged = f"{var_target} = "
                    right_side = var_solve
                    for step in reversed(st.session_state.problem['solution_steps']):
                        op = step[0].lower()
                        val = step[1]
                        if op.startswith('multiply'):
                            right_side = f"({right_side} · {val})"
                        elif op.startswith('divide'):
                            right_side = f"\\frac{{{right_side}}}{{{val}}}"
                        elif op.startswith('add'):
                            right_side = f"({right_side} + {val})"
                        elif op.startswith('subtract'):
                            right_side = f"({right_side} - {val})"
                        elif op.startswith('take the root'):
                            right_side = f"\\sqrt[{val}]{{{right_side}}}"
                        elif op.startswith('square'):
                            right_side = f"({right_side} ^ {val})"

                    rearranged += right_side

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.latex(rearranged)
                    with col2:
                        st.success("Correct!")
                else:
                    st.error("Try again!")



class sci_notate:
    
    def sci_not_format(term,exponent):
        if abs(term) < 10 and abs(term)>=1:
            return term, exponent
        else:
            logtest = math.floor( math.log10( abs(term) ) )
            term /= 10**logtest
            exponent += logtest
            return term, exponent


    def generate_sci_not_problem(difficulty):
        q_term_1 = random.randint(1,9)
        q_exp_1 = random.randint(1,9)
        q_term_2 = random.randint(1,9)
        q_exp_2 = random.randint(1,9)
        flip = random.randint(0,1)
        if difficulty == 'easy': # two input, no negatives
            if flip == 0: # multiplication
                ans_term = q_term_1 * q_term_2
                ans_exp = q_exp_1 + q_exp_2
                ans_term, ans_exp = sci_notate.sci_not_format(ans_term,ans_exp)
                question = f"({q_term_1} \;\cdot\; 10^{{{q_exp_1}}})\;\cdot\;({q_term_2}\;\cdot\;10^{{{q_exp_2}}})"
            else: # division
                ans_term = q_term_1 * q_term_2
                ans_term, q_term_1 = q_term_1, ans_term
                ans_exp = q_exp_1 - q_exp_2
                q_term_1, q_exp_1 = sci_notate.sci_not_format(q_term_1, q_exp_1)
                ans_term, ans_exp = sci_notate.sci_not_format(ans_term,ans_exp)
                question = f"\\frac{{{q_term_1}\;\cdot\;10^{{{q_exp_1}}}}}{{{q_term_2}\;\cdot\;10^{{{q_exp_2}}}}}"
        elif difficulty == 'medium': # three inputs, negatives (combo mul, div)
            q_term_3 = random.randint(1,9)
            q_exp_3 = random.randint(1,9)
            q_term_list = [q_term_1,q_term_2,q_term_3]
            q_exp_list = [q_exp_1,q_exp_2,q_exp_3]
            q_term_list[random.randint(0,2)]*=-1
            q_exp_list[random.randint(0,2)]*=-1
            if flip == 0: # 2 mul 1 div
                ans_term = q_term_1*q_term_2
                q_term_2*= q_term_3
                ans_exp = q_exp_1 + q_exp_2 - q_exp_3
                q_term_2, q_exp_2 = sci_notate.sci_not_format(q_term_2, q_exp_2)
                ans_term, ans_exp = sci_notate.sci_not_format(ans_term,ans_exp)
                question = f"\\frac{{({q_term_1}\;\cdot\;10^{{{q_exp_1}}})\;\cdot\;({q_term_2}\;\cdot\;10^{{{q_exp_2}}})}}{{{q_term_3}\;\cdot\;10^{{{q_exp_3}}}}}"
            else: # 1 mul 2 div
                ans_term = q_term_1
                q_term_1*= q_term_2*q_term_3
                ans_exp = q_exp_1 - q_exp_2 - q_exp_3
                q_term_1, q_exp_1 = sci_notate.sci_not_format(q_term_1, q_exp_1)
                ans_term, ans_exp = sci_notate.sci_not_format(ans_term,ans_exp)
                question = f"\\frac{{{q_term_1}\;\cdot\;10^{{{q_exp_1}}}}}{{({q_term_3}\;\cdot\;10^{{{q_exp_3}}})\;\cdot\;({q_term_2}\;\cdot\;10^{{{q_exp_2}}})}}"
        else: # hard
            q_term_3 = random.randint(1,9)
            q_exp_3 = random.randint(1,9)
            q_term_4 = random.randint(1,9)
            q_exp_4 = random.randint(1,9)
            q_term_list = [q_term_1,q_term_2,q_term_3,q_term_4]
            q_exp_list = [q_exp_1,q_exp_2,q_exp_3,q_exp_4]
            q_term_list[random.randint(0,3)]*=-1
            q_exp_list[random.randint(0,3)]*=-1

            # t4 * (t1)(t2) / t3^2
            ans_term = q_term_1*q_term_2*q_term_4
            ans_exp = q_exp_1 + q_exp_2 + q_exp_4 - 2*q_exp_3
            q_term_1*=q_term_3
            q_term_2*=q_term_3
            q_term_1, q_exp_1 = sci_notate.sci_not_format(q_term_1, q_exp_1)
            q_term_2, q_exp_2 = sci_notate.sci_not_format(q_term_2, q_exp_2)
            ans_term, ans_exp = sci_notate.sci_not_format(ans_term,ans_exp)
            question = f"({q_term_4}\;\cdot\;10^{{{q_exp_4}}})\;\cdot\;\\frac{{({q_term_1}\;\cdot\;10^{{{q_exp_1}}})\;\cdot\;({q_term_2}\;\cdot\;10^{{{q_exp_2}}})}}{{({q_term_3}\;\cdot\;10^{{{q_exp_3}}})^2}}"

        return question, ans_term, ans_exp

    def initialize_session_state():
        if 'sci_problem' not in st.session_state:
            st.session_state.sci_problem = None
        if 'submitted' not in st.session_state:
            st.session_state.submitted = False
        if 'user_input1' not in st.session_state:
            st.session_state.user_answer1 = None
        if 'user_input2' not in st.session_state:
            st.session_state.user_answer2 = None
        if 'question_id' not in st.session_state:
            st.session_state.question_id = 0

    def new_question(difficulty):
        st.session_state.sci_problem, st.session_state.ans1, st.session_state.ans2 = sci_notate.generate_sci_not_problem(difficulty)
        st.session_state.difficulty = difficulty
        st.session_state.user_answer = None
        st.session_state.user_answer2 = None
        st.session_state.submitted = False
        st.session_state.question_id += 1

    def main():
        st.title("Scientific Notation Practice")

        sci_notate.initialize_session_state()

        difficulty = st.selectbox(
            "Select difficulty:",
            ['easy', 'medium', 'hard'],key="sci notate difficulty"
        )

        if st.session_state.sci_problem is None:
            sci_notate.new_question(difficulty)

        if st.session_state.sci_problem:
            st.latex(st.session_state.sci_problem)

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col2:
                st.header("")
                user_input1 = st.number_input(label='leading term', value=None,
                    step=None,
                    format="%f", key=f"user_input_sci_notate_{st.session_state.question_id}")
            with col3:
                st.header("")
                st.title("x 10",anchor=False)
            with col4:
                st.write("")
                st.write("")
                st.write("")
                user_input2 = st.number_input(label='exponent', value=None,
                    step=None,
                    format="%f", key=f"user_input2_sci_notate{st.session_state.question_id}")
            with col1:
                st.write("")
            with col6:
                st.write("")
            with col5:
                st.write("")
            
            if st.button("Submit",key="sci_notate_submit"):
                    st.session_state.submitted = True
                    if user_input1 is not None:
                        st.session_state.user_answer1 = user_input1
                        correct_answer = st.session_state.ans1
                        #tolerance = abs(correct_answer * 0.05)
                        
                        if user_input2 is not None:
                            st.session_state.user_answer2 = user_input2
                            correct_answer2 = st.session_state.ans2
                            if (user_input1 == correct_answer) and (user_input2 == correct_answer2):
                                st.success("Correct!")
                            elif ((user_input1 * 10**user_input2) == (correct_answer * 10**correct_answer2)):
                                st.error(f"Right math, wrong format")
                            else:
                                st.error(f"Incorrect.")
                    else:
                        st.error("Please enter both answers before submitting.")

            st.write("")
            # New Question button
            if st.button("New Question", key="sci_notate_new"):
                sci_notate.new_question(difficulty)
                st.rerun()


def main():
    tab1,tab2 = st.tabs(["Algebra","Scientific Notation"])
    with tab1:
        algebra.algebra_tab()
    with tab2:
        sci_notate.main()
if __name__ == "__main__":
    main()

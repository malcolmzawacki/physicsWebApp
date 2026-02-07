import streamlit as st
import random
import math
import sympy as sp
import re
from utils.ui import interface



from utils.state_proxy import StateProxy


algebra_state = StateProxy("algebra")
sci_state = StateProxy("sci_notate")

class arithmetic: 
    
    @staticmethod
    def question_parameters():
        """Holds current options for questions for centralized updating"""
        problem_type_dict = {
            "Addition": {
                "honors" : r"", 
                "conceptual": r""""""
                },
            "Subtraction": {
                "honors": r"",
                "conceptual": r""""""
            },               
            "Multiplication" : {
                "honors": r"",
                "conceptual": r""""""
            },
            "Division": {
                "honors": r"",
                "conceptual": r""""""
            },
            }
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, difficulties
    
    @staticmethod
    def main():
        from utils.generators.arithmetic_generator import ArithmeticGenerator
        title = "Fast Practice"
        prefix = "arithmetic"
        problem_type_dict, difficulties = arithmetic.question_parameters()
        generator = ArithmeticGenerator()
        ui = interface(prefix,title,generator,problem_type_dict,difficulties)
        ui.unified_smart_layout(timer=0.1)

class algebra:

    @staticmethod
    def latex_equation(equation):
        """Convert a sympy equation to a LaTeX string with some custom formatting"""
        # Convert to standard LaTeX
        latex_str = sp.latex(equation)
        
        # Add custom formatting for better display
        # Replace decimal powers with roots when possible
        latex_str = re.sub(r'\^\{0\.5\}', r'^{\\frac{1}{2}}', latex_str)
        latex_str = r"\LARGE{" + latex_str + r"}"
        
        return latex_str
    

    @staticmethod
    def count_operations(expr):
        """Count the number of operations in an expression - used for complexity"""
        if isinstance(expr, sp.Eq):
            return algebra.count_operations(expr.lhs) + algebra.count_operations(expr.rhs)
        
        if expr.is_Add or expr.is_Mul:
            return sum(algebra.count_operations(arg) for arg in expr.args) + len(expr.args) - 1
        
        if expr.is_Pow:
            return algebra.count_operations(expr.base) + algebra.count_operations(expr.exp) + 1
        
        if isinstance(expr, sp.Pow) and expr.exp == 0.5:  # sqrt
            return algebra.count_operations(expr.base) + 1
            
        return 0  # Atomic expression (symbol or number)


    @staticmethod
    def generate_equation(difficulty):
        """Generate a random algebra equation with a pedagogically sound solution path"""
        # Define difficulty parameters
        if difficulty == 'easy':
            num_steps = 2
            operations = ['add', 'sub', 'mul', 'div']
            max_value = 5
        elif difficulty == 'medium':
            num_steps = 3
            operations = ['add', 'sub', 'mul', 'div']
            max_value = 8
        elif difficulty == 'hard':
            num_steps = 3
            operations = ['add', 'sub', 'mul', 'div', 'sqr']
            max_value = 10
        else:  # extra_hard
            num_steps = 4
            operations = ['add', 'sub', 'mul', 'div', 'sqr', 'sqrt']
            max_value = 12
        
        # Choose target variable
        variables = ['x', 'y', 'z', 'a', 'b', 'c', 'm', 'n', 'p', 'q']
        var_target = random.choice(variables)
        var_solve = random.choice([v for v in variables if v != var_target])
        
        # Start with the target variable
        target_sym = sp.symbols(var_target)
        solve_sym = sp.symbols(var_solve)
        
        # Begin with the simplest equation: solve_var = target_var
        current_expr = target_sym
        
        # Build the solution path by applying random operations
        solution_path = []
        final_operations = []
        
        # Operation functions and their inverses
        op_funcs = {
            'add': (lambda x, v: x + v, 'Subtract', lambda x, v: x - v),
            'sub': (lambda x, v: x - v, 'Add', lambda x, v: x + v),
            'mul': (lambda x, v: x * v, 'Divide by', lambda x, v: x / v),
            'div': (lambda x, v: x / v, 'Multiply by', lambda x, v: x * v),
            'sqr': (lambda x, v: x ** 2, 'Take the square root', lambda x, v: sp.sqrt(x)),
            'sqrt': (lambda x, v: sp.sqrt(x), 'Square it', lambda x, v: x ** 2),
        }
        
        # Avoid consecutive inverse operations
        inverse_pairs = {
            'add': 'sub', 'sub': 'add',
            'mul': 'div', 'div': 'mul',
            'sqr': 'sqrt', 'sqrt': 'sqr'
        }
        
        prev_op = None
        
        for _ in range(num_steps):
            # Choose an operation (avoiding inverse of the previous one)
            available_ops = [op for op in operations if op != inverse_pairs.get(prev_op, None)]
            if not available_ops:
                available_ops = operations.copy()
            
            op_name = random.choice(available_ops)
            prev_op = op_name
            
            # Choose a value for the operation
            if op_name in ['sqr', 'sqrt']:
                value = None
            else:
                # For division, avoid values that make fractions too complex
                if op_name == 'div':
                    value = random.choice([2, 3, 4, 5])
                else:
                    value = random.randint(2, max_value)
            
            # Get the forward operation function
            op_func, inverse_name, inverse_func = op_funcs[op_name]
            
            # Apply the operation to our expression
            if value is None:
                current_expr = op_func(current_expr, None)
            else:
                current_expr = op_func(current_expr, value)
            
            # Store the inverse operation for the solution path
            solution_path.append({
                'operation': inverse_name,
                'value': value
            })
            
            # Store the forward operation for display
            final_operations.append({
                'operation': op_name,
                'value': value
            })
        
        # Create the final equation
        final_equation = sp.Eq(solve_sym, current_expr)
        
        # Now create a proper solution path in reverse
        solution_steps = []
        for step in reversed(solution_path):
            solution_steps.append(step)
        
        return {
            'equation': final_equation,
            'target_var': var_target,
            'solve_var': var_solve,
            'solution_steps': solution_steps,
            'operations_applied': final_operations,
            'steps_taken': [],
            'current_state': final_equation,
            'original_equation': final_equation,
        }


    @staticmethod
    def analyze_equation_state(equation, target_var):
        """Analyze the current state of the equation to determine hint suggestions"""
        target = sp.symbols(target_var)
        lhs, rhs = equation.args
        
        # Check where the target variable appears
        target_in_lhs = target in lhs.free_symbols
        target_in_rhs = target in rhs.free_symbols
        
        # Analyze the structure
        analysis = {
            'target_alone': False,
            'target_almost_alone': False,
            'target_on_both_sides': target_in_lhs and target_in_rhs,
            'target_on_left': target_in_lhs,
            'target_on_right': target_in_rhs,
            'has_addition': '+' in str(equation),
            'has_subtraction': '-' in str(equation),
            'has_multiplication': '*' in str(equation),
            'has_division': '/' in str(equation),
            'has_power': '**' in str(equation) or 'sqrt' in str(equation),
        }
        
        # Check if target is already isolated (or nearly so)
        if (lhs == target and not target_in_rhs) or (rhs == target and not target_in_lhs):
            analysis['target_alone'] = True
        
        # Check if target is almost isolated (like 2*x or x/3)
        if not analysis['target_alone']:
            if target_in_lhs and not target_in_rhs:
                lhs_factors = lhs.as_ordered_factors() if hasattr(lhs, 'as_ordered_factors') else [lhs]
                if len(lhs_factors) == 2 and any(factor.is_number for factor in lhs_factors):
                    analysis['target_almost_alone'] = True
                    
            elif target_in_rhs and not target_in_lhs:
                rhs_factors = rhs.as_ordered_factors() if hasattr(rhs, 'as_ordered_factors') else [rhs]
                if len(rhs_factors) == 2 and any(factor.is_number for factor in rhs_factors):
                    analysis['target_almost_alone'] = True
        
        return analysis


    @staticmethod
    def apply_operation(equation, operation, value=None):
        """Apply an algebraic operation to both sides of the equation"""
        lhs, rhs = equation.args
        
        if operation == "add":
            if value is None:
                return equation
            return sp.Eq(lhs + value, rhs + value)
        
        elif operation == "subtract":
            if value is None:
                return equation
            return sp.Eq(lhs - value, rhs - value)
        
        elif operation == "multiply":
            if value is None or value == 0:
                return equation
            return sp.Eq(lhs * value, rhs * value)
        
        elif operation == "divide":
            if value is None or value == 0:
                return equation
            return sp.Eq(lhs / value, rhs / value)
        
        elif operation == "square":
            return sp.Eq(lhs ** 2, rhs ** 2)
        
        elif operation == "sqrt":
            try:
                return sp.Eq(sp.sqrt(lhs), sp.sqrt(rhs))
            except:
                return equation
        
        # If operation not recognized, return the original equation
        return equation


    @staticmethod
    def simplify_powers(expr):
        # Look for sqrt(x**2) -> x pattern
        if isinstance(expr, sp.Pow) and expr.exp == sp.Rational(1, 2):  # sqrt
            if isinstance(expr.base, sp.Pow) and expr.base.exp == 2:
                return expr.base.base  # sqrt(x**2) -> x
            
            # Recurse through the expression tree
        if hasattr(expr, 'args') and len(expr.args) > 0:
            return expr.func(*[algebra.simplify_powers(arg) for arg in expr.args])
        return expr
    

    @staticmethod
    def minimal_simplify(equation):
        """Only perform basic simplification without solving"""
        try:
            # Basic expansion
            lhs = sp.expand(equation.lhs)
            rhs = sp.expand(equation.rhs)
            
            # Try sympy's built-in powsimp function first
            lhs = sp.powsimp(lhs)
            rhs = sp.powsimp(rhs)
            
            # Then apply our custom power simplifications
            lhs = algebra.simplify_powers(lhs)
            rhs = algebra.simplify_powers(rhs)
            
            expanded = sp.Eq(lhs, rhs)
            
            # Only update if it actually simplifies without solving
            if algebra.count_operations(expanded) < algebra.count_operations(equation):
                return expanded
        except:
            pass
        return equation


    @staticmethod
    def is_truly_solved(equation, target_var):
        """STRICT check if the target variable is truly isolated"""
        target = sp.symbols(target_var)
        lhs, rhs = equation.args
        
        # The target must be EXACTLY the symbol, not an expression containing it
        if (lhs == target and target not in rhs.free_symbols):
            return True
        
        if (rhs == target and target not in lhs.free_symbols):
            return True
        
        # Extra check - if it's x = number or number = x
        if (target in lhs.free_symbols and not target in rhs.free_symbols and 
            len(lhs.free_symbols) == 1 and len(rhs.free_symbols) == 0):
            return True
            
        if (target in rhs.free_symbols and not target in lhs.free_symbols and 
            len(rhs.free_symbols) == 1 and len(lhs.free_symbols) == 0):
            return True
        
        return False


    @staticmethod
    def process_step(equation, operation, value, target_var):
        """Process a single algebraic step"""
        # Apply the operation
        new_eq = algebra.apply_operation(equation, operation, value)
        
        # Check if this makes any change
        if str(new_eq) == str(equation):
            return False, equation, "This operation doesn't change the equation."
        
        # Do minimal simplification
        simplified_eq = algebra.minimal_simplify(new_eq)
        
        # Check if solved
        solved = algebra.is_truly_solved(simplified_eq, target_var)
        
        # Generate feedback
        if solved:
            feedback = "¡Excelente! You've solved the equation correctly! 🎉"
        else:
            # Analyze if this was a good step
            old_analysis = algebra.analyze_equation_state(equation, target_var)
            new_analysis = algebra.analyze_equation_state(simplified_eq, target_var)
            
            if new_analysis['target_alone'] and not old_analysis['target_alone']:
                feedback = "¡Perfecto! That isolated the variable. Great work! 👏"
            elif old_analysis['target_on_both_sides'] and not new_analysis['target_on_both_sides']:
                feedback = "¡Bien hecho! You got the variable to one side of the equation."
            elif algebra.count_operations(simplified_eq) < algebra.count_operations(equation):
                feedback = "Good step! You simplified the equation. 👍"
            else:
                feedback = ""
        
        return True, simplified_eq, feedback


    @staticmethod
    def initialize_session_state():
        """Initialize all session state variables"""
        if 'problem' not in algebra_state:
            algebra_state.problem = None
        if 'feedback' not in algebra_state:
            algebra_state.feedback = ""
        if 'solved' not in algebra_state:
            algebra_state.solved = False
        if 'question_id' not in algebra_state:
            algebra_state.question_id = 0
        if 'next_problem_data' not in algebra_state:
            algebra_state.next_problem_data = None
        if 'show_solution' not in algebra_state:
            algebra_state.show_solution = False
        if 'stars' not in algebra_state:
            algebra_state.stars = 0
        if 'hint_used' not in algebra_state:
            algebra_state.hint_used = False
        if 'selected_operation' not in algebra_state:
            algebra_state.selected_operation = "add"


    @staticmethod
    def select_operation(operation):
        algebra_state.selected_operation = operation


    @staticmethod
    def prepare_next_problem(difficulty):
        """Prepare the next problem in advance"""
        next_problem = algebra.generate_equation(difficulty)
        
        algebra_state.next_problem_data = {
            'problem': next_problem
        }


    @staticmethod
    def switch_to_next_problem():
        """Switch to the next problem that was prepared in advance"""
        if algebra_state.next_problem_data:
            algebra_state.problem = algebra_state.next_problem_data['problem']
            algebra_state.feedback = ""
            algebra_state.solved = False
            algebra_state.show_solution = False
            algebra_state.question_id += 1
            algebra_state.next_problem_data = None
            algebra_state.hint_used = False
            return True
        return False


    @staticmethod
    def main():
        st.title("Step-by-Step Algebra Practice")
        
        algebra.initialize_session_state()

        col1, col2, col3 = st.columns(3)
        with col1:
            difficulty = st.selectbox(
                "Select difficulty:",
                ['easy', 'medium', 'hard', 'extra_hard']
            )
            # Generate initial problem if needed
            if algebra_state.problem is None:
                algebra_state.problem = algebra.generate_equation(difficulty)
                algebra_state.question_id += 1
                algebra.prepare_next_problem(difficulty)
        with col2:
            st.write("")    
        with col3:
            st.write("")
            st.write("")
            if st.button("New Problem"):
                if algebra.switch_to_next_problem():
                    st.rerun()
                else:
                    # Fallback if next problem wasn't prepared
                    algebra_state.problem = algebra.generate_equation(difficulty)
                    algebra_state.feedback = ""
                    algebra_state.solved = False
                    algebra_state.show_solution = False
                    algebra_state.question_id += 1
        
        st.markdown(f"### Solve for {algebra_state.problem['target_var']}")
        current_eq = algebra_state.problem['current_state']
        eq_latex = algebra.latex_equation(current_eq)
        st.latex(eq_latex)
            
        # If the problem is solved, show congratulations
        if algebra_state.solved:
            st.success(algebra_state.feedback)
            
            # Prepare next problem if needed
            if algebra_state.next_problem_data is None:
                algebra.prepare_next_problem(difficulty)
                
            if st.button("Try Another Problem", key="new_problem_button"):
                    
                if algebra.switch_to_next_problem():
                    st.rerun()
                else:
                    # Fallback
                    algebra_state.problem = algebra.generate_equation(difficulty)
                    algebra_state.feedback = ""
                    algebra_state.solved = False
                    algebra_state.show_solution = False
                    algebra_state.question_id += 1
                    st.rerun()
        else:
            # Show operation selection form
            st.markdown("### Choose an operation to apply:")
            
           # Create a 3x2 grid of operation buttons
            col1, col2, col3 = st.columns(3)

            with col1:
                add_button = st.button("Add", 
                                    key="add_button", 
                                    type="primary" if algebra_state.selected_operation == "add" else "secondary",
                                    width='stretch')
                if add_button:
                    algebra.select_operation("add")
                    st.rerun()
                
                multiply_button = st.button("Multiply", 
                                        key="multiply_button", 
                                        type="primary" if algebra_state.selected_operation == "multiply" else "secondary",
                                        width='stretch')
                if multiply_button:
                    algebra.select_operation("multiply")
                    st.rerun()

                square_button = st.button("Square", 
                                        key="square_button", 
                                        type="primary" if algebra_state.selected_operation == "square" else "secondary",
                                        width='stretch')
                if square_button:
                    algebra.select_operation("square")
                    st.rerun()
               

            with col2:
                subtract_button = st.button("Subtract", 
                                        key="subtract_button", 
                                        type="primary" if algebra_state.selected_operation == "subtract" else "secondary",
                                        width='stretch')
                if subtract_button:
                    algebra.select_operation("subtract")
                    st.rerun()
                    
                divide_button = st.button("Divide", 
                                        key="divide_button", 
                                        type="primary" if algebra_state.selected_operation == "divide" else "secondary",
                                        width='stretch')
                if divide_button:
                    algebra.select_operation("divide")
                    st.rerun()
                
                sqrt_button = st.button("Square Root", 
                                    key="sqrt_button", 
                                    type="primary" if algebra_state.selected_operation == "sqrt" else "secondary",
                                    width='stretch')
                if sqrt_button:
                    algebra.select_operation("sqrt")
                    st.rerun()

            with col3:
                # Only show value input for operations that need it
                with st.form(f"Answer"):
                    if algebra_state.selected_operation in ["add", "subtract", "multiply", "divide"]:
                        value = st.number_input(
                            "Value:",
                            min_value=1, value=2,
                            key=f"value_{algebra_state.question_id}"
                        )
                    else:
                        value = None
                        st.write("No value needed for this operation")
                    submitted = st.form_submit_button("Apply Operation")
                    # Apply Operation button
                    if submitted:
                        success, new_eq, feedback = algebra.process_step(
                            algebra_state.problem['current_state'],
                            algebra_state.selected_operation,
                            value,
                            algebra_state.problem['target_var']
                        )
                        
                        if success:
                            # Update the equation
                            algebra_state.problem['current_state'] = new_eq
                            algebra_state.feedback = feedback
                            
                            # Add to steps taken
                            step_display = f"{algebra_state.selected_operation.capitalize()}"
                            if value is not None:
                                step_display += f" {value}"
                            
                            algebra_state.problem['steps_taken'].append({
                                'operation': algebra_state.selected_operation.capitalize(),
                                'value': value,
                                'display': step_display
                            })
                            
                            # Check if solved
                            if algebra.is_truly_solved(new_eq, algebra_state.problem['target_var']):
                                algebra_state.solved = True
                            
                            st.rerun()
                        else:
                            algebra_state.feedback = feedback

            # Display feedback
            if algebra_state.feedback:
                if "solved" in algebra_state.feedback.lower() or "excelente" in algebra_state.feedback.lower():
                    st.success(algebra_state.feedback)
                elif "correcto" in algebra_state.feedback.lower() or "bien" in algebra_state.feedback.lower() or "good" in algebra_state.feedback.lower():
                    st.info(algebra_state.feedback)
                else:
                    st.warning(algebra_state.feedback)
       
        # Show steps taken so far
        with st.expander("Show Steps Taken"):
            if algebra_state.problem['steps_taken']:
                for i, step in enumerate(algebra_state.problem['steps_taken']):
                    if 'display' in step:
                        st.markdown(f"{i+1}. {step['display']}")
                    elif 'operation' in step:
                        if step['value'] is not None:
                            # Check if value is a symbolic expression
                            if hasattr(step['value'], 'name'):
                                st.markdown(f"{i+1}. {step['operation']} {step['value'].name}")
                            else:
                                st.markdown(f"{i+1}. {step['operation']} {step['value']}")
                        else:
                            st.markdown(f"{i+1}. {step['operation']}")
            else:
                st.write("No steps taken yet.")
        # Show solution path if requested
        if algebra_state.show_solution:
            st.markdown("### Solution Path:")
            st.markdown("Here's how to solve this equation:")
            
            target_var = algebra_state.problem['target_var']
            current_equation = algebra_state.problem['original_equation']
            
            steps = []
            for i, step in enumerate(algebra_state.problem['solution_steps']):
                operation = step['operation']
                value = step['value']
                
                # Format the step description
                if value is None:
                    step_text = f"{i+1}. {operation}"
                else:
                    step_text = f"{i+1}. {operation} {value}"
                
                # Apply the step
                if operation == "Take the square root":
                    op = "sqrt"
                elif operation == "Square it":
                    op = "square"
                elif operation == "Add":
                    op = "add"
                elif operation == "Subtract":
                    op = "subtract"
                elif operation == "Multiply by":
                    op = "multiply"
                elif operation == "Divide by":
                    op = "divide"
                else:
                    op = operation.lower()
                    
                current_equation = algebra.apply_operation(current_equation, op, value)
                current_equation = algebra.minimal_simplify(current_equation)
                
                # Add to solution steps
                steps.append({
                    "text": step_text,
                    "equation": algebra.latex_equation(current_equation)
                })
            
            # Display the solution steps
            for step in steps:
                st.markdown(step["text"])
                st.latex(step["equation"])



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
                question = rf"({q_term_1} \;\cdot\; 10^{{{q_exp_1}}})\;\cdot\;({q_term_2}\;\cdot\;10^{{{q_exp_2}}})"
            else: # division
                ans_term = q_term_1 * q_term_2
                ans_term, q_term_1 = q_term_1, ans_term
                ans_exp = q_exp_1 - q_exp_2
                q_term_1, q_exp_1 = sci_notate.sci_not_format(q_term_1, q_exp_1)
                ans_term, ans_exp = sci_notate.sci_not_format(ans_term,ans_exp)
                question = rf"\\frac{{{q_term_1}\;\cdot\;10^{{{q_exp_1}}}}}{{{q_term_2}\;\cdot\;10^{{{q_exp_2}}}}}"
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
                question = rf"\\frac{{({q_term_1}\;\cdot\;10^{{{q_exp_1}}})\;\cdot\;({q_term_2}\;\cdot\;10^{{{q_exp_2}}})}}{{{q_term_3}\;\cdot\;10^{{{q_exp_3}}}}}"
            else: # 1 mul 2 div
                ans_term = q_term_1
                q_term_1*= q_term_2*q_term_3
                ans_exp = q_exp_1 - q_exp_2 - q_exp_3
                q_term_1, q_exp_1 = sci_notate.sci_not_format(q_term_1, q_exp_1)
                ans_term, ans_exp = sci_notate.sci_not_format(ans_term,ans_exp)
                question = rf"\\frac{{{q_term_1}\;\cdot\;10^{{{q_exp_1}}}}}{{({q_term_3}\;\cdot\;10^{{{q_exp_3}}})\;\cdot\;({q_term_2}\;\cdot\;10^{{{q_exp_2}}})}}"
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
            question = rf"({q_term_4}\;\cdot\;10^{{{q_exp_4}}})\;\cdot\;\\frac{{({q_term_1}\;\cdot\;10^{{{q_exp_1}}})\;\cdot\;({q_term_2}\;\cdot\;10^{{{q_exp_2}}})}}{{({q_term_3}\;\cdot\;10^{{{q_exp_3}}})^2}}"
        return question, ans_term, ans_exp

    def initialize_session_state():
        if 'sci_problem' not in sci_state:
            sci_state.sci_problem = None
        if 'submitted' not in sci_state:
            sci_state.submitted = False
        if 'user_input1' not in sci_state:
            sci_state.user_answer1 = None
        if 'user_input2' not in sci_state:
            sci_state.user_answer2 = None
        if 'question_id' not in sci_state:
            sci_state.question_id = 0

    def new_question(difficulty):
        sci_state.sci_problem, sci_state.ans1, sci_state.ans2 = sci_notate.generate_sci_not_problem(difficulty)
        sci_state.difficulty = difficulty
        sci_state.user_answer = None
        sci_state.user_answer2 = None
        sci_state.submitted = False
        sci_state.question_id += 1

    def main():
        st.title("Scientific Notation Practice")

        sci_notate.initialize_session_state()

        difficulty = st.selectbox(
            "Select difficulty:",
            ['easy', 'medium', 'hard'],key="sci notate difficulty"
        )

        if sci_state.sci_problem is None:
            sci_notate.new_question(difficulty)

        if sci_state.sci_problem:
            st.latex(sci_state.sci_problem)

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col2:
                st.header("")
                user_input1 = st.number_input(label='leading term', value=None,
                    step=None,
                    format="%f", key=f"user_input_sci_notate_{sci_state.question_id}")
            with col3:
                st.header("")
                st.title("x 10",anchor=False)
            with col4:
                st.write("")
                st.write("")
                st.write("")
                user_input2 = st.number_input(label='exponent', value=None,
                    step=None,
                    format="%f", key=f"user_input2_sci_notate{sci_state.question_id}")
            with col1:
                st.write("")
            with col6:
                st.write("")
            with col5:
                st.write("")
            
            if st.button("Submit",key="sci_notate_submit"):
                    sci_state.submitted = True
                    if user_input1 is not None:
                        sci_state.user_answer1 = user_input1
                        correct_answer = sci_state.ans1
                        #tolerance = abs(correct_answer * 0.05)
                        
                        if user_input2 is not None:
                            sci_state.user_answer2 = user_input2
                            correct_answer2 = sci_state.ans2
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






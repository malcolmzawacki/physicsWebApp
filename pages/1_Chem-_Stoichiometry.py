import random
import math
import streamlit as st

# A simple dictionary of elements with their atomic masses
elements = {
    'H': 1.01, 'He': 4.00, 'Li': 6.94, 'Be': 9.01, 'B': 10.81, 'C': 12.01, 'N': 14.01, 'O': 16.00,
    'F': 19.00, 'Ne': 20.18, 'Na': 22.99, 'Mg': 24.31, 'Al': 26.98, 'Si': 28.09, 'P': 30.97,
    'S': 32.07, 'Cl': 35.45, 'Ar': 39.95, 'K': 39.10, 'Ca': 40.08, 'Ti': 47.87, 'V': 50.94,
    'Cr': 52.00, 'Mn': 54.94, 'Fe': 55.85, 'Co': 58.93, 'Ni': 58.69, 'Cu': 63.55, 'Zn': 65.39,
    'Br': 79.90, 'I': 126.90, 'Ag': 107.87, 'Au': 196.97, 'Hg': 200.59, 'Pb': 207.2
}

def parse_formula(formula):
    """Parse a chemical formula into its constituent elements and their counts"""
    # This is a simplified parser that handles basic formulas
    elements_dict = {}
    i = 0
    while i < len(formula):
        # Find the element symbol (1 or 2 characters)
        if i + 1 < len(formula) and formula[i+1].islower():
            element = formula[i:i+2]
            i += 2
        else:
            element = formula[i]
            i += 1
        
        # Find the count (may be multiple digits)
        count = ''
        while i < len(formula) and formula[i].isdigit():
            count += formula[i]
            i += 1
        
        # If no count is specified, it's 1
        if count == '':
            count = 1
        else:
            count = int(count)
        
        # Add to the elements dictionary
        if element in elements_dict:
            elements_dict[element] += count
        else:
            elements_dict[element] = count
    
    return elements_dict

def calculate_molar_mass(formula):
    """Calculate the molar mass of a compound from its formula"""
    elements_dict = parse_formula(formula)
    molar_mass = 0
    
    for element, count in elements_dict.items():
        if element in elements:
            molar_mass += elements[element] * count
        else:
            # Handle unknown elements (for robustness)
            molar_mass += 10 * count  # Arbitrary value
    
    return round(molar_mass, 2)

def create_random_formula(complexity=1):
    """Create a random chemical formula with specified complexity"""
    common_elements = ['H', 'C', 'N', 'O', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', 'Fe', 'Cu', 'Zn']
    num_elements = random.randint(1, min(3 + complexity, 4))
    
    # Select random elements
    selected_elements = random.sample(common_elements, num_elements)
    
    # Create formula
    formula = ""
    for element in selected_elements:
        # Subscript (number of atoms)
        if complexity == 1:  # Easy - mostly 1-2
            subscript = random.choices([1, 2, 3], weights=[5, 3, 1])[0]
        else:  # Medium/Hard - can be larger
            subscript = random.choices([1, 2, 3, 4, 5], weights=[4, 3, 2, 1, 1])[0]
        
        formula += element
        if subscript > 1:
            formula += str(subscript)
    
    return formula

def create_random_reaction(num_reactants=None, num_products=None, complexity=1):
    """
    Create a random chemical reaction with the specified number of reactants and products
    Returns: unbalanced reaction (list of reactants, list of products)
    """
    # Determine number of compounds if not specified
    if num_reactants is None:
        num_reactants = random.randint(1, 3)
    if num_products is None:
        num_products = random.randint(1, 3)
    
    # Create random compounds
    reactants = [create_random_formula(complexity) for _ in range(num_reactants)]
    products = [create_random_formula(complexity) for _ in range(num_products)]
    
    return reactants, products

def count_elements(compounds, coefficients):
    """
    Count the number of each element in a set of compounds with coefficients
    Returns: dictionary of {element: count}
    """
    element_counts = {}
    
    for compound, coefficient in zip(compounds, coefficients):
        elements_in_compound = parse_formula(compound)
        
        for element, count in elements_in_compound.items():
            if element in element_counts:
                element_counts[element] += count * coefficient
            else:
                element_counts[element] = count * coefficient
    
    return element_counts

def balance_reaction(reactants, products):
    """
    Balance a chemical reaction using linear algebra (simplified approach)
    Returns: lists of coefficients for reactants and products
    
    Note: This is a simplified balancer that works for many cases but not all.
    For a complete solution, you'd need to use linear algebra to solve the system of equations.
    """
    # Start with all coefficients at 1
    reactant_coefficients = [1] * len(reactants)
    product_coefficients = [1] * len(products)
    
    # Count elements on both sides
    reactant_elements = count_elements(reactants, reactant_coefficients)
    product_elements = count_elements(products, product_coefficients)
    
    # Get all unique elements in the reaction
    all_elements = set(list(reactant_elements.keys()) + list(product_elements.keys()))
    
    # Simple balancing approach - adjust coefficients to match element counts
    # This won't work for all reactions but is sufficient for educational purposes
    max_attempts = 10
    balanced = False
    
    for _ in range(max_attempts):
        # Check if balanced
        balanced = True
        for element in all_elements:
            reactant_count = reactant_elements.get(element, 0)
            product_count = product_elements.get(element, 0)
            
            if reactant_count != product_count:
                balanced = False
                break
        
        if balanced:
            break
        
        # Try to balance by adjusting coefficients
        for element in all_elements:
            reactant_count = reactant_elements.get(element, 0)
            product_count = product_elements.get(element, 0)
            
            if reactant_count < product_count:
                # Find a reactant containing this element and increase its coefficient
                for i, reactant in enumerate(reactants):
                    elements_in_compound = parse_formula(reactant)
                    if element in elements_in_compound:
                        # Increase coefficient
                        multiplier = math.ceil(product_count / (elements_in_compound[element] * reactant_coefficients[i]))
                        reactant_coefficients[i] *= multiplier
                        # Recalculate element counts
                        reactant_elements = count_elements(reactants, reactant_coefficients)
                        break
            
            elif reactant_count > product_count:
                # Find a product containing this element and increase its coefficient
                for i, product in enumerate(products):
                    elements_in_compound = parse_formula(product)
                    if element in elements_in_compound:
                        # Increase coefficient
                        multiplier = math.ceil(reactant_count / (elements_in_compound[element] * product_coefficients[i]))
                        product_coefficients[i] *= multiplier
                        # Recalculate element counts
                        product_elements = count_elements(products, product_coefficients)
                        break
    
    # Find the GCD to simplify the coefficients
    all_coefficients = reactant_coefficients + product_coefficients
    if len(all_coefficients) > 1:
        gcd = all_coefficients[0]
        for i in range(1, len(all_coefficients)):
            gcd = math.gcd(gcd, all_coefficients[i])
        
        # Simplify only if there's a common divisor greater than 1
        if gcd > 1:
            reactant_coefficients = [c // gcd for c in reactant_coefficients]
            product_coefficients = [c // gcd for c in product_coefficients]
    
    # If not balanced, return a simple set of coefficients that at least have the right elements
    if not balanced:
        return [1] * len(reactants), [1] * len(products)
    
    return reactant_coefficients, product_coefficients

def grams_to_moles(grams, formula):
    """Convert grams to moles using the molar mass"""
    molar_mass = calculate_molar_mass(formula)
    return grams / molar_mass

def moles_to_grams(moles, formula):
    """Convert moles to grams using the molar mass"""
    molar_mass = calculate_molar_mass(formula)
    return moles * molar_mass

def format_reaction(reactants, products, reactant_coefficients, product_coefficients):
    """Format a balanced chemical reaction as a string"""
    reactant_terms = []
    for i, compound in enumerate(reactants):
        coefficient = reactant_coefficients[i]
        if coefficient == 1:
            reactant_terms.append(compound)
        else:
            reactant_terms.append(f"{coefficient} {compound}")
    
    product_terms = []
    for i, compound in enumerate(products):
        coefficient = product_coefficients[i]
        if coefficient == 1:
            product_terms.append(compound)
        else:
            product_terms.append(f"{coefficient} {products[i]}")
    
    reaction_str = " + ".join(reactant_terms) + " → " + " + ".join(product_terms)
    return reaction_str

def find_limiting_reagent(reactant_moles, reactant_coefficients):
    """
    Determine the limiting reagent based on moles available and stoichiometric coefficients
    Returns: limiting reagent index and the moles that will react
    """
    # Calculate how many moles of reaction each reactant can support
    reaction_equivalents = []
    for i, (moles, coefficient) in enumerate(zip(reactant_moles, reactant_coefficients)):
        reaction_equivalents.append((i, moles / coefficient))
    
    # The limiting reagent is the one that can support the least number of reaction equivalents
    limiting_idx, max_reaction_equivalents = min(reaction_equivalents, key=lambda x: x[1])
    
    return limiting_idx, max_reaction_equivalents

def calculate_product_amount(reactant_moles, reactant_coefficients, product_coefficient, target_product_idx):
    """
    Calculate the amount of a specific product produced given the reactant amounts
    Returns: moles of the target product
    """
    # Find the limiting reagent and max reaction equivalents
    limiting_idx, max_reaction_equivalents = find_limiting_reagent(reactant_moles, reactant_coefficients)
    
    # Calculate product amount
    product_moles = product_coefficient * max_reaction_equivalents
    
    return product_moles, limiting_idx, max_reaction_equivalents

def generate_reaction_type(reaction_type):
    """Generate a reaction based on the specified type"""
    if reaction_type == "Combustion":
        # Hydrocarbon + O2 → CO2 + H2O
        hydrocarbon = "C" + str(random.randint(1, 5)) + "H" + str(random.randint(4, 12))
        reactants = [hydrocarbon, "O2"]
        products = ["CO2", "H2O"]
    
    elif reaction_type == "Decomposition":
        # Single compound → multiple products
        reactants = [create_random_formula(2)]
        products = create_random_reaction(None, random.randint(2, 3), 1)[1]
    
    elif reaction_type == "Synthesis":
        # Multiple reactants → single product
        reactants = create_random_reaction(random.randint(2, 3), None, 1)[0]
        products = [create_random_formula(2)]
    
    elif reaction_type == "Single Replacement":
        # AX + B → BX + A
        metal1 = random.choice(['Li', 'Na', 'K', 'Rb', 'Cs', 'Be', 'Mg', 'Ca', 'Sr', 'Ba'])
        metal2 = random.choice(['Fe', 'Cu', 'Ag', 'Pb', 'Hg', 'Zn', 'Al'])
        nonmetal = random.choice(['F', 'Cl', 'Br', 'I', 'O', 'S'])
        compound1 = metal1 + nonmetal
        compound2 = metal2 + nonmetal
        reactants = [compound1, metal2]
        products = [compound2, metal1]
    
    elif reaction_type == "Double Replacement":
        # AX + BY → AY + BX
        metal1 = random.choice(['Li', 'Na', 'K', 'Ca', 'Mg', 'Ba'])
        metal2 = random.choice(['Fe', 'Cu', 'Ag', 'Pb', 'Zn', 'Al'])
        nonmetal1 = random.choice(['F', 'Cl', 'Br', 'I'])
        nonmetal2 = random.choice(['O', 'S', 'P', 'N'])
        compound1 = metal1 + nonmetal1
        compound2 = metal2 + nonmetal2
        compound3 = metal1 + nonmetal2
        compound4 = metal2 + nonmetal1
        reactants = [compound1, compound2]
        products = [compound3, compound4]
    
    else:  # Random
        reactants, products = create_random_reaction(random.randint(1, 3), random.randint(1, 3), 2)
    
    return reactants, products

def generate_stoichiometry_problem(reaction_type="Random", difficulty="Medium"):
    """
    Generate a random stoichiometry problem
    
    Difficulty affects the complexity of the problem:
    - Easy: Mole-to-mole calculations
    - Medium: Gram-to-mole or mole-to-gram calculations
    - Hard: Gram-to-gram calculations with limiting reagent
    
    Returns: question text, answer value, answer units, and problem details
    """
    # Generate reaction based on type
    reactants, products = generate_reaction_type(reaction_type)
    
    # Balance the equation
    reactant_coefficients, product_coefficients = balance_reaction(reactants, products)
    
    # Choose a random reactant and product for the problem
    reactant_idx = random.randint(0, len(reactants) - 1)
    target_reactant = reactants[reactant_idx]
    
    product_idx = random.randint(0, len(products) - 1)
    target_product = products[product_idx]
    
    # Generate random amount for the reactant (in moles for simplicity)
    if difficulty == "Easy":
        reactant_moles = random.randint(1, 10)  # Simple whole number
    else:
        reactant_moles = round(random.uniform(1, 20), 2)  # Decimal value
    
    # For medium/hard, we'll need multiple reactants with amounts
    if difficulty in ["Medium", "Hard"]:
        reactant_amounts = [0] * len(reactants)
        
        # Set the target reactant amount
        if difficulty == "Medium":
            # For medium, we'll do gram-to-mole or mole-to-gram
            conversion_type = random.choice(["gram-to-mole", "mole-to-gram"])
            
            if conversion_type == "gram-to-mole":
                # Convert moles to grams for the question
                reactant_grams = moles_to_grams(reactant_moles, target_reactant)
                reactant_grams = round(reactant_grams, 2)
                reactant_amounts[reactant_idx] = reactant_grams
                input_unit = "g"
                output_unit = "mol"
            else:  # mole-to-gram
                reactant_amounts[reactant_idx] = reactant_moles
                input_unit = "mol"
                output_unit = "g"
        
        else:  # Hard - gram-to-gram with limiting reagent
            # Convert all reactants to grams
            total_reactants = len(reactants)
            all_reactant_moles = [0] * total_reactants
            all_reactant_moles[reactant_idx] = reactant_moles
            
            # Generate random amounts for other reactants, making sure there's a limiting reagent
            for i in range(total_reactants):
                if i != reactant_idx:
                    # Determine equivalents needed for this reactant based on target
                    target_equivalents = reactant_moles / reactant_coefficients[reactant_idx]
                    
                    # Choose a value that may be limiting or in excess
                    if random.random() < 0.5:  # 50% chance of being limiting
                        multiplier = random.uniform(0.5, 0.9)  # Make it limiting
                    else:
                        multiplier = random.uniform(1.1, 2.0)  # Make it in excess
                    
                    # Calculate moles needed
                    all_reactant_moles[i] = round(target_equivalents * reactant_coefficients[i] * multiplier, 2)
                    
            # Convert all to grams
            for i in range(total_reactants):
                reactant_amounts[i] = round(moles_to_grams(all_reactant_moles[i], reactants[i]), 2)
            
            input_unit = "g"
            output_unit = "g"
    else:  # Easy - just mole-to-mole
        reactant_amounts = [0] * len(reactants)
        reactant_amounts[reactant_idx] = reactant_moles
        input_unit = "mol"
        output_unit = "mol"
    
    # Format the balanced reaction
    balanced_reaction = format_reaction(reactants, products, reactant_coefficients, product_coefficients)
    
    # Calculate the answer based on difficulty
    if difficulty == "Easy":
        # Simple mole-to-mole calculation
        mole_ratio = product_coefficients[product_idx] / reactant_coefficients[reactant_idx]
        product_moles = reactant_moles * mole_ratio
        answer = round(product_moles, 2)
        answer_unit = "mol"
        
        # Create explanation
        explanation = f"""
        Step 1: Find the mole ratio from the balanced equation.
        {reactant_coefficients[reactant_idx]} mol {target_reactant} produces {product_coefficients[product_idx]} mol {target_product}
        Mole ratio = {product_coefficients[product_idx]}/{reactant_coefficients[reactant_idx]} = {mole_ratio}
        
        Step 2: Use the mole ratio to calculate moles of product.
        Moles of {target_product} = {reactant_moles} mol {target_reactant} × {mole_ratio} = {answer} mol
        """
        
        # Create problem statement
        question = f"""Consider the reaction: {balanced_reaction}
        
        If you start with {reactant_moles} mol of {target_reactant}, how many moles of {target_product} will be produced?
        """
    
    elif difficulty == "Medium":
        if input_unit == "g" and output_unit == "mol":
            # Convert grams to moles, then mole-to-mole
            reactant_moles_actual = grams_to_moles(reactant_grams, target_reactant)
            mole_ratio = product_coefficients[product_idx] / reactant_coefficients[reactant_idx]
            product_moles = reactant_moles_actual * mole_ratio
            answer = round(product_moles, 2)
            answer_unit = "mol"
            
            # Create explanation
            explanation = f"""
            Step 1: Convert {reactant_grams} g of {target_reactant} to moles.
            Molar mass of {target_reactant} = {calculate_molar_mass(target_reactant)} g/mol
            Moles = {reactant_grams} g ÷ {calculate_molar_mass(target_reactant)} g/mol = {reactant_moles_actual:.2f} mol
            
            Step 2: Find the mole ratio from the balanced equation.
            {reactant_coefficients[reactant_idx]} mol {target_reactant} produces {product_coefficients[product_idx]} mol {target_product}
            Mole ratio = {product_coefficients[product_idx]}/{reactant_coefficients[reactant_idx]} = {mole_ratio}
            
            Step 3: Use the mole ratio to calculate moles of product.
            Moles of {target_product} = {reactant_moles_actual:.2f} mol {target_reactant} × {mole_ratio} = {answer} mol
            """
            
            # Create problem statement
            question = f"""Consider the reaction: {balanced_reaction}
            
            If you start with {reactant_grams} g of {target_reactant}, how many moles of {target_product} will be produced?
            """
        
        else:  # input_unit == "mol" and output_unit == "g"
            # Mole-to-mole, then convert to grams
            mole_ratio = product_coefficients[product_idx] / reactant_coefficients[reactant_idx]
            product_moles = reactant_moles * mole_ratio
            product_grams = moles_to_grams(product_moles, target_product)
            answer = round(product_grams, 2)
            answer_unit = "g"
            
            # Create explanation
            explanation = f"""
            Step 1: Find the mole ratio from the balanced equation.
            {reactant_coefficients[reactant_idx]} mol {target_reactant} produces {product_coefficients[product_idx]} mol {target_product}
            Mole ratio = {product_coefficients[product_idx]}/{reactant_coefficients[reactant_idx]} = {mole_ratio}
            
            Step 2: Use the mole ratio to calculate moles of product.
            Moles of {target_product} = {reactant_moles} mol {target_reactant} × {mole_ratio} = {product_moles:.2f} mol
            
            Step 3: Convert moles to grams.
            Molar mass of {target_product} = {calculate_molar_mass(target_product)} g/mol
            Mass = {product_moles:.2f} mol × {calculate_molar_mass(target_product)} g/mol = {answer} g
            """
            
            # Create problem statement
            question = f"""Consider the reaction: {balanced_reaction}
            
            If you start with {reactant_moles} mol of {target_reactant}, how many grams of {target_product} will be produced?
            """
    
    else:  # Hard - gram-to-gram with limiting reagent
        # Convert all reactant grams to moles
        reactant_moles_list = [grams_to_moles(grams, reactant) for grams, reactant in zip(reactant_amounts, reactants)]
        
        # Find limiting reagent and calculate product moles
        product_moles, limiting_idx, max_reaction_equivalents = calculate_product_amount(
            reactant_moles_list, reactant_coefficients, product_coefficients[product_idx], product_idx
        )
        
        # Convert product moles to grams
        product_grams = moles_to_grams(product_moles, target_product)
        answer = round(product_grams, 2)
        answer_unit = "g"
        
        # Create reactant descriptions
        reactant_descriptions = []
        for i, (reactant, amount) in enumerate(zip(reactants, reactant_amounts)):
            if amount > 0:
                reactant_descriptions.append(f"{amount} g of {reactant}")
        
        # Join with commas and 'and' for the last one
        if len(reactant_descriptions) == 1:
            reactant_text = reactant_descriptions[0]
        else:
            reactant_text = ", ".join(reactant_descriptions[:-1]) + ", and " + reactant_descriptions[-1]
        
        # Create explanation
        explanation_steps = []
        for i, (reactant, grams) in enumerate(zip(reactants, reactant_amounts)):
            if grams > 0:
                moles = reactant_moles_list[i]
                step = f"""Convert {grams} g of {reactant} to moles:
                Molar mass of {reactant} = {calculate_molar_mass(reactant)} g/mol
                Moles = {grams} g ÷ {calculate_molar_mass(reactant)} g/mol = {moles:.4f} mol"""
                explanation_steps.append(step)
        
        limiting_reagent_steps = []
        for i, (reactant, moles, coef) in enumerate(zip(reactants, reactant_moles_list, reactant_coefficients)):
            if moles > 0:
                equivalents = moles / coef
                step = f"{moles:.4f} mol {reactant} ÷ {coef} = {equivalents:.4f} reaction equivalents"
                limiting_reagent_steps.append(step)
        
        explanation = f"""
        Step 1: Convert each reactant from grams to moles.
        {'; '.join(explanation_steps)}
        
        Step 2: Determine the limiting reagent by calculating reaction equivalents.
        {'; '.join(limiting_reagent_steps)}
        
        The lowest value corresponds to {reactants[limiting_idx]}, which is the limiting reagent.
        
        Step 3: Calculate moles of {target_product} produced.
        Moles of {target_product} = {max_reaction_equivalents:.4f} × {product_coefficients[product_idx]} = {product_moles:.4f} mol
        
        Step 4: Convert moles of {target_product} to grams.
        Molar mass of {target_product} = {calculate_molar_mass(target_product)} g/mol
        Mass = {product_moles:.4f} mol × {calculate_molar_mass(target_product)} g/mol = {answer} g
        """
        
        # Create problem statement
        question = f"""Consider the reaction: {balanced_reaction}
        
        If you start with {reactant_text}, how many grams of {target_product} will be produced?
        (Hint: You need to identify the limiting reagent.)
        """
    
    # Create problem details
    problem_details = {
        "reaction": balanced_reaction,
        "reactants": reactants,
        "products": products,
        "reactant_coefficients": reactant_coefficients,
        "product_coefficients": product_coefficients,
        "target_reactant_idx": reactant_idx,
        "target_product_idx": product_idx,
        "explanation": explanation
    }
    
    return question, answer, answer_unit, problem_details

def initialize_stoichiometry_session_state():
    """Initialize session state variables for the stoichiometry page"""
    prefix = "stoichiometry_"
    if f"{prefix}question" not in st.session_state:
        st.session_state[f"{prefix}question"] = None
    if f"{prefix}answer" not in st.session_state:
        st.session_state[f"{prefix}answer"] = None
    if f"{prefix}units" not in st.session_state:
        st.session_state[f"{prefix}units"] = None
    if f"{prefix}details" not in st.session_state:
        st.session_state[f"{prefix}details"] = None
    if f"{prefix}submitted" not in st.session_state:
        st.session_state[f"{prefix}submitted"] = False
    if f"{prefix}user_answer" not in st.session_state:
        st.session_state[f"{prefix}user_answer"] = None
    if f"{prefix}show_solution" not in st.session_state:
        st.session_state[f"{prefix}show_solution"] = False

def stoichiometry_practice_page():
    """Create a Streamlit page for stoichiometry practice problems"""
    st.title("Stoichiometry Practice")
    
    initialize_stoichiometry_session_state()
    prefix = "stoichiometry_"
    
    # UI Controls
    col1, col2 = st.columns(2)
    
    with col1:
        reaction_type = st.selectbox(
            "Select reaction type:",
            ["Random", "Combustion", "Decomposition", "Synthesis", "Single Replacement", "Double Replacement"],
            key=f"{prefix}reaction_type"
        )
    
    with col2:
        difficulty = st.selectbox(
            "Select difficulty level:",
            ["Easy", "Medium", "Hard"],
            key=f"{prefix}difficulty"
        )
        
        if difficulty == "Easy":
            st.caption("Mole-to-mole calculations")
        elif difficulty == "Medium":
            st.caption("Gram-to-mole or mole-to-gram calculations")
        else:  # Hard
            st.caption("Gram-to-gram with limiting reagent")
    
    # Generate a new problem if needed
    if st.button("New Problem") or st.session_state[f"{prefix}question"] is None:
        question, answer, units, details = generate_stoichiometry_problem(reaction_type, difficulty)
        st.session_state[f"{prefix}question"] = question
        st.session_state[f"{prefix}answer"] = answer
        st.session_state[f"{prefix}units"] = units
        st.session_state[f"{prefix}details"] = details
        st.session_state[f"{prefix}submitted"] = False
        st.session_state[f"{prefix}user_answer"] = None
        st.session_state[f"{prefix}show_solution"] = False
        st.rerun()  # Rerun to reset the form
    
    # Display the current problem
    if st.session_state[f"{prefix}question"]:
        st.markdown(st.session_state[f"{prefix}question"])
        
        # Input form for the answer
        with st.form(key=f"{prefix}answer_form"):
            user_answer = st.number_input(
                f"Enter your answer ({st.session_state[f'{prefix}units']}):",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                key=f"{prefix}user_input"
            )
            
            submitted = st.form_submit_button("Submit Answer")
            if submitted:
                st.session_state[f"{prefix}submitted"] = True
                st.session_state[f"{prefix}user_answer"] = user_answer
                
                # Check if the answer is correct within tolerance
                correct_answer = st.session_state[f"{prefix}answer"]
                tolerance = correct_answer * 0.05  # 5% tolerance
                
                if abs(user_answer - correct_answer) <= tolerance:
                    st.success("Correct! Well done.")
                else:
                    st.error(f"Incorrect. The correct answer is {correct_answer} {st.session_state[f'{prefix}units']}.")
                    
                # Show the solution option
                st.session_state[f"{prefix}show_solution"] = True
                st.rerun()  # Rerun to show solution button
        
        # Show solution if requested
        if st.session_state[f"{prefix}submitted"] and st.session_state[f"{prefix}show_solution"]:
            if st.button("Show Solution"):
                explanation = st.session_state[f"{prefix}details"]["explanation"]
                st.markdown("### Solution")
                st.markdown(explanation)

def stoichiometry_explorer_page():
    """Create an exploratory page to learn about stoichiometry concepts"""
    st.title("Stoichiometry Explorer")
    
    # Tabs for different concepts
    tab1, tab2, tab3 = st.tabs(["Molar Mass Calculator", "Balancing Equations", "Limiting Reagent"])
    
    with tab1:
        st.header("Molar Mass Calculator")
        formula = st.text_input("Enter a chemical formula (e.g., H2O, C6H12O6):", key="molar_mass_input")
        
        if formula:
            try:
                molar_mass = calculate_molar_mass(formula)
                elements_dict = parse_formula(formula)
                
                # Display the molar mass
                st.success(f"Molar mass of {formula}: {molar_mass:.2f} g/mol")
                
                # Display the composition
                st.subheader("Composition")
                for element, count in elements_dict.items():
                    element_mass = elements[element] * count
                    percentage = (element_mass / molar_mass) * 100
                    st.write(f"{element}: {count} atom(s) × {elements[element]:.2f} g/mol = {element_mass:.2f} g/mol ({percentage:.1f}%)")
            except:
                st.error("Invalid formula. Please check your input.")
    
    with tab2:
        st.header("Balancing Chemical Equations")
        
        col1, col2 = st.columns(2)
        with col1:
            reactants_input = st.text_input("Enter reactants (comma separated, e.g., CH4,O2):", key="reactants_input")
        with col2:
            products_input = st.text_input("Enter products (comma separated, e.g., CO2,H2O):", key="products_input")
        
        if reactants_input and products_input:
            try:
                reactants = [r.strip() for r in reactants_input.split(",")]
                products = [p.strip() for p in products_input.split(",")]
                
                # Balance the equation
                reactant_coefficients, product_coefficients = balance_reaction(reactants, products)
                
                # Display the balanced equation
                balanced_eq = format_reaction(reactants, products, reactant_coefficients, product_coefficients)
                st.success(f"Balanced equation: {balanced_eq}")
                
                # Verify that elements are balanced
                reactant_elements = count_elements(reactants, reactant_coefficients)
                product_elements = count_elements(products, product_coefficients)
                
                st.subheader("Element Count Check")
                for element in sorted(set(list(reactant_elements.keys()) + list(product_elements.keys()))):
                    reactant_count = reactant_elements.get(element, 0)
                    product_count = product_elements.get(element, 0)
                    
                    if reactant_count == product_count:
                        st.write(f"{element}: {reactant_count} atoms ✅")
                    else:
                        st.write(f"{element}: {reactant_count} atoms (reactants) vs {product_count} atoms (products) ❌")
                        
                if reactant_elements == product_elements:
                    st.success("The equation is perfectly balanced!")
                else:
                    st.warning("The equation is not fully balanced. This can happen with more complex reactions.")
            except:
                st.error("Invalid input. Please check your formulas.")
    
    with tab3:
        st.header("Limiting Reagent Calculator")
        
        col1, col2 = st.columns(2)
        with col1:
            reactants_input = st.text_input("Enter reactants (comma separated, e.g., CH4,O2):", key="lr_reactants_input")
        with col2:
            products_input = st.text_input("Enter products (comma separated, e.g., CO2,H2O):", key="lr_products_input")
        
        # If reactants and products are provided
        if reactants_input and products_input:
            try:
                reactants = [r.strip() for r in reactants_input.split(",")]
                products = [p.strip() for p in products_input.split(",")]
                
                # Balance the equation
                reactant_coefficients, product_coefficients = balance_reaction(reactants, products)
                
                # Display the balanced equation
                balanced_eq = format_reaction(reactants, products, reactant_coefficients, product_coefficients)
                st.success(f"Balanced equation: {balanced_eq}")
                
                # Input for reactant amounts
                st.subheader("Enter amounts of reactants")
                
                # Choose input type
                input_type = st.radio("Input type:", ["Grams", "Moles"], key="lr_input_type")
                
                # Create input fields for each reactant
                reactant_amounts = {}
                for i, reactant in enumerate(reactants):
                    reactant_amounts[reactant] = st.number_input(
                        f"{reactant} ({input_type.lower()}):",
                        min_value=0.0,
                        step=0.1,
                        format="%.2f",
                        key=f"lr_amount_{i}"
                    )
                
                # Calculate button
                if st.button("Calculate Limiting Reagent"):
                    # Convert to moles if needed
                    reactant_moles = []
                    for reactant, amount in reactant_amounts.items():
                        if input_type == "Grams":
                            moles = grams_to_moles(amount, reactant)
                        else:
                            moles = amount
                        reactant_moles.append(moles)
                    
                    # Find limiting reagent
                    limiting_idx, max_reaction_equivalents = find_limiting_reagent(reactant_moles, reactant_coefficients)
                    limiting_reactant = reactants[limiting_idx]
                    
                    # Display results
                    st.markdown(f"### Limiting reagent: **{limiting_reactant}**")
                    
                    # Show calculation details
                    st.subheader("Calculation Details")
                    
                    for i, (reactant, moles, coef) in enumerate(zip(reactants, reactant_moles, reactant_coefficients)):
                        equivalents = moles / coef
                        
                        if i == limiting_idx:
                            st.write(f"**{reactant}**: {moles:.4f} mol ÷ {coef} = {equivalents:.4f} reaction equivalents ← Limiting")
                        else:
                            excess_percentage = ((equivalents / max_reaction_equivalents) - 1) * 100
                            st.write(f"{reactant}: {moles:.4f} mol ÷ {coef} = {equivalents:.4f} reaction equivalents ({excess_percentage:.1f}% excess)")
                    
                    # Calculate product yields
                    st.subheader("Product Yields")
                    
                    for i, (product, coef) in enumerate(zip(products, product_coefficients)):
                        product_moles = coef * max_reaction_equivalents
                        product_grams = moles_to_grams(product_moles, product)
                        
                        st.write(f"{product}: {product_moles:.4f} mol ({product_grams:.2f} g)")
            except:
                st.error("Invalid input. Please check your formulas and values.")

# Main function to run the app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", ["Practice Problems", "Stoichiometry Explorer"])
    
    if page == "Practice Problems":
        stoichiometry_practice_page()
    else:
        stoichiometry_explorer_page()

# For testing directly
if __name__ == "__main__":
    main()
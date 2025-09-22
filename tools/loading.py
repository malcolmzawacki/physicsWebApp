import streamlit as st
import importlib
from utils.ui import Interface

def lazy_load_tab(tab_name, generator_module, generator_class, ui_method="default_layout"):
    """Lazy load a tab only when clicked"""
    init_key = f"{tab_name}_initialized"
    generator_key = f"{tab_name}_generator"
    
    if init_key not in st.session_state:
        with st.spinner(f"Loading {tab_name}..."):
            # Dynamic import
            module = importlib.import_module(generator_module)
            generator_class_obj = getattr(module, generator_class)
            st.session_state[generator_key] = generator_class_obj()
            st.session_state[init_key] = True
    
    # Create UI and run
    ui = Interface(st.session_state[generator_key], tab_name.lower(), f"{tab_name} Problems")
    getattr(ui, ui_method)()
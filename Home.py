import streamlit as st
st.set_page_config(page_title="Home")
st.sidebar.header("Home")

st.title("Welcome to the Physics Practice Tool")
st.write(f"Streamlit version: {st.__version__}")

st.write("""
Select a problem type from the sidebar to begin practicing.
""")
import streamlit as st
from utils.ui import interface
from utils.generators.force_generator import ForceGenerator



def newtons_2nd():
     title = "Newton's Second Law"
     prefix = "newtons_2nd"
     difficulties = ["Easy","Medium","Hard"]
     generator = ForceGenerator()
     metadata = generator.stored_metadata()
     ui = interface(prefix,title,generator,metadata,difficulties)
     ui.unified_smart_layout()

def main():
     tab1,tab2 = st.tabs(["Newton's Second Law","TBD"])
     with tab1:
          newtons_2nd()
     with tab2:
        st.write("Currently Under Construction")

if __name__ == "__main__":
    main()
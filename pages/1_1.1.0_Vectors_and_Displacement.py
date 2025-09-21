import streamlit as st
import matplotlib.pyplot as plt


# Use a dark background for matplotlib so it fits a "dark mode" style
plt.style.use("dark_background")


from utils.ui import interface


class dist_disp:
  def distance_displacement():
      problem_type_dict = {
          "One Dimensional": {
                  "honors": r"""
                  \textrm{distance } =\; d_1 + d_2 + ... \newline ~ \newline
                  \textrm{displacement } =\; d_{final} - d_{initial} \; \textrm{(with direction)}
                  """,

                  "conceptual": r"""
                  \textrm{distance } =\; d_1 + d_2 + ... 
                  
                  \newline ~ \newline \textrm{"Positive" directions are right, East, up, and North}
                  \newline ~ \newline \textrm{"Negative" directions are left, West, down, and South}
                  \newline ~ \newline \textrm{displacement } =\; d_{final} - d_{initial} \; \textrm{(with direction)}
                  """},
          "Two Dimensional": {
                  "honors": r"""
                  \textrm{distance } =\; d_1 + d_2 + ... \newline ~ \newline
              \textrm{displacement } =\; \sqrt{d_{horizontal}^2 + d_{vertical}^2} \;\; \textrm{(with direction)}
                  """,

                  "conceptual": r"""
                  \textrm{distance } =\; d_1 + d_2 + ... \newline ~ \newline
                  \textrm{Horizontal Displacement } =\; D_{East} - D_{West} \newline ~ \newline
                  \textrm{Vertical Displacement } =\; D_{North} - D_{South} \newline ~ \newline
              \textrm{Net Displacement } =\; \sqrt{D_{horizontal}^{\;2} + D_{vertical}^2} \;\; \textrm{(with direction)}
                  """},
          }
      difficulties = ["Easy","Medium","Hard"]
      from utils.generators.dist_disp_generator import DistDispGenerator
      title = "Distance & Displacement"
      prefix = "constant"
      ui = interface(prefix,title,DistDispGenerator(),
                  problem_type_dict,difficulties,True)
      ui.unified_smart_layout()


class vectors:
    def vector_practice():
        problem_type_dict = {
            "Find Components": {
                "honors" : r"", 
                "conceptual": r""""""
                },
            "Find Resultant": {
                "honors": r"",
                "conceptual": r""""""
            },
            "Summing Vectors": {
                "honors": r"",
                "conceptual": r""""""
            },
        }
        difficulties = ["Easy", "Medium", "Hard"]
        from utils.generators.vector_generator import VectorGenerator
        title = "Vectors"
        prefix = "vect"
        generator = VectorGenerator()
        ui = interface(prefix, title, generator, problem_type_dict, difficulties)
        ui.unified_smart_layout(equations=True)

def main():
    tab1, tab2 = st.tabs([
        "Distance and Displacement", 
        "Vector Practice"
        ])
    with tab1:
        dist_disp.distance_displacement()
    with tab2:
        vectors.vector_practice()


if __name__ == "__main__":
    main()

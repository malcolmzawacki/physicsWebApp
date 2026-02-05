import matplotlib.pyplot as plt


# Use a dark background for matplotlib so it fits a "dark mode" style
plt.style.use("dark_background")


from utils.ui import interface
from tools.loading import lazy_tabs
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
      generator = DistDispGenerator()
      metadata = generator.stored_metadata()
      ui = interface(prefix, title, generator, metadata, difficulties)
      ui.unified_smart_layout()


class vectors:
    def vector_practice():

        difficulties = ["Easy", "Medium", "Hard"]
        from utils.generators.vector_generator import VectorGenerator
        title = "Vectors"
        prefix = "vect"
        generator = VectorGenerator()
        metadata = generator.stored_metadata()
        ui = interface(prefix, title, generator, metadata, difficulties)
        ui.unified_smart_layout(equations=True)

def main():
    tab_specs = [
        ("Distance and Displacement", dist_disp.distance_displacement),
        ("Vector Practice", vectors.vector_practice),
    ]

    lazy_tabs(tab_specs, state_key="vectors_tabs", auto_load_first=True)

if __name__ == "__main__":
    main()


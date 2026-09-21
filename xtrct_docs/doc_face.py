import sys
from pathlib import Path
import matplotlib

matplotlib.use("Agg")

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from xtrct_docs.document_creator import create_doc
from xtrct_docs.question_organizer import Org
title = "Advanced Forces Practice"
number_of_docs = 1
org = Org()

question_generator = org.funny_forces_practice()

# Explicit target worksheets use the same catalog as the site's Solve for control.
# See docs/solve_for_evaluation.md for a complete example and available-target listing.


def main():
  print("Accessing create document")
  create_doc(title, question_generator, number_of_docs, tables=False)


if __name__ == "__main__":
  main()

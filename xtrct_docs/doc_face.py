from document_creator import create_doc

from question_organizer import Org
title = "Motion Test"
number_of_docs = 6
org = Org()

question_generator = org.mixed_motion_with_graphs()


def main():
  print("Accessing create document")
  create_doc(title, question_generator, number_of_docs, tables=True)


if __name__ == "__main__":
  main()
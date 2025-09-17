from document_creator import create_doc

from question_organizer import Org
title = "Constant Motion Quiz"
number_of_docs = 3
org = Org()

question_generator = org.constant_motion_quiz()


def main():
  print("Accessing create document")
  create_doc(title, question_generator, number_of_docs)


if __name__ == "__main__":
  main()
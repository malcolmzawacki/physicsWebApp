from document_creator import create_documents

from question_organizer import Org
title = "Constant Motion Quiz"
number_of_docs = 1
org = Org()
questions = org.constant_motion_quiz()


def main():
  print("Accessing create document")
  create_documents(title, questions, number_of_docs)


if __name__ == "__main__":
  main()
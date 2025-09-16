from document_creator import create_doc_from_gen

from question_organizer import Org
title = "Constant Motion Quiz"
number_of_docs = 3
org = Org()

question_generator = org.create_first_doc()


def main():
  print("Accessing create document")
  create_doc_from_gen(title, question_generator, number_of_docs)


if __name__ == "__main__":
  main()
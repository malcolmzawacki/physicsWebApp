from document_creator import create_doc

from question_organizer import Org
title = "Projectile Quiz H"
number_of_docs = 5
org = Org()

question_generator = org.projectile_quiz_H()


def main():
  print("Accessing create document")
  create_doc(title, question_generator, number_of_docs, tables=True)


if __name__ == "__main__":
  main()
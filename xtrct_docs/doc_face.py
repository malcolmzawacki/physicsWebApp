from document_creator import create_doc

from question_organizer import Org
title = "Projectile Practice"
number_of_docs = 1
org = Org()

question_generator = org.projectile_practice()


def main():
  print("Accessing create document")
  create_doc(title, question_generator, number_of_docs, tables=False)


if __name__ == "__main__":
  main()
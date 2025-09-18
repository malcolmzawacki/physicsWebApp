from docx import Document
from docx.shared import Inches
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

# Create main test document
 # Store answers as you generate
def create_vert_answer_table(doc, problem_units, problem_number):
    """
    Create a formatted answer table for multipart questions
    
    :param doc: Document object
    :param problem_units: List of unit strings (e.g., ["Direction", "Motion State"])
    :param problem_number: The problem number for labeling
    """
    # Add a small space before the table
    doc.add_paragraph()
    
    # Add "Final Answers:" label
    final_answers_para = doc.add_paragraph()
    final_answers_run = final_answers_para.add_run("Final Answers:")
    final_answers_run.bold = True
    
    # Create table with 2 columns and rows equal to number of answer parts
    table = doc.add_table(rows=len(problem_units), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    
    # Set table style and format
    table.style = 'Table Grid'
    
    # Populate the table
    for i, unit in enumerate(problem_units):
        # Clean up the unit string (remove parentheses if present)
        clean_unit = unit.replace('(', '').replace(')', '').strip()
        
        # Left column: unit label
        left_cell = table.cell(i, 0)
        left_cell.text = clean_unit
        left_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        # Right column: blank line for student answer
        right_cell = table.cell(i, 1) 
        right_cell.text = "_" * 20  # Underline for student to write on
        right_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # Set column widths - make label column narrower, answer column wider
    for row in table.rows:
        row.cells[0].width = Inches(1.5)  # Unit label column
        row.cells[1].width = Inches(3.0)  # Answer column


def create_answer_table(doc, problem_units, problem_number):
    """
    Create a formatted answer table for multipart questions with horizontal layout
    
    :param doc: Document object
    :param problem_units: List of unit strings (e.g., ["Direction", "Motion State"])
    :param problem_number: The problem number for labeling
    """
    # Add "Final Answers:" label on same line, no extra spacing
    final_answers_para = doc.add_paragraph()
    final_answers_run = final_answers_para.add_run("Final Answers:")
    final_answers_run.bold = True
    
    # Keep the "Final Answers:" label with the table
    final_answers_para.paragraph_format.keep_with_next = True
    
    # Create table with 2 rows and columns equal to number of answer parts
    num_parts = len(problem_units)
    table = doc.add_table(rows=2, cols=num_parts)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    
    # Set table style and format
    table.style = 'Table Grid'
    
    # Keep table together and prevent it from breaking across pages
    try:
        from docx.oxml.shared import qn
        from docx.oxml import OxmlElement
        
        # Access table properties and set keep together
        tbl = table._element
        tbl_pr = tbl.find(qn('w:tblPr'))
        if tbl_pr is None:
            tbl_pr = OxmlElement('w:tblPr')
            tbl.insert(0, tbl_pr)
        
        # Add keep together property for the table
        keep_together = OxmlElement('w:cantSplit')
        keep_together.set(qn('w:val'), 'true')
        tbl_pr.append(keep_together)
        
    except ImportError:
        # If XML manipulation fails, continue without it
        pass
    
    # First row: unit labels
    for i, unit in enumerate(problem_units):
        # Clean up the unit string (remove parentheses if present)
        
        
        # Top row: unit label
        header_cell = table.cell(0, i)
        header_cell.text = unit
        header_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        # Make header row bold
        for paragraph in header_cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
    
    # Second row: blank spaces for student answers
    for i in range(num_parts):
        answer_cell = table.cell(1, i)
        answer_cell.text = ""  # Leave completely blank for students to write
        answer_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Set column widths to be evenly distributed
    column_width = Inches(6.0 / num_parts)  # Distribute 6 inches across all columns
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            cell.width = column_width
    
    # Set the height of the answer row (second row, index 1)
    table.rows[1].height = Inches(0.5)  # Good amount of writing room


def keep_question_together(doc, question_paragraphs):
    """Apply 'keep with next' to all paragraphs in a question except the last one"""
    for i in range(len(question_paragraphs) - 1):
        question_paragraphs[i].paragraph_format.keep_with_next = True


def is_multipart_question(problem):
    """
    Determine if a question has multiple answer parts
    
    :param problem: Problem dictionary with 'answers' and 'units' keys
    :return: Boolean indicating if question is multipart
    """
    return len(problem["answers"]) > 1



def create_and_embed_graph(doc, graph_data, filename = "temp_graph.png"):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(4,4))
    plt.plot(graph_data['x'], graph_data['y'])
    plt.xlabel(graph_data['xlabel'])
    plt.ylabel(graph_data['ylabel'])
    plt.title(graph_data['title'])
    plt.grid(True)

    plt.savefig(filename, dpi=300,bbox_inches='tight')
    plt.close()

    doc.add_picture(filename, width = Inches(5))

    os.remove(filename)
    

def create_doc(title: str, question_generator, number_of_docs: int):
  doc = Document()
  answer_key = [] 
  for doc_num in range(1, number_of_docs + 1):
      questions = question_generator()
      # Add test header
      doc.add_heading(f'{title} {doc_num}', 0)
      doc.add_paragraph(f'Name: _____________________________________________ Date: __________________')
      
      # Generate problems here
      problem_number = 1
      version_answers = {}
      section_num = 1

      for section in questions:
         
         heading = section["heading"]
         doc.add_heading(f"Section {section_num}: {heading}", level=2)
         spaces = section["gap"]
         section_answers = []

         for problem in section["problems"]:

            clean_question = problem["question"].split(" ")
            clean_tuple = ()
            for word in clean_question:
                clean_tuple += tuple((word, " "))
            clean_question = "".join(tuple(clean_tuple))

            question_para = doc.add_paragraph(f'{problem_number}. {clean_question}')
            question_para.paragraph_format.keep_with_next = True
            question_para.paragraph_format.keep_together = True

            # Check if this is a multipart question
            if is_multipart_question(problem):
                # Create answer table for multipart questions
                create_answer_table(doc, problem["units"], problem_number)
 
                
                # Store formatted answer for answer key
                answers = problem["answers"]
                units = problem["units"]
                answer_parts = ["Multiple Answers:"]
                for answer, unit in zip(answers, units):

                    answer_parts.append(f"{unit}: {answer}")
                answer_str = " \n ".join(answer_parts)
                section_answers.append(f"{problem_number}. {answer_str}")
            else:
                # Single-part question: use original spacing method
                #for i in range(spaces):
                    #doc.add_paragraph()
                
                # Store single answer for answer key
                answer = problem["answers"][0]
                unit = problem["units"][0]
                section_answers.append(f"{problem_number}. {unit}: {answer}")

            if "graph" in problem:
                from utils.graph_utils import embed_graph_in_doc
                embed_graph_in_doc(doc, problem["graph"])
            for _ in range(spaces):
                blank_para = doc.add_paragraph()
                blank_para.paragraph_format.keep_together = True
            
            problem_number += 1
          
         version_answers[f"Section {section_num}: {heading}"] = section_answers
         section_num += 1
      

      
      # Store answers for this version
      answer_key.append({f"Version {doc_num}": version_answers})
      # ensure full page gap between pages
      doc.add_page_break()
      doc.add_page_break()


  doc.add_heading('Answer Key - All Versions', 1)
  for version_dict in answer_key:
    for version_name, sections in version_dict.items():
        doc.add_heading(version_name, level=2)
        for section_name, answers in sections.items():
            doc.add_heading(section_name, level=3)
            for answer in answers:
                doc.add_paragraph(answer)
    doc.add_page_break()            # Space between versions

  # Save main document
  file_name = f'{title}_x{number_of_docs}.docx'
  doc.save(file_name)
  try:
    os.startfile(file_name)
  except:
    pass
  print("Saving document")
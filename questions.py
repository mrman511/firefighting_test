import PyPDF2
import re
import pprint
pprint = pprint.PrettyPrinter(indent=4).pprint
from .testing_questions.questions.models import Question


# Define the pattern using a regular expression
path = './test-questions/questions'

# string to save total of pdf page questions
string = ''


for i in range(1, 13):
  # # Assigning the pdfWriter() function to pdfWriter.
  pdfWriter = PyPDF2.PdfWriter()
  pdfFileObj = open(f'{path}{i}.pdf', 'rb') 
  pdfReader = PyPDF2.PdfReader(pdfFileObj, strict=False)

  # add contents off all pages to string
  for page in pdfReader.pages:
    text = page.extract_text()
    string += text

# regrex for number followed by a . surrounded by whitespace
pattern = re.compile(r'\d+\.\s')
questions = pattern.split(string)

num = 1

parsed_questions = []
for question in questions:
  is_valid=True
  question = f'{str(num)}. ' + question

  new_question={}

  question_regrex = re.compile(r'\d+\.\s(.+):')
  # Use search to find the match
  parsed_question = question_regrex.search(question)
  # if question is successfull
  if parsed_question:
    # Extract the desired portion
    q = parsed_question.group(1)
    if q.startswith("Match") or q.startswith('Directions'):
      is_valid=False
    new_question['question']=q.strip()
  else:
    is_valid=False

  # get A. answer
  a_pattern = re.compile(r'A\.\s(.*?)(?=B\.)', re.DOTALL)
  # Use search to find the match
  a = a_pattern.search(question)
  # Check if a match is found
  if a:
    # Extract the text between "A." and "B."
    a_answer = a.group(1)
    new_question['A'] = a_answer.strip()
  else:
    is_valid=False

  # get B. answer
  b_pattern = re.compile(r'B\.\s(.*?)(?=C\.)', re.DOTALL)
  # Use search to find the match
  b = b_pattern.search(question)
  # Check if a match is found
  if b:
    # Extract the text between "A." and "B."
    b_answer = b.group(1)
    new_question['B'] = b_answer.strip()
  else:
    is_valid=False

  # get C. answer
  c_pattern = re.compile(r'C\.\s(.*?)(?=D\.)', re.DOTALL)
  # Use search to find the match
  c = c_pattern.search(question)
  # Check if a match is found
  if c:
    # Extract the text between "A." and "B."
    c_answer = c.group(1)
    new_question['C'] = c_answer.strip()
  else:
    is_valid=False

  # get D. answer
  pattern = re.compile(r'D\.\s(.*?)(?=Answer:)', re.DOTALL)

  # Use search to find the match
  d = pattern.search(question)
  # Check if a match is found
  if d:
    # Extract the text between "C." and "Answer:"
    d_answer = d.group(1)
    new_question['D'] = d_answer.strip()
  else:
    is_valid=False

  # get answer
  answer_pattern = re.compile(r'Answer:\s(.*)')
  # Use search to find the match
  answer = answer_pattern.search(question)
  # Check if a match is found
  if answer:
    # Extract the text after "Answer:"
    answer_text = answer.group(1)
    new_question['answer']=answer_text.strip()
  else:
    is_valid=False

  if is_valid:
    parsed_questions.append(new_question)

  num += 1

for question in parsed_questions:
  try:
    question = Question.objects.create(
      question=question['question'],
      a=question['A'],
      b=question['B'],
      c=question['C'],
      d=question['D'],
      answer=question['answer']
    )
    question.save()
    print('question added')
  except:
    print('question failed')
import re
import string
from mail import Email
from nltk import sent_tokenize, word_tokenize
from pos_tagger import POSTagger
from ner_tagger import NERTagger
from ner_tagger_io import ner_features


"""
Tags the locations in the Email.

1. Looks for a line starting with 'Place' in the header. If found, it will tag it
and tag all the occurences of it in the body.

2. If no info in header is found, NER tagger is used and all the
-geo types are tagged
"""


def tag_location(email):
  header = email.header
  body = email.body

  reg_line = r'Place.*\n'
  reg_loc  = r':.*'

  # Tag header

  line = []

  try:
    # Get line which contains time info
    line = re.findall(reg_line, header)[0]

    location = re.findall(reg_loc, line)[0][1:].strip() # remove semicolon from beginning [1:]
    n_location = '<location>' + location + '</location>'
    np_location = 'Place: <location>' + location + '</location>\n'

    header = re.sub(reg_line, np_location, header)
    body = re.sub(location, n_location, body)
    return Email(header, body, email.fileid)
  except:
    pass

  file = open('./Data/locations.txt', 'r')
  locations = file.readlines()
  locations = [x.strip() for x in locations]
  file.close()

  body = email.body

  for l in locations:
    if l in body:
      loc = '<location>' + l + '</location>'
      body = re.sub(l,loc,body)

  return Email(header, body, email.fileid)

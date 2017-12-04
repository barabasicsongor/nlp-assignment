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

  # Use NER Tagger for tagging
  pos = POSTagger()
  pos.load_pos_tagger()

  chunker = NERTagger(ner_features)
  chunker.load_ner_tagger('./Data/models/ner_tagger.pkl')

  body = email.body
  body = [list(pos.predict(word_tokenize(s))) for s in sent_tokenize(body)]
  body = [chunker.parse(s) for s in body]
  
  for t in body:
    for c in t:
      if hasattr(c,'label'):
        print(c.label())
        # s = ''
        # for x in c:
        #   s += x[0]
        # print(s)

  return Email(header, body, email.fileid)

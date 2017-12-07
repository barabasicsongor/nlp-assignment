import re
import string
from mail import Email
from nltk import sent_tokenize, word_tokenize
from pos_tagger import POSTagger
from ner_tagger import NERTagger
from ner_tagger_io import ner_features
from cleaner import del_stopwords


"""
Tags the speakers in the Email.

1. Looks for a line starting with 'Who' in the header. If found, it will tag it
and tag all the occurences of it in the body.

2. If no info in header is found, NER tagger is used and all the
-per types are tagged
"""


def tag_speaker(email,pos_tagger_path,ner_tagger_path):
  file = open('./Data/speakers.txt', 'r')
  speakers = file.readlines()
  speakers = [x.strip() for x in speakers]
  file.close()

  header = email.header
  body = email.body

  reg_line = r'Who.*\n'
  reg_loc = r':.*'

  # Tag header
  found = False

  try:

    line = re.findall(reg_line, header)

    if len(line) > 0:
      line = line[0]
      for s in speakers:
        if s in line:
          ns = '<speaker>' + s + '</speaker>'
          header = re.sub(s,ns,header)
          body = re.sub(s,ns,body)
          found = True

    if not found:
      # Get line which contains time info
      line = re.findall(reg_line, header)[0]

      # remove semicolon from beginning [1:]
      speaker = re.findall(reg_loc, line)[0][1:].strip()
      n_speaker = '<speaker>' + speaker + '</speaker>'
      np_speaker = 'Who: <speaker>' + speaker + '</speaker>\n'

      header = re.sub(reg_line, np_speaker, header)
      body = re.sub(speaker, n_speaker, body)
    
    return Email(header, body, email.fileid)
  except:
    pass

  # Use NER Tagger for tagging
  pos = POSTagger()
  pos.load_pos_tagger(pos_tagger_path)

  chunker = NERTagger(ner_features)
  chunker.load_ner_tagger(ner_tagger_path)

  body = email.body
  body = [list(pos.predict(word_tokenize(s))) for s in sent_tokenize(body)]
  body = [chunker.parse(s) for s in body]

  speakers_n = []

  for chunk in body:
    for c in chunk:
      if hasattr(c, 'label'):
        if c.label() == 'per':
          s = ''
          for v in c:
            s = s + v[0] + ' '
          s = s.strip()
          speakers_n.append(s)
        elif c.label() == 'org':
          s = ''
          for v in c:
            s = s + v[0] + ' '
          s = s.strip()
          speakers_n.append(s)

  body = email.body
  for s in speakers_n:
    if s in speakers:
      ns = '<speaker>' + s + '</speaker>'
      body = re.sub(s,ns,body)

  return Email(header, body, email.fileid)

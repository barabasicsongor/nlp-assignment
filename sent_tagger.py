import re
from mail import Email
from nltk.tokenize import sent_tokenize

"""
Tag sentences by splitting the body of the text in sentences
using the sentence tokenizer from NLTK.
"""
def tag_sents(email):
  # Remove the 'Abstract:' part
  body = email.body[9:]

  body_sents = sent_tokenize(body)
  body_sents = [re.sub(r'\n','',b) for b in body_sents]

  body = email.body
  for s in body_sents:
    if not s.startswith(' '):
      ns = '<sentence>' + s + ' </sentence>'
      body = body.replace(s,ns)

  return Email(email.header, body, email.fileid)

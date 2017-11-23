from mail import Email
from nltk.tokenize import sent_tokenize

"""
Tag sentences by splitting the body of the text in sentences
using the sentence tokenizer from NLTK.

TODO: Change the inbuild sentence tokenizer to my custom one. First test how mine works.
"""
def tag_sents(email):
  # Remove the 'Abstract:' part
  body = email.body[9:].strip()

  body_sents = sent_tokenize(body)

  body = "Abstract:\n"
  for s in body_sents:
    body += '<sentence>' + s + '</sentence>'

  return Email(email.header, body, email.fileid)

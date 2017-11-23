from mail import Email

"""
Tag paragraphs by seeing where is more than one '\n' character
TODO: Handle when there are more than 2 newline characters
"""
def tag_paragraphs(email):
  body = email.body[9:].strip()

  body_split = body.split('\n\n')

  body = "Abstract:\n"

  for s in body_split:
    body += '<paragraph>' + s + '</paragraph>'

  return Email(email.header, body, email.fileid)

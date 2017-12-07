from mail import Email

"""
Tag paragraphs by seeing where is more than one '\n' character
"""
def tag_paragraphs(email):
  body = email.body[9:].strip()

  body_split = body.split('\n\n')
  body_split = [b for b in body_split if b != '']

  body = email.body

  for s in body_split:
    if (not s.startswith(' ')) and s[0].isalnum():
      ns = '<paragraph>' + s + '</paragraph>'
      body = body.replace(s,ns)

  return Email(email.header, body, email.fileid)

import re
from mail import Email


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

  return Email(header, body, email.fileid)

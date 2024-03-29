import re
from mail import Email


"""
Tags the times in the email

1. Checks if there is time detail in the header
   and tags it appropiately.

2. Uses the info gathered about time from the header
   and tags the similar times in the body with the same tag.
   If no info is found in the header, no tagging is made on the body.
   If one time in the header, then it is <stime>.
   If two times in the header, then there is <stime> and <etime>.

3. Returns the tagged Email object
"""
def tag_time(email):
  header = email.header
  body = email.body

  reg_time = r'\[0-9]+:[0-9][0-9]|[0-9]+:[0-9][0-9] +[APap]\.?[mM]'
  reg_line = r'Time.*\n'

  # Tag header

  times = []
  times_tag = []

  try:
    # Get line which contains time info
    line = re.findall(reg_line, header)[0]
    times = re.findall(reg_time, line)

    if len(times) == 1:
      times_tag.append('<stime>' + times[0] + '</stime>')
    else:
      times_tag.append('<stime>' + times[0] + '</stime>')
      times_tag.append('<etime>' + times[1] + '</etime>')

    for i in range(0, len(times)):
      line = re.sub(times[i], times_tag[i], line)

    header = re.sub(reg_line, line, header)
  except:
    pass

  # Tag times in body

  if len(times) > 0:
    # Strip times from header to contain only digits
    for i in range(0, len(times)):
      times[i] = re.findall(r'[0-9]+:[0-9][0-9]', times[i])[0]

    # Get all times from body
    times_b = re.findall(reg_time, body)
    times_b_tag = list(times_b)

    # Tag the times from body based on header time tags
    for i in range(0, len(times_b)):
      if times[0] in times_b[i]:
        times_b_tag[i] = '<stime>' + times_b[i] + '</stime>'

    if len(times) > 1:
      for i in range(0, len(times_b)):
        if times[1] in times_b[i]:
          times_b_tag[i] = '<etime>' + times_b[i] + '</etime>'

    # Put tagged times in body
    for i in range(0, len(times_b)):
      body = re.sub(times_b[i], times_b_tag[i], body)

  return Email(header, body, email.fileid)

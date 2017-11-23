import re

from nltk.corpus.reader import WordListCorpusReader
from os import listdir
from os.path import isfile, join
from mail import Email
from cleaner import clean

"""
Splits the raw text of all the emails read
into Email objects and returns a list of them

text: All the emails read, combined into one big string
fileids: The fileid of the emails, in order of reading
"""
def split_emails(text, fileids):
  emails = []
  reg_header = r'<.*?@.*?>\nType'
  headers = re.findall(reg_header, text)
  ind = 0

  for i in range(0, len(headers) - 1):
    start_h = text.find(headers[i])
    end_h = text.find('Abstract')
    header = text[start_h:end_h]

    start_b = end_h
    end_b = text.find(headers[i + 1])
    body = text[start_b:end_b]

    emails.append(Email(header.strip(), body.strip(), fileids[ind]))

    text = text[end_b:]
    ind += 1

  end_h = text.find('Abstract')
  header = text[:end_h]
  body = text[end_h:]
  emails.append(Email(header, body, fileids[ind]))

  return emails

"""
Reads the files and returns the name parsed into
Email objects
"""
def read_emails(path):
  files = [f for f in listdir(path) if isfile(join(path, f))]

  try:
    del(files[files.index('.DS_Store')])
  except:
    pass

  reader = WordListCorpusReader(path, files)

  text = clean(reader.raw())
  emails = split_emails(text, reader.fileids())

  return emails

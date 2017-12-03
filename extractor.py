import re
from cleaner import delete_tags

"""
Extracts all the tags in the text, and returns
a dictionary of arrays.

"""
def extract_tags(text):
  regex = {
      'time': r'<[s|e]time>.*?</[s|e]time>',
      'speaker': r'<speaker>.*?</speaker>',
      'location': r'<location>.*?</location>',
      'sentence': r'<sentence>.*?</sentence>',
      'paragraph': r'<paragraph>.*?</paragraph>'
  }

  tags = {}
  text = text.replace('\n','')

  for k in regex.keys():
    tags[k] = re.findall(regex[k], text, re.M)
    for i in range(0,len(tags[k])):
      tags[k][i] = delete_tags(tags[k][i])

  return tags

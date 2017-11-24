import re

def extract_tags(text):
  regex = {
      'time': r'<[s|e]time>.*?</[s|e]time>',
      'speaker': r'<speaker>.*?</speaker>',
      'paragraph': r'<paragraph>.*?</paragraph>',
      'sentence': r'<sentence>.*?</sentence>',
      'location': r'<location>.*?</location>'
  }

  tags = {}
  text = text.replace('\n','')

  for k in regex.keys():
    tags[k] = re.findall(regex[k], text, re.M)

  return tags

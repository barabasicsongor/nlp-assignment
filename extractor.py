import re

def times(text):
  return re.findall(r'<[s|e]time>.*?</[s|e]time>', text, re.M)

def speakers(text):
  return re.findall(r'<speaker>.*?</speaker>', text, re.M)

def paragraphs(text):
  return re.findall(r'<paragraph>.*?</paragraph>', text, re.M)

def sentences(text):
  return re.findall(r'<sentence>.*?</sentence>', text, re.M)

def locations(text):
  return re.findall(r'<location>.*?</location>', text, re.M)

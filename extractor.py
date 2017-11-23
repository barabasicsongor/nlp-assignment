import re

# Extracts all the <stime> and <etime> tags
def extract_times(text):
  return re.findall(r'<[s|e]time>.*?</[s|e]time>', text, re.M)

# Extracts all the <speaker> tags
def extract_speakers(text):
  return re.findall(r'<speaker>.*?</speaker>', text, re.M)

# Extracts all the <paragraph> tags
def extract_paragraphs(text):
  return re.findall(r'<paragraph>.*?</paragraph>', text, re.M)

# Extracts all the <sentence> tags
def extract_sentences(text):
  return re.findall(r'<sentence>.*?</sentence>', text, re.M)

# Extracts all the <location> tags
def extract_locations(text):
  return re.findall(r'<location>.*?</location>', text, re.M)

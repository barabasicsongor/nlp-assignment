import re
from nltk.corpus import stopwords

"""
Function to clean text from parts like
-------, *******, =======
"""
def clean(text):
  while(re.search(r'==*', text)):
    text = re.sub(r'==*', '', text, re.M)

  while(re.search(r'~~*', text)):
    text = re.sub(r'~~*', '', text, re.M)

  while(re.search(r'%%*', text)):
    text = re.sub(r'%%*', '', text, re.M)

  while(re.search(r'--*', text)):
    text = re.sub(r'--*', '', text, re.M)
  
  while(re.search(r'(<>)(<>)*', text)):
    text = re.sub(r'(<>)(<>)*', '', text, re.M)

  while(re.search(r'__*', text)):
    text = re.sub(r'__*', '', text, re.M)

  while(re.search(r'\*\**', text)):
    text = re.sub(r'\*\**', '', text, re.M)

  while(re.search(r'\|\|*', text)):
    text = re.sub(r'\|\|*', '', text, re.M)

  return text

"""
Deletes all the tags from the text
"""
def delete_tags(text):
  tags = [r'<[s|e]time>', r'</[s|e]time>', r'<speaker>', r'</speaker>', r'<paragraph>',
          r'</paragraph>', r'<sentence>', r'</sentence>', r'<location>', r'</location>']

  for t in tags:
    while(re.search(t, text)):
      text = re.sub(t, '', text, re.M)

  return text

"""
From a list of words removes the English stopwords
"""
def del_stopwords(words):
  without_stopwords = []
  stop_words = stopwords.words('english')

  for word in words:
        if word not in stop_words:
            without_stopwords.append(word)

  return without_stopwords

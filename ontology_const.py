import re
import math
from cleaner import delete_tags, del_stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob as tb

def tf(word, blob):
  return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
  return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
  return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
  return tf(word, blob) * idf(word, bloblist)

"""
Using the TF-IDF algorithm get the least frequent
words. Save them into a file for later usager
"""
def get_important_words(emails):

  text = ''
  for e in emails:
    e.header = delete_tags(e.header)
    e.body = delete_tags(e.body)

    line = re.findall(r'Topic.*\n', e.header)[0]
    line = line[6:].strip()

    text = text + line + '\n' + e.body + '\n'

  # Cleaning the text  
  text = re.sub('\n', ' ', text)
  text = re.sub('\s', ' ', text)

  text = text.lower()

  text = tb(text)
  bloblist = [text]

  file = open('./Data/less_freq_words.txt','w')

  for i, blob in enumerate(bloblist):
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print(len(sorted_words))
    for word, score in sorted_words:
      file.write('{}\n'.format(word))
      # print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

  file.close()

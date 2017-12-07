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
def get_important_words(emails,path=None):

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
  words = []

  for i, blob in enumerate(bloblist):
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words:
      words.append(word)
    words = del_stopwords(words)

    if path != None:
      file = open('./Data/less_freq_words.txt', 'w')
      for word in words:
        file.write('{}\n'.format(word))
        # print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
      file.close()
  
  return words

def get_words_from_email(email, my_words):
  words = []

  for w in my_words:
    if w in email.body:
      words.append(w)

  imp_words = get_important_words([email])
  imp_words = imp_words[(len(imp_words)-10):]
  words.extend(imp_words)

  return words

def classify_emails(model, emails):
  ontology = {
    'science': {
      'chemistry': [],
      'engineering': {
        'computer': {
          'vision': [],
          'robotics':[],
          'software': [],
          'interaction': []
        },
        'electronics': []
      },
      'mathematics': [],
      'biology': {
        'environment': [],
        'medicine': []
      },
      'physics': [],
      'psychology': []
    },
    'business': {
      'marketing': [],
      'career': {
        'graduate': [],
        'employment': []
      }
    }
  }

  file = open('./Data/less_freq_words.txt', 'r')
  my_words = file.readlines()
  my_words = [x.strip() for x in my_words]
  file.close()

  # Classifiy emails

  for e in emails:
    words = get_words_from_email(e, my_words)
    n_words = []

    for w in words:
      if w in model:
        n_words.append(w)
    
    words = n_words
    ontology_1 = ''
    MAX_SIM = float('-inf')
    for k in ontology.keys():
      if k in words:
        ontology_1 = k
        break
      else:
        similarity = model.n_similarity(words, [k])
        if similarity > MAX_SIM:
          MAX_SIM = similarity
          ontology_1 = k
    
    if type(ontology[ontology_1]) is list:
      ontology[ontology_1].append(e.fileid)
    else:
      ontology_2 = ''
      MAX_SIM = float('-inf')
      for k in ontology[ontology_1].keys():
        if k in words:
          ontology_2 = k
          break
        else:
          similarity = model.n_similarity(words, [k])
          if similarity > MAX_SIM:
            MAX_SIM = similarity
            ontology_2 = k

      if type(ontology[ontology_1][ontology_2]) is list:
        ontology[ontology_1][ontology_2].append(e.fileid)
      else:
        ontology_3 = ''
        MAX_SIM = float('-inf')
        for k in ontology[ontology_1][ontology_2].keys():
          if k in words:
            ontology_3 = k
            break
          else:  
            similarity = model.n_similarity(words, [k])
            if similarity > MAX_SIM:
              MAX_SIM = similarity
              ontology_3 = k
        
        if type(ontology[ontology_1][ontology_2][ontology_3]) is list:
          ontology[ontology_1][ontology_2][ontology_3].append(e.fileid)
        else:
          ontology_4 = ''
          MAX_SIM = float('-inf')
          for k in ontology[ontology_1][ontology_2][ontology_3].keys():
            if k in words:
              ontology_4 = k
              break
            else:
              similarity = model.n_similarity(words, [k])
              if similarity > MAX_SIM:
                MAX_SIM = similarity
                ontology_4 = k
          
          ontology[ontology_1][ontology_2][ontology_3][ontology_4].append(e.fileid)

  return ontology

import os
import re
from nltk.stem.snowball import SnowballStemmer
from nltk import conlltags2tree

stemmer = SnowballStemmer('english')

def to_conll_iob(annotated_sentence):
  """
  annotated_sentence = list of triplets [(w1, t1, iob1) ...]
  Transform a pseudo-IOB notation: O, PERSON, PERSON, O, O, LOCATION, O
  to proper IOB notation: O, B-PERSON, I-PERSON, O, O, B-LOCATION, O
  """
  proper_iob_tokens = []
  for idx, annotated_token in enumerate(annotated_sentence):
    tag, word, ner = annotated_token

    if ner != 'O':
      if idx == 0:
        ner = 'B-' + ner
      elif annotated_sentence[idx-1][2] == ner:
        ner = 'I-' + ner
      else:
        ner = 'B-' + ner
    proper_iob_tokens.append((tag,word,ner))
  
  return proper_iob_tokens

def read_gmb_ner(path):
  for root, dirs, files in os.walk(path):
    for filename in files:
      if filename.endswith('.tags'):
        with open(os.path.join(root,filename), 'rb') as file_handle:
          file_content = file_handle.read().decode('utf-8').strip()
          annotated_sentences = file_content.split('\n\n')
          for annotated_sentence in annotated_sentences:
            annotated_tokens = [seq for seq in annotated_sentence.split('\n') if seq]

            standard_form_tokens = []

            for idx, annotated_token in enumerate(annotated_tokens):
              annotations = annotated_token.split('\t')
              word, tag, ner = annotations[0], annotations[1], annotations[3]

              if ner != '0':
                ner = ner.split('-')[0]
              
              standard_form_tokens.append((word,tag,ner))
            
            conll_tokens = to_conll_iob(standard_form_tokens)
            yield conlltags2tree(conll_tokens)


def shape(word):
  word_shape = 'other'
  if re.match('[0-9]+(\.[0-9]*)?|[0-9]*\.[0-9]+$', word):
    word_shape = 'number'
  elif re.match('\W+$', word):
    word_shape = 'punct'
  elif re.match('[A-Z][a-z]+$', word):
    word_shape = 'capitalized'
  elif re.match('[A-Z]+$', word):
    word_shape = 'uppercase'
  elif re.match('[a-z]+$', word):
    word_shape = 'lowercase'
  elif re.match('[A-Z][a-z]+[A-Z][a-z]+[A-Za-z]*$', word):
    word_shape = 'camelcase'
  elif re.match('[A-Za-z]+$', word):
    word_shape = 'mixedcase'
  elif re.match('__.+__$', word):
    word_shape = 'wildcard'
  elif re.match('[A-Za-z0-9]+\.$', word):
    word_shape = 'ending-dot'
  elif re.match('[A-Za-z0-9]+\.[A-Za-z0-9\.]+\.$', word):
    word_shape = 'abbreviation'
  elif re.match('[A-Za-z0-9]+\-[A-Za-z0-9\-]+.*$', word):
    word_shape = 'contains-hyphen'

  return word_shape


def ner_features(tokens, index, history):
  """
  tokens  = a POS-tagged sentence [(w1,t1) ...]
  index   = the index of the token we want to extract features for
  history = the previous predicted IOB tag
  """

  # Pad the sequence with placeholders
  tokens = [('__START2__', '__START2__'), ('__START1__', '__START1__')] + list(tokens) + [('__END1__', '__END1__'), ('__END2__', '__END2__')]
  history = ['__START2__', '__START1__'] + list(history)

  # shift the index with 2, to accomodate the padding
  index += 2

  word, pos = tokens[index]
  prevword, prevpos = tokens[index - 1]
  prevprevword, prevprevpos = tokens[index - 2]
  nextword, nextpos = tokens[index + 1]
  nextnextword, nextnextpos = tokens[index + 2]
  previob = history[-1]
  prevpreviob = history[-2]

  feat_dict = {
      'word': word,
      'lemma': stemmer.stem(word),
      'pos': pos,
      'shape': shape(word),

      'next-word': nextword,
      'next-pos': nextpos,
      'next-lemma': stemmer.stem(nextword),
      'next-shape': shape(nextword),

      'next-next-word': nextnextword,
      'next-next-pos': nextnextpos,
      'next-next-lemma': stemmer.stem(nextnextword),
      'next-next-shape': shape(nextnextword),

      'prev-word': prevword,
      'prev-pos': prevpos,
      'prev-lemma': stemmer.stem(prevword),
      'prev-iob': previob,
      'prev-shape': shape(prevword),

      'prev-prev-word': prevprevword,
      'prev-prev-pos': prevprevpos,
      'prev-prev-lemma': stemmer.stem(prevprevword),
      'prev-prev-iob': prevpreviob,
      'prev-prev-shape': shape(prevprevword)
  }

  return feat_dict

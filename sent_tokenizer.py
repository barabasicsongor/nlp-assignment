from nltk.corpus import gutenberg
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer

"""
Train custom sentence tokenizer on gutenberg corpus
"""
def train_sent_tokenizer():
  text = gutenberg.raw()
  trainer = PunktTrainer()
  trainer.INCLUDE_ALL_COLLOCS = True
  trainer.train(text)

  # Adding abbreviations which need to be detected manually
  tokenizer._params.abbrev_types.add('dr')

  return PunktSentenceTokenizer(trainer.get_params())

"""
Splits a text into sentences and returns a list of them
"""
def tokenize_sents(text, tokenizer=None):
  if tokenizer == None:
    tokenizer = train_sent_tokenizer()

  return tokenizer.tokenize(text)
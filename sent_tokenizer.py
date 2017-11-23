from nltk.corpus import gutenberg
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer

def train_sent_tokenizer(text):
  trainer = PunktTrainer()
  trainer.INCLUDE_ALL_COLLOCS = True
  trainer.train(text)

  # Adding abbreviations which need to be detected manually
  tokenizer._params.abbrev_types.add('dr')

  return PunktSentenceTokenizer(trainer.get_params())

def sent_tokenizer(tokenizer, text):
  return tokenizer.tokenize(text)
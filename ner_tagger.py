import itertools
import pickle

from nltk import tree2conlltags, conlltags2tree
from nltk.chunk import ChunkParserI
from sklearn.linear_model import Perceptron
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

class ScikitLearnChunker(ChunkParserI):

  def __init__(self, feature_detector, classifier=None):
    self._classifier = classifier
    self._feature_detector = feature_detector


  def to_dataset(self, parsed_sentences):
    """
    Transform a list of tagged sentences into a scikit-learn compatible POS dataset
    """
  
    X, y = [], []
    for parsed in parsed_sentences:
      iob_tagged = tree2conlltags(parsed)
      words, tags, iob_tags = zip(*iob_tagged)
    
      tagged = list(zip(words, tags))
    
      for index in range(len(iob_tagged)):
        X.append(self._feature_detector(tagged, index, history=iob_tags[:index]))
        y.append(iob_tags[index])
      
    return X, y

  def get_minibatch(self, parsed_sentences, batch_size=500):
    batch = list(itertools.islice(parsed_sentences, batch_size))
    X, y = self.to_dataset(batch)

    return X, y

  def train(self, parsed_sentences, save, path=None, **kwargs):
    all_classes = ['O', 'B-per', 'I-per', 'B-gpe', 'I-gpe',
                   'B-geo', 'I-geo', 'B-org', 'I-org', 'B-tim', 'I-tim',
                   'B-art', 'I-art', 'B-eve', 'I-eve', 'B-nat', 'I-nat']

    X, y = self.get_minibatch(parsed_sentences, kwargs.get('batch_size', 500))
    vectorizer = DictVectorizer(sparse=False)
    vectorizer.fit(X)

    clf = Perceptron(verbose=10, n_jobs=-1, n_iter=kwargs.get('n_iter', 5))

    while len(X):
      X = vectorizer.transform(X)
      clf.partial_fit(X, y, all_classes)
      X, y = self.get_minibatch(parsed_sentences, kwargs.get('batch_size', 500))

    clf = Pipeline([
      ('vectorizer', vectorizer),
      ('classifier', clf)
    ])

    if save:
      model_pkl = open(path, 'wb')
      pickle.dump(clf, model_pkl)
      model_pkl.close()

    self._classifier = clf

    return clf

  """
  Loads the NER tagger classifier from file
  """
  def load_ner_tagger(self, path):
    model_pkl = open(path, 'rb')
    clf = pickle.load(model_pkl)
    self._classifier = clf
    return clf

  def parse(self, tokens):
    """
    Chunk a tagged sentence
    tokens = list of words [(w1,t1) ...]
    return: chunked sentence nltk.Tree
    """
    history = []
    iob_tagged_tokens = []
    for index, (word, tag) in enumerate(tokens):
      iob_tag = self._classifier.predict([self._feature_detector(tokens, index, history)])[0]
      history.append(iob_tag)
      iob_tagged_tokens.append((word, tag, iob_tag))
    
    return conlltags2tree(iob_tagged_tokens)

  def score(self, parsed_sentences):
    """
    Compute the accuracy of the tagger for a list of test sentences
    parsed_senteces = list of nltk.Tree
    return: float 0.0 - 1.0
    """
    X_test, y_test = self.to_dataset(parsed_sentences)
    return self._classifier.score(X_test, y_test)

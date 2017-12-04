import nltk
import pickle
from nltk.corpus import treebank
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

POS_TAGGER_PATH = './Data/models/pos_tagger_dt.pkl'

class POSTagger:

  def __init__(self):
    self.classifier = None

  """
  Features of a word used for classification
  with the Decision Tree.

  sentence: [word1, word2, ...], 
  index: the index of the word 
  """
  def word_features(self,sentence, index):
    return {
      'word': sentence[index],
      'is_first': index == 0,
      'is_last': index == len(sentence) - 1,
      'is_capitalized': sentence[index][0].upper() == sentence[index][0],
      'is_all_caps': sentence[index].upper() == sentence[index],
      'is_all_lower': sentence[index].lower() == sentence[index],
      'prefix-1': sentence[index][0],
      'prefix-2': sentence[index][:2],
      'prefix-3': sentence[index][:3],
      'suffix-1': sentence[index][-1],
      'suffix-2': sentence[index][-2:],
      'suffix-3': sentence[index][-3:],
      'prev_word': '' if index == 0 else sentence[index - 1],
      'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
      'has_hyphen': '-' in sentence[index],
      'is_numeric': sentence[index].isdigit(),
      'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
    }

  """
  Untags a sentence by extracting the words from the 
  list of tuples (word, tag)
  """
  def untag(self,tagged_sent):
    return [w for w, t in tagged_sent]

  """
  Transforms the training tagged sentences to dataset format
  X: list of word features
  y: expected POS tag
  """
  def transform_to_dataset(self,tagged_sents):
    X, y = [], []

    for tagged in tagged_sents:
      untagged = untag(tagged)

      for index in range(len(tagged)):
        X.append(word_features(untagged, index))
        y.append(tagged[index][1])

    return X, y

  """
  Loads the POS tag classifier from file
  """
  def load_pos_tagger(self):
    model_pkl = open(POS_TAGGER_PATH, 'rb')
    clf = pickle.load(model_pkl)
    self.classifier = clf

  """
  Trains the POS tag classifier on the treebank corpus 
  and returns it.
  If save == True, then the classifier is saved to file
  """
  def train_pos_tagger(self,save):
    tagged_sents = treebank.tagged_sents()

    train_size = int(.75 * len(tagged_sents))
    training_sents = tagged_sents[:train_size]
    test_sents = tagged_sents[train_size:]

    X, y = transform_to_dataset(training_sents)

    clf = Pipeline([
      ('vectorizer', DictVectorizer(sparse=False)),
      ('classifier', DecisionTreeClassifier(criterion="entropy"))
    ])

    print('Training started')
    clf.fit(X, y)
    print('Training finished')

    X_test, y_test = transform_to_dataset(test_sents)
    print('Accuracy: {}'.format(clf.score(X_test, y_test)))

    # Save model to file
    if save:
      model_pkl = open(POS_TAGGER_PATH, 'wb')
      pickle.dump(clf, model_pkl)
      model_pkl.close()

    self.classifier = clf

    return clf

  def predict(self,sentence):
    tagged_sentence = []
    tags = self.classifier.predict([self.word_features(sentence, index) for index in range(len(sentence))])

    return zip(sentence, tags)

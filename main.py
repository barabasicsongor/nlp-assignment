import itertools
from io_manager import read_emails
from mail import Email
from pos_tagger import POSTagger
from ner_tagger import NERTagger
from ner_tagger_io import ner_features, read_gmb_ner
from cleaner import delete_tags
from time_tagger import tag_time
from speaker_tagger import tag_speaker
from location_tagger import tag_location
from sent_tagger import tag_sents
from paragraph_tagger import tag_paragraphs
from eval import evaluate, calculateScore
from extractor import extract_tags

if __name__ == '__main__':
  EMAILS_TRAIN_PATH         = './Data/training/'
  EMAILS_TEST_TAGGED_PATH   = './Data/seminar_testdata/test_tagged/'
  EMAILS_TEST_UNTAGGED_PATH = './Data/seminar_testdata/test_untagged/'
  GMB_CORPUS_ROOT           = './Data/gmb-2.2.0'
  NER_TAGGER_PATH           = './Data/models/ner_tagger.pkl'
  POS_TAGGER_PATH           = './Data/models/pos_tagger_dt.pkl'

  # Read emails
  emails_train         = read_emails(EMAILS_TRAIN_PATH)
  emails_test_tagged   = read_emails(EMAILS_TEST_TAGGED_PATH)
  emails_test_untagged = read_emails(EMAILS_TEST_UNTAGGED_PATH)

  # POSTagger usage. Train it or wait for it to load from disk
  pos = POSTagger()
  # pos.train_pos_tagger(POS_TAGGER_PATH)
  pos.load_pos_tagger(POS_TAGGER_PATH)

  # NERTagger usage. Train it or wait for it to load from disk
  # You must have the GMB dataset in the Data folder to be able to train
  ner_dataset = read_gmb_ner(GMB_CORPUS_ROOT)
  ner = NERTagger(feature_detector=ner_features)
  # ner.train(itertools.islice(ner_dataset, 50000), path='./Data/models/ner_tagger.pkl', batch_size=500, n_iter=5)
  ner.load_ner_tagger(NER_TAGGER_PATH)
  # accuracy = ner.score(itertools.islice(ner_dataset, 5000))  # 0.970287054168
  # print(accuracy)

  # Testing of tagging

  # Tag the untagged testing emails
  for i in range(0,len(emails_test_untagged)):
    emails_test_untagged[i] = tag_paragraphs(tag_sents(tag_location(tag_time(tag_speaker(emails_test_untagged[i], POS_TAGGER_PATH,NER_TAGGER_PATH)))))

  # Evaluate the tagging algorithm
  # If you want to calculate on specific tags
  # go to eval.py and see comments in function
  tp, fp, fn = 0, 0, 0

  for e in emails_test_tagged:
    gr_email = e
    pred_email = None

    for em in emails_test_untagged:
      if em.fileid == e.fileid:
        pred_email = em
        break
    
    ntp, nfp, nfn = evaluate(gr_email, pred_email)
    tp = tp + ntp
    fp = fp + nfp
    fn = fn + nfn

  precision, recall, fscore = calculateScore(tp, fp, fn)



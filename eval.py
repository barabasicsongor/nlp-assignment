import re
from extractor import extract_tags

"""
gr: the list of correct tags - ground truth
pred: predicted tags
return: (precision, recall, f1)
"""
def evaluate(gr_email, pred_email):

  gr_tags = extract_tags(gr_email.header + gr_email.body)
  pred_tags = extract_tags(pred_email.header + pred_email.body)

  tp = 0
  fp = 0
  fn = 0

  # change gr_tags.keys() to ['key'] to evaluate a specific tag
  for k in gr_tags.keys():
    gr = gr_tags[k]
    pred = pred_tags[k]
  
    # removing all punctuations and spaces
    for i in range(0,len(gr)):
      gr[i] = re.sub(r'[^\w\s]','',gr[i])
      gr[i] = re.sub(' ','',gr[i])

    for i in range(0, len(pred)):
      pred[i] = re.sub(r'[^\w\s]', '', pred[i])
      pred[i] = re.sub(' ', '', pred[i])

    # Calculating TP, FP, FN
    for t in gr:
      if t in pred:
        tp = tp + 1
        pred.remove(t)
      else:
        fn = fn + 1

    fp = fp + len(pred)

  return tp, fp, fn

def calculateScore(tp, fp, fn):
  precision = float(tp / (tp + fp))
  recall = float(tp / (tp + fn))
  fscore = float((2 * precision * recall) / (precision + recall))

  return (precision, recall, fscore)

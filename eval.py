import re
"""
gr: the list of correct tags - ground truth
pred: predicted tags
return: (precision, recall, f1)
"""
def evaluate(gr, pred):
  
  # removing all punctuations and spaces
  for i in range(0,len(gr)):
    gr[i] = re.sub(r'[^\w\s]','',gr[i])
    gr[i] = re.sub(' ','',gr[i])

  for i in range(0, len(pred)):
    pred[i] = re.sub(r'[^\w\s]', '', pred[i])
    pred[i] = re.sub(' ', '', pred[i])

  # Calculating TP, TN, FP, FN

  tp = 0
  tn = 0
  fp = 0
  fn = 0

  for t in gr:
    if t in pred:
      tp = tp + 1
      pred.remove(t)
    else:
      fn = fn + 1

  fp = len(pred)

  precision = float(tp/(tp+fp))
  recall = float(tp/(tp+fn))
  fscore = float((2*precision*recall)/(precision+recall))

  return (precision, recall, fscore)

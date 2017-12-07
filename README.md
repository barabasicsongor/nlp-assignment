Report of the system can be found in the documents folder, separately for part 1 and 2. There is also a file showing the result of the ontology classification in case you don't want to run it.

Run main.py in order to run the application.

All the code to run the full system is in the main file, but some of them are commented, because there are certain datasets that are needed in order to run properly.

1. In case you want to see the POS tagger training, the line which is doing the training in the main is commented, because it takes lots of time to train. But it is saved to disk, so it will be loaded from there, pre-trained.

2. In case you want to see the NER tagger training, it doesn't take much time, but you need the GMB dataset placed in the Data folder. You can download it from here: http://gmb.let.rug.nl/data.php. Version 2.2.0 is needed. But this is also saved to disk, so it will load properly from disk, pre-trained.

3. Tagging algorithm work. As output you will get the precision, recall and F1-Score of the algorithm.

4. In case you want to see the ontology classification running, uncomment the last 4 lines of the main file and make sure you have the GoogleNews dataset in the Data folder (or change the path) so the word2vec model is able to train.

Thank you, and have fun! :D
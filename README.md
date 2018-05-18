# Naive-Bayes-Classifier
Naive Bayes classifier to identify hotel reviews as either true or fake, and either positive or negative.

# Overview
Naive Bayes classifier to identify hotel reviews as either true or fake, and either positive or negative, using the word tokens as features for classification.

# Data
One file train-labeled.txt containing labeled training data with a single training instance (hotel review) per line (total 960 lines). The first 3 tokens in each line are:
  a)a unique 7-character alphanumeric identifier
  b)a label True or Fake
  c)a label Pos or Neg
These are followed by the text of the review.
One file dev-text.txt with unlabeled development data, containing just the unique identifier followed by the text of the review (total 320 lines).
One file dev-key.txt with the corresponding labels for the development data, to serve as an answer key.

# Programs
There are two programs: nblearn.py will learn a naive Bayes model from the training data, and nbclassify.py will use the model to classify new data:

> python nblearn.py train-labeled.txt

The argument is a single file containing the training data; the program will learn a naive Bayes model, and write the model parameters to a file called nbmodel.txt. 
The model file contains sufficient information for nbclassify.py to successfully label new data.

The classification program will be invoked in the following way:

> python nbclassify.py dev-text.txt

The argument is a single file containing the test data file; the program will read the parameters of a naive Bayes model from the file nbmodel.txt, classify each entry in the test data, and write the results to a text file called nboutput.txt in the same format as the answer key.

# Results on test data
Results:
Neg 0.93 0.97 0.95
True 0.88 0.86 0.87
Pos 0.97 0.93 0.95
Fake 0.87 0.89 0.88
Mean F1: 0.9125



import sys
import json
import codecs
import string
import re
from collections import Counter
from decimal import Decimal
import ast
import cPickle as pickle
import math


fw = codecs.open("nboutput.txt", 'w', 'utf-8')

def classify(data, probability):

    probTrue = Decimal(probability["TRUE"])
    probFake = Decimal(probability["FALSE"])
    probNeg = Decimal(probability["NEG"])
    probPos = Decimal(probability["POS"])
    #print probability["TRUEPOS"][words[1]]

    stopWords = []

    stopWords.append("i")
    stopWords.extend(
        ("me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "he", "him"))
    stopWords.extend(("his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they"))
    stopWords.extend(
        ("them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those"))
    stopWords.extend(
        ("am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did"))
    stopWords.extend((
                     "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at",
                     "by", "for"))
    stopWords.extend(("with", "about", "against", "between", "into", "through", "during", "before", "after", "above",
                      "below", "to", "from"))
    stopWords.extend(("up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once",
                      "here", "there", "when", "where"))
   # stopWords.extend(("why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no",
   #                   "not", "only", "own", "same"))
    stopWords.extend(("so", "than", "too", "very", "can", "will", "just", "should", "now"))



    line = data

    #line = line.replace("'", "")
    #line = line.replace("-", "")

    #for p in string.punctuation:
        #line = line.replace(p, ' ')
    words = line.split(" ")
    for word in words:
        wordLower = word.lower()
        puncChar = set(string.punctuation)
        wordNew = ''.join(ch for ch in wordLower if ch not in puncChar)
        #wordNew = wordLower
        if wordNew in stopWords:
            continue

        if wordNew in probability["TRUEWORDS"]:
            probTrue += Decimal(probability["TRUEWORDS"][wordNew])

        if wordNew in probability["FAKEWORDS"]:
            probFake += Decimal(probability["FAKEWORDS"][wordNew])

        if wordNew in probability["NEGWORDS"]:
            probNeg += Decimal(probability["NEGWORDS"][wordNew])

        if wordNew in probability["POSWORDS"]:
            probPos += Decimal(probability["POSWORDS"][wordNew])

    fw.write(words[0])
    fw.write(" ")
    if probFake > probTrue:
        fw.write("Fake")
    else:
        fw.write("True")
    fw.write(" ")
    if probNeg > probPos:
        fw.write("Neg")
    else:
        fw.write("Pos")
    fw.write("\n")


def main():
    fp = codecs.open("nbmodel.txt", 'r', 'utf-8')
    json_contents = fp.read()
    probability = json.loads(json_contents)
    fp.close()

    fd = codecs.open(sys.argv[1], 'r', "utf-8")
    lines = fd.read().splitlines()
    #c = 1
    #print  math.log(probability["TRUE"])
    for line in lines:
        classify(line, probability)

    fw.close()

main()


import sys
import json
import codecs
import string
import re
from collections import Counter
from decimal import Decimal
import cPickle as pickle
import math

fp = codecs.open(sys.argv[1], 'r', "utf-8")
lines = fp.read().splitlines()
fp.close()

#fw = codecs.open('nbmodel.txt', 'w', "utf-8")
fw = codecs.open('nbmodel.txt', 'w', 'utf-8')


total = 0

#print  uniquewords
trueWords = []
fakeWords = []
negWords = []
posWords = []
allWords = []

stopWords = []
stopWords.append("i")
stopWords.extend(("me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "he", "him"))
stopWords.extend(("his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they"))
stopWords.extend(("them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those"))
stopWords.extend(("am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did"))
stopWords.extend(("doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for"))
stopWords.extend(("with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from"))
stopWords.extend(("up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where"))
#stopWords.extend(("why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "not", "only", "own", "same"))
stopWords.extend(("so", "than", "too", "very", "can", "will", "just", "should", "now"))
#stopWords.extend(('the', 'for', 'had', 'and', 'to', 'a', 'was', 'in', 'of', 'you', 'is', 'it', 'at', 'with', 'they', 'on', 'our', 'be', 'as', 'there', 'an', 'or', 'this','my', 'that' ))


for line in lines:
    #line = line.replace("'", "")
    #line = line.replace("-","")

    #for p in string.punctuation:
        #line = line.replace(p, ' ')
    words = line.split(" ")


    for word in words:
        wordLower = word.lower()
        #wordFinal = wordLower

        puncChar = set(string.punctuation)
        wordFinal = ''.join(ch for ch in wordLower if ch not in puncChar)
        #for p in string.punctuation:
            #wordFinal = wordLower.replace(p, ' ')
        if wordFinal in stopWords:
            continue
        if words[1] == "True":
            trueWords.append(wordFinal)

        if words[1] == "Fake":
            fakeWords.append(wordFinal)

        if words[2] == "Pos":
            posWords.append(wordFinal)

        if words[2] == "Neg":
            negWords.append(wordFinal)

        allWords.append(wordFinal)


counterTrues = {}
counterFakes = {}
counterNegs = {}
counterPos = {}


counterTrues = Counter(trueWords)
counterFakes = Counter(fakeWords)
counterNegs = Counter(negWords)
counterPos = Counter(posWords)
counterAll = Counter(allWords)
vocablen = len(counterAll.keys())


totalTrue = 0
totalFake = 0
totalPos = 0
totalNeg = 0

for t in counterTrues:
    totalTrue += counterTrues[t]

for f in counterFakes:
    totalFake += counterFakes[f]

for p in counterPos:
    totalPos += counterPos[p]

for n in counterNegs:
    totalNeg += counterNegs[n]

allCount = totalTrue + totalFake
probT = {}
probF = {}
probP = {}
probN = {}

priorT = math.log(totalTrue) - math.log(allCount)
priorF = math.log(totalFake) - math.log(allCount)
priorN = math.log(totalNeg) - math.log(allCount)
priorP = math.log(totalPos) - math.log(allCount)

for w in counterAll:
    if w in counterTrues:
        probT[w] = math.log(counterTrues[w] + 1) - math.log(totalTrue + vocablen)
    else:
        probT[w] = math.log(1) - math.log(totalTrue + vocablen)
    if w in counterFakes:
        probF[w] = math.log(counterFakes[w] + 1) - math.log(totalFake + vocablen)
    else:
        probF[w] = math.log(1) - math.log(totalFake + vocablen)

    if w in counterPos:
        probP[w] = math.log(counterPos[w] + 1) - math.log(totalPos + vocablen)
    else:
        probP[w] = math.log(1) - math.log(totalPos + vocablen)
    if w in counterNegs:
        probN[w] = math.log(counterNegs[w] + 1) - math.log(totalNeg + vocablen)
    else:
        probN[w] = math.log(1) - math.log(totalNeg + vocablen)


'''myobj = {}

myobj["TRUE"] = priorT
myobj["FALSE"] = priorF
myobj["NEG"] = priorN
myobj["POS"] = priorP
myobj["TRUEWORDS"] = probT
myobj["FAKEWORDS"] = probF
myobj["POSWORDS"] = probP
myobj["NEGWORDS"] = probN

#myobj[]
strobj = ""
for key, val in myobj.iteritems():
    strobj = strobj + key + str(val)
#print  strobj'''

myobj = json.dumps({'TRUE': priorT, 'FALSE': priorF, 'NEG': priorN, 'POS': priorP, 'TRUEWORDS': probT, 'FAKEWORDS': probF, 'POSWORDS': probP, 'NEGWORDS': probN})
fw.write((myobj))
fw.close()


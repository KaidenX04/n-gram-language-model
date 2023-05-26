from nltk.corpus import twitter_samples
from nltk import trigrams, bigrams
from nltk.tokenize import word_tokenize
from collections import Counter, defaultdict
import random

model = defaultdict(lambda: defaultdict(lambda: 0))

for sentence in twitter_samples.strings():
    words = word_tokenize(sentence)
    for w1, w2, w3 in trigrams(words, pad_right=True, pad_left=True):
        model[(w1, w2)][w3] += 1

for w1_w2 in model:
    total_count = float(sum(model[w1_w2].values()))
    for w3 in model[w1_w2]:
        model[(w1_w2)][w3] /= total_count

inputText = input("\nPlease enter a prompt to start generating: ")
rInput = float(input("\nPlease enter a preferred accuracy for words 0-1: "))
minAccuracy = float(input("\nPlease enter a minimum accuracy for words 0-1: "))
text = inputText.split(" ")
sentence_finished = False
wordLimit = 50
wordcount = 0
reverseCount = 4
reverseCounter = 0
wordCounter = 0

while not sentence_finished:
    r = rInput
    accumulator = .0
    wordFound = False

    while (wordFound == False):
        for word in model[tuple(text[-2:])].keys():
            accumulator = model[tuple(text[-2:])][word]
            selectRandom = random.randint(0, 2)
            if accumulator >= r and selectRandom > 0:
                text.append(word)
                print(word)
                print(wordcount)
                wordcount += 1
                wordFound = True
                wordCounter += 1
        r -= 0.10
        if (r == minAccuracy):
            sentence_finished = True

    if wordcount >= wordLimit:
        sentence_finished = True

    if text[-2:] == [None, None]:
        if (len(text) < reverseCount):
            reverseCount = 2
        text = text[:-reverseCount]
        wordcount -= reverseCount
        reversed = True
        reverseCounter += 1
        wordCounter = 0

    if reverseCounter == 4:
        reverseCount += 2
        reverseCounter = 0

    if wordCounter == reverseCount:
        reverseCount == 4

print (' '.join([t for t in text if t]))
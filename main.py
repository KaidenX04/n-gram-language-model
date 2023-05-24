from nltk.corpus import twitter_samples
from nltk import trigrams, bigrams
from nltk.tokenize import word_tokenize
from collections import Counter, defaultdict
import random

# Create the datastructure to store the model
model = defaultdict(lambda: defaultdict(lambda: 0))

# Count the amount of times a certain word is found after 2 other words
for sentence in twitter_samples.strings("tweets.20150430-223406.json"):
    words = word_tokenize(sentence)
    for w1, w2, w3 in trigrams(words, pad_right=True, pad_left=True):
        model[(w1, w2)][w3] += 1

# Turn the count into a probability
for w1_w2 in model:
    # Add together the counts from all the w3s within the w1_w2
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

while not sentence_finished:
    # select a random probability threshold 
    r = rInput
    accumulator = .0
    wordFound = False

    while (wordFound == False):
        for word in model[tuple(text[-2:])].keys():
            accumulator = model[tuple(text[-2:])][word]
            # select words that are above the probability threshold
            selectRandom = random.randint(0, 2)
            if accumulator >= r and selectRandom > 0:
                text.append(word)
                wordcount += 1
                wordFound = True
        r -= 0.10
        if (r == minAccuracy):
            sentence_finished = True

    if wordcount >= wordLimit:
        sentence_finished = True
#   for word in model[tuple(text[-2:])].keys():
#       accumulator += model[tuple(text[-2:])][word]
#       # select words that are above the probability threshold
#       if accumulator >= r:
#           text.append(word)
#           break

    if text[-2:] == [None, None]:
        sentence_finished = True
 
print (' '.join([t for t in text if t]))
import re
from collections import defaultdict
import random

two_word_titles = []
firsts = set()
lasts = set()

with open('simplewiki-20190101-all-titles-in-ns0') as titles:
    for title in titles.readlines():
        title = title.strip().lower()
        if (re.search(r'^[a-z]+_[a-z]+$', title)):
            two_word_titles.append(title)
            [first, last] = title.split('_')
            firsts.add(first)
            lasts.add(last)

boths = firsts & lasts
linking_titles = []
for title in two_word_titles:
    [first, last] = title.split('_')
    if first in boths and last in boths:
        linking_titles.append(title)

print('building child index...')

index_1 = defaultdict(set)
for title in linking_titles:
    [word, child] = title.split('_')
    index_1[word].add(child)

seen = set()

def tree(word, depth):
    if word in seen and depth > 0:
        print(word)
    else:
        print(word, end=' ')
        seen.add(word)
        for child in index_1[word]:
            tree(child, depth+1)

words = list(boths)
random.shuffle(words)
for word in words:
    tree(word, 0)
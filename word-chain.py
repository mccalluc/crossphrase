import re
from collections import defaultdict

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

print('building grandchild index...')

index_2 = defaultdict(set)
for (word, children) in index_1.items():
    for child in children:
        if child in index_1:
            for grandchild in index_1[child]:
                index_2[word].add(grandchild)

print('scanning index...')

loops = defaultdict(set)
for (word, grandchildren) in index_2.items():
    for grandchild in grandchildren:
        if grandchild in index_2:
            if word in index_2[grandchild] and word != grandchild:
                loops[word].add(grandchild)

for (word, grandchildren) in loops.items():
    for child in index_1[word]:
        for grandchild in index_1[child]:
            if grandchild in grandchildren:
                for ggrandchild in index_1[grandchild]:
                    if child != ggrandchild:
                        if word in index_1[ggrandchild]:
                            starts_with = min(word, child, grandchild, ggrandchild)
                            if word == starts_with:
                                print('{} -> {} -> {} -> {} -> {}'.format(word, child, grandchild, ggrandchild, word))

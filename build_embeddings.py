from __future__ import print_function
import numpy as np


def loadGlove(maxcnt=50000, path="./data/glove.42B.300d.txt"):
    m = 300
    print ("  Loading embeddings...")
    with open(path) as fi:
        cnt = 0
        d = {}
        for line in fi:
            if cnt > 0 and cnt > maxcnt:
                break
            cnt += 1
            lst = line.split(" ")
            w = lst[0]
            v = np.array(lst[1:], dtype=float)
            d[w] = v

    arr = np.ndarray([len(d),m])
    word_to_idx = {}
    for (i,kv) in enumerate(d.items()):
        word_to_idx[kv.first()] = i
        arr[i] = kv.second()

    if 'unk' not in word_to_idx:
        print (" WARNING: unk is not in the vocab !!!")

    print ("  ...Done loading embeddings (%d)"%len(d))

    return (word_to_idx,arr)


def build_embeddings():
    return loadGlove()

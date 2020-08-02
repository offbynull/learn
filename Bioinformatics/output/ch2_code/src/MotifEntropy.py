from collections import Counter
from typing import List

from Entropy import calculate_entropy


# According to the book, method of scoring a motif matrix as defined in ScoreMotif.py isn't the method used in the
# real-world. The method used in the real-world is this method, where...
# 1. each column has its probability distribution calculated (prob of A vs prob C vs prob of T vs prob of G)
# 2. the entropy of each of those prob dist are calculated
# 3. those entropies are summed up to get the ENTROPY OF THE MOTIF MATRIX
def motify_entropy(motif_matrix: List[str]) -> float:
    rows = len(motif_matrix)
    cols = len(motif_matrix[0])

    # count up each column
    counter_per_col = []
    for c in range(0, cols):
        counter = Counter()
        for r in range(0, rows):
            counter[motif_matrix[r][c]] += 1
        counter_per_col.append(counter)

    # counts to prob dist
    prob_dist_per_col = []
    for counter in counter_per_col:
        prob_dist = {
            'a': counter['a'] / rows,
            'c': counter['c'] / rows,
            't': counter['t'] / rows,
            'g': counter['g'] / rows
        }
        prob_dist_per_col.append(prob_dist)

    # prob dist to entropy
    entropy_per_col = []
    for prob_dist in prob_dist_per_col:
        entropy = calculate_entropy([prob_dist['a'], prob_dist['c'], prob_dist['g'], prob_dist['t']])
        entropy_per_col.append(entropy)

    # sum up entropies to get entropy of motif
    return sum(entropy_per_col)


if __name__ == '__main__':
    entropy = motify_entropy([
        'TCGGGGgTTTtt'.lower(),
        'cCGGtGAcTTaC'.lower(),
        'aCGGGGATTTtC'.lower(),
        'TtGGGGAcTTtt'.lower(),
        'aaGGGGAcTTCC'.lower(),
        'TtGGGGAcTTCC'.lower(),
        'TCGGGGATTcat'.lower(),
        'TCGGGGATTcCt'.lower(),
        'TaGGGGAacTaC'.lower(),
        'TCGGGtATaaCC'.lower()
    ])

    print(f'{entropy}')
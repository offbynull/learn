from collections import Counter
from typing import List, Dict


# For each column in a motif matrix, count up how many times each nucleotide appears.
def motif_matrix_count(motif_matrix: List[str], elements='ACGT') -> Dict[str, List[int]]:
    rows = len(motif_matrix)
    cols = len(motif_matrix[0])

    ret = {}
    for ch in elements:
        ret[ch] = [0] * cols
    
    for c in range(0, cols):
        for r in range(0, rows):
            item = motif_matrix[r][c]
            ret[item][c] += 1
            
    return ret


if __name__ == '__main__':
    counts = motif_matrix_count([
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

    print(f'{counts}')

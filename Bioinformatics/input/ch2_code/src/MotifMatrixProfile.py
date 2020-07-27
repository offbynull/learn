from collections import Counter
from typing import List, Dict


# For each column in a motif matrix, count up how many times each nucleotide appears.
from MotifMatrixCount import motif_matrix_count


def motif_matrix_profile(motif_matrix: List[str], elements='ACGT') -> Dict[str, List[float]]:
    rows = len(motif_matrix)
    cols = len(motif_matrix[0])

    counts = motif_matrix_count(motif_matrix, elements)

    ret = {}
    for item in counts.keys():
        ret[item] = [0.0] * cols

    total_count_per_column = rows
    for c in range(cols):
        for item in counts.keys():
            val = counts[item][c] / total_count_per_column
            ret[item][c] = val

    return ret


if __name__ == '__main__':
    counts = motif_matrix_profile([
        'TCGGGGgTTTtt'.upper(),
        'cCGGtGAcTTaC'.upper(),
        'aCGGGGATTTtC'.upper(),
        'TtGGGGAcTTtt'.upper(),
        'aaGGGGAcTTCC'.upper(),
        'TtGGGGAcTTCC'.upper(),
        'TCGGGGATTcat'.upper(),
        'TCGGGGATTcCt'.upper(),
        'TaGGGGAacTaC'.upper(),
        'TCGGGtATaaCC'.upper()
    ])

    print(f'{counts}')

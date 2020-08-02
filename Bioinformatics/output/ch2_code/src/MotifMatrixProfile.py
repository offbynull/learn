from collections import Counter
from typing import List, Dict
from MotifMatrixCount import motif_matrix_count


# For each column in a motif matrix, count up how many times each nucleotide appears.
def motif_matrix_profile(motif_matrix_counts: Dict[str, List[int]]) -> Dict[str, List[float]]:
    ret = {}
    for elem, counts in motif_matrix_counts.items():
        ret[elem] = [0.0] * len(counts)

    cols = len(counts)  # all elems should have the same len, so just grab the last one that was walked over
    for i in range(cols):
        total = 0
        for elem in motif_matrix_counts.keys():
            total += motif_matrix_counts[elem][i]
        for elem in motif_matrix_counts.keys():
            ret[elem][i] = motif_matrix_counts[elem][i] / total

    return ret


if __name__ == '__main__':
    profile = motif_matrix_profile(
        motif_matrix_count([
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
    )

    print(f'{profile}')

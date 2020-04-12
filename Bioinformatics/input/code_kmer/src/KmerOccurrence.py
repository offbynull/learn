from __future__ import annotations

from typing import List


# MARKDOWN
def kmer_occurrence_count(sequence: str, kmer: str) -> List[int]:
    k = len(kmer)
    idxes = []
    for i in range(0, len(seq) - k):
        if seq[i:i + k] == kmer:
            idxes.append(i)
    return idxes
# MARKDOWN


if __name__ == '__main__':
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        seq = input()
        kmer = input()
        idxes = kmer_occurrence_count(seq, kmer)
        print(f'Found {kmer} in {seq} at index {idxes}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")

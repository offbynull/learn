from typing import List


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


def string_spelled_by_genome_path(path: List[str]) -> str:
    if len(path) == 0:
        return ''

    k = len(path[0])
    ret = path[0]
    for p2 in path[1:]:
        p1 = ret[-k:]

        overlap1 = suffix(p1)
        overlap2 = prefix(p2)

        ret = ret[:-k]

        ret += p1[0]
        for ch1, ch2 in zip(overlap1, overlap2):
            ret += ch1 if ch1 == ch2 else '?'  # for failure, use IUPAC nucleotide codes instead of question mark?
        ret += p2[-1]
    return ret


if __name__ == '__main__':
    out = string_spelled_by_genome_path(['ACCGA', 'CCGAA', 'CGAAG', 'GAAGC', 'AAGCT'])
    print(f'{out}')

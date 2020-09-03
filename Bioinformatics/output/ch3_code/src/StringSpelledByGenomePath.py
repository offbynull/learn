from typing import List


def string_spelled_by_genome_path(path: List[str]) -> str:
    if len(path) == 0:
        return ''

    # sanity check
    for i, p in enumerate(path[:-1]):
        next_p = path[i+1]
        assert p[1:] == next_p[0:-1]

    ret = path[0] + ''.join([p[-1] for p in path[1:]])
    return ret


if __name__ == '__main__':
    out = string_spelled_by_genome_path(['ACCGA', 'CCGAA', 'CGAAG', 'GAAGC', 'AAGCT'])
    print(f'{out}')

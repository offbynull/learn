from typing import List

from Kdmer import Kdmer
from Utils import slide_window_kd


def string_composition(k: int, d:int, text: str) -> List[Kdmer]:
    ret = []
    for kdmer, _ in slide_window_kd(text, k, d):
        ret.append(kdmer)
    return ret


def main():
    out = string_composition(2, 1, 'ACTACTGGTACT')
    print(f'{out}')


if __name__ == '__main__':
    main()
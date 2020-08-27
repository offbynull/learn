from typing import List

from Utils import slide_window


def string_composition(k: int, text: str) -> List[str]:
    ret = []
    for kmer in slide_window(text, k):
        ret.append(kmer[0])
    return ret


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        k = int(input())
        text = input()

        composition = string_composition(k, text)
        print(f'String composition of {text} is {str(composition)}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
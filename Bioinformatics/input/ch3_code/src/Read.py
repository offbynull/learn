from __future__ import annotations

from collections import Counter
from typing import List

from Utils import slide_window


class Read:
    def __init__(self: Read, data: str, instance: int = 0, source: List[Read] = None) -> None:
        if source is None:
            source = []
        self.data = data
        self.instance = instance
        self.source = source
        self._hash_cache = hash((self.data, self.instance))  # this is an immutable class, so caching hash is okay

    # If instantize is true, each duplicate kmer in text will be given a unique instance number, meaning that it'll be
    # distinct from its duplicates.
    @staticmethod
    def from_string(text: str, k: int, instantize: bool = False):
        counter = Counter()
        ret = []
        for kmer, _ in slide_window(text, k):
            instance = counter[kmer] if instantize else 0
            ret.append(Read(kmer, instance=instance))
            counter[kmer] += 1
        return ret

    @property
    def k(self: Read) -> int:
        return len(self.data)

    def prefix(self: Read, skip: int = 1) -> Read:
        return Read(self.data[:-skip], source=[self])

    def suffix(self: Read, skip: int = 1) -> Read:
        return Read(self.data[skip:], source=[self])

    def append_overlap(self: Read, other: Read, skip: int = 1) -> Read:
        offset = len(self.data) - len(other.data)
        data_head = self.data[:offset]
        data = self.data[offset:]

        prefix = data[:skip]
        overlap1 = data[skip:]
        overlap2 = other.data[:-skip]
        suffix = other.data[-skip:]
        ret = data_head + prefix
        for ch1, ch2 in zip(overlap1, overlap2):
            ret += ch1 if ch1 == ch2 else '?'  # for failure, use IUPAC nucleotide codes instead of question mark?
        ret += suffix
        return Read(ret, source=[self, other])

    def stitch(self: Read, subsequent: List[Read]) -> str:
        ret = self
        for other in subsequent:
            ret = ret.append_overlap(other)
        return ret.data

    # This is read breaking -- why not just call it break? because break is a reserved keyword.
    def shatter(self: Read, k: int) -> List[Read]:
        ret = []
        for kmer, _ in slide_window(self.data, k):
            r = Read(kmer, source=[self])
            ret.append(r)
        return ret

    def __eq__(self, x: Read) -> bool:
        return type(self) is type(x) and self.data == x.data and self.instance == x.instance

    def __hash__(self: Read) -> int:
        return self._hash_cache

    def __repr__(self: Read) -> str:
        return self.data

    def __str__(self: Read) -> str:
        return self.data
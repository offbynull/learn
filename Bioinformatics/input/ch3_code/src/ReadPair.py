from __future__ import annotations

from collections import Counter
from typing import List

from Kdmer import Kdmer
from Read import Read
from Utils import slide_window, slide_window_kd


class ReadPair:
    def __init__(self: ReadPair, data: Kdmer, instance: int = 0, source: List[ReadPair] = None) -> None:
        if source is None:
            source = []
        self.data = data
        self.instance = instance
        self.source = source
        self._hash_cache = hash((self.data, self.instance))  # this is an immutable class, so caching hash is okay

    # If instantize is true, each duplicate kdmer in text will be given a unique instance number, meaning that it'll be
    # distinct from its duplicates.
    @staticmethod
    def from_string(text: str, k: int, d: int, instantize: bool = False):
        counter = Counter()
        ret = []
        for kdmer, _ in slide_window_kd(text, k, d):
            instance = counter[kdmer] if instantize else 0
            ret.append(ReadPair(kdmer, instance=instance))
            counter[kdmer] += 1
        return ret

    @property
    def k(self: ReadPair) -> int:
        return self.data.k

    @property
    def d(self: ReadPair) -> int:
        return self.data.d

    def prefix(self: ReadPair, skip: int = 1) -> ReadPair:
        return ReadPair(
            Kdmer(
                self.data.head[:-skip],
                self.data.tail[:-skip],
                self.data.d
            ),
            source=[self]
        )

    def suffix(self: ReadPair, skip: int = 1) -> ReadPair:
        return ReadPair(
            Kdmer(
                self.data.head[skip:],
                self.data.tail[skip:],
                self.data.d
            ),
            source=[self]
        )

    def append_overlap(self: ReadPair, other: ReadPair, skip: int = 1) -> ReadPair:
        self_head = Read(self.data.head)
        other_head = Read(other.data.head)
        new_head = self_head.append_overlap(other_head)
        new_head = new_head.data

        self_tail = Read(self.data.tail)
        other_tail = Read(other.data.tail)
        new_tail = self_tail.append_overlap(other_tail)
        new_tail = new_tail.data

        # WARNING: new_d may go negative -- In the event of a negative d, it means that rather than there being a gap
        # in between the head and tail, there's an OVERLAP in between the head and tail. To get rid of the overlap, you
        # need to remove either the last d chars from head or first d chars from tail.
        new_d = self.d - skip
        kdmer = Kdmer(new_head, new_tail, new_d)

        return ReadPair(kdmer, source=[self, other])

    def stitch(self: ReadPair, subsequent: List[ReadPair]) -> str:
        ret = self
        for other in subsequent:
            ret = ret.append_overlap(other)
        assert ret.d <= 0, "Gap still exists -- not enough to stitch"
        overlap_count = -ret.d
        return ret.data.head + ret.data.tail[overlap_count:]

    # This is read breaking -- why not just call it break? because break is a reserved keyword.
    def shatter(self: ReadPair, k: int) -> List[ReadPair]:
        ret = []
        for window_head, window_tail in zip(slide_window(self.data.head, k), slide_window(self.data.tail, k)):
            kmer_head, _ = window_head
            kmer_tail, _ = window_tail
            kdmer = Kdmer(kmer_head, kmer_tail, self.data.d)
            rp = ReadPair(kdmer, source=[self])
            ret.append(rp)
        return ret

    def __eq__(self, x: ReadPair) -> bool:
        return type(self) is type(x) and self.data == x.data and self.instance == x.instance

    def __hash__(self: ReadPair) -> int:
        return self._hash_cache

    def __repr__(self: ReadPair) -> str:
        return str(self.data)

    def __str__(self: ReadPair) -> str:
        return str(self.data)

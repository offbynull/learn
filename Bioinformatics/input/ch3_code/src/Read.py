from __future__ import annotations

from collections import Counter
from random import Random
from typing import List, Tuple, Optional, Callable

from Utils import slide_window


class Read:
    def __init__(self: Read, data: str, instance: int = 0, source: Optional[Tuple[str, List[Read]]] = None) -> None:
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
        return Read(self.data[:-skip], source=('prefix', [self]))

    def suffix(self: Read, skip: int = 1) -> Read:
        return Read(self.data[skip:], source=('suffix', [self]))

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
        return Read(ret, source=('overlap', [self, other]))

    def stitch(self: Read, subsequent: List[Read]) -> str:
        ret = self
        for other in subsequent:
            ret = ret.append_overlap(other)
        return ret.data

    # This is read breaking -- why not just call it break? because break is a reserved keyword.
    def shatter(self: Read, k: int) -> List[Read]:
        ret = []
        for kmer, _ in slide_window(self.data, k):
            r = Read(kmer, source=('shatter', [self]))
            ret.append(r)
        return ret

    def collapse(self: Read, subsequent: List[Read]) -> List[Read]:
        full_list = [self] + subsequent
        collector = dict()
        for item in full_list:
            collector.setdefault(item.data, []).append(item)
        ret = []
        for data, matches in collector.items():
            collapsed = Read(data, source=('collapse', matches))
            ret.append(collapsed)
        return ret

    def __eq__(self, x: Read) -> bool:
        return type(self) is type(x) and self.data == x.data and self.instance == x.instance

    def __hash__(self: Read) -> int:
        return self._hash_cache

    def __repr__(self: Read) -> str:
        return self.data

    def __str__(self: Read) -> str:
        return self.data

    @staticmethod
    def random_fragment(data: str, k: int, read_count: int, r: Optional[Random] = None) -> List[Read]:
        if r is None:
            r = Random()
        total_kmers = len(data) - k + 1
        ret = []
        for i in range(read_count):
            offset = r.randint(0, total_kmers)
            kmer = data[offset:offset + k]
            read = Read(kmer)
            ret.append(read)
        return ret

    def introduce_random_errors(self: Read, count: int, include_source: bool = False, r: Optional[Random] = None) -> Read:
        if r is None:
            r = Random()
        data = self.data
        offsets = list(range(len(data)))
        for i in range(count):
            offset = r.choice(offsets)
            offsets.remove(offset)
            choices = ['A', 'C', 'T', 'G']
            choices.remove(data[offset])
            data = data[:offset] + r.choice(choices) + data[offset + 1:]
        source = ('introduce_error', [self]) if include_source else None
        return Read(data, source=source)

    def to_sources(self: Read, stop_func: Callable[[str, List[Read]], bool] = lambda x: False) -> List[List[Read]]:
        def walk_up(item: Read, path: List[Read]) -> List[List[Read]]:
            if item.source is None:
                return [path]
            source_name, source_list = item.source
            if stop_func(source_name, source_list):
                return [path]
            ret = []
            for new_source in source_list:
                new_path = path.copy() + [new_source]
                new_paths = walk_up(new_source, new_path)
                ret.extend(new_paths)
            return ret
        return walk_up(self, [self])

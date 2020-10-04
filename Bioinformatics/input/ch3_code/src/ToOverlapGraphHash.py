from typing import List, TypeVar

from Graph import Graph
from Kdmer import Kdmer
from Read import Read
from ReadPair import ReadPair

T = TypeVar('T', Read, ReadPair)


# MARKDOWN
def to_overlap_graph(items: List[T], skip: int = 1) -> Graph[T]:
    ret = Graph()

    prefixes = dict()
    suffixes = dict()
    for i, item in enumerate(items):
        prefix = item.prefix(skip)
        prefixes.setdefault(prefix, set()).add(i)
        suffix = item.suffix(skip)
        suffixes.setdefault(suffix, set()).add(i)

    for key, indexes in suffixes.items():
        other_indexes = prefixes.get(key)
        if other_indexes is None:
            continue
        for i in indexes:
            item = items[i]
            for j in other_indexes:
                if i == j:
                    continue
                other_item = items[j]
                ret.insert_edge(item, other_item)
    return ret
# MARKDOWN


if __name__ == '__main__':
    out = to_overlap_graph([
        Read('ATGCG'),
        Read('GCATG'),
        Read('CATGC'),
        Read('AGGCA'),
        Read('GGCAT'),
        Read('GGCAC')
    ])
    print(f'{out}')

    out = to_overlap_graph([
        ReadPair(Kdmer('AT', 'CG', 1)),
        ReadPair(Kdmer('GC', 'TG', 1)),
        ReadPair(Kdmer('CA', 'GC', 1)),
        ReadPair(Kdmer('AG', 'CA', 1)),
        ReadPair(Kdmer('GG', 'AT', 1)),
        ReadPair(Kdmer('GG', 'AC', 1))
    ])
    print(f'{out}')
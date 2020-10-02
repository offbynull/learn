from typing import List, TypeVar

from Graph import Graph
from Kdmer import Kdmer
from Read import Read
from ReadPair import ReadPair

T = TypeVar('T', Read, ReadPair)


def to_overlap_graph(items: List[T], skip: int = 1) -> Graph[T]:
    ret = Graph()
    for i, item in enumerate(items):
        for j, other_item in enumerate(items):
            if i == j:
                continue
            if item.suffix(skip) == other_item.prefix(skip):
                ret.insert_edge(item, other_item)
    return ret


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
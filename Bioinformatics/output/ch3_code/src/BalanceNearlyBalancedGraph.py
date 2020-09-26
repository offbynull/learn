import typing
from collections import Counter
from typing import Dict, List, Tuple, TypeVar

from Utils import copy_graph, normalize_graph
from WalkEulerianCycle import walk_eularian_cycle

T = TypeVar('T')


def find_unbalanced_nodes(graph: Dict[T, typing.Counter[T]]) -> List[Tuple[T, int, int]]:
    all_nodes = graph.keys()
    unbalanced_nodes = []
    for node in all_nodes:
        out_degree = sum(graph[node].values())
        in_degree = sum([children[node] for children in graph.values() if node in children])
        if in_degree != out_degree:
            unbalanced_nodes.append((node, in_degree, out_degree))
    return unbalanced_nodes


# creates a balanced graph from a nearly balanced graph -- nearly balanced means the graph has an equal number of
# missing outputs and missing inputs.
def balance_graph(graph: Dict[T, typing.Counter[T]]) -> Dict[T, typing.Counter[T]]:
    unbalanced_nodes = find_unbalanced_nodes(graph)
    nodes_with_missing_ins = filter(lambda x: x[1] < x[2], unbalanced_nodes)
    nodes_with_missing_outs = filter(lambda x: x[1] > x[2], unbalanced_nodes)

    graph = copy_graph(graph)

    # create 1 copy per missing input / per missing output
    n_per_need_in = [_n for n, in_degree, out_degree in nodes_with_missing_ins for _n in [n] * (out_degree - in_degree)]
    n_per_need_out = [_n for n, in_degree, out_degree in nodes_with_missing_outs for _n in [n] * (in_degree - out_degree)]
    assert len(n_per_need_in) == len(n_per_need_out)  # need an equal count of missing ins and missing outs to balance

    # balance
    for n_need_in, n_need_out in zip(n_per_need_in, n_per_need_out):
        graph[n_need_out][n_need_in] += 1

    return graph


if __name__ == '__main__':
    graph = {
        '0': Counter(['2']),
        '1': Counter(['3']),
        '2': Counter(['1']),
        '3': Counter(['0', '4']),
        '6': Counter(['3', '7']),
        '7': Counter(['8']),
        '8': Counter(['9']),
        '9': Counter(['6'])
    }
    graph = normalize_graph(graph)

    graph = balance_graph(graph)
    path = walk_eularian_cycle(graph, '0')
    print(f'{"->".join(path)}')

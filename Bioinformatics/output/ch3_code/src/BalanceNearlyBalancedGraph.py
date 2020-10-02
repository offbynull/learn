from typing import List, Tuple, TypeVar, Set

from Graph import Graph
from WalkEulerianCycle import walk_eularian_cycle

T = TypeVar('T')


def find_unbalanced_nodes(graph: Graph[T]) -> List[Tuple[T, int, int]]:
    unbalanced_nodes = []
    for node in graph.get_nodes():
        in_degree = graph.get_in_degree(node)
        out_degree = graph.get_out_degree(node)
        if in_degree != out_degree:
            unbalanced_nodes.append((node, in_degree, out_degree))
    return unbalanced_nodes


# creates a balanced graph from a nearly balanced graph -- nearly balanced means the graph has an equal number of
# missing outputs and missing inputs.
def balance_graph(graph: Graph[T]) -> Tuple[Graph[T], Set[T], Set[T]]:
    unbalanced_nodes = find_unbalanced_nodes(graph)
    nodes_with_missing_ins = filter(lambda x: x[1] < x[2], unbalanced_nodes)
    nodes_with_missing_outs = filter(lambda x: x[1] > x[2], unbalanced_nodes)

    graph = graph.copy()

    # create 1 copy per missing input / per missing output
    n_per_need_in = [_n for n, in_degree, out_degree in nodes_with_missing_ins for _n in [n] * (out_degree - in_degree)]
    n_per_need_out = [_n for n, in_degree, out_degree in nodes_with_missing_outs for _n in [n] * (in_degree - out_degree)]
    assert len(n_per_need_in) == len(n_per_need_out)  # need an equal count of missing ins and missing outs to balance

    # balance
    for n_need_in, n_need_out in zip(n_per_need_in, n_per_need_out):
        graph.insert_edge(n_need_out, n_need_in)

    return graph, set(n_per_need_in), set(n_per_need_out)  # return graph with cycle, orig root nodes, orig tail nodes


if __name__ == '__main__':
    g = Graph()
    g.insert_edge('0', '2')
    g.insert_edge('1', '3')
    g.insert_edge('2', '1')
    g.insert_edge('3', '0')
    g.insert_edge('3', '4')
    g.insert_edge('6', '3')
    g.insert_edge('6', '7')
    g.insert_edge('7', '8')
    g.insert_edge('8', '9')
    g.insert_edge('9', '6')

    g, _, _ = balance_graph(g)
    path = walk_eularian_cycle(g, '0')
    print(f'{"->".join(path)}')

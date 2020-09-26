import typing
from collections import Counter
from typing import Dict, List, Tuple, TypeVar

from Utils import copy_graph, walk_edge_nodes

T = TypeVar('T')


def randomly_walk_and_remove_edges_until_cycle(node: T, graph: Dict[T, typing.Counter[T]]) -> List[Tuple[T, T]]:
    end_node = node
    edge_list = []
    from_node = node
    while len(graph) > 0:
        to_nodes = graph.get(from_node)
        assert len(to_nodes) > 0  # eularian graphs are strongly connected, meaning we should never hit dead-end nodes

        to_node = next(to_nodes.elements())
        to_nodes[to_node] -= 1
        if to_nodes[to_node] == 0:
            del to_nodes[to_node]
        if len(to_nodes) == 0:
            del graph[from_node]

        edge = (from_node, to_node)
        edge_list.append(edge)
        from_node = to_node
        if from_node == end_node:
            return edge_list

    assert False  # eularian graphs are strongly connected and balanced, meaning we should never run out of nodes


# graph must be strongly connected
# graph must be balanced
# if the 2 conditions above are met, the graph will be eularian (a eulerian cycle exists)
def walk_eularian_cycle(graph: Dict[T, typing.Counter[T]], start_node: T) -> List[T]:
    graph = copy_graph(graph)

    node_cycle = list(
        walk_edge_nodes(
            randomly_walk_and_remove_edges_until_cycle(start_node, graph)
        )
    )
    node_cycle_ptr = 0
    while len(graph) > 0:
        new_node_cycle = None
        for local_ptr, node in enumerate(node_cycle[node_cycle_ptr:]):
            to_nodes = graph.get(node)
            if to_nodes is None:
                continue
            node_cycle_ptr += local_ptr
            inject_node_cycle = list(
                walk_edge_nodes(
                    randomly_walk_and_remove_edges_until_cycle(node, graph)
                )
            )
            new_node_cycle = node_cycle[:]
            new_node_cycle[node_cycle_ptr:node_cycle_ptr+1] = inject_node_cycle
            break
        assert new_node_cycle is not None
        node_cycle = new_node_cycle

    return node_cycle


if __name__ == '__main__':
    graph = {
        '0': Counter(['3']),
        '1': Counter(['0']),
        '2': Counter(['1', '6']),
        '3': Counter(['2']),
        '4': Counter(['2']),
        '5': Counter(['4']),
        '6': Counter(['5', '8']),
        '7': Counter(['9']),
        '8': Counter(['7']),
        '9': Counter(['6'])
    }
    print(f'{"->".join(walk_eularian_cycle(graph, "0"))}')

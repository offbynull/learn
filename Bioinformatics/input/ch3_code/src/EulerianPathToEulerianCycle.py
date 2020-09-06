from typing import Dict, List, Set, Tuple

from EulerianCycle import eularian_cycle


def normalize_graph_representation(graph: Dict[str, List[str]]):
    all_nodes = graph.keys() | set([node for nodes in graph.values() for node in nodes])
    for n in all_nodes:
        graph.setdefault(n, [])


def find_unbalanced_nodes(graph: Dict[str, List[str]]) -> List[Tuple[str, int, int]]:
    all_nodes = graph.keys() | set([node for nodes in graph.values() for node in nodes])
    unbalanced_nodes = []
    for node in all_nodes:
        out_degree = len(graph.get(node, []))
        in_degree = sum([1 for children in graph.values() if node in children])
        if in_degree != out_degree:
            unbalanced_nodes.append((node, in_degree, out_degree))
    return unbalanced_nodes


def find_eularian_path_in_nearly_balanced_graph(graph: Dict[str, List[str]]) -> List[str]:
    unbalanced_nodes = find_unbalanced_nodes(graph)
    if len(unbalanced_nodes) == 0:
        pass
    elif len(unbalanced_nodes) == 2:
        node1, node1_in_degree, node1_out_degree = unbalanced_nodes[0]
        node2, node2_in_degree, node2_out_degree = unbalanced_nodes[1]
        node1_excess = node1_in_degree - node1_out_degree
        node2_excess = node2_in_degree - node2_out_degree
        if node1_excess + node2_excess == 0:
            if node1_excess > 0:  # node1 has more inputs, node 2 has more outputs -- connect 1 to 2
                children = graph.setdefault(node1, [])
                children += [node2] * node1_excess
                cycle = eularian_cycle(graph)
                cycle.pop()
                i = cycle.index(node2)
                return cycle[i:] + cycle[:i]
            elif node2_excess > 0:  # node2 has more inputs, node 1 has more outputs -- connect to 2 to 1
                children = graph.setdefault(node2, [])
                children += [node1] * node2_excess
                cycle = eularian_cycle(graph)
                cycle.pop()
                i = cycle.index(node1)
                return cycle[i:] + cycle[:i]
            else:
                raise Exception('Unsure what to do here')
    else:
        raise Exception('Unsure what to do here')


if __name__ == '__main__':
    graph = {
        '0': ['2'],
        '1': ['3'],
        '2': ['1'],
        '3': ['0', '4'],
        '6': ['3', '7'],
        '7': ['8'],
        '8': ['9'],
        '9': ['6']
    }

    path = find_eularian_path_in_nearly_balanced_graph(graph)
    print(f'{"->".join(path)}')

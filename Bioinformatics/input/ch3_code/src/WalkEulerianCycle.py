from collections import Counter
from typing import List, Tuple, TypeVar

from Graph import Graph
from Kdmer import Kdmer
from Read import Read
from ReadPair import ReadPair
from ToDeBruijnGraph import to_debruijn_graph, to_graphviz

T = TypeVar('T')


# MARKDOWN
def randomly_walk_and_remove_edges_until_cycle(graph: Graph[T], node: T) -> List[Tuple[T, T]]:
    end_node = node
    edge_list = []
    from_node = node
    while len(graph) > 0:
        to_nodes = graph.get_outputs(from_node)
        to_node = next(to_nodes, None)
        assert to_node is not None  # eularian graphs are strongly connected, meaning we should never hit dead-end nodes

        graph.delete_edge(from_node, to_node, True, True)

        edge = (from_node, to_node)
        edge_list.append(edge)
        from_node = to_node
        if from_node == end_node:
            return edge_list

    assert False  # eularian graphs are strongly connected and balanced, meaning we should never run out of nodes


# (6, 8), (8, 7), (7, 9), (9, 6)  ---->  68796
def walk_edge_nodes(edges: List[Tuple[T, T]]) -> T:
    yield edges[0][0]
    for e in edges:
        yield e[1]


# graph must be strongly connected
# graph must be balanced
# if the 2 conditions above are met, the graph will be eularian (a eulerian cycle exists)
def walk_eularian_cycle(graph: Graph[T], start_node: T) -> List[T]:
    graph = graph.copy()

    node_cycle = list(
        walk_edge_nodes(
            randomly_walk_and_remove_edges_until_cycle(graph, start_node)
        )
    )
    node_cycle_ptr = 0
    while len(graph) > 0:
        new_node_cycle = None
        for local_ptr, node in enumerate(node_cycle[node_cycle_ptr:]):
            if node not in graph:
                continue
            node_cycle_ptr += local_ptr
            inject_node_cycle = list(
                walk_edge_nodes(
                    randomly_walk_and_remove_edges_until_cycle(graph, node)
                )
            )
            new_node_cycle = node_cycle[:]
            new_node_cycle[node_cycle_ptr:node_cycle_ptr+1] = inject_node_cycle
            break
        assert new_node_cycle is not None
        node_cycle = new_node_cycle

    return node_cycle
# MARKDOWN


# if __name__ == '__main__':
#     g = Graph()
#     g.insert_edge('0', '3')
#     g.insert_edge('1', '0')
#     g.insert_edge('2', '1')
#     g.insert_edge('2', '6')
#     g.insert_edge('3', '2')
#     g.insert_edge('4', '2')
#     g.insert_edge('5', '4')
#     g.insert_edge('6', '5')
#     g.insert_edge('6', '8')
#     g.insert_edge('7', '9')
#     g.insert_edge('8', '7')
#     g.insert_edge('9', '6')
#     print(f'{"->".join(walk_eularian_cycle(g, "0"))}')

def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        lines = []
        while True:
            try:
                line = input().strip()
                if len(line) > 0:
                    lines.append(line)
            except EOFError:
                break

        command = lines[0]
        lines = lines[1:]
        counter = Counter(lines)
        if command == 'reads':
            frags = [Read(r, i) for r, c in counter.items() for i in range(c)]
        elif command == 'read-pairs':
            frags = [ReadPair(Kdmer(r.split('|')[0], r.split('|')[2], int(r.split('|')[1])), i) for r, c in counter.items() for i in range(c)]
        else:
            raise
        graph = to_debruijn_graph(frags)
        print(f'Given the fragments {lines}, the de Bruijn graph is...', end="\n\n")
        print(f'```{{dot}}\n{to_graphviz(graph)}\n```\n\n')
        print(f'... and a Eulerian cycle is ...', end="\n\n")
        path = walk_eularian_cycle(graph, frags[0].prefix())
        print(f'{" -> ".join([str(p) for p in path])}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
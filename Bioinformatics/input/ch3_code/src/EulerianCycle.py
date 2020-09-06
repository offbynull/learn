from typing import Dict, List, Tuple


def random_walk_until_back_at_node_while_removing_edges_as_walking(node: str, graph: Dict[str, List[str]]) -> List[Tuple[str, str]]:
    current_node = node
    end_node = node
    edge_list = []
    while len(graph) > 0:
        children = graph.get(current_node)
        next_node = children.pop()
        if len(children) == 0:
            del graph[current_node]

        edge = (current_node, next_node)
        edge_list.append(edge)
        current_node = next_node
        if current_node == end_node:
            return edge_list


# graph must be strongly connected
# graph must be eulerian
def eularian_cycle(graph: Dict[str, List[str]]) -> List[str]:
    graph_copy = dict(graph)

    start_id = list(graph_copy.keys())[0]
    edge_cycle = random_walk_until_back_at_node_while_removing_edges_as_walking(
        start_id,
        graph_copy
    )
    node_cycle = [edge_cycle[0][0]] + [e[1] for e in edge_cycle]

    total_node_cycle = list(node_cycle)
    while len(graph_copy) > 0:
        unexplored_nodes = set(total_node_cycle).intersection(graph_copy.keys())
        for unexplored_node in unexplored_nodes:
            if len(graph_copy) == 0:
                break
            start_id = unexplored_node
            edge_cycle = random_walk_until_back_at_node_while_removing_edges_as_walking(
                start_id,
                graph_copy
            )
            node_cycle = [edge_cycle[0][0]] + [e[1] for e in edge_cycle]
            i = total_node_cycle.index(start_id)
            total_node_cycle = total_node_cycle[:i] + node_cycle + total_node_cycle[i+1:]

    return total_node_cycle


if __name__ == '__main__':
    graph = {
        '0': ['3'],
        '1': ['0'],
        '2': ['1', '6'],
        '3': ['2'],
        '4': ['2'],
        '5': ['4'],
        '6': ['5', '8'],
        '7': ['9'],
        '8': ['7'],
        '9': ['6']
    }
    print(f'{"->".join(eularian_cycle(graph))}')

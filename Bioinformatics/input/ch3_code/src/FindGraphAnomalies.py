from collections import Counter
from random import Random
from typing import Dict, List, TypeVar, Optional, Tuple

from FragmentOccurrenceProbabilityCalculator import calculate_fragment_occurrence_probabilities
from Graph import Graph
from Kdmer import Kdmer
from Read import Read
from ReadPair import ReadPair
from ToDeBruijnGraph import to_debruijn_graph
from Utils import generate_random_genome, count_kmers

T = TypeVar('T', Read, ReadPair)


def walk_outs_until_converge(graph: Graph[T], node: T) -> Optional[List[T]]:
    ret = [node]
    ret_quick_lookup = {node}
    while True:
        in_degree = graph.get_in_degree(node)
        if in_degree > 1:
            return ret

        children = graph.get_outputs(node)
        child = next(children, None)
        if child is None or child in ret_quick_lookup:
            return None

        node = child
        ret.append(node)
        ret_quick_lookup.add(node)


def walk_ins_until_diverge(graph: Graph[T], node: T) -> Optional[List[T]]:
    ret = [node]
    ret_quick_lookup = {node}
    while True:
        in_degree = graph.get_out_degree(node)
        if in_degree > 1:
            return ret

        parents = graph.get_inputs(node)
        parent = next(parents, None)
        if parent is None or parent in ret_quick_lookup:
            return None

        node = parent
        ret.insert(0, node)
        ret_quick_lookup.add(node)


# MARKDOWN
def find_head_convergences(graph: Graph[T], branch_len: int) -> List[Tuple[Optional[T], List[T], Optional[T]]]:
    root_nodes = filter(lambda n: graph.get_in_degree(n) == 0, graph.get_nodes())

    ret = []
    for n in root_nodes:
        for child in graph.get_outputs(n):
            path_from_child = walk_outs_until_converge(graph, child)
            if path_from_child is None:
                continue
            diverging_node = None
            branch_path = [n] + path_from_child[:-1]
            converging_node = path_from_child[-1]
            path = (diverging_node, branch_path, converging_node)
            if len(branch_path) <= branch_len:
                ret.append(path)
    return ret


def find_tail_divergences(graph: Graph[T], branch_len: int) -> List[Tuple[Optional[T], List[T], Optional[T]]]:
    tail_nodes = filter(lambda n: graph.get_out_degree(n) == 0, graph.get_nodes())

    ret = []
    for n in tail_nodes:
        for child in graph.get_inputs(n):
            path_from_child = walk_ins_until_diverge(graph, child)
            if path_from_child is None:
                continue
            diverging_node = path_from_child[0]
            branch_path = path_from_child[1:] + [n]
            converging_node = None
            path = (diverging_node, branch_path, converging_node)
            if len(branch_path) <= branch_len:
                ret.append(path)
    return ret


def find_bubbles(graph: Graph[T], branch_len: int) -> List[Tuple[Optional[T], List[T], Optional[T]]]:
    branching_nodes = filter(lambda n: graph.get_out_degree(n) > 1, graph.get_nodes())

    ret = []
    for n in branching_nodes:
        for child in graph.get_outputs(n):
            path_from_child = walk_outs_until_converge(graph, child)
            if path_from_child is None:
                continue
            diverging_node = n
            branch_path = path_from_child[:-1]
            converging_node = path_from_child[-1]
            path = (diverging_node, branch_path, converging_node)
            if len(branch_path) <= branch_len:
                ret.append(path)
    return ret
# MARKDOWN


def to_graphviz(graph: Graph, weights: Dict[T, float]) -> str:
    out = ''
    for node in graph.get_nodes():
        for to_node in graph.get_outputs(node):
            read = node.append_overlap(to_node)
            weight = weights[read]
            r = 0
            g = 0
            b = 0
            if weight < 1.0:
                r = int(255 * (1.0 - weight))
            elif weight > 1.0:
                r = int(255 * (max(weight - 1.0, 1.0)))
                b = r
            color = '#' + format(r, '02x') + format(g, '02x') + format(b, '02x')
            out += '"' + str(node).replace("\"", "\\\"") + '\"'\
                   + ' -> '\
                   + '"' + str(to_node).replace("\"", "\\\"") + '"'\
                   + f' [color="{color}", label="{weight: .3f}"];\n'
    # https://stackoverflow.com/questions/8610710/compacting-a-digraph-in-graphviz-using-dot-language
    return 'digraph {\n'\
           + 'graph[center=true, margin=0.1, nodesep=0.1, ranksep=0.1]\n'\
           + 'node[shape=none, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'\
           + 'edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]\n'\
           + out\
           + '}\n'


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
        r = Random(int(lines[1]))
        genome = lines[2]
        bad_frag = lines[3]
        coverage = int(lines[4])
        if command == 'reads':
            k = int(lines[5])
            frags = Read.random_fragment(genome, k, count_kmers(len(genome), k) * coverage, r=r)
            bad_frag = Read(bad_frag)
        elif command == 'read-pairs':
            k, d = tuple([int(s) for s in lines[5].split()])
            frags = ReadPair.random_fragment(genome, k, d, count_kmers(len(genome), k) * coverage, r=r)
            bad_frag = ReadPair(Kdmer(bad_frag.split('|')[0], bad_frag.split('|')[2], int(bad_frag.split('|')[1])))
        else:
            raise
        frags += [bad_frag]
        k_break = int(lines[6])
        frags = [broken_read for frag in frags for broken_read in frag.shatter(k_break)]
        frag_to_count = Counter(frags)
        print(f'Genome: {genome}', end='\n\n')
        print(f'Probability of occurrence in genome:', end='\n\n')
        occurrence_probabilities = calculate_fragment_occurrence_probabilities(frags)
        for f, appearances in occurrence_probabilities.items():
            print(f' * {f} was scanned in {frag_to_count[f]} times, so it probably appears in the genome {appearances} times.')
        print(f'', end='\n\n')
        print(f'De Bruijn graph:', end='\n\n')
        frags = frags[0].collapse(frags)
        graph = to_debruijn_graph(frags)
        print(f'```{{dot}}\n{to_graphviz(graph, occurrence_probabilities)}\n```')
        print(f'', end='\n\n')
        print(f'Problem paths:', end='\n\n')
        potentially_bad_paths = find_bubbles(graph, k_break)\
                                + find_head_convergences(graph, k_break)\
                                + find_tail_divergences(graph, k_break)
        for src, branch, dst in potentially_bad_paths:
            print(f' * Src: {src}, Dst: {dst}, Branch: {"->".join([str(x) for x in branch])}')

    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
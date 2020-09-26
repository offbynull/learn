from Kmer_ToOverlapGraphHash import to_overlap_graph
from Kmer_StringComposition import string_composition
from Kmer_StringSpelledByGenomePath import string_spelled_by_genome_path
from Utils import normalize_graph, count_graph_edges, find_graph_roots
from WalkHamiltonianPath import walk_hamiltonian_path

if __name__ == '__main__':
    kmers = string_composition(3, 'TAATGCCATGGGATGTT')
    graph = to_overlap_graph(kmers)
    graph = normalize_graph(graph)
    total_edges_count = count_graph_edges(graph)
    for root in find_graph_roots(graph):
        paths = walk_hamiltonian_path(graph, root)
        for path in paths:
            dna = string_spelled_by_genome_path(path)
            print(f'{dna} -- {len(set(path))} of {len(graph.keys())} nodes walked')
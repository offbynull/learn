from DistanceBetweenPatternAndStrings import distance_between_pattern_and_strings
from FindMostProbableKmerUsingProfileMatrix import find_most_probable_kmer_using_profile_matrix
from GreedyMotifSearch import greedy_motif_search
from GreedyMotifSearchWithPsuedocounts import greedy_motif_search_with_psuedocounts
from MedianString import median_string
from MotifEnumeration import motif_enumeration

with open('/home/user/Downloads/dataset_240242_9.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0].split()[0])
dnas_count = int(lines[0].split()[1])  # ignore
dnas = lines[1:]
dnas = [l.strip() for l in dnas] # get rid of whitespace
dnas = [l for l in dnas if len(l) > 0] # get rid of empty lines

found_motif_matrix = greedy_motif_search_with_psuedocounts(k, dnas)
for motif in found_motif_matrix:
    print(f'{motif}')

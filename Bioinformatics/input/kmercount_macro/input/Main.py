import sys

data = sys.stdin.read() #having truoble reading stdin if run from conda run
print('ggg ' + data)

# dna_seq = data[0]
# kmer = data[1]

# k = len(kmer)
# idxes = []
# for i in range(0, len(dna_seq) - k):
#     if dna_seq[i:i+k] == kmer:
#         idxes.append(i)
# print(f'{idxes}')
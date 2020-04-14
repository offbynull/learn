from CountASequencesKmers import kmer_frequency
from ReverseComplementADnaKmer import reverse_complement

x = """aactctatacctcctttttgtcgaatttgtgtgatttatagagaaaatcttattaactga
aactaaaatggtaggtttggtggtaggttttgtgtacattttgtagtatctgatttttaa
ttacataccgtatattgtattaaattgacgaacaattgcatggaattgaatatatgcaaa
acaaacctaccaccaaactctgtattgaccattttaggacaacttcagggtggtaggttt
ctgaagctctcatcaatagactattttagtctttacaaacaatattaccgttcagattca
agattctacaacgctgttttaatgggcgttgcagaaaacttaccacctaaaatccagtat
ccaagccgatttcagagaaacctaccacttacctaccacttacctaccacccgggtggta
agttgcagacattattaaaaacctcatcagaagcttgttcaaaaatttcaatactcgaaa
cctaccacctgcgtcccctattatttactactactaataatagcagtataattgatctga""".replace("\n", "").upper()

counter = kmer_frequency(x, 9)
print(f'{counter.most_common(6)}')

for kmer, count in counter.most_common(6):
    kmer_revcomp = reverse_complement(kmer);
    print(f'{kmer} ({counter[kmer]}) -> {kmer_revcomp} ({counter[kmer_revcomp]})')

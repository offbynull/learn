from Utils import dna_to_rna, dna_reverse_complement, slide_window, codon_to_amino_acid, split_to_size, rna_to_dna

with open('/home/user/Downloads/test.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
dna_seq = lines[0]
amino_acid_eq = lines[1]

codon_seq_rna_len = len(amino_acid_eq) * 3

rna_seq = dna_to_rna(dna_seq)
rna_seq_rev = dna_to_rna(dna_reverse_complement(dna_seq))

for kmer, _ in slide_window(rna_seq, len(amino_acid_eq) * 3):
    found_amino_acid_seq = ''.join([codon_to_amino_acid(codon) for codon in split_to_size(kmer, 3)])
    if found_amino_acid_seq == amino_acid_eq:
        print(f'{rna_to_dna(kmer)}')

for kmer, _ in slide_window(rna_seq_rev, len(amino_acid_eq) * 3):
    found_amino_acid_seq = ''.join([codon_to_amino_acid(codon) for codon in split_to_size(kmer, 3)])
    if found_amino_acid_seq == amino_acid_eq:
        print(f'{rna_to_dna(kmer)}')
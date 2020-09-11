import lzma
import csv
from collections import Counter
from random import randint

from Utils import slide_window, enumerate_patterns


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        fasta_filepath = 'GCA_000008865.2_ASM886v2_genomic.fna.xz'
        with lzma.open(fasta_filepath, mode='rt', encoding='utf-8') as f:
            lines = f.read().splitlines()
            lines = [line for line in lines if not line.startswith('>')]
            seq = ''.join(lines)

        genes_filepath = 'GCA_000008865.2_ASM886v2_genes.txt.xz'
        with lzma.open(genes_filepath, mode='rt', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter='\t')
            genes_data = []
            for row in csv_reader:
                genes_data.append(row)

        gene_upstreams = []
        for row in genes_data[1:]:
            gene_start_pos_str = row[12].strip()
            if gene_start_pos_str == '':
                continue
            gene_start_pos = int(gene_start_pos_str)
            gene_upstream = seq[max(0, gene_start_pos-2000):gene_start_pos]
            gene_upstreams.append(gene_upstream)

        gene_count = len(gene_upstreams)
        for i in range(5):
            gene_id = randint(0, gene_count)
            gene_upstream = gene_upstreams[gene_id]
            counter = Counter()
            for kmer, _ in slide_window(gene_upstream, 1):
                counter[kmer] += 1
            print(f'{counter}')


        # gene_count = len(gene_upstreams)
        # for i in range(gene_count ** 2):
        #     gene_id1 = randint(0, gene_count)
        #     gene_id2 = randint(0, gene_count)
        #     upstream1 = gene_upstreams[gene_id1]
        #     upstream2 = gene_upstreams[gene_id2]
        #     if upstream1 is upstream2:
        #         continue
        #     found_motif_matrix = greedy_motif_search_with_psuedocounts(16, [upstream1, upstream2])
        #     score = score_motif(found_motif_matrix)
        #     if score <= 2:
        #         print(f'Potential match #{i}: {gene_id1} vs {gene_id2}: {found_motif_matrix} ({score})')

        # counts = motif_matrix_count([
        #     'TTATACAAA',
        #     'TTATACACA',
        #     'TTATCCAAA',
        #     'TTATCCACA'
        # ])
        # apply_psuedocounts_to_count_matrix(counts)
        # profile = motif_matrix_profile(counts)
        # for i, gene_upstream in enumerate(gene_upstreams):
        #     found, prob = find_most_probable_kmer_using_profile_matrix(profile, gene_upstream)
        #     print(f'{i}: {found} {prob}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
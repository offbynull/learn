```{title}
Bioinformatics
```

```{toc}
```

# Introduction



# K-mers

A `{bm} k-mer/(k-mer|kmer)/i` is a substring of length k within some larger biological string (e.g. DNA or amino acid chain). For example, in the DNA sequence `GAAATC`, the following k-mer's exist:

| k | k-mers          |
|---|-----------------|
| 1 | G A A A T C     |
| 2 | GA AA AA AT TC  |
| 3 | GAA AAA AAT ATC |
| 4 | GAAA AAAT AATC  |
| 5 | GAAAT AAATC     |
| 6 | GAAATC          |

Often times we'll need to either...

* search for an exact k-mer.
* search for an approximate k-mer (fuzzy search).
* find k-mers of interest in a sequence (e.g. repeating k-mers).

A common use-case for k-mer search is to find the `{bm} replication origin` (`{bm} ori/\b(ori)\b/i`) of a prokaryotic organism's DNA. The replication origin is a region within a prokaryotic cell's circular DNA where DNA replication starts. Within the ori region, several smaller regions exist that contain DNA sequences known as `{bm} DnaA box`es. These DnaA boxes are sequences that enzymes responsible for DNA strand replication (`{bm} DNA polymerase`s) bind to to begin the process of replication.

```{dot}
digraph {
  Ori -> DnaA_box [taillabel="1..*", arrowhead=none]
}
```

Typically multiple DnaA boxes exist in the ori.

```
                     DnaA boxes within the ori

+--------------------------------------------------------------------+
|   :   :             :   :                            :   :         |
+---+-+-+-------------+-+-+----------------------------+-+-+---------+
      |                 |                                |           
  DnaA box          DnaA box                         DnaA box        
    
```

The DnaA boxes in an ori don't have to be exactly the same. The enzyme will still bind to them if they're slightly different.

## Count K-mers

Counting k-mers is essentially just sliding a window of size k over a string and seeing if the contents in that window match some k-mer.

```{define-block}
kmercount
kmercount_macro/
```

```{kmercount}
ACTGAACCTTACACTTAAAGGAGATGATGATTCAAAT
AC
```
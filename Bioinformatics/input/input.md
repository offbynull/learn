```{title}
Bioinformatics
```

```{toc}
```

# Introduction



# K-mers

A `{bm} k-mer/(k-mer|kmer)/i` is a subsequence of length k within some larger biological sequence (e.g. DNA or amino acid chain). For example, in the DNA sequence `GAAATC`, the following k-mer's exist:

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

```{svgbob}
                     DnaA boxes within the ori

+--------------------------------------------------------------------+
|   :   :             :   :                            :   :         |
+-----+-----------------+--------------------------------+-----------+
      |                 |                                |           
  DnaA box          DnaA box                         DnaA box        
    
```

The DnaA boxes in an ori don't have to be exactly the same. The enzyme will still bind to them if they're slightly different.

## K-mer Reverse Complement

Given a DNA k-mer, calculate its reverse complement.

```{output}
code_kmer/src/KmerReverseComplement.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{kmer}
KmerReverseComplement
TAATCCG
```

Depending on the type of biological sequence, a k-mer may have one or more alternatives. For DNA sequences specifically, a k-mer of interest may have an alternate form. Since DNA sequences come in 2 strands, where ...
 * each strand's direction is opposite of the other,
 * each strand position has a nucleotide that complements the nucleotide at that same position on the other stand:
   * A ⟷ T
   * C ⟷ G

```{svgbob}
------------------------------>
  "A" "C" "T" "T" "C" "G" "C"
  |   |   |   |   |   |   |
  "T" "G" "A" "A" "G" "C" "G"
<------------------------------
```

, ... the reverse complement of that k-mer may be just as valid as the original k-mer. For example, if an enzyme is known to bind to a specific DNA k-mer, it's possible that it might also bind to the reverse complement of that k-mer.

## K-mer Location

Given a k-mer, find where that k-mer occurs in some larger sequence.

```{output}
code_kmer/src/KmerFindLocations.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{kmer}
KmerFindLocations
ACTGAACCTTACACTTAAAGGAGATGATGATTCAAAT
AC
```

Imagine that you know of a specific k-mer pattern that serves some function in an organism. If you see that same k-mer pattern appearing in some other related organism, it could be a sign that that k-mer pattern serves a similar function. For example, the same k-mer pattern could be used by 2 related types of bacteria as a DnaA box.

## K-mer Location Cluster

```{prereq}
K-mer Location
```

```{output}
code_kmer/src/KmerFindClusters.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{kmer}
KmerFindClusters
GGGACTGAACAAACAAATTTGGGAGGGCACGGGTTAAAGGAGATGATGATTCAAAGGGT
GGG
3
13
```

Given a k-mer, find where that k-mer clusters in some larger sequence.

An enzyme may need to bind to a specific region of DNA to begin doing its job. That is, it looks for a specific k-mer pattern to bind to, where that k-mer represents the beginning of some larger DNA region that it operates on. Since DNA is known to mutate, often times you'll find multiple copies of the same k-mer pattern clustered together -- if one copy mutated to become unusable, the other copies are still around.

For example, the DnaA box in bacteria can be found repeating multiple times in the ori region.

## K-mer Frequency

Given a sequence, count how many times each unique k-mer occurs.

The `{bm} most frequent k-mer` in a string is the k-mer that appears most often in that string.

```{output}
code_kmer/src/KmerFrequency.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{kmer}
KmerFrequency
AAAACAAAAAGAAAAAAT
4
```

From past experiments, you know that a specific region of genome clusters a certain pattern. The pattern is different for each organism, but you know that it's there.

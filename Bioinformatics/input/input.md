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

## Reverse Complement of a DNA K-mer

**WHAT**: Given a DNA k-mer, calculate its reverse complement.

**WHY**: Depending on the type of biological sequence, a k-mer may have one or more alternatives. For DNA sequences specifically, a k-mer of interest may have an alternate form. Since the DNA molecule comes as 2 strands, where ...
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

**ALGORITHM**:

```{output}
ch1_code/src/ReverseComplementADnaKmer.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
ReverseComplementADnaKmer
TAATCCG
```

## Hamming Distance Between K-mers

**WHAT**: Given 2 k-mers, the hamming distance is the number of positional mismatches between them.

**WHY**: Imagine an enzyme that looks for a specific DNA k-mer pattern to bind to. Since DNA is known to mutate, it may be that that enzyme can also bind to other k-mer patterns that are slight variations of the original. For example, that enzyme may be able to bind to both AAACTG and AAAGTG.

**ALGORITHM**:

```{output}
ch1_code/src/HammingDistanceBetweenKmers.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
HammingDistanceBetweenKmers
ACTTTGTT
AGTTTCTT
```

## Hamming Distance Neighbourhood of a DNA K-mer

```{prereq}
Hamming Distance Between K-mers
```

**WHAT**: Given a source k-mer and a minimum hamming distance, find all k-mers such within the hamming distance of the source k-mer. In other words, find all k-mers such that `hamming_distance(source_kmer, kmer) <= min_distance`.

**WHY**: Imagine an enzyme that looks for a specific DNA k-mer pattern to bind to. Since DNA is known to mutate, it may be that that enzyme can also bind to other k-mer patterns that are slight variations of the original. This algorithm finds all such variations.

**ALGORITHM**:

```{output}
ch1_code/src/FindAllDnaKmersWithinHammingDistance.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
FindAllDnaKmersWithinHammingDistance
AAAA
1
```

# K-mer Search

## Find Locations of a K-mer

```{prereq}
Hamming Distance Neighbourhood of a K-mer
Reverse Complement a DNA K-mer
```

**WHAT**: Given a k-mer, find where that k-mer occurs in some larger sequence. The search may potentially include the k-mer's variants (e.g. reverse complement).

**WHY**: Imagine that you know of a specific k-mer pattern that serves some function in an organism. If you see that same k-mer pattern appearing in some other related organism, it could be a sign that that k-mer pattern serves a similar function. For example, the same k-mer pattern could be used by 2 related types of bacteria as a DnaA box.

The enzyme that operates on that k-mer may also operate on its reverse complement as well as slight variations on that k-mer. For example, if an enzyme binds to AAAAAAAAA, it may also bind to its...
* reverse complement: TTTTTTTTT
* approximate variants: AAAAAAAAA, AAATAAAAA, AAAAAGAAA, ...
* approximate variants of its reverse complements: TTTTTTTTT, TTTTTTATT, TTCTTTTTT, ...

**ALGORITHM**:

```{output}
ch1_code/src/FindLocations.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
FindLocations
AAAAGAACCTAATCTTAAAGGAGATGATGATTCTAA
AAAA
1
True
```

## Find Clumps of a K-mer

```{prereq}
Find Locations of a K-mer
```

**WHAT**: Given a k-mer, find where that k-mer clusters in some larger sequence. The search may potentially include the k-mer's variants (e.g. reverse complement).

**WHY**: An enzyme may need to bind to a specific region of DNA to begin doing its job. That is, it looks for a specific k-mer pattern to bind to, where that k-mer represents the beginning of some larger DNA region that it operates on. Since DNA is known to mutate, often times you'll find multiple copies of the same k-mer pattern clustered together -- if one copy mutated to become unusable, the other copies are still around.

For example, the DnaA box is a special k-mer pattern used by enzymes during DNA replication. Since DNA is known to mutate, the DnaA box can be found repeating multiple times in the region of DNA known as the replication origin. Finding the DnaA box clustered in a small region is a good indicator that you've found the replication origin.

**ALGORITHM**:

```{output}
ch1_code/src/FindClumps.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
FindClumps
GGGACTGAACAAACAAATTTGGGAGGGCACGGGTTAAAGGAGATGATGATTCAAAGGGT
GGG
3
13
1
True
```

## Find Repeating K-mers

```{prereq}
Hamming Distance Neighbourhood of a K-mer
Reverse Complement a DNA K-mer
```

**WHAT**: Given a sequence, find clusters of unique k-mers within that sequence. In other words, for each unique k-mer that exists in the sequence, see if it clusters in the sequence. The search may potentially include variants of k-mer variants (e.g. reverse complements of the k-mers).

**WHY**: An enzyme may need to bind to a specific region of DNA to begin doing its job. That is, it looks for a specific k-mer pattern to bind to, where that k-mer represents the beginning of some larger DNA region that it operates on. Since DNA is known to mutate, often times you'll find multiple copies of the same k-mer pattern clustered together -- if one copy mutated to become unusable, the other copies are still around.

For example, the DnaA box is a special k-mer pattern used by enzymes during DNA replication. Since DNA is known to mutate, the DnaA box can be found repeating multiple times in the region of DNA known as the replication origin. Given that you don't know the k-mer pattern for the DnaA box but you do know the replication origin, you can scan through the replication origin for repeating k-mer patterns. If a pattern is found to heavily repeat, it's a good candidate that it's the k-mer pattern for the DnaA box.

**ALGORITHM**:

```{output}
ch1_code/src/FindRepeating.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
FindRepeating
GGGACTGAACAAACAAATTTGGGAGGGCACGGGTTAAAGGAGATGATGATTCAAAGGGT
5
1
True
```

## Find Repeating K-mers in Window

```{prereq}
Find Repeating K-mers
```

**WHAT**: Given a sequence, find regions within that sequence that contain clusters of unique k-mers. In other words, ...
 * slide a window over the cluster.
 * for each unique k-mer that exists in the window, see if it clusters in the sequence.
 
 The search may potentially include variants of k-mer variants (e.g. reverse complements of the k-mers).

**WHY**: An enzyme may need to bind to a specific region of DNA to begin doing its job. That is, it looks for a specific k-mer pattern to bind to, where that k-mer represents the beginning of some larger DNA region that it operates on. Since DNA is known to mutate, often times you'll find multiple copies of the same k-mer pattern clustered together -- if one copy mutated to become unusable, the other copies are still around.

For example, the DnaA box is a special k-mer pattern used by enzymes during DNA replication. Since DNA is known to mutate, the DnaA box can be found repeating multiple times in the region of DNA known as the replication origin. Given that you don't know the k-mer pattern for the DnaA box but you do know the replication origin, you can scan through the replication origin for repeating k-mer patterns. If a pattern is found to heavily repeat, it's a good candidate that it's the k-mer pattern for the DnaA box.

**ALGORITHM**:

```{output}
ch1_code/src/FindRepeatingInWindow.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
FindRepeatingInWindow
TTTTTTTTTTTTTCCCTTTTTTTTTCCCTTTTTTTTTTTTT
9
6
20
1
True
```

# GC Skew

**WHAT**: Given a sequence, walk over it and ...
* increment every time you spot a G.
* decrement every time you spot a C.

**WHY**: Given the DNA sequence of an organism, some segments may have lower count of Gs vs Cs.

During replication, some segments of DNA stay single-stranded for a much longer time than other segments. Single-stranded DNA is 100 times more susceptible to mutations than double-stranded DNA. Specifically, in single-stranded DNA, C has a greater tendency to mutate to T. When that single-stranded DNA re-binds to a neighbouring strand, the positions of any nucleotides that mutated from C to T will change on the neighbouring strand from G to A.

```{note}
Recall that the reverse complements of ...
 * C is G
 * A is T

It mutated from C to T. Since its now T, its complement is A.
```

Plotting the skew lets you know the rough location of segments that stayed single-stranded for a longer period of time. That information hints at special / useful locations in the organism's DNA sequence (replication origin / replication terminus).

**ALGORITHM**:

```{output}
ch1_code/src/GCSkew.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
GCSkew
CACGGGTGGTTTTGGGGGCCCCCC
```

# Stories

## Bacteria Replication

Bacteria are known to have a single chromosome of circular / looping DNA. On that DNA, the replication origin (ori) is the region in which DNA replication starts, while the replication terminus (ter) is where it ends. The ori and ter and usually placed on opposite ends of each other.

```{svgbob}
        5' ----> 3'
.---------- ori ----------.
|   | | | | | | | | | |   |
| -  ------ ori ------  - |
| - |   3' <---- 5'   | - |
| - |                 | - |
| - |                 | - |
| - |                 | - |
| -  ------ ter ------  - |
|   | | | | | | | | | |   |
`---------- ter ----------`
```

The replication process begins by a replication fork opening at the ori. As replication happens, that fork widens until the point it reaches ter...

```{svgbob}
              ori
               |
               v
     .+----------------+.
-----+                  +------
| | |                    | | | 
-----+                  +------
     `+----------------+`
               ^
               |
              ori
```
   
For each forked single-stranded DNA, DNA polymerases attach on and synthesize a new reverse complement strand so that it turns back into double-stranded DNA....

```{svgbob}
                        G <- C <- T <- T <- T <- T <- G <- . . .
                        |                            
           <-------- .- | ----------.                    
5' . . . A -> A -> A -> C -> C -> G -> A -> A -> A -> C -> . . . 3'
                     `--------------`                    

                 "Forward direction of DNA:"                       5' -----> 3'
                 "DNA polymerases moves in the reverse direction:" 5' <----- 3'
```

The process of synthesizing a reverse complement strand is different based on the section of DNA that DNA polymerase is operating on. For each single-stranded DNA, if the direction of that DNA strand is traveling from ...

 * ori to ter, it's called a forward half-strand.
 * ter to ori, it's called a reverse half-strand.

```{svgbob}
                              5' ----> 3'
                      .---------- ori ----------.
                      |   | | | | | | | | | |   |
                      | -  ------ ori ------  - |
                      | - |   3' <---- 5'   | - |
                      | - |                 | - |
                      | - |                 | - |
                      | - |                 | - |
                      | -  ------ ter ------  - |
                      |   | | | | | | | | | |   |
                      `---------- ter ----------`


      forward half-strands                      reverse half-strands 
                                                                     
            ori ->----->--.                   .-->--->--- ori        
                          |                   |                        
    .---<-  ori           v                   ^           ori ---<--.
    |                     |                   |                     |
    v                     v                   ^                     |
    |                     |                   |                     ^
    |                     v                   ^                     |
    `->---  ter           |                   |           ter --->--`  
                          |                   |                        
            ter ---<---<--`                   `--<---<--- ter        
```

Since DNA polymerase can only walk over DNA in the reverse direction (3' to 5'), the 2 reverse half-strands will quickly get walked over in one shot. A primer gets attached to the ori, then a DNA polymerase attaches to that primer to begin synthesis of a new strand. Synthesis continues until the ter is reached...

```{svgbob}
                                              "DNA polymerase synthesizing the reverse half-strand"

    "A single DNA polymerase walks the reverse half-strand,"
    "from ori to ter, as the replication fork widens."
                                             
                                                                 ori
                                                                  
                                                                  
                                        G <- C <- T <- . . . T <- G
                                        |                                         
                           <------  .-- | ----------.                       
                              A -> C -> C -> G -> A -> . . . A -> C -> T -> . . . -> G -> A -> A -> A -> C                     
                             /      `---------------`                                                     \                    
      5' . . . A -> C -> T -+                                                                              A -> C -> T . . . 3'
ter                                                                                                                               ter
      3' . . . T <- G <- A <+                                                                              T <- G <- A . . . 5'
                             \                                                       .---------------.    /                    
                              T <- G <- G <- C <- T <- . . . T <- G <- A <- . . . <- C <- T <- T <- T <- G                     
                                                                                     `-------- | ----`  ------>
                                                                                               |
                                                                  C -> T -> . . . -> G -> A -> A
                                                                  
                                                                  
                                                                 ori
``` 

For the forward half-strands, the process is much slower. Since DNA polymerase can only walk DNA in the reverse direction, the forward half-strands get replicated in small segments. That is, as the replication fork continues to grow, every ~2000 nucleotides a new primer attaches to the end of the fork on the forward strands. A new DNA polymerase attaches to each primer and walks in the reverse direction (towards the ori) to synthesize a small segment of DNA. That small segment of DNA is called an Okazaki fragment...


```{svgbob}
                                              "DNA polymerase synthesizing the forward half-strand"

    "A DNA polymerase attaches to the tip of the replication fork at"
    "the forward half-strand, roughly every 2000 nucleotide opening,"
    "to produce a small segment of DNA called an Okazaki fragment."

                                                           ori                          
      
      
                                                                       C <- T <- T <- T <- G
                                                                       |                                         
                                                              <---- .- | ----------.                                 
                              A -> C -> C -> G -> A -> . . . . . . -> G -> A -> A -> A -> C                     
                             /                                      `--------------`       \                    
      5' . . . A -> C -> T -+                                                               A -> C -> T . . . 3'
ter                                                                                                               ter
      3' . . . T <- G <- A <+                                                               T <- G <- A . . . 5'
                             \         .-------------.                                     /                    
                              T <- G <- G <- C <- T <- . . . . . . <- C <- T <- T <- T <- G                     
                                       `--------- | -` ---->                                               
                                                  |
                              A -> C -> C -> G -> A


                                                           ori                             
``` 

The replication fork will keep widening until the original 2 strands split off. DNA polymerase will have made sure that for each separated strand, a newly synthesized reverse complement is paired to it. The end result is 2 daughter chromosome where each chromosome has gaps...

```{svgbob}
                        "Two daughter chromosomes"

  "The end result is 2 daughter chromosomes, but the synthesized strand for each"
  "forward strand is chopped up into pieces (Okazaki fragments)."

          5' ----> 3'                            5' ----> 3'        
  .---------- ori ----------.            .---------- ori  - - - - -.
  |   | | | | | | | | | |   |            |   | | | | | | | | | |   :
  | -  ------ ori  - - -  - |            | -  ------ ori ------  - :
  | - |   3' <---- 5'   : - |            | - |   3' <---- 5'   | - :
  | - |                 : - |            | - |                 | - :
  | - |                 : - |            | - |                 | - :
  | - |                 : - |            | - |                 | - :
  | -  ------ ter - - -   - |            | -  ------ ter ------  - :
  |   | | | | | | | | | |   |            |   | | | | | | | | | |   :
  `---------- ter ----------`            `---------- ter  - - - - -`

  "original strand is outside strand"    "original strand is inner strand"
```

The Okazaki fragments synthesized on the forward strands end up getting sewn together by DNA ligase...

```{svgbob}
                        "Two daughter chromosomes"

  "Totally complete once DNA ligase has sewn together the Okazaki fragments."

          5' ----> 3'                            5' ----> 3'        
  .---------- ori ----------.            .---------- ori ----------.
  |   | | | | | | | | | |   |            |   | | | | | | | | | |   |
  | -  ------ ori ------  - |            | -  ------ ori ------  - |
  | - |   3' <---- 5'   | - |            | - |   3' <---- 5'   | - |
  | - |                 | - |            | - |                 | - |
  | - |                 | - |            | - |                 | - |
  | - |                 | - |            | - |                 | - |
  | -  ------ ter ------  - |            | -  ------ ter ------  - |
  |   | | | | | | | | | |   |            |   | | | | | | | | | |   |
  `---------- ter ----------`            `---------- ter ----------`
```

You now have two complete copies of the DNA.

### Find Ori and Ter

Since the forward half-strand gets its reverse complement synthesized at a much slower rate than the reverse half-strand, it stays single stranded for a much longer time. Single-stranded DNA is 100 times more susceptible to mutations than double-stranded DNA. Specifically, in single-stranded DNA, C has a greater tendency to mutate to T. This process of mutation is referred to as deanimation.

```{svgbob} 
                             ori -->---->--.
                                           |
                                           v
                                           |
                                           v
                                           |
                                           v
                                           |
                                           |
                             ter --<---<---`

                                   |
                                   | "synthesize reverse complement"
                                   v

                             ori -->---->--.       
                                | | | |    |       
                             ori --<---  - v       
                                       | - |    
"Reverse half-strand (synthesized)"    | - v    "Forward half-strand (original)"
"less Gs / more As"                    ^ - |    "less Cs / more Ts"     
                                       | - v       
                             ter -->---  - |       
                                | | | |    |       
                             ter --<---<---`       

"The forward half-strand ends up with less Cs and more Ts. As such, the"
"reverse complement strand that gets synthesized for it by DNA polymerase"
"will have less Gs and more As."
```

The reverse half-strand spends much less time as a single-stranded DNA. As such, it experiences much less C to T mutations.

```{svgbob} 
                                    .-->--->--- ori
                                    |              
                                    ^           
                                    |              
                                    ^              
                                    |              
                                    ^              
                                    |           
                                    |              
                                    `--<---<--- ter
       
                                          |
                                          | "synthesize reverse complement"
                                          v
       
                                    .-->--->---- ori       
                                    |   | | | | |          
                                    ^ -  --<---- ori       
                                    | - |              
"Reverse half-strand (original)"    ^ - v    "Forward half-strand (synthesized)"
"more normal G / A distribution"    | - |    "more normal C / more T distribution"     
                                    ^ - |                 
                                    | -  -->---- ter       
                                    |   | | | | |             
                                    `--<---<---- ter       

"The reverse half-strands end up with a more normal G and A distribution. As such, the"
"reverse complement strand that gets synthesized for it by DNA polymerase will have a"
"more normal C and T distribution."
```

Ultimately, that means that a single strand will have a different nucleotide distribution between its forward half-strand vs its backward half-strand. If the half-strand being targeted for replication is the ...

 * forward half-strand, some Cs get replaced with Ts. As such, its synthesized reverse half-strand will have less Gs.
 * reverse half-strand, most Cs are kept. As such, its synthesized forward half-strand will keep its Gs.

To simplify, the ...

 * forward half-strand: loses Cs, keeps Gs.
 * reverse half-strand: keeps Cs, loses Gs.

```{prereq}
GC Skew
```

You can use a GC skew diagram to help pinpoint where the ori and ter might be. The plot will typically form a peak where the ter is (more G vs C) and form a V where the ori is (less G vs C).

TODO: ADD GENOMES AND CALL CH1_CODE/GCSKEW_FILE ON THEM TO GENERATE GRAPH HERE

TODO: ADD GENOMES AND CALL CH1_CODE/GCSKEW_FILE ON THEM TO GENERATE GRAPH HERE

TODO: ADD GENOMES AND CALL CH1_CODE/GCSKEW_FILE ON THEM TO GENERATE GRAPH HERE

TODO: ADD GENOMES AND CALL CH1_CODE/GCSKEW_FILE ON THEM TO GENERATE GRAPH HERE

TODO: ADD GENOMES AND CALL CH1_CODE/GCSKEW_FILE ON THEM TO GENERATE GRAPH HERE

TODO: ADD GENOMES AND CALL CH1_CODE/GCSKEW_FILE ON THEM TO GENERATE GRAPH HERE

### Find the DnaA Box

Within the ori region, several smaller regions exist known as `{bm} DnaA box`es -- sequences that are either the same as or very similar to each other....

```{svgbob}
                     DnaA boxes within the ori

+--------------------------------------------------------------------+
|   :   :             :   :                            :   :         |
+-----+-----------------+--------------------------------+-----------+
      |                 |                                |           
  DnaA box          DnaA box                         DnaA box        
```

The DnaA protein binds to a DnaA box to activate the process of DNA replication. The reason why multiple DnaA box copies exist has to do with DNA mutation. If one of the copies mutates to a point where the DnaA protein doesn't bind to it, it can still bind to the other copies.

Through experiments, biologists have determined that DnaA boxes are typical 9-mers. Given that you know the where the ori of a specific bacterial organism is, you can search for 9-mer instances that may be similar to each other. Find a set of repeating 9-mers and group them if they're similar. Of the groups found, are any of them reverse complements of each other? If so, merge the groups together. These groups are are potential DnaA box candidates.


TODO: FLESH THIS OUT BY USING KMER ALGORITHMS

TODO: FLESH THIS OUT BY USING KMER ALGORITHMS

TODO: FLESH THIS OUT BY USING KMER ALGORITHMS

TODO: FLESH THIS OUT BY USING KMER ALGORITHMS

TODO: FLESH THIS OUT BY USING KMER ALGORITHMS

TODO: FLESH THIS OUT BY USING KMER ALGORITHMS

TODO: FLESH THIS OUT BY USING KMER ALGORITHMS

TODO: FLESH THIS OUT BY USING KMER ALGORITHMS

TODO: FLESH THIS OUT BY USING KMER ALGORITHMS

# Terminology

 * `{bm} 5'` (`{bm} 5 prime`) / `{bm} 3'` (`{bm} 3 prime`) - 5' (5 prime) and 3' (3 prime) describe the opposite ends of DNA. The chemical structure at each end is what defines if it's 5' or 3' -- each end is guaranteed to be different from the other. The forward direction on DNA is defined as 5' to 3', while the backwards direction is 3' to 5'.

   Two complementing DNA strands will always be attached in opposite directions.
 
   ```{svgbob}
         forward
        --------->
   5' -+-+-+-+-+-+-+- 3'
       | | | | | | |
   3' -+-+-+-+-+-+-+- 5'
        <---------
         backward
   ```
 
 * `{bm} DNA polymerase` - An enzyme that replicates a strand of DNA. That is, DNA polymerase walks over a single strand of DNA bases (not the strand of base pairs) and  generates a strand of complements. Before DNA polymerase can attach itself and start replicating DNA, it requires a primer.
 
 
   ```{svgbob}
                           G <- C <- T <- T <- T <- T <- G <- . . .
                           |                            
              <-------- .- | ----------.                    
   5' . . . A -> A -> A -> C -> C -> G -> A -> A -> A -> C -> . . . 3'
                        `--------------`                    
   
                    "Forward direction of DNA:"                       5' -----> 3'
                    "DNA polymerases moves in the reverse direction:" 5' <----- 3'
   ```
 
   DNA polymerase is unidirectional, meaning that it can only walk a DNA strand in one direction: reverse (3' to 5') 
 
 * `{bm} primer` - A primer is a short strand of RNA that binds to some larger strand of DNA (single bases, not a strand of base pairs) and allows DNA synthesis to  happen. That is, the primer acts as the entry point for special enzymes DNA polymerases. DNA polymerases bind to the primer to get access to the strand.
 
 * `{bm} replication fork` - The process of DNA replication requires that DNA's 2 complementing strands be unwound and split open. The area where the DNA starts to  split is called the replication fork. In bacteria, the replication fork starts at the replication origin and keeps expanding until it reaches the replication terminus.  Special enzymes called DNA polymerases walk over each unwound strand and create complementing strands.
 
   ```{svgbob}
                 ori
                  |
                  v
        .+----------------+.
   -----+                  +------
   | | |                    | | | 
   -----+                  +------
        `+----------------+`
                  ^
                  |
                 ori
   ```
 
 * `{bm} replication origin` (`{bm} ori/\b(ori)\b/i`) - The point in DNA at which replication starts.
 
 * `{bm} replication terminus` (`{bm} ter/\b(ter)\b/i`) - The point in DNA at which replication ends.

 * `{bm} forward half-strand` / `{bm} reverse half-strand/(reverse half-strand|backward half-strand|backwards half-strand)/i` - Bacteria are known to have a single chromosome of circular / looping DNA. In this DNA, the replication origin (ori) is the region of DNA where replication starts, while the replication terminus (ter) is where replication ends.

   ```{svgbob}
           5' ----> 3`
   .---------- ori ----------.
   |   | | | | | | | | | |   |
   | -  ------ ori ------  - |
   | - |   3' <---- 5`   | - |
   | - |                 | - |
   | - |                 | - |
   | - |                 | - |
   | -  ------ ter ------  - |
   |   | | | | | | | | | |   |
   `---------- ter ----------`
   ```

   If you split up the DNA based on ori and ter being cutting points, you end up with 4 distinct strands. Given that the direction of a strand is 5' to 3', if the direction of the strand starts at...

   * ori and ends at ter, it's called the forward half-strand.

     ```{svgbob}
      forward half-strands  
                            
             ori ->----->--.
                           |
     .---<-  ori           v
     |                     |
     v                     v
     |                     |
     |                     v
     `->---  ter           |
                           |
             ter ---<---<--`
     ```

   * ter and ends at ori, it's called the reverse half-strand.

     ```{svgbob}
       reverse half-strands 
                            
     .-->--->--- ori        
     |                      
     ^           ori ---<--.
     |                     |
     ^                     |
     |                     ^
     ^                     |
     |           ter --->--`
     |                      
     `--<---<--- ter        
     ```

   ```{note}
   * Forward half-strand is the same as lagging half-strand.
   * Reverse half-strand is the same as leading half-strand.
   ```

 * `{bm} leading half-strand` / `{bm} lagging half-strand` - Given the 2 strands tha make up a DNA molecule, the strand that goes in the...

   * reverse direction (3' to 5') is called the leading half-strand.
   * forward direction (5' to 3') is called the lagging half-strand.

   This nomenclature has to do with DNA polymerase. Since DNA polymerase can only walk in the reverse direction (3' to 5'), it synthesizes the leading half-strand in one shot. For the lagging half-strand (5' to 3'), multiple DNA polymerases have to used to synthesize DNA, each binding to the lagging strand and walking backwards a small amount to generate a small fragment of DNA (Okazaki fragment). the process is much slower for the lagging half-strand, that's why it's called lagging.

   ```{note}
   * Leading half-strand is the same as reverse half-strand.
   * Lagging half-strand is the same as forward half-strand.
   ```

 * `{bm} Okazaki fragment` - A small fragment of DNA generated by DNA polymerase for forward half-strands. DNA synthesis for the forward half-strands can only happen in small pieces. As the fork open ups every ~2000 nucleotides, DNA polymerase attaches to the end of the fork on the forward half-strand and walks in reverse to generate that small segment (DNA polymerase can only walk in the reverse direction).

 * `{bm} DNA ligase` - An enzyme that sews together short segments of DNA called Okazaki fragments by binding the phosphate group on the end of one strand with the deoxyribose group on the other strand.

 * `{bm} single stranded DNA/(single stranded DNA|single-stranded DNA)/i` - A single strand of DNA, not bound to a strand of its reverse complements.

   ```{svgbob}
   5' . . . A -> A -> A -> C -> C -> G -> A -> A -> A -> C -> . . . 3'
   ```

 * `{bm} double stranded DNA/(double stranded DNA|double-stranded DNA)/i` - Two strands of DNA bound together, where each strand is the reverse complement of the other.

   ```{svgbob}
   3' . . . T <- T <- T <- G <- C <- T <- T <- T <- T <- G <- . . . 5'
            |    |    |    |    |    |    |    |    |    | 
   5' . . . A -> A -> A -> C -> C -> G -> A -> A -> A -> C -> . . . 3'    
   ```
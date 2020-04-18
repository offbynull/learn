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

## Reverse Complement a DNA K-mer

Given a DNA k-mer, calculate its reverse complement.

```{output}
code_kmer/src/ReverseComplementADnaKmer.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{kmer}
ReverseComplementADnaKmer
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

## Find Locations of a Known K-mer

Given a k-mer, find where that k-mer occurs in some larger sequence.

```{output}
code_kmer/src/FindLocationsOfAKnownKmer.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{kmer}
FindLocationsOfAKnownKmer
ACTGAACCTTACACTTAAAGGAGATGATGATTCAAAT
AC
```

Imagine that you know of a specific k-mer pattern that serves some function in an organism. If you see that same k-mer pattern appearing in some other related organism, it could be a sign that that k-mer pattern serves a similar function. For example, the same k-mer pattern could be used by 2 related types of bacteria as a DnaA box.

## Find Clumps of a Known K-mer

```{prereq}
K-mer Location
```

Given a k-mer, find where that k-mer clusters in some larger sequence.

```{output}
code_kmer/src/FindClumpsOfAKnownKmer.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{kmer}
FindClumpsOfAKnownKmer
GGGACTGAACAAACAAATTTGGGAGGGCACGGGTTAAAGGAGATGATGATTCAAAGGGT
GGG
3
13
```

An enzyme may need to bind to a specific region of DNA to begin doing its job. That is, it looks for a specific k-mer pattern to bind to, where that k-mer represents the beginning of some larger DNA region that it operates on. Since DNA is known to mutate, often times you'll find multiple copies of the same k-mer pattern clustered together -- if one copy mutated to become unusable, the other copies are still around.

For example, the DnaA box in bacteria can be found repeating multiple times in the ori region.

## Count a Sequence's K-mers

Given a sequence, count how many times each unique k-mer in that sequence occurs.

```{output}
code_kmer/src/CountASequencesKmers.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{kmer}
CountASequencesKmers
AAAACAAAAAGAAAAAAT
4
```

From past experiments, you know that a specific region of genome clusters a certain pattern. The pattern is different for each organism, but you know that it's there.

## Find a Sequence's K-mer Clusters

```{prereq}
Find Where a K-mer Clusters
```


```{output}
code_kmer/src/FindASequencesKmerClusters.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{kmer}
FindASequencesKmerClusters
GGGACTGAACAAACAAATTTGGGAGGGCACGGGTTAAAGGAGATGATGATTCAAAGGGT
3
2
13
```

Given a sequence, find clusters of unique k-mers within that sequence. In other words, for each unique k-mer that exists in the sequence, see if it clusters in the sequence.

An enzyme may need to bind to a specific region of DNA to begin doing its job. That is, it looks for a specific k-mer pattern to bind to, where that k-mer represents the beginning of some larger DNA region that it operates on. Since DNA is known to mutate, often times you'll find multiple copies of the same k-mer pattern clustered together -- if one copy mutated to become unusable, the other copies are still around.

For example, the DnaA box in bacteria can be found repeating multiple times in the ori region. If you don't know where the ori is, searching for clusters can give a list of potential locations.

# Stories

## Find the Replication Origin

Bacteria are known to have a single chromosome of circular / looping DNA. In this DNA, the replication origin (ori) is the region of DNA where replication starts, while the replication terminus (ter) is where replication ends.

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

The replication process begins by a replication fork opening at the ori. As replication happens, that fork widens up until the point it reaches ter.

```{svgbob}
       replication origin
                |
                v
        +-+-+-+-+-+-+-+-+
       /  | | | | | | |  \
+-+-+-+                   +-+-+-+
| | | |                   | | | |
+-+-+-+                   +-+-+-+
       \  | | | | | | |  /
        +-+-+-+-+-+-+-+-+
                ^
                |
       replication origin
```
   
DNA polymerases attach on to the forked strands and synthesize a strand of DNA with complementing bases.

```{svgbob}
                        G <- C <- T <- T <- T <- T <- G <- . . .
                        |                            
           <-------- .- | ----------.                    
5' . . . A -> A -> A -> C -> C -> G -> A -> A -> A -> C -> . . . 3'
                     `--------------`                    

                 "Direction of DNA:"  5' ----> 3'
                 "DNA polymerases moves in the reverse direction"
```

The process of replication is different depending on the segment of DNA. That is, if you use ori and ter as cutting points, you'll have 4 different strands of DNA. Of those strands, if the directionality of the strand is going from ...

 * from ori to ter, it's called a forward half-strand.
 * from ter to ori, it's called a reverse half-strand.

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

For the forward half-strands, the process is much slower. Since DNA polymerase can only walk DNA in the reverse direction, the foreword half-strands get replicated in small segments. That is, as the replication fork continues to grow, every ~2000 nucleotides a new primer attaches to the end of the fork on the forward strands. A new DNA polymerase attaches to eacg primer and walks in the reverse direction (towards the ori) to synthesize a small segment of DNA. That small segment of DNA is called an Okazaki fragment...


```{svgbob}
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

TODO: FLESH THIS OUT BY TALKING ABOUT SKEW DIAGRAM

TODO: FLESH THIS OUT BY TALKING ABOUT SKEW DIAGRAM

TODO: FLESH THIS OUT BY TALKING ABOUT SKEW DIAGRAM

TODO: FLESH THIS OUT BY TALKING ABOUT SKEW DIAGRAM

TODO: FLESH THIS OUT BY TALKING ABOUT SKEW DIAGRAM

TODO: FLESH THIS OUT BY TALKING ABOUT SKEW DIAGRAM

TODO: FLESH THIS OUT BY TALKING ABOUT SKEW DIAGRAM


## Find the DnaA Box

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
   T    G    G  
             ^    
       .---+ | +-----.  ----------> 
   A    C    C    G    A    A    A    C  
       `-------------` 
   ```
 
   DNA polymerase is unidirectional, meaning that it can only walk a DNA strand in one direction. That direction is backwards (3' to 5') 
 
 * `{bm} primer` - A primer is a short strand of RNA that binds to some larger strand of DNA (single bases, not a strand of base pairs) and allows DNA synthesis to  happen. That is, the primer acts as the entry point for special enzymes DNA polymerases. DNA polymerases bind to the primer to get access to the strand.
 
 * `{bm} replication fork` - The process of DNA replication requires that DNA's 2 complementing strands be unwound and split open. The area where the DNA starts to  split is called the replication fork. In bacteria, the replication fork starts at the replication origin and keeps expanding until it reaches the replication terminus.  Special enzymes called DNA polymerases walk over each unwound strand and create complementing strands.
 
   ```{svgbob}
          replication origin
                   |
                   v
           +-+-+-+-+-+-+-+-+
          /  | | | | | | |  \
   +-+-+-+                   +-+-+-+
   | | | |                   | | | |
   +-+-+-+                   +-+-+-+
          \  | | | | | | |  /
           +-+-+-+-+-+-+-+-+
                   ^
                   |
          replication origin
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
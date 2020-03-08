package com.offbynull.lcm;

import com.google.common.base.Preconditions;
import static com.google.common.base.Throwables.getStackTraceAsString;
import com.google.common.collect.SortedMultiset;
import com.google.common.collect.TreeMultiset;
import java.io.IOException;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;
import java.util.SortedSet;
import java.util.TreeSet;

public class PrimeFactorizeMultiples {
    public static void main(String[] args) throws IOException {
        try (Writer writer = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            writer.append("<div style=\"border:1px solid black;\">\n\n");
            writer.append("`{bm-disable-all}`\n\n");
            try (Scanner scanner = new Scanner(Files.newBufferedReader(Path.of("/input/input.data")))) {
                int num1 = scanner.nextInt();
                int num2 = scanner.nextInt();
                
                Preconditions.checkArgument(num1 > 0);
                Preconditions.checkArgument(num2 > 0);

                //MARKDOWN_ISOLATE
                SortedMultiset<Integer> num1Primes = calculatePrimeFactors(num1);
                SortedMultiset<Integer> num2Primes = calculatePrimeFactors(num2);
                
                SortedSet<Integer> distinctPrimes = new TreeSet<>();
                distinctPrimes.addAll(num1Primes.elementSet());
                distinctPrimes.addAll(num2Primes.elementSet());
                
                int leastCommonMultiple = 1;
                SortedMultiset<Integer> leastCommonMultiplePrimes = TreeMultiset.create();
                for (int prime : distinctPrimes) {
                    int num1Count = num1Primes.count(prime);
                    int num2Count = num2Primes.count(prime);
                    if (num1Count >= num2Count) {
                        for (int i = 0; i < num1Count; i++) {
                            leastCommonMultiple *= prime;
                        }
                        leastCommonMultiplePrimes.add(prime, num1Count);
                    } else {
                        for (int i = 0; i < num2Count; i++) {
                            leastCommonMultiple *= prime;
                        }
                        leastCommonMultiplePrimes.add(prime, num2Count);
                    }
                }
                //MARKDOWN_ISOLATE

                writer.append("prime factor occurence counts of " + num1 + " = " + num1Primes + "\n\n");
                writer.append("prime factor occurence counts of " + num2 + " = " + num2Primes + "\n\n");
                writer.append("least common multiple is " + leastCommonMultiple + " = " + leastCommonMultiplePrimes + "\n\n");
            } catch (Exception e) {
                writer.append(getStackTraceAsString(e));
            } finally {
                writer.append("`{bm-enable-all}`\n\n");
                writer.append("</div>\n\n");
            }
        }
    }
    
    
    
    
    
    private static final SortedMultiset<Integer> calculatePrimeFactors(int input) {
        Node root = factorTree(input);
        List<Integer> primeFactors = new ArrayList<>();
        
        walkPrimeFactorTree(root, primeFactors);
       
        SortedMultiset<Integer> primeFactorsSet = TreeMultiset.create();
        primeFactorsSet.addAll(primeFactors);
        
        return primeFactorsSet;
    }
    
    private static final void walkPrimeFactorTree(Node node, List<Integer> primeFactors) {
        if (node.left == null && node.right == null) {
            primeFactors.add(node.value);
            return;
        }
        
        walkPrimeFactorTree(node.left, primeFactors);
        walkPrimeFactorTree(node.right, primeFactors);
    }
    
    private static final Node factorTree(int input) {
        Set<FactorPair> factorPairs = getFactorPairs(input);
        
        // remove factor pairs [1, input] and/or [input, 1], then pick a factor
        FactorPair factorPair = factorPairs.stream()
                .filter(fp -> fp.factor1 != 1 && fp.factor2 != 1)
                .findFirst().orElse(null);
        
        if (factorPair == null) {
            Node node = new Node();
            node.value = input;
            node.left = null;
            node.right = null;
            return node;
        } else {
            Node node = new Node();
            node.value = input;
            node.left = factorTree(factorPair.factor1);
            node.right = factorTree(factorPair.factor2);
            return node;
        }
    }
    
    private static final class Node {
        private int value;
        private Node left;
        private Node right;
    }
    
    private static final Set<FactorPair> getFactorPairs(int input) {
        Set<FactorPair> factorPairs = new HashSet<>();
        for (int factor1 = 1; factor1 <= input; factor1++) {
            int factor2 = input / factor1;
            boolean divHadRemainder = input % factor1 > 0;
            if (!divHadRemainder) {
                factorPairs.add(new FactorPair(factor1, factor2));
            }
            if (factor2 <= factor1) {
                break;
            }
        }
        return factorPairs;
    }
    
    private static final class FactorPair {
        private final int factor1;
        private final int factor2;

        public FactorPair(int factor1, int factor2) {
            this.factor1 = factor1;
            this.factor2 = factor2;
        }

        @Override
        public int hashCode() {
            int hash = 3;
            hash = 37 * hash + this.factor1;
            hash = 37 * hash + this.factor2;
            return hash;
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) {
                return true;
            }
            if (obj == null) {
                return false;
            }
            if (getClass() != obj.getClass()) {
                return false;
            }
            final FactorPair other = (FactorPair) obj;
            if (this.factor1 != other.factor1) {
                return false;
            }
            if (this.factor2 != other.factor2) {
                return false;
            }
            return true;
        }

        @Override
        public String toString() {
            return factor1 + "/" + factor2;
        }
        
    }
}

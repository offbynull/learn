package com.offbynull.factor;

import com.google.common.base.Preconditions;
import static com.google.common.base.Throwables.getStackTraceAsString;
import java.io.IOException;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.Set;
import java.util.TreeSet;
import static org.apache.commons.lang3.StringUtils.repeat;

public class Ladder {
    public static void main(String[] args) throws IOException {
        try (Writer writer = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            writer.append("<div style=\"border:1px solid black;\">\n\n");
            writer.append("`{bm-disable-all}`\n\n");
            try (Scanner scanner = new Scanner(Files.newBufferedReader(Path.of("/input/input.data")))) {
                int num = scanner.nextInt();
                
                Preconditions.checkArgument(num >= 1);
                
                List<Integer> primeFactors = ladder(num);
                Integer oldNum = null;
                String output = "";
                while (primeFactors.size() > 1) {
                    int nextPrime = primeFactors.remove(0);
                    int quotient = num / nextPrime;
                    
                    int indent = calculateIndent(output, oldNum, num);
                    output = repeat(' ', indent + 1) + nextPrime + ")" + num + "\n" + output;
                    
                    oldNum = num;
                    num = quotient;
                }
                
                int lastPrime = primeFactors.remove(0);
                int indent = calculateIndent(output, oldNum, lastPrime);
                output = repeat(' ', indent + 1) + lastPrime + "\n" + output;
                
                writer.append("```\n" + output + "\n```");
                writer.append("\n\n");
            } catch (Exception e) {
                writer.append(getStackTraceAsString(e));
            } finally {
                writer.append("`{bm-enable-all}`\n\n");
                writer.append("</div>\n\n");
            }
        }
    }

    private static int calculateIndent(String output, Integer oldNum, int num) {
        int indent = output.indexOf(")");
        if (indent == -1) {
            indent = 0;
        } else {
            indent += 1;
        }
        if (oldNum != null) {
            indent += oldNum.toString().length() - ("" + num).length();
        }
        return indent;
    }
    
    private static final List<Integer> ladder(int input) {
        //MARKDOWN_ISOLATE
        List<Integer> primeFactors = new ArrayList<>();

        while (!isPrime(input)) {
            resetPrimeCounter();
            
            int nextPrime;
            do {
                nextPrime = getNextPrime();
            } while (input % nextPrime != 0); // while it's NOT divisible (if it has a remainder)
            
            primeFactors.add(nextPrime);
            input = input / nextPrime;
        }
        primeFactors.add(input);
        //MARKDOWN_ISOLATE
        
        return primeFactors;
    }
    
    private static int nextPossiblePrime = 2;
    
    private static void resetPrimeCounter() {
        nextPossiblePrime = 2;
    }
    
    private static int getNextPrime() {
        while (true) {
            if (isPrime(nextPossiblePrime)) { // if only 2 factors, those factors are guaranteed to be {1, input}
                int ret = nextPossiblePrime;
                nextPossiblePrime++;
                return ret;
            } else {
                nextPossiblePrime++;
            }
        }
    }
   
    private static boolean isPrime(int input) {
        return getFactors(input).size() == 2; // if only 2 factors, those factors are guaranteed to be {1, input}
    }
    
    private static final Set<Integer> getFactors(int input) {
        TreeSet<Integer> factors = new TreeSet<>();
        for (int factor1 = 1; factor1 <= input; factor1++) {
            int factor2 = input / factor1;
            boolean divHadRemainder = input % factor1 > 0;
            if (!divHadRemainder) {
                factors.add(factor1);
                factors.add(factor2);
            }
            if (factor2 <= factor1) {
                break;
            }
        }
        return factors;
    }
}

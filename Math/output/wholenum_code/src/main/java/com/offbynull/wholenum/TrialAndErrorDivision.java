package com.offbynull.wholenum;

import com.google.common.base.Preconditions;
import static com.google.common.base.Throwables.getStackTraceAsString;
import java.io.IOException;
import java.io.Writer;
import static java.lang.Integer.parseInt;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Scanner;
import static org.apache.commons.lang3.StringUtils.repeat;

public class TrialAndErrorDivision {
    
    public static void main(String[] args) throws IOException {
//        String input = "98 3";
        try (Writer writer = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
//        try (Writer writer = new PrintWriter(System.out)) {
            writer.append("<div style=\"border:1px solid black;\">\n\n");
            writer.append("`{bm-linker-off}`\n\n");
            try (Scanner scanner = new Scanner(Files.newBufferedReader(Path.of("/input/input.data")))) {
//            try (Scanner scanner = new Scanner(input)) {
                int dividend = scanner.nextInt();
                int divisor = scanner.nextInt();
                
                Preconditions.checkArgument(dividend >= 0);
                Preconditions.checkArgument(divisor > 0);
                
                writer.append("PERFORMING " + dividend + " / " + divisor + "...\n\n");
                
                if (dividend == 0) {
                    writer.append("FOUND: " + dividend + " / " + divisor + " = 0R0\n\n");
                    return;
                }
                
                //MARKDOWN_ISOLATE
                Range range = pickStartingRange(dividend);
                writer.append("START RANGE: [" + range.min + ", " + range.max + "]\n\n");
                
                int quotient;
                int remainder;
                while (true) {
                    int minTest = divisor * range.min;
                    int maxTest = divisor * range.max;
                    
                    writer.append(" * " + divisor + " * " + range.min + " = " + minTest + "\n");
                    writer.append(" * " + divisor + " * " + range.max + " = " + maxTest + "\n\n");
                    
                    // check if found
                    if (minTest == dividend) { // found as min
                        quotient = range.min;
                        remainder = 0;
                        break;
                    }

                    if (maxTest == dividend) { // found as max
                        quotient = range.max;
                        remainder = 0;
                        break;
                    }
                    
                    if (minTest < dividend && maxTest > dividend && range.max - range.min == 1) { // found between min and max
                        quotient = range.min;
                        remainder = dividend - minTest;
                        break;
                    }
                    
                    // not found, so modify range
                    if (minTest < dividend && maxTest > dividend) {
                        narrowRange(dividend, divisor, range);
                        writer.append("NARROWING RANGE: [" + range.min + ", " + range.max + "]\n\n");
                    } else if (minTest < dividend && maxTest < dividend) {
                        moveUpRange(range);
                        writer.append("INCREASING RANGE: [" + range.min + ", " + range.max + "]\n\n");
                    } else if (minTest > dividend && maxTest > dividend) {
                        moveDownRange(range);
                        writer.append("DECREASING RANGE: [" + range.min + ", " + range.max + "]\n\n");
                    }
                }
                
                writer.append("FOUND: " + dividend + " / " + divisor + " = " + quotient + "R" + remainder + "\n\n");
                //MARKDOWN_ISOLATE
            } catch (Exception e) {
                writer.append(getStackTraceAsString(e));
            } finally {
                writer.append("`{bm-linker-on}`\n\n");
                writer.append("</div>\n\n");
            }
        }
    }
    
    private static int digitCount(int num) {
        return ("" + num).length();
    }
    
    private static Range pickStartingRange(int dividend) {
        return new Range(
                parseInt("1" + repeat("0", digitCount(dividend) - 1)),
                parseInt("1" + repeat("0", digitCount(dividend)))
        );
    }
    
    private static void narrowRange(int dividend, int divisor, Range range) {
        int diff = range.max - range.min - 1;
        int adjustment = parseInt("1" + repeat("0", digitCount(diff) - 1));
        
        int minTest = divisor * range.min;
        int maxTest = divisor * range.max;
        
        if (dividend - minTest > maxTest - dividend) {
            range.min += adjustment;
        } else {
            range.max -= adjustment;
        }
    }
    
    private static void moveUpRange(Range range) {
        int diff = range.max - range.min;
        
        int adjustment = parseInt("1" + repeat("0", digitCount(diff) - 1));
        
        range.min += adjustment;
        range.max += adjustment;
    }
    
    private static void moveDownRange(Range range) {
        int diff = range.max - range.min;
        
        int adjustment = parseInt("1" + repeat("0", digitCount(diff) - 1));
        
        range.min -= adjustment;
        range.max -= adjustment;
    }
    
    private static final class Range {
        private int min;
        private int max;

        public Range(int min, int max) {
            this.min = min;
            this.max = max;
        }
    }
}

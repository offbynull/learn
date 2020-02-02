package com.offbynull.wholenum;

import static com.google.common.base.Throwables.getStackTraceAsString;
import java.io.IOException;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import static java.util.Arrays.stream;
import java.util.Scanner;
import static java.util.stream.Collectors.joining;
import java.util.stream.IntStream;
import static java.util.stream.IntStream.concat;
import static java.util.stream.IntStream.range;
import static org.apache.commons.lang3.StringUtils.repeat;

public class MainAddition {
    
    public static void main(String[] args) throws IOException {
        try (Writer writer = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            writer.append("<div style=\"border:1px solid black;\">\n\n");
            writer.append("`{bm-linker-off}`\n\n");
            try (Scanner scanner = new Scanner(Files.newBufferedReader(Path.of("/input/input.data")))) {
                String num1 = scanner.next("[0-9]+");
                String num2 = scanner.next("[0-9]+");

                int[] num1Digits = num1.chars().map(i -> i - '0').toArray();
                int[] num2Digits = num2.chars().map(i -> i - '0').toArray();
                
                writer.append("Adding " + num1 + " to " + num2 + "\n\n");
                
                new MainAddition(writer).add(num1Digits, num2Digits);
            } catch (Exception e) {
                writer.append(getStackTraceAsString(e));
            } finally {
                writer.append("`{bm-linker-on}`\n\n");
                writer.append("</div>\n\n");
            }
        }
        
//        int[] num1Digits = "999".chars().map(i -> i - '0').toArray();
//        int[] num2Digits = "999".chars().map(i -> i - '0').toArray();
//        int[] resDigits = add(num1Digits, num2Digits);
//        System.out.println(Arrays.toString(resDigits));
        
//        int[] num1Digits = "999".chars().map(i -> i - '0').toArray();
//        int[] num2Digits = "999".chars().map(i -> i - '0').toArray();
//        int[] resDigits = add(num1Digits, num2Digits);
//        System.out.println(Arrays.toString(resDigits));
        
//        int[] num1Digits = "999".chars().map(i -> i - '0').toArray();
//        int[] num2Digits = "999".chars().map(i -> i - '0').toArray();
//        int[] resDigits = add(num1Digits, num2Digits);
//        System.out.println(Arrays.toString(resDigits));
        
//        int[] num1Digits = "999".chars().map(i -> i - '0').toArray();
//        int[] num2Digits = "999".chars().map(i -> i - '0').toArray();
//        int[] resDigits = add(num1Digits, num2Digits);
//        System.out.println(Arrays.toString(resDigits));
    }
    
    private final Writer out;

    public MainAddition(Writer writer) {
        this.out = writer;
    }
    
    static final int[][][] DIGIT_ADD_CACHE = {
        {{0  },{1  },{2  },{3  },{4  },{5  },{6  },{7  },{8  },{9  }},
        {{1  },{2  },{3  },{4  },{5  },{6  },{7  },{8  },{9  },{1,0}},
        {{2  },{3  },{4  },{5  },{6  },{7  },{8  },{9  },{1,0},{1,1}},
        {{3  },{4  },{5  },{6  },{7  },{8  },{9  },{1,0},{1,1},{1,2}},
        {{4  },{5  },{6  },{7  },{8  },{9  },{1,0},{1,1},{1,2},{1,3}},
        {{5  },{6  },{7  },{8  },{9  },{1,0},{1,1},{1,2},{1,3},{1,4}},
        {{6  },{7  },{8  },{9  },{1,0},{1,1},{1,2},{1,3},{1,4},{1,5}},
        {{7  },{8  },{9  },{1,0},{1,1},{1,2},{1,3},{1,4},{1,5},{1,6}},
        {{8  },{9  },{1,0},{1,1},{1,2},{1,3},{1,4},{1,5},{1,6},{1,7}},
        {{9  },{1,0},{1,1},{1,2},{1,3},{1,4},{1,5},{1,6},{1,7},{1,8}}        
    };
    
    int[] add(int[] num1Digits, int[] num2Digits) throws IOException {
        borderStart();
        
        try {
            int maxLen = Math.max(num1Digits.length, num2Digits.length);
            num1Digits = padWithZeros(num1Digits, maxLen);
            num2Digits = padWithZeros(num2Digits, maxLen);

            int[] result = IntStream.range(0, maxLen).map(i -> 0).toArray();
            int[] carryOverDigits = null;
            for (int i = maxLen - 1; i >= 0; i--) {
                int num1Digit = i >= num1Digits.length ? 0 : num1Digits[i];
                int num2Digit = i >= num2Digits.length ? 0 : num2Digits[i];
                int[] digitsAdded = DIGIT_ADD_CACHE[num1Digit][num2Digit];

                borederReset();
                println("pos ", maxLen - i, " -- adding ", isolate(num1Digit, i, maxLen), " and ", isolate(num2Digit, i, maxLen));
                println("start state: ", "carry-over=",  carryOverDigits, ".");
                println(num1Digit, " + ", num2Digit, " is ", digitsAdded, ".");

                if (carryOverDigits != null) {
                    println("carry-over of ", carryOverDigits, " exists, ", digitsAdded, " + ", carryOverDigits, "...");
                    digitsAdded = add(carryOverDigits, digitsAdded);
                    carryOverDigits = null;
                    println("... is ", digitsAdded, " (carry-over reset).");
                }

                switch (digitsAdded.length) {
                    case 1:
                        result[i] = digitsAdded[0];
                        break;
                    case 2:
                        result[i] = digitsAdded[1];
                        carryOverDigits = new int[] { digitsAdded[0] };
                        break;
                    default:
                        throw new IllegalStateException(); // should never happen
                }
                
                println("end state: ", "result=", isolate(result, i), " / carry-over=",  carryOverDigits, ".");
            }

            borederReset();
            if (carryOverDigits != null) {
                result = concat(stream(carryOverDigits), stream(result)).toArray();
                println("prepend remaining carry-over of ", carryOverDigits, ".");
                println("end state: ", "result=", isolate(result, 0), ".");
            }
            
            borederReset();
            println("result is ", result);

            return result;
        } finally {
            borderStop();
        }
    }
    
    private int indent = -2;
    private boolean firstLine = true;
    private void borderStart() {
        indent += 2;
        firstLine = true;
    }
    
    private void borderStop() {
        indent -= 2;
    }
    
    private void borederReset() {
        firstLine = true;
    }
    
    private void println(Object... objs) throws IOException {
        if (firstLine) {
            out.append(repeat(' ', indent) + " * ");
            firstLine = false;
        } else {
            out.append(repeat(' ', indent) + "   ");
        }
        
        for (Object obj : objs) {
            if (obj instanceof int[]) {
                out.append(stream((int[]) obj).mapToObj(d -> d + "").collect(joining()));
            } else {
                out.append(obj == null ? "null" : obj.toString());
            }
        }
        out.append("\n\n");
    }
    
    private static String isolate(int[] digits, int idx) {
        String ret = "";
        for (int i = 0; i < digits.length; i++) {
            ret += i == idx ? "" + digits[i] : "x";
        }
        return ret;
    }
    
    private static String isolate(int digit, int idx, int max) {
        String ret = "";
        for (int i = 0; i < max; i++) {
            ret += i == idx ? "" + digit : "x";
        }
        return ret;
    }
    
    private static int[] padWithZeros(int[] digits, int len) {
        return concat(range(digits.length, len).map(i -> 0), stream(digits)).toArray();
    }
}

package com.offbynull.wholenum;

import static com.google.common.base.Throwables.getStackTraceAsString;
import java.io.IOException;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import static java.util.Arrays.stream;
import java.util.List;
import java.util.Scanner;
import static java.util.stream.Collectors.joining;
import java.util.stream.IntStream;
import static java.util.stream.IntStream.concat;
import static java.util.stream.IntStream.range;
import static org.apache.commons.lang3.StringUtils.repeat;

public class MainMultiplication {
    
    public static void main(String[] args) throws IOException {
        try (Writer writer = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            writer.append("<div style=\"border:1px solid black;\">\n\n");
            writer.append("`{bm-linker-off}`\n\n");
            try (Scanner scanner = new Scanner(Files.newBufferedReader(Path.of("/input/input.data")))) {
                String num1 = scanner.next("[0-9]+");
                String num2 = scanner.next("[0-9]+");

                int[] num1Digits = num1.chars().map(i -> i - '0').toArray();
                int[] num2Digits = num2.chars().map(i -> i - '0').toArray();
                
                writer.append("Multiplying " + num1 + " and " + num2 + "\n\n");
                
                new MainMultiplication(writer).mult(num1Digits, num2Digits);
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

    public MainMultiplication(Writer writer) {
        this.out = writer;
    }
    
    //MARKDOWN_ISOLATE
    static final int[][][] DIGIT_MULT_CACHE = {
        {{0  },{0  },{0  },{0  },{0  },{0  },{0  },{0  },{0  },{0  }},
        {{0  },{1  },{2  },{3  },{4  },{5  },{6  },{7  },{8  },{9  }},
        {{0  },{2  },{4  },{6  },{8  },{1,0},{1,2},{1,4},{1,6},{1,8}},
        {{0  },{3  },{6  },{9  },{1,2},{1,5},{1,8},{2,1},{2,4},{2,7}},
        {{0  },{4  },{8  },{1,2},{1,6},{2,0},{2,4},{2,8},{3,2},{3,6}},
        {{0  },{5  },{1,0},{1,5},{2,0},{2,5},{3,0},{3,5},{4,0},{4,5}},
        {{0  },{6  },{1,2},{1,8},{2,4},{3,0},{3,6},{4,2},{4,8},{5,4}},
        {{0  },{7  },{1,4},{2,1},{2,8},{3,5},{4,2},{4,9},{5,6},{6,3}},
        {{0  },{8  },{1,6},{2,4},{3,2},{4,0},{4,8},{5,6},{6,4},{7,2}},
        {{0  },{9  },{1,8},{2,7},{3,6},{4,5},{5,4},{6,3},{7,2},{8,1}}        
    };
    
    int[] mult(int[] topDigits, int[] bottomDigits) throws IOException {
        printBulletOpen();
        
        try {
            int maxLen = Math.max(topDigits.length, bottomDigits.length);
            topDigits = prependWithZeros(topDigits, maxLen);
            bottomDigits = prependWithZeros(bottomDigits, maxLen);

            List<int[]> iterationResults = new ArrayList<>();
            for (int i = maxLen - 1; i >= 0; i--) {
                int bottomDigit = bottomDigits[i];
                int[] carryOverDigits = null;
                
                printBulletNewLine();
                println("isolating bottom to ", isolate(bottomDigits, i));

                int[] iterationResult = IntStream.range(0, maxLen).map(x -> 0).toArray();                
                for (int j = maxLen - 1; j >= 0; j--) {
                    printBulletOpen();
                    print("isolating top to ", isolate(topDigits, j));
                    if (carryOverDigits != null) {
                        print(" (carry-over is ",  carryOverDigits, ")");
                    }
                    println("");
                    
                    int topDigit = topDigits[j];
                    int[] digitsMultiplied = DIGIT_MULT_CACHE[bottomDigit][topDigit];
                    print(bottomDigit, " (bottom) times ", topDigit, " (top) is ", digitsMultiplied);

                    if (carryOverDigits != null) {
                        int[] newDigitsMultiplied = add(carryOverDigits, digitsMultiplied);
                        print(", added carry-over of ", carryOverDigits, " to get ", newDigitsMultiplied);
                        digitsMultiplied = newDigitsMultiplied;
                        carryOverDigits = null;
                    }
                    println("");
                    
                    switch (digitsMultiplied.length) {
                        case 1:
                            iterationResult[j] = digitsMultiplied[0];
                            break;
                        case 2:
                            println("setting carry-over to ", digitsMultiplied[0], " and keeping ", digitsMultiplied[1]);
                            iterationResult[j] = digitsMultiplied[1];
                            carryOverDigits = new int[] { digitsMultiplied[0] };
                            break;
                        default:
                            throw new IllegalStateException(); // should never happen
                    }
                    printBulletClose();
                }

                iterationResult = appendWithZeros(iterationResult, maxLen + (maxLen - 1 - i));
                if (carryOverDigits != null) {
                    iterationResult = concat(stream(carryOverDigits), stream(iterationResult)).toArray();
                    println("prepend remaining carry-over of ", carryOverDigits, ": ", isolate(iterationResult, 0));
                }
                println("done: ", iterationResult);
                
                iterationResults.add(iterationResult);
            }

            
            printBulletNewLine();
            int[] finalResult = new int[] { 0 };
            println("adding intermediate results to get final result...");
            for (int[] iterationResult : iterationResults) {
                int[] newFinalResult = add(iterationResult, finalResult);
                println("adding ", iterationResult, " to ", finalResult, " to get ", newFinalResult);
                finalResult = newFinalResult;
            }
            println("final result is ", finalResult);

            return finalResult;
        } finally {
            printBulletClose();
        }
    }
    //MARKDOWN_ISOLATE
    
    int[] add(int[] num1Digits, int[] num2Digits) throws IOException {
        return new MainAddition(Writer.nullWriter()).add(num1Digits, num2Digits);
    }
    
    private int indent = -2;
    private boolean firstLine = true;
    private void printBulletOpen() {
        indent += 2;
        firstLine = true;
    }
    
    private void printBulletClose() {
        indent -= 2;
    }
    
    private void printBulletNewLine() throws IOException {
        out.append("\n\n");
        firstLine = true;
    }
    
    private void println(Object... objs) throws IOException {
        print(objs);
        out.append("\n\n");
    }

    
    private void print(Object... objs) throws IOException {
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
    }
    
    private static String isolate(int[] digits, int idx) {
        String ret = "";
        for (int i = 0; i < digits.length; i++) {
            ret += i == idx ? " [" + digits[i] + "] " : " " + digits[i] + " ";
        }
        return ret;
    }
    
    private static String isolate(int digit, int idx, int max) {
        String ret = "";
        for (int i = 0; i < max; i++) {
            ret += i == idx ? " [" + digit + "] " : " x ";
        }
        return ret;
    }
    
    private static int[] prependWithZeros(int[] digits, int len) {
        return concat(range(digits.length, len).map(i -> 0), stream(digits)).toArray();
    }
    
    private static int[] appendWithZeros(int[] digits, int len) {
        return concat(stream(digits), range(digits.length, len).map(i -> 0)).toArray();
    }
}

package com.offbynull.wholenum;

import static com.google.common.base.Throwables.getStackTraceAsString;
import static com.offbynull.wholenum.Number.isolate;
import static com.offbynull.wholenum.Number.isolateLast;
import java.io.IOException;
import java.io.Writer;
import static java.io.Writer.nullWriter;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import static java.util.Arrays.stream;
import java.util.List;
import java.util.Scanner;
import static java.util.stream.Collectors.joining;
import static org.apache.commons.lang3.StringUtils.repeat;

public class MainMultiplication {
    
    public static void main(String[] args) throws IOException {
        try (Writer writer = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            writer.append("<div style=\"border:1px solid black;\">\n\n");
            writer.append("`{bm-linker-off}`\n\n");
            try (Scanner scanner = new Scanner(Files.newBufferedReader(Path.of("/input/input.data")))) {
                String num1Str = scanner.next("[0-9]+");
                String num2Str = scanner.next("[0-9]+");

                int[] num1Digits = num1Str.chars().map(i -> i - '0').toArray();
                int[] num2Digits = num2Str.chars().map(i -> i - '0').toArray();
                
                int maxLen = Math.max(num1Digits.length, num2Digits.length);
                Number num1 = Number.createFromDigits(num1Digits);
                Number num2 = Number.createFromDigits(num2Digits);
                num1.prependZerosIfShorterThan(maxLen);
                num2.prependZerosIfShorterThan(maxLen);
                
                writer.append("Multiplying " + num1 + " and " + num2 + "\n\n");
                
                new MainMultiplication(writer).mult(num1, num2);
            } catch (Exception e) {
                writer.append(getStackTraceAsString(e));
            } finally {
                writer.append("`{bm-linker-on}`\n\n");
                writer.append("</div>\n\n");
            }
        }
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
    
    Number mult(Number topNum, Number bottomNum) throws IOException {
        printBulletOpen();
        
        try {
            int maxLen = Math.max(topNum.length(), bottomNum.length());

            List<Number> iterationResults = new ArrayList<>();
            for (int i = 0; i < maxLen; i++) {
                int bottomDigit = bottomNum.getDigit(i);
                Number carryOverDigits = null;

                printBulletNewLine();
                println("isolating to ", isolate(bottomNum, i));
                
                Number iterationResult = Number.createAllZeros(i);
                for (int j = 0; j < maxLen; j++) {
                    printBulletOpen();
                    println("multiplying ", isolate(topNum, j), " and ", isolate(bottomNum, i));
                    println("start state: ", "carry-over=",  carryOverDigits, ".");
                    
                    int topDigit = topNum.getDigit(j);
                    Number digitsMultiplied = Number.createFromDigits(DIGIT_MULT_CACHE[bottomDigit][topDigit]);

                    println(bottomDigit, " multiplied by ",  topDigit, " is ", digitsMultiplied);
                    
                    if (carryOverDigits != null) {
                        print("carry-over of ", carryOverDigits, " exists, ");
                        Number newDigitsMultiplied = add(carryOverDigits, digitsMultiplied);
                        print(digitsMultiplied, " + ", carryOverDigits, " results in ", newDigitsMultiplied, " ");
                        digitsMultiplied = newDigitsMultiplied;
                        carryOverDigits = null;
                        println("(carry-over reset).");
                    }
                    
                    switch (digitsMultiplied.length()) {
                        case 1:
                            iterationResult.prependDigits(digitsMultiplied.getDigit(0));
                            break;
                        case 2:
                            iterationResult.prependDigits(digitsMultiplied.getDigit(0));
                            carryOverDigits = Number.createFromDigits(digitsMultiplied.getDigit(1));
                            break;
                        default:
                            throw new IllegalStateException(); // should never happen
                    }
                    
                    println("end state: ", "result=", isolateLast(iterationResult), " / carry-over=",  carryOverDigits, ".");
                    printBulletClose();
                }

                printBulletNewLine();
                if (carryOverDigits != null) {
                    printBulletOpen();
                    iterationResult.prepend(carryOverDigits);
                    println("prepend remaining carry-over of ", carryOverDigits, ".");
                    println("end state: ", "result=", isolateLast(iterationResult), ".");
                    printBulletClose();
                }

                printBulletOpen();
                println("result is ", iterationResult);
                printBulletClose();
                
                iterationResults.add(iterationResult);
            }

            
            printBulletNewLine();
            println("adding intermediate results to get final result...");
            Number finalResult = Number.createAllZeros(1);
            for (Number iterationResult : iterationResults) {
                Number newFinalResult = add(iterationResult, finalResult);
                println("adding ", iterationResult, " to ", finalResult, " to get ", newFinalResult);
                finalResult = newFinalResult;
            }
            printBulletNewLine();
            println("final result is ", finalResult);

            return finalResult;
        } finally {
            printBulletClose();
        }
    }
    //MARKDOWN_ISOLATE
    
    Number add(Number num1, Number num2) throws IOException {
        return new MainAddition(nullWriter()).add(num1.copy(), num2.copy());
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
}

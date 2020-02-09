package com.offbynull.wholenum;

import static com.google.common.base.Throwables.getStackTraceAsString;
import static com.offbynull.wholenum.Number.isolate;
import static com.offbynull.wholenum.Number.isolateLast;
import java.io.IOException;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import static java.util.Arrays.stream;
import java.util.Scanner;
import static java.util.stream.Collectors.joining;
import static org.apache.commons.lang3.StringUtils.repeat;

public class MainAddition {
    
    public static void main(String[] args) throws IOException {
        try (Writer writer = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            writer.append("<div style=\"border:1px solid black;\">\n\n");
            writer.append("`{bm-linker-off}`\n\n");
            try (Scanner scanner = new Scanner(Files.newBufferedReader(Path.of("/input/input.data")))) {
                String num1Str = scanner.next("[0-9]+");
                String num2Str = scanner.next("[0-9]+");

                int[] num1Digits = num1Str.chars().map(i -> i - '0').toArray();
                int[] num2Digits = num2Str.chars().map(i -> i - '0').toArray();
                
                Number num1 = Number.createFromDigits(num1Digits);
                Number num2 = Number.createFromDigits(num2Digits);
                
                writer.append("Adding " + num1 + " to " + num2 + "\n\n");
                
                new MainAddition(writer).add(num1, num2);
            } catch (Exception e) {
                writer.append(getStackTraceAsString(e));
            } finally {
                writer.append("`{bm-linker-on}`\n\n");
                writer.append("</div>\n\n");
            }
        }
    }
    
    private final Writer out;

    public MainAddition(Writer writer) {
        this.out = writer;
    }
    
    //MARKDOWN_ISOLATE
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
    
    Number add(Number num1, Number num2) throws IOException {
        printBulletOpen();
        
        try {
            int maxLen = Math.max(num1.length(), num2.length());
            num1.prependZerosIfShorterThan(maxLen);
            num2.prependZerosIfShorterThan(maxLen);

            Number result = Number.createFromDigits();
            Number carryOverDigits = null;
            for (int i = 0; i < maxLen; i++) {
                int num1Digit = num1.getDigit(i);
                int num2Digit = num2.getDigit(i);
                Number digitsAdded = Number.createFromDigits(DIGIT_ADD_CACHE[num1Digit][num2Digit]);

                printBulletNewLine();
                println("adding ", isolate(num1, i), " and ", isolate(num2, i));
                println("start state: ", "carry-over=",  carryOverDigits, ".");
                println(num1Digit, " + ", num2Digit, " is ", digitsAdded, ".");

                if (carryOverDigits != null) {
                    println("carry-over of ", carryOverDigits, " exists, ", digitsAdded, " + ", carryOverDigits, "...");
                    digitsAdded = add(carryOverDigits, digitsAdded);
                    carryOverDigits = null;
                    println("... is ", digitsAdded, " (carry-over reset).");
                }

                switch (digitsAdded.length()) {
                    case 1:
                        result.prependDigits(digitsAdded.getDigit(0));
                        break;
                    case 2:
                        result.prependDigits(digitsAdded.getDigit(0));
                        carryOverDigits = Number.createFromDigits(digitsAdded.getDigit(1));
                        break;
                    default:
                        throw new IllegalStateException(); // should never happen
                }
                
                println("end state: ", "result=", isolate(result, i), " / carry-over=",  carryOverDigits, ".");
            }

            printBulletNewLine();
            if (carryOverDigits != null) {
                result.prepend(carryOverDigits);
                println("prepend remaining carry-over of ", carryOverDigits, ".");
                println("end state: ", "result=", isolateLast(result), ".");
            }
            
            printBulletNewLine();
            println("result is ", result);

            return result;
        } finally {
            printBulletClose();
        }
    }
    //MARKDOWN_ISOLATE
    
    private int indent = -2;
    private boolean firstLine = true;
    private void printBulletOpen() {
        indent += 2;
        firstLine = true;
    }
    
    private void printBulletClose() {
        indent -= 2;
    }
    
    private void printBulletNewLine() {
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
}

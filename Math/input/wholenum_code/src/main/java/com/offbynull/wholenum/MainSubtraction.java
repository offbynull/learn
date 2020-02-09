package com.offbynull.wholenum;

import static com.google.common.base.Throwables.getStackTraceAsString;
import static com.offbynull.wholenum.Number.isolate;
import java.io.IOException;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import static java.util.Arrays.stream;
import java.util.Scanner;
import static java.util.stream.Collectors.joining;
import static java.util.stream.IntStream.concat;
import static java.util.stream.IntStream.range;
import static org.apache.commons.lang3.StringUtils.repeat;

public class MainSubtraction {
    
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
                
                writer.append("Subtracting " + num2 + " from " + num1 + "\n\n");
                
                new MainSubtraction(writer).subtract(num1, num2);
            } catch (Exception e) {
                writer.append(getStackTraceAsString(e));
            } finally {
                writer.append("`{bm-linker-on}`\n\n");
                writer.append("</div>\n\n");
            }
        }
    }
    
    private final Writer out;

    public MainSubtraction(Writer writer) {
        this.out = writer;
    }
    
    //MARKDOWN_ISOLATE
    static final Integer[][] DIGIT_SUB_CACHE = {
        {0   ,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {1   ,0   ,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {2   ,1   ,0   ,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {3   ,2   ,1   ,0   ,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {4   ,3   ,2   ,1   ,0   ,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {5   ,4   ,3   ,2   ,1   ,0   ,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {6   ,5   ,4   ,3   ,2   ,1   ,0   ,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   ,null,null,null,null,null,null,null,null,null,null,null,null},
        {8   ,7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   ,null,null,null,null,null,null,null,null,null,null,null},
        {9   ,8   ,7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   ,null,null,null,null,null,null,null,null,null,null},
        {10  ,9   ,8   ,7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   ,null,null,null,null,null,null,null,null,null},
        {11  ,10  ,9   ,8   ,7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   ,null,null,null,null,null,null,null,null},
        {12  ,11  ,10  ,9   ,8   ,7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   ,null,null,null,null,null,null,null},
        {13  ,12  ,11  ,10  ,9   ,8   ,7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   ,null,null,null,null,null,null},
        {14  ,13  ,12  ,11  ,10  ,9   ,8   ,7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   ,null,null,null,null,null},
        {15  ,14  ,13  ,12  ,11  ,10  ,9   ,8   ,7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   ,null,null,null,null},
        {16  ,15  ,14  ,13  ,12  ,11  ,10  ,9   ,8   ,7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   ,null,null,null},
        {17  ,16  ,15  ,14  ,13  ,12  ,11  ,10  ,9   ,8   ,7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   ,null,null},
        {18  ,17  ,16  ,15  ,14  ,13  ,12  ,11  ,10  ,9   ,8   ,7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   ,null},
        {19  ,18  ,17  ,16  ,15  ,14  ,13  ,12  ,11  ,10  ,9   ,8   ,7   ,6   ,5   ,4   ,3   ,2   ,1   ,0   }
    };
    
    static final Integer[][] DIGIT_ADD_CACHE = {
        {null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {10  ,11  ,12  ,13  ,14  ,15  ,16  ,17  ,18  ,19  ,null,null,null,null,null,null,null,null,null,null},
        {11  ,12  ,13  ,14  ,15  ,16  ,17  ,18  ,19  ,null,null,null,null,null,null,null,null,null,null,null},
        {12  ,13  ,14  ,15  ,16  ,17  ,18  ,19  ,null,null,null,null,null,null,null,null,null,null,null,null},
        {13  ,14  ,15  ,16  ,17  ,18  ,19  ,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {14  ,15  ,16  ,17  ,18  ,19  ,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {15  ,16  ,17  ,18  ,19  ,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {16  ,17  ,18  ,19  ,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {17  ,18  ,19  ,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {18  ,19  ,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null},
        {19  ,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null}
    };
    
    Number subtract(Number num1, Number num2) throws IOException {
        printBulletOpen();
        
        try {
            int maxLen = Math.max(num1.length(), num2.length());
            num1.prependZerosIfShorterThan(maxLen);
            num2.prependZerosIfShorterThan(maxLen);

            Number result = Number.createFromDigits();
            for (int i = 0; i < maxLen; i++) {
                int num1Digit = num1.getDigit(i);
                int num2Digit = num2.getDigit(i);
                
                printBulletNewLine();
                println("subtracting ", isolate(num1, i), " and ", isolate(num2, i));
                
                Integer resultDigit = DIGIT_SUB_CACHE[num1Digit][num2Digit];
                if (resultDigit == null) {
                    println("not possible -- attempting to borrow");
                    borrow(num1, num2, i);
                    println("trying again after borrow");
                    i--;
                    continue;
                }
                
                println("result of ", num1Digit, "-", num2Digit, " is ", resultDigit);
                result.prependDigits(resultDigit);
            }
            
            printBulletNewLine();
            println("final result is ", result);

            return result;
        } finally {
            printBulletClose();
        }
    }
    
    void borrow(Number num1, Number num2, int i) throws IOException {
        printBulletOpen();
        
        try {
            Integer currNum1Digit = num1.getDigit(i);
            Integer nextNum1Digit = num1.getDigit(i+1);

            printBulletNewLine();
            println("borrowing from next largest ", isolate(num1, i + 1));

            if (nextNum1Digit == 0) { // if the next digit is 0, it's impossible to borrow from it
                println("not possible -- attempting to borrow");
                borrow(num1, num2, i+1); // recursively borrow
                nextNum1Digit = num1.getDigit(i+1); // next largest position should be updated so that it's 10 or more after the borrow() above
            }
            nextNum1Digit = DIGIT_SUB_CACHE[nextNum1Digit][1]; // subtract 1 from next largest position
            currNum1Digit = DIGIT_ADD_CACHE[10][currNum1Digit]; // add 10 to current position
            
            num1.setDigit(i+1, nextNum1Digit);
            num1.setDigit(i, currNum1Digit);
            
            println("completed borrowing ", isolate(num1, i, i + 1));
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
    
    private static int[] padWithZeros(int[] digits, int len) {
        return concat(range(digits.length, len).map(i -> 0), stream(digits)).toArray();
    }
}

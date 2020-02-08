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

public class MainSubtraction {
    
    public static void main(String[] args) throws IOException {
        try (Writer writer = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            writer.append("<div style=\"border:1px solid black;\">\n\n");
            writer.append("`{bm-linker-off}`\n\n");
            try (Scanner scanner = new Scanner(Files.newBufferedReader(Path.of("/input/input.data")))) {
                String num1 = scanner.next("[0-9]+");
                String num2 = scanner.next("[0-9]+");

                int[] num1Digits = num1.chars().map(i -> i - '0').toArray();
                int[] num2Digits = num2.chars().map(i -> i - '0').toArray();
                
                writer.append("Subtracting " + num2 + " from " + num1 + "\n\n");
                
                new MainSubtraction(writer).subtract(num1Digits, num2Digits);
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
    
    int[] subtract(int[] num1Digits, int[] num2Digits) throws IOException {
        printBulletOpen();
        
        try {
            int maxLen = Math.max(num1Digits.length, num2Digits.length);
            num1Digits = padWithZeros(num1Digits, maxLen);
            num2Digits = padWithZeros(num2Digits, maxLen);

            int[] result = IntStream.range(0, maxLen).map(i -> 0).toArray();
            for (int i = maxLen - 1; i >= 0; i--) {
                int num1Digit = num1Digits[i];
                int num2Digit = num2Digits[i];
                
                printBulletNewLine();
                println("pos ", maxLen - i, " -- subtracting ", isolate(num1Digits, i), " and ", isolate(num2Digits, i));
                
                Integer resultDigit = DIGIT_SUB_CACHE[num1Digit][num2Digit];
                if (resultDigit == null) {
                    println("not possible -- attempting to borrow");
                    borrow(num1Digits, num2Digits, i);
                    println("trying again after borrow");
                    i++;
                    continue;
                }
                
                println("result of ", num1Digit, "-", num2Digit, " is ", resultDigit);
                result[i] = resultDigit;
            }
            
            printBulletNewLine();
            println("final result is ", result);

            return result;
        } finally {
            printBulletClose();
        }
    }
    
    void borrow(int[] num1Digits, int[] num2Digits, int i) throws IOException {
        printBulletOpen();
        
        try {
            Integer currNum1Digit = num1Digits[i];
            Integer nextNum1Digit = num1Digits[i-1];

            printBulletNewLine();
            println("borrowing from next largest ", isolate(num1Digits, i - 1));

            if (nextNum1Digit == 0) { // if the next digit is 0, it's impossible to borrow from it
                println("not possible -- attempting to borrow");
                borrow(num1Digits, num2Digits, i-1); // recursively borrow
                nextNum1Digit = num1Digits[i-1]; // next largest position should be updated so that it's 10 or more after the borrow() above
            }
            nextNum1Digit = DIGIT_SUB_CACHE[nextNum1Digit][1]; // subtract 1 from next largest position
            currNum1Digit = DIGIT_ADD_CACHE[10][currNum1Digit]; // add 10 to current position
            
            num1Digits[i-1] = nextNum1Digit;
            num1Digits[i] = currNum1Digit;
            
            println("completed borrowing ", isolate(num1Digits, i, i - 1));
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
    
    private static String isolate(int[] digits, int idx) {
        String ret = "";
        for (int i = 0; i < digits.length; i++) {
            ret += i == idx ? " [" + digits[i] + "] " : " " + digits[i] + " ";
        }
        return ret;
    }

    private static String isolate(int[] digits, int... idxes) {
        String ret = "";
        for (int i = 0; i < digits.length; i++) {
            int finalI = i;
            ret += IntStream.of(idxes).anyMatch(idx -> finalI == idx) ? " [" + digits[i] + "] " : " " + digits[i] + " ";
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
    
    private static int[] padWithZeros(int[] digits, int len) {
        return concat(range(digits.length, len).map(i -> 0), stream(digits)).toArray();
    }
}

package com.offbynull.cdt;

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

public class CommonDivisibilityTest {
    public static void main(String[] args) throws IOException {
        try (Writer writer = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            writer.append("<div style=\"border:1px solid black;\">\n\n");
            writer.append("`{bm-disable-all}`\n\n");
            try (Scanner scanner = new Scanner(Files.newBufferedReader(Path.of("/input/input.data")))) {
                int input = scanner.nextInt();

                //MARKDOWN_ISOLATE
                int lastDigit = getLastDigit(input);
                
                // is divisible by 2?
                boolean divisibleBy2 = false;
                if (lastDigit == 0 || lastDigit == 2 || lastDigit == 4 || lastDigit == 6 || lastDigit == 8) {
                    writer.append(" * " + input + " is divisibly by 2\n");
                    divisibleBy2 = true;
                } else {
                    writer.append(" * " + input + " is NOT divisibly by 2\n");
                }
                
                // is divisible by 5?
                if (lastDigit == 0 || lastDigit == 5) {
                    writer.append(" * " + input + " is divisibly by 5\n");
                } else {
                    writer.append(" * " + input + " is NOT divisibly by 5\n");
                }
                
                // is divisible by 10?
                if (lastDigit == 0) {
                    writer.append(" * " + input + " is divisibly by 10\n");
                } else {
                    writer.append(" * " + input + " is NOT divisibly by 10\n");
                }
                
                // is divisible by 3?
                int reducedInput = input;
                while (true) {
                    int[] digits = toDigits(reducedInput);
                    if (digits.length == 1) {
                        break;
                    }
                    reducedInput = stream(digits).sum();
                }
                boolean divisibleBy3 = false;
                if (reducedInput == 3 || reducedInput == 6 || reducedInput == 9) {
                    writer.append(" * " + input + " is divisibly by 3\n");
                    divisibleBy3 = true;
                } else {
                    writer.append(" * " + input + " is NOT divisibly by 3\n");
                }
                
                if (divisibleBy2 && divisibleBy3) {
                    writer.append(" * " + input + " is divisibly by 6\n");
                } else {
                    writer.append(" * " + input + " is NOT divisibly by 6\n");
                }
                //MARKDOWN_ISOLATE
            } catch (Exception e) {
                writer.append(getStackTraceAsString(e));
            } finally {
                writer.append("`{bm-enable-all}`\n\n");
                writer.append("</div>\n\n");
            }
        }
    }
    
    private static int getLastDigit(int input) {
        return input % 10;
    }

    private static int[] toDigits(int input) {
        List<Integer> digits = new ArrayList<>();
        while (input > 0) {
            int digit = input % 10;
            digits.add(0, digit);
            input /= 10;
        }
        return digits.stream().mapToInt(d -> d).toArray();
    }
}

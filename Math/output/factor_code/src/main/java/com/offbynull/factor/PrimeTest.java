package com.offbynull.factor;

import com.google.common.base.Preconditions;
import static com.google.common.base.Throwables.getStackTraceAsString;
import java.io.IOException;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Scanner;
import java.util.Set;
import java.util.TreeSet;

public class PrimeTest {
    public static void main(String[] args) throws IOException {
        try (Writer writer = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            writer.append("<div style=\"border:1px solid black;\">\n\n");
            writer.append("`{bm-disable-all}`\n\n");
            try (Scanner scanner = new Scanner(Files.newBufferedReader(Path.of("/input/input.data")))) {
                int input = scanner.nextInt();

                Preconditions.checkArgument(input >= 1, "Natural numbers only.");

                //MARKDOWN_ISOLATE
                Set<Integer> factors = getFactors(input);
                
                writer.append(input + "'s factors are " + factors + "\n\n");
                
                // At a minimum, all counting numbers have the factors 1 and the number itself (2 factors). If
                // there are more factore than that, it's a composite. Otherwise, it's a primse.
                if (factors.size() == 2) {
                    writer.append(input + " is a prime\n");
                } else {
                    writer.append(input + " is a composite\n");
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

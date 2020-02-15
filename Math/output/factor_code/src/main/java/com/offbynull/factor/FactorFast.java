package com.offbynull.factor;

import com.google.common.base.Preconditions;
import static com.google.common.base.Throwables.getStackTraceAsString;
import java.io.IOException;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Scanner;

public class FactorFast {
    public static void main(String[] args) throws IOException {
        try (Writer writer = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            writer.append("<div style=\"border:1px solid black;\">\n\n");
            writer.append("`{bm-linker-off}`\n\n");
            try (Scanner scanner = new Scanner(Files.newBufferedReader(Path.of("/input/input.data")))) {
                int testNum = scanner.nextInt();

                Preconditions.checkArgument(testNum >= 1);
                                
                //MARKDOWN_ISOLATE
                for (int factor1 = 1; factor1 <= testNum; factor1++) {
                    int factor2 = testNum / factor1;
                    boolean divHadRemainder = testNum % factor1 > 0;
                    if (!divHadRemainder) {
                        writer.append(" * " + factor1 + " and " + factor2 + " are factors of " + testNum + "\n");
                    }
                }
                //MARKDOWN_ISOLATE
            } catch (Exception e) {
                writer.append(getStackTraceAsString(e));
            } finally {
                writer.append("`{bm-linker-on}`\n\n");
                writer.append("</div>\n\n");
            }
        }
    }
}

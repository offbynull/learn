package com.offbynull.kthelper;

import static com.google.common.base.Throwables.getStackTraceAsString;
import static com.offbynull.kthelper.Parameterizer.parameterize;
import java.io.IOException;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public final class MainLongDivision {
    public static void main(String[] args) throws IOException {
        String input = Files.readString(Path.of("/input/input.data"), UTF_8).trim();
        try (Writer mdOut = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            try {
                List<String> parameters = parameterize(input);
                String quotient = parameters.remove(0);
                String divisor = parameters.remove(0);
                String dividend = parameters.remove(0);
                
                String output = "";
                output += "`{kt}";
                output += "\\begin{array}{l}";
                output += "\\phantom{{" + divisor + "\\smash{)}}}{" + quotient + "} \\\\";
                output += "{" + divisor + "}\\overline{\\smash{)}" + dividend + "} \\\\";
                
                while (!parameters.isEmpty()) {
                    String under = parameters.remove(0);
                    output += "\\phantom{{" + divisor + "\\smash{)}}}" + under + " \\\\";
                }
                
                output += "\\end{array}";
                output += "`";

                mdOut.write(output);
            } catch (Exception e) {
                mdOut.append("`{bm-linker-off}`\n\n");
                mdOut.append(getStackTraceAsString(e));
                mdOut.append("`{bm-linker-on}`");
            }
        }
    }
}

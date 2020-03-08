package com.offbynull.lcm;

import com.google.common.base.Preconditions;
import static com.google.common.base.Throwables.getStackTraceAsString;
import java.io.IOException;
import java.io.Writer;
import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import static java.util.Collections.nCopies;
import java.util.List;
import java.util.Scanner;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toList;

public class ListMultiples {
    public static void main(String[] args) throws IOException {
        try (Writer writer = Files.newBufferedWriter(Path.of("/output/output.md"), UTF_8)) {
            writer.append("<div style=\"border:1px solid black;\">\n\n");
            writer.append("`{bm-disable-all}`\n\n");
            try (Scanner scanner = new Scanner(Files.newBufferedReader(Path.of("/input/input.data")))) {
                int num1 = scanner.nextInt();
                int num2 = scanner.nextInt();
                
                Preconditions.checkArgument(num1 > 0);
                Preconditions.checkArgument(num2 > 0);

                List<Integer> num1Multiples = new ArrayList<>();
                List<Integer> num2Multiples = new ArrayList<>();
                
                //MARKDOWN_ISOLATE
                int num1Counter = 1;
                int num2Counter = 1;
                
                int num1Multiple = num1 * num1Counter;
                num1Multiples.add(num1Multiple);
                
                int num2Multiple = num2 * num2Counter;
                num2Multiples.add(num2Multiple);
                
                while (true) {
                    if (num1Multiple < num2Multiple) {
                        // num1Multiple is less than num2Multiple, increase it
                        num1Counter++;
                        num1Multiple = num1 * num1Counter;
                        num1Multiples.add(num1Multiple);
                    } else if (num1Multiple > num2Multiple) {
                        // num2Multiple is less than num1Multiple, increase it
                        num2Counter++;
                        num2Multiple = num2 * num2Counter;
                        num2Multiples.add(num2Multiple);        
                    } else {
                        // multiples match -- we're done.
                        break;
                    }
                }
                //MARKDOWN_ISOLATE
                
                List<String> num1MultiplesTds = num1Multiples.stream().map(i -> "<td>" + i + "</td>").collect(toList());
                List<String> num2MultiplesTds = num2Multiples.stream().map(i -> "<td>" + i + "</td>").collect(toList());
                if (num1Multiples.size() < num2Multiples.size()) {
                    num1MultiplesTds.addAll(nCopies(num2Multiples.size() - num1Multiples.size(), "<td></td>"));
                } else  if (num1Multiples.size() > num2Multiples.size()) {
                    num2MultiplesTds.addAll(nCopies(num1Multiples.size() - num2Multiples.size(), "<td></td>"));
                }
                
                writer.append(
                        "<table>"
                        + "<tr>"
                        + "<td>multiples of " + num1 + "</td>"
                        + num1MultiplesTds.stream().collect(joining())
                        + "</tr>"
                        + "<tr>"
                        + "<td>multiples of " + num2 + "</td>"
                        + num2MultiplesTds.stream().collect(joining())
                        + "</tr>"
                        + "</table>\n\n");
                writer.append("least common multiple is " + num1Multiples.get(num1Multiples.size() - 1) + "\n\n");
            } catch (Exception e) {
                writer.append(getStackTraceAsString(e));
            } finally {
                writer.append("`{bm-enable-all}`\n\n");
                writer.append("</div>\n\n");
            }
        }
    }
}

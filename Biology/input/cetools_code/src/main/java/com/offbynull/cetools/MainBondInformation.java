package com.offbynull.cetools;

import com.offbynull.cetools.parser.Parser;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;

public final class MainBondInformation {
    public static void main(String[] args) throws IOException {
        try (Scanner s = new Scanner(System.in);
                PrintWriter pw = new PrintWriter(System.out, true);
                MarkdownWriter mdw = new MarkdownWriter(pw)) {
            mdw.out("<div style=\"border:1px solid black;\">\n\n");
            String input = s.nextLine();
            
            mdw.out("Pulling information for ").out(input).out("\n\n");
            
            Bond bond = new Parser().parseBond(input);
            bond.items.forEach(bu -> mdw.out(" * ").out(bu.count).out(bu.element.name).out("\n"));
            mdw.out(" * atomic weight ").out(bond.atomicWeight()).out("amu\n");
            mdw.out("\n\n</div>\n\n");
        }
    }
}

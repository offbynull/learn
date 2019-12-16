



package com.offbynull.cetools;

import com.offbynull.cetools.parser.Parser;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;

public final class MainEquationParse {
    public static void main(String[] args) throws IOException {
        try (Scanner s = new Scanner(System.in);
                PrintWriter pw = new PrintWriter(System.out, true);
                MarkdownWriter mdw = new MarkdownWriter(pw)) {
            mdw.out("<div style=\"border:1px solid black;\">\n\n");
            String input = s.nextLine();
            
            mdw.out("Parsing ").out(input).out("\n\n");
            
            ChemicalEquation ce = new Parser().parseChemicalEquation(input);
            for (var r : ce.reactants.items) {
                mdw.out(" * Input: ").out(r.count).out(" x ( ");
                for (var bu : r.bond.items) {
                    mdw.out(bu.count).out(bu.element.name).out(" ");
                }
                mdw.out(")\n");
            }
            for (var r : ce.products.items) {
                mdw.out(" * Output: ").out(r.count).out(" x ( ");
                for (var bu : r.bond.items) {
                    mdw.out(bu.count).out(bu.element.name).out(" ");
                }
                mdw.out(")\n");
            }
            mdw.out(" * Direction: ").out(ce.direction).out("\n");
            mdw.out("\n\n</div>\n\n");
        }
    }
}

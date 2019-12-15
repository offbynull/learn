package com.offbynull.stoichiometry;

import java.io.IOException;
import java.io.Writer;

public final class MarkdownHelper {
    private MarkdownHelper() {
    }

    public static void chemicalEquation(Writer writer, ChemicalEquation ce) throws IOException {
        writer.write("`{kt} ");
        rawChemicalEquationSet(writer, ce.reactants);
        switch (ce.direction) {
            case UNIDIRECTIONAL:
                writer.write(" \\rightarrow ");
                break;
            case BIDIRECTIONAL:
                writer.write(" \\rightleftharpoons ");
                break;
            default:
                throw new IllegalStateException();
        }
        rawChemicalEquationSet(writer, ce.products);
        writer.write("`");
    }
    
    private static void rawChemicalEquationSet(Writer writer, ChemicalEquationSet ces) throws IOException {
        int remaining = ces.items.size();
        for (ChemicalEquationUnit ceu : ces.items) {
            writer.append(ceu.count == 1 ? "" : "" + ceu.count);
            rawBond(writer, ceu.bond);
            remaining--;
            if (remaining > 0) {
                writer.write(" + ");
            }
        }
    }
    
    public static void bond(Writer writer, Bond b) throws IOException {
        writer.write("`{kt} ");
        rawBond(writer, b);
        writer.write("`");
    }
    
    private static void rawBond(Writer writer, Bond b) throws IOException {
        for (BondUnit bu : b.items) {
            rawBondUnit(writer, bu);
        }
    }
    
    private static void rawBondUnit(Writer writer, BondUnit bu) throws IOException {
        writer.write(bu.element.symbol);
        if (bu.count > 1) {
            writer.write("_" + bu.count);
        }
    }
}

package com.offbynull.chemeq;

import com.offbynull.chemeq.parser.Parser;

public final class Main {
    public static void main(String[] args) {
        ChemicalEquation ce = new Parser().parseChemicalEquation("Fe + O + H -> Fe(OH)2");
        System.out.println(ce);
    }
}

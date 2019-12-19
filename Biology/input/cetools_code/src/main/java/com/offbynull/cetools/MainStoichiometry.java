package com.offbynull.cetools;

import com.google.common.base.Preconditions;
import static com.google.common.base.Throwables.getStackTraceAsString;
import com.google.common.collect.HashMultiset;
import com.google.common.collect.Multiset;
import com.offbynull.cetools.parser.Parser;
import java.io.IOException;
import java.io.PrintWriter;
import static java.util.Arrays.stream;
import static java.util.Collections.nCopies;
import java.util.Scanner;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toList;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public final class MainStoichiometry {
    public static void main(String[] args) throws Throwable {
        try (Scanner s = new Scanner(System.in);
                PrintWriter pw = new PrintWriter(System.out, true);
                MarkdownWriter mdw = new MarkdownWriter(pw)) {
            mdw.out("<div style=\"border:1px solid black;\">\n\n");
            try {
                String inputCe = s.nextLine();
                String inputKnownBond = s.nextLine();
                double inputKnownBondMass = s.nextDouble();

                mdw.out("Stoichiometry for ").out(inputCe).out("\n\n");

                ChemicalEquation ce = new Parser().parseChemicalEquation(inputCe);
                Bond knownBond = new Parser().parseBond(inputKnownBond);
                double knownBondMass = inputKnownBondMass;

                mdw.out("My equation is ").out(ce)
                        .out(". Given that I have ").out(knownBondMass).out("g of ").out(knownBond)
                        .out(", how many grams of the remaining bonds will be required/produced?\n\n");

                performStoichiometry(mdw, ce, knownBond, knownBondMass);
            } catch (Exception e) {
                mdw.out(getStackTraceAsString(e));
            }
            mdw.out("\n\n</div>\n\n");
        }
    }




    public static double[] performStoichiometry(MarkdownWriter mdw, ChemicalEquation ce, Bond knownBond, double knownBondMass) throws IOException {
        Preconditions.checkNotNull(mdw);
        Preconditions.checkNotNull(ce);
        
        if (!isBalanced(ce)) {
            mdw.out("Equation is unbalanced! Cannot perform!!\n\n");
            return null;
        }
        
        var bonds = Stream.concat(
                ce.reactants.items.stream(),
                ce.products.items.stream()
        ).collect(toList());
        if (bonds.stream().map(ceu -> ceu.bond).noneMatch(b -> b.equals(knownBond))) {
            mdw.out(knownBond).out(" does not exist in ").out(ce).out("! Cannot perform!!\n\n");
            return null;
        }
        
        var ratios = DoubleStream.concat(
                ce.reactants.items.stream().mapToDouble(i -> i.count),
                ce.products.items.stream().mapToDouble(i -> i.count)
        ).toArray();
        
        int idx = IntStream.range(0, bonds.size())
                .filter(i -> bonds.get(i).bond.equals(knownBond))
                .findFirst().getAsInt();
        if (idx == -1) {
            mdw.out(knownBond);
            mdw.out(" not found\n\n");
            return null;
        }
        
        
        // write out ratios
        mdw.out("Stoichiometric ratio for the balanced chemical equation is: ["
                + stream(ratios).mapToObj(d -> "" + d).collect(joining(" : "))
                + "]\n\n");
        double[] scaledRatio = stream(ratios)
                .map(r -> r / ratios[idx])
                .toArray(); // scale all ratios against the ratio of the known bond (known ratio gets scaled to become 1 and all others get scaled relative to it).
        mdw.out("Scaling stoichiometric ratio so that ");
        mdw.out(knownBond);
        mdw.out("'s entry is 1: ["
                + stream(scaledRatio).mapToObj(d -> "" + d).collect(joining(" : "))
                + "]\n\n");
        
        
        // convert known bond's mass to moles
        mdw.out("Converting " + knownBondMass + "g of ");
        mdw.out(knownBond);
        mdw.out(" to moles: \n");
        double knownBondAtomicWeight = knownBond.items.stream().mapToDouble(bu -> bu.element.atomicWeight.lowerEndpoint() * bu.count).sum();
        double knownBondGramsPerMole = knownBondAtomicWeight;
        double knownBondMoles = knownBondMass * knownBondGramsPerMole;
        mdw.out(" * atomic weight is " + knownBondAtomicWeight + "amu\n");
        mdw.out(" * so, " + knownBondGramsPerMole + "g = 1 mole\n");
        mdw.out(" * so, " + knownBondMass + "g = " + knownBondMass + "g * " + knownBondGramsPerMole + "g per mole = " + knownBondMoles + " mole\n");
        mdw.out("\n\n");
        
        
        // use that to figure out the unknown bonds' moles
        mdw.out("Multiplying by scaled stoichiometric ratio to get moles for other bonds:\n\n");
        double[] allBondMoles = IntStream.range(0, bonds.size())
                .mapToDouble(i -> knownBondMoles * scaledRatio[i])
                .toArray(); // calculate the number of moles for all bonds based on the scaledRatios
        for (int i = 0; i < bonds.size(); i++) {
            mdw.out(" * ");
            mdw.out(bonds.get(i).bond);
            mdw.out(": " + knownBondMoles + " moles * " + scaledRatio[i] + " ratio = " + allBondMoles[i] + " moles\n");
        }
        mdw.out("\n\n");
        
        
        mdw.out("Converting moles back to grams:\n\n");
        double[] allBondGrams = new double[bonds.size()];
        for (int i = 0; i < bonds.size(); i++) {
            double bondAtomicWeight = bonds.get(i).bond.items.stream().mapToDouble(bu -> bu.element.atomicWeight.lowerEndpoint() * bu.count).sum();
            double bondGramsPerMole = bondAtomicWeight;
            double bondGrams = allBondMoles[i] / bondGramsPerMole;
            mdw.out(" * ");
            mdw.out(bonds.get(i).bond);
            mdw.out(" (" + bondAtomicWeight + "amu): " + allBondMoles[i] + " moles / " + bondGramsPerMole + " grams per mole = " + bondGrams + "g\n");
            allBondGrams[i] = bondGrams;
        }
        
        
        return allBondGrams;
    }
    
    private static boolean isBalanced(ChemicalEquation ce) {
        Multiset<Element> reactantElementBag = HashMultiset.create();
        ce.reactants.items.stream()
                .flatMap(i -> nCopies(i.count, i.bond.items).stream())
                .flatMap(i -> i.stream())
                .forEach(bu -> reactantElementBag.add(bu.element, bu.count));
        
        Multiset<Element> productElementBag = HashMultiset.create();
        ce.products.items.stream()
                .flatMap(i -> nCopies(i.count, i.bond.items).stream())
                .flatMap(i -> i.stream())
                .forEach(bu -> productElementBag.add(bu.element, bu.count));
        
        return reactantElementBag.equals(productElementBag);
    }
}

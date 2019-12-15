package com.offbynull.stoichiometry;

import com.google.common.base.Preconditions;
import static com.google.common.collect.ImmutableList.toImmutableList;
import com.google.common.collect.LinkedHashMultiset;
import com.google.common.collect.Multiset;
import com.google.common.collect.Streams;
import com.offbynull.stoichiometry.parser.Parser;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.Writer;
import static java.util.Arrays.stream;
import java.util.Scanner;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toList;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import org.ejml.alg.dense.misc.RrefGaussJordanRowPivot;
import org.ejml.simple.SimpleMatrix;

public final class Main {
    public static void main(String[] args) throws Throwable {
//        ChemicalEquation ce = new Parser().parseChemicalEquation("C3H8 + O2 -> CO2 + H2O");
//        Bond knownQuantityBond = new Parser().parseBond("O2");
//        double knownQuantityMass = 2;
        
        try (Scanner s = new Scanner(System.in);
                PrintWriter pw = new PrintWriter(System.out, true)) {
            ChemicalEquation ce = new Parser().parseChemicalEquation(s.nextLine());
            Bond knownBond = new Parser().parseBond(s.nextLine());
            double knownBondMass = s.nextDouble();
            pw.write("My chemical equation is ");
            MarkdownHelper.chemicalEquation(pw, ce);
            pw.write(". Given that I have " + knownBondMass + "g of ");
            MarkdownHelper.bond(pw, knownBond);
            pw.write(", how many grams of the remaining bonds will be required/produced?\n\n");

            ChemicalEquation balancedCe = balanceEquation(pw, ce);
            performStoichiometry(pw, balancedCe, knownBond, knownBondMass);
        }
    }
    
    
    
    
    public static ChemicalEquation balanceEquation(Writer writer, ChemicalEquation ce) throws IOException {
        Preconditions.checkNotNull(writer);
        Preconditions.checkNotNull(ce);        
        
        
        // unbalance
        writer.write("Removing stoichiometric coefficients: ");
        ChemicalEquation unbalancedCe = new ChemicalEquation(
                new ChemicalEquationSet(
                        ce.reactants.items.stream()
                               .map(i -> new ChemicalEquationUnit(1, i.bond))
                               .collect(toImmutableList())
                ),
                new ChemicalEquationSet(
                        ce.products.items.stream()
                               .map(i -> new ChemicalEquationUnit(1, i.bond))
                               .collect(toImmutableList())
                ),
                ce.direction
        );
        MarkdownHelper.chemicalEquation(writer, unbalancedCe);
        writer.write("\n\n");
        
        
        
        // get all elements used
        writer.write("Counting up elements: \n\n");
        Multiset<Element> elementBag = LinkedHashMultiset.create();
        unbalancedCe.reactants.items.stream()
                .flatMap(i -> i.bond.items.stream())
                .forEach(bu -> elementBag.add(bu.element, bu.count));
        unbalancedCe.products.items.stream()
                .flatMap(i -> i.bond.items.stream())
                .forEach(bu -> elementBag.add(bu.element, bu.count));
        for (Multiset.Entry<Element> bagEntry : elementBag.entrySet()) {
            writer.write(" * " + bagEntry.getElement().symbol + " -> " + bagEntry.getCount() + "\n");
        }

        int eqCount = elementBag.elementSet().size();
        writer.write("\n\n");
        
        
        
        // list equations to solve
        writer.write("For each element, determining linear equations to solve: \n\n");
        var bondMapping = Streams.zip(
                Stream.concat(unbalancedCe.reactants.items.stream(), unbalancedCe.products.items.stream()),
                IntStream.range('a', 'z').mapToObj(i -> i),
                (a,b) -> new VariableToBond("" + ((char) b.intValue()), a.bond))
                .sorted((a,b) -> a.var.compareTo(b.var))
                .collect(toList());
        for (var e : elementBag.elementSet()) {
            writer.write(" * " + e.symbol + ": ");
            writer.write("`{kt} ");
            int remainingReactants = unbalancedCe.reactants.items.size();
            for (var ceu : unbalancedCe.reactants.items) {
                var bondElemCount = ceu.bond.items.stream().mapToInt(bu -> bu.element.equals(e) ? bu.count : 0).sum();
                var bondVarName = bondMapping.stream().filter(bm -> bm.bond.equals(ceu.bond)).findFirst().get().var;
                writer.write(bondElemCount + bondVarName);
                remainingReactants--;
                if (remainingReactants > 0) {
                    writer.write(" + ");
                }
            }
            writer.write(" = ");
            int remainingProducts = unbalancedCe.products.items.size();
            for (var ceu : unbalancedCe.products.items) {
                var bondElemCount = ceu.bond.items.stream().mapToInt(bu -> bu.element.equals(e) ? bu.count : 0).sum();
                var bondVarName = bondMapping.stream().filter(bm -> bm.bond.equals(ceu.bond)).findFirst().get().var;
                writer.write(bondElemCount + bondVarName);
                remainingProducts--;
                if (remainingProducts > 0) {
                    writer.write(" + ");
                }
            }
            writer.write("`\n");
        }
        writer.write("\n\n... where ...\n\n");
        for (var bondMap : bondMapping) {
            writer.write(" * " + bondMap.var);
            writer.write(" maps to ");
            MarkdownHelper.bond(writer, bondMap.bond);
            writer.write("\n");
        }
        writer.write("\n\n");
        
        int varCount = bondMapping.size();
        
        
        
        // solve system of linear equations
          // solving using matrix instead of substitution: https://www.youtube.com/watch?v=1i2nvMli0GY
        writer.write("Solving system of linear equations: \n\n");
        double[][] matrixA = new double[varCount][varCount];
        int rowIdx = 0;
        for (var e : elementBag.elementSet()) {
            int colIdx = 0;
            for (var ceu : unbalancedCe.reactants.items) {
                var bondElemCount = ceu.bond.items.stream().mapToInt(bu -> bu.element.equals(e) ? bu.count : 0).sum();
                matrixA[rowIdx][colIdx] = bondElemCount;
                colIdx++;
            }
            for (var ceu : unbalancedCe.products.items) {
                var bondElemCount = ceu.bond.items.stream().mapToInt(bu -> bu.element.equals(e) ? bu.count : 0).sum();
                matrixA[rowIdx][colIdx] = -bondElemCount;
                colIdx++;
            }
            rowIdx++;
        }
        if (varCount <= eqCount) {
            // do nothing, enough equations availabe for unknown vars
        } else if (eqCount == varCount - 1) {
            // missing 1 eq -- notify of strategy
            writer.write("There are " + eqCount + " equations but " + varCount + " variables. For the last equation, picking"
                    + " the remaining variable and setting it to 1. We can do this because we're dealing with ratios -- the coefficients"
                    + " are all relative to each other.\n\n");
            matrixA[rowIdx][varCount - 1] = -1.0;
        } else {
            // missing more than 1 eq -- bail out
            writer.write("Unable to balance! Not enough equations for variables");
            return null;
        }
        SimpleMatrix simpleMatrixA = new SimpleMatrix(matrixA);
        new RrefGaussJordanRowPivot().reduce(simpleMatrixA.getMatrix(), varCount - 1);
        double[] stoichiometricRatios = new double[varCount];
        for (var i = 0; i < varCount; i++) {
            double stoichiometricCoefficient = -simpleMatrixA.get(i, varCount - 1);
            stoichiometricRatios[i] = stoichiometricCoefficient;
            writer.write(" * " + bondMapping.get(i).var + " (mapped to ");
            MarkdownHelper.bond(writer, bondMapping.get(i).bond);
            writer.write(") = " + stoichiometricCoefficient + "\n");
        }
        writer.write("\n\n");
        
        
        
        // get it to whole numbers the cheap-and-easy but inefficient way
        writer.write("Getting it to whole numbers: \n\n");
        double[] newRatios = stoichiometricRatios;
        for (int i = 1; i < 1000; i++) {
            boolean isWholeNums = stream(newRatios).allMatch(d -> isWholeNumber(d, 0.0001));
            if (isWholeNums) {
                break;
            }
            int finalI = i;
            newRatios = stream(stoichiometricRatios).map(d -> d * finalI).toArray();
            writer.write(" * Scaling by " + i + ": " + stream(newRatios).mapToObj(d -> "" + d).collect(joining(", ")) + "\n");
        }
        stoichiometricRatios = newRatios;
        writer.write("\n\n");
        boolean isWholeNums = stream(newRatios).allMatch(d -> isWholeNumber(d, 0.0001));
        if (!isWholeNums) {
            writer.write("Unable to get to whole nums");
            return null;
        }

        
        // print it back out
        ChemicalEquation balancedCe = new ChemicalEquation(
                new ChemicalEquationSet(
                        Streams.zip(
                                ce.reactants.items.stream(),
                                stream(stoichiometricRatios).limit(ce.reactants.items.size()).boxed(), // limited to reactants
                                (a,b) -> new ChemicalEquationUnit(b.intValue(), a.bond))
                               .collect(toImmutableList())
                ),
                new ChemicalEquationSet(
                        Streams.zip(
                                ce.products.items.stream(),
                                stream(stoichiometricRatios).skip(ce.reactants.items.size()).boxed(), // skips past reactants
                                (a,b) -> new ChemicalEquationUnit(b.intValue(), a.bond))
                               .collect(toImmutableList())
                ),
                ce.direction
        );
        writer.write("Balanced chemical equation: ");
        MarkdownHelper.chemicalEquation(writer, balancedCe);
        writer.write("\n\n");
        
        return balancedCe;
    }
    
    // https://stackoverflow.com/a/23975512
    private static boolean isWholeNumber(double n, double tolerance) {
        double absN = Math.abs(n);
        return Math.abs(absN - Math.round(absN)) <= tolerance;
    }

    private static final class VariableToBond {
        private final String var;
        private final Bond bond;

        public VariableToBond(String var, Bond bond) {
            this.var = var;
            this.bond = bond;
        }
    }




    public static double[] performStoichiometry(Writer writer, ChemicalEquation ce, Bond knownBond, double knownBondMass) throws IOException {
        Preconditions.checkNotNull(writer);
        Preconditions.checkNotNull(ce);
        
        var bonds = Stream.concat(
                ce.reactants.items.stream(),
                ce.products.items.stream()
        ).collect(toList());
        var ratios = DoubleStream.concat(
                ce.reactants.items.stream().mapToDouble(i -> i.count),
                ce.products.items.stream().mapToDouble(i -> i.count)
        ).toArray();
        
        int idx = IntStream.range(0, bonds.size())
                .filter(i -> bonds.get(i).bond.equals(knownBond))
                .findFirst().getAsInt();
        if (idx == -1) {
            MarkdownHelper.bond(writer, knownBond);
            writer.write(" not found\n\n");
            return null;
        }
        
        
        // write out ratios
        writer.write("Stoichiometric ratio for the balanced chemical equation is: ["
                + stream(ratios).mapToObj(d -> "" + d).collect(joining(" : "))
                + "]\n\n");
        double[] scaledRatio = stream(ratios)
                .map(r -> r / ratios[idx])
                .toArray(); // scale all ratios against the ratio of the known bond (known ratio gets scaled to become 1 and all others get scaled relative to it).
        writer.write("Scaling stoichiometric ratio so that ");
        MarkdownHelper.bond(writer, knownBond);
        writer.write("'s entry is 1: ["
                + stream(scaledRatio).mapToObj(d -> "" + d).collect(joining(" : "))
                + "]\n\n");
        
        
        // convert known bond's mass to moles
        writer.write("Converting " + knownBondMass + "g of ");
        MarkdownHelper.bond(writer, knownBond);
        writer.write(" to moles: \n");
        double knownBondAtomicWeight = knownBond.items.stream().mapToDouble(bu -> bu.element.atomicWeight.lowerEndpoint() * bu.count).sum();
        double knownBondGramsPerMole = knownBondAtomicWeight;
        double knownBondMoles = knownBondMass * knownBondGramsPerMole;
        writer.write(" * atomic weight is " + knownBondAtomicWeight + "amu\n");
        writer.write(" * so, " + knownBondGramsPerMole + "g = 1 mole\n");
        writer.write(" * so, " + knownBondMass + "g = " + knownBondMass + "g * " + knownBondGramsPerMole + "g per mole = " + knownBondMoles + " mole\n");
        writer.write("\n\n");
        
        
        // use that to figure out the unknown bonds' moles
        writer.write("Multiplying by scaled stoichiometric ratio to get moles for other bonds:\n\n");
        double[] allBondMoles = IntStream.range(0, bonds.size())
                .mapToDouble(i -> knownBondMoles * scaledRatio[i])
                .toArray(); // calculate the number of moles for all bonds based on the scaledRatios
        for (int i = 0; i < bonds.size(); i++) {
            writer.write(" * ");
            MarkdownHelper.bond(writer, bonds.get(i).bond);
            writer.write(": " + knownBondMoles + " moles * " + scaledRatio[i] + " ratio = " + allBondMoles[i] + " moles\n");
        }
        writer.write("\n\n");
        
        
        writer.write("Converting moles back to grams:\n\n");
        double[] allBondGrams = new double[bonds.size()];
        for (int i = 0; i < bonds.size(); i++) {
            double bondAtomicWeight = bonds.get(i).bond.items.stream().mapToDouble(bu -> bu.element.atomicWeight.lowerEndpoint() * bu.count).sum();
            double bondGramsPerMole = bondAtomicWeight;
            double bondGrams = allBondMoles[i] / bondGramsPerMole;
            writer.write(" * ");
            MarkdownHelper.bond(writer, bonds.get(i).bond);
            writer.write(" (" + bondAtomicWeight + "amu): " + allBondMoles[i] + " moles / " + bondGramsPerMole + " grams per mole = " + bondGrams + "g\n");
            allBondGrams[i] = bondGrams;
        }
        
        
        return allBondGrams;
    }
}

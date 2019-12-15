package com.offbynull.chemeq;

import com.google.common.base.Preconditions;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.LinkedHashMultiset;
import com.google.common.collect.Multiset;
import com.google.common.collect.Streams;
import com.offbynull.chemeq.parser.Parser;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.Writer;
import java.util.Arrays;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toList;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import org.ejml.alg.dense.misc.RrefGaussJordanRowPivot;
import org.ejml.simple.SimpleMatrix;

public final class ChemicalEquationAtomCounter {
    public static void main(String[] args) throws Throwable {
//        ChemicalEquation ce = new Parser().parseChemicalEquation("H2 + O2 -> H2O");

        ChemicalEquation ce = new Parser().parseChemicalEquation("C3H8 + O2 -> CO2 + H2O");
        Bond knownQuantityBond = new Parser().parseBond("O2");
        double knownQuantityMass = 2;
        
        try (PrintWriter pw = new PrintWriter(System.out, true)) {
            ChemicalEquation balancedCe = balance(pw, ce);
            calculateMasses(pw, balancedCe, knownQuantityBond, knownQuantityMass);
        }
    }
    
    
    
    
    public static ChemicalEquation balance(Writer writer, ChemicalEquation ce) throws IOException {
        Preconditions.checkNotNull(writer);
        Preconditions.checkNotNull(ce);
        
        
        MarkdownHelper.chemicalEquation(writer, ce);
        writer.write("\n\n");
        
        
        
        // unbalance
        writer.write("Removing stoichiometric coefficients: ");
        ChemicalEquation unbalancedCe = new ChemicalEquation(
                new ChemicalEquationSet(
                        ce.reactants.items.stream()
                               .map(i -> new ChemicalEquationUnit(1, i.bond))
                               .collect(ImmutableList.toImmutableList())
                ),
                new ChemicalEquationSet(
                        ce.products.items.stream()
                               .map(i -> new ChemicalEquationUnit(1, i.bond))
                               .collect(ImmutableList.toImmutableList())
                ),
                ce.direction
        );
        MarkdownHelper.chemicalEquation(writer, unbalancedCe);
        writer.write("\n\n");
        
        
        
        // get all elements used
        writer.write("Counting up elements for each bond: \n\n");
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
            writer.write("\n");
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
            writer.write(" * " + bondMapping.get(i).var + " = " + stoichiometricCoefficient + "\n");
        }
        writer.write("\n\n");
        
        
        
        // get it to whole numbers the cheap-and-easy but inefficient way
        writer.write("Getting it to whole numbers: \n\n");
        double[] newRatios = stoichiometricRatios;
        for (int i = 1; i < 1000; i++) {
            boolean isWholeNums = Arrays.stream(newRatios).allMatch(d -> isWholeNumber(d, 0.0001));
            if (isWholeNums) {
                break;
            }
            int finalI = i;
            newRatios = Arrays.stream(stoichiometricRatios).map(d -> d * finalI).toArray();
            writer.write(" * Scaling by " + i + ": " + Arrays.stream(newRatios).mapToObj(d -> "" + d).collect(joining(", ")) + "\n");
        }
        stoichiometricRatios = newRatios;
        writer.write("\n\n");
        boolean isWholeNums = Arrays.stream(newRatios).allMatch(d -> isWholeNumber(d, 0.0001));
        if (!isWholeNums) {
            writer.write("Unable to get to whole nums");
            return null;
        }

        
        
        // print it back out
        ChemicalEquation balancedCe = new ChemicalEquation(
                new ChemicalEquationSet(
                        Streams.zip(
                                ce.reactants.items.stream(),
                                Arrays.stream(stoichiometricRatios).limit(ce.reactants.items.size()).boxed(), // limited to reactants
                                (a,b) -> new ChemicalEquationUnit(b.intValue(), a.bond))
                               .collect(ImmutableList.toImmutableList())
                ),
                new ChemicalEquationSet(
                        Streams.zip(
                                ce.products.items.stream(),
                                Arrays.stream(stoichiometricRatios).skip(ce.reactants.items.size()).boxed(), // skips past reactants
                                (a,b) -> new ChemicalEquationUnit(b.intValue(), a.bond))
                               .collect(ImmutableList.toImmutableList())
                ),
                ce.direction
        );
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




    public static double[] calculateMasses(Writer writer, ChemicalEquation ce, Bond bond, double bondGrams) throws IOException {
        Preconditions.checkNotNull(writer);
        Preconditions.checkNotNull(ce);
        
        var bonds = Stream.concat(
                ce.reactants.items.stream(),
                ce.products.items.stream()
        ).collect(toList());
        int idx = IntStream.range(0, bonds.size())
                .filter(i -> bonds.get(i).bond.equals(bond))
                .findFirst().getAsInt();
        
        if (idx == -1) {
            MarkdownHelper.bond(writer, bond);
            writer.write(" not found\n\n");
            return null;
        }
        
        writer.write("Converting " + bondGrams + "g of ");
        MarkdownHelper.bond(writer, bond);
        writer.write(" to moles: \n\n");
        double bondAtomicWeight = bond.items.stream().mapToDouble(bu -> bu.element.atomicWeight.lowerEndpoint()).sum();
        writer.write(" * total atomic weight: " + bondAtomicWeight + "amu\n");
        double bondGramsPerMole = bondAtomicWeight;
        writer.write(" * " + bondGramsPerMole + "g = 1 mole\n");
        double bondMoles = bondGrams / bondGramsPerMole;
        writer.write(" * " + bondGrams + "g = " + bondMoles + " mole\n");
        writer.write("\n\n");
        
        
        writer.write("Applying to ratios in balanced chemical equation to calculate remaining moles:\n\n");
        
        
        writer.write("Converting moles back to grams:\n\n");
        
        return null;
    }
}

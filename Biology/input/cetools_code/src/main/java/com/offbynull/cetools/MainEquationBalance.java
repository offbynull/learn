package com.offbynull.cetools;

import com.google.common.base.Preconditions;
import static com.google.common.collect.ImmutableList.toImmutableList;
import com.google.common.collect.LinkedHashMultiset;
import com.google.common.collect.Multiset;
import com.google.common.collect.Streams;
import com.offbynull.cetools.parser.Parser;
import java.io.IOException;
import java.io.PrintWriter;
import static java.util.Arrays.stream;
import java.util.Scanner;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toList;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import org.ejml.alg.dense.misc.RrefGaussJordanRowPivot;
import org.ejml.simple.SimpleMatrix;

public final class MainEquationBalance {
    public static void main(String[] args) throws Throwable {
        try (Scanner s = new Scanner(System.in);
                PrintWriter pw = new PrintWriter(System.out, true);
                MarkdownWriter mdw = new MarkdownWriter(pw)) {
            mdw.out("<div style=\"border:1px solid black;\">\n\n");
            String input = s.nextLine();
            
            mdw.out("Balancing ").out(input).out("\n\n");
            
            ChemicalEquation ce = new Parser().parseChemicalEquation(input);
            balanceEquation(mdw, ce);
            mdw.out("\n\n</div>\n\n");
        }
    }
    
    
    
    
    public static ChemicalEquation balanceEquation(MarkdownWriter mdw, ChemicalEquation ce) throws IOException {
        Preconditions.checkNotNull(mdw);
        Preconditions.checkNotNull(ce);        
        
        
        // unbalance
        mdw.out("Removing stoichiometric coefficients: ");
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
        mdw.out(unbalancedCe);
        mdw.out("\n\n");
        
        
        
        // get all elements used
        mdw.out("Counting up elements: \n\n");
        Multiset<Element> elementBag = LinkedHashMultiset.create();
        unbalancedCe.reactants.items.stream()
                .flatMap(i -> i.bond.items.stream())
                .forEach(bu -> elementBag.add(bu.element, bu.count));
        unbalancedCe.products.items.stream()
                .flatMap(i -> i.bond.items.stream())
                .forEach(bu -> elementBag.add(bu.element, bu.count));
        for (Multiset.Entry<Element> bagEntry : elementBag.entrySet()) {
            mdw.out(" * " + bagEntry.getElement().symbol + " -> " + bagEntry.getCount() + "\n");
        }

        int eqCount = elementBag.elementSet().size();
        mdw.out("\n\n");
        
        
        
        // list equations to solve
        mdw.out("For each element, determining linear equations to solve: \n\n");
        var bondMapping = Streams.zip(
                Stream.concat(unbalancedCe.reactants.items.stream(), unbalancedCe.products.items.stream()),
                IntStream.range('a', 'z').mapToObj(i -> i),
                (a,b) -> new VariableToBond("" + ((char) b.intValue()), a.bond))
                .sorted((a,b) -> a.var.compareTo(b.var))
                .collect(toList());
        for (var e : elementBag.elementSet()) {
            mdw.out(" * " + e.symbol + ": ");
            mdw.out("`{kt} ");
            int remainingReactants = unbalancedCe.reactants.items.size();
            for (var ceu : unbalancedCe.reactants.items) {
                var bondElemCount = ceu.bond.items.stream().mapToInt(bu -> bu.element.equals(e) ? bu.count : 0).sum();
                var bondVarName = bondMapping.stream().filter(bm -> bm.bond.equals(ceu.bond)).findFirst().get().var;
                mdw.out(bondElemCount + bondVarName);
                remainingReactants--;
                if (remainingReactants > 0) {
                    mdw.out(" + ");
                }
            }
            mdw.out(" = ");
            int remainingProducts = unbalancedCe.products.items.size();
            for (var ceu : unbalancedCe.products.items) {
                var bondElemCount = ceu.bond.items.stream().mapToInt(bu -> bu.element.equals(e) ? bu.count : 0).sum();
                var bondVarName = bondMapping.stream().filter(bm -> bm.bond.equals(ceu.bond)).findFirst().get().var;
                mdw.out(bondElemCount + bondVarName);
                remainingProducts--;
                if (remainingProducts > 0) {
                    mdw.out(" + ");
                }
            }
            mdw.out("`\n");
        }
        mdw.out("\n\n... where ...\n\n");
        for (var bondMap : bondMapping) {
            mdw.out(" * " + bondMap.var);
            mdw.out(" maps to ");
            mdw.out(bondMap.bond);
            mdw.out("\n");
        }
        mdw.out("\n\n");
        
        int varCount = bondMapping.size();
        
        
        
        // solve system of linear equations
          // solving using matrix instead of substitution: https://www.youtube.com/watch?v=1i2nvMli0GY
        mdw.out("Solving system of linear equations: \n\n");
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
            mdw.out("There are " + eqCount + " equations but " + varCount + " variables. For the last equation, picking"
                    + " the remaining variable and setting it to 1. We can do this because we're dealing with ratios -- the coefficients"
                    + " are all relative to each other.\n\n");
            matrixA[rowIdx][varCount - 1] = -1.0;
        } else {
            // missing more than 1 eq -- bail out
            mdw.out("Unable to balance! Not enough equations for variables");
            return null;
        }
        SimpleMatrix simpleMatrixA = new SimpleMatrix(matrixA);
        new RrefGaussJordanRowPivot().reduce(simpleMatrixA.getMatrix(), varCount - 1);
        double[] stoichiometricRatios = new double[varCount];
        for (var i = 0; i < varCount; i++) {
            double stoichiometricCoefficient = -simpleMatrixA.get(i, varCount - 1);
            stoichiometricRatios[i] = stoichiometricCoefficient;
            mdw.out(" * " + bondMapping.get(i).var + " (mapped to ");
            mdw.out(bondMapping.get(i).bond);
            mdw.out(") = " + stoichiometricCoefficient + "\n");
        }
        mdw.out("\n\n");
        
        
        
        // get it to whole numbers the cheap-and-easy but inefficient way
        mdw.out("Getting it to whole numbers: \n\n");
        double[] newRatios = stoichiometricRatios;
        for (int i = 1; i < 1000; i++) {
            boolean isWholeNums = stream(newRatios).allMatch(d -> isWholeNumber(d, 0.0001));
            if (isWholeNums) {
                break;
            }
            int finalI = i;
            newRatios = stream(stoichiometricRatios).map(d -> d * finalI).toArray();
            mdw.out(" * Scaling by " + i + ": " + stream(newRatios).mapToObj(d -> "" + d).collect(joining(", ")) + "\n");
        }
        stoichiometricRatios = newRatios;
        mdw.out("\n\n");
        boolean isWholeNums = stream(newRatios).allMatch(d -> isWholeNumber(d, 0.0001));
        if (!isWholeNums) {
            mdw.out("Unable to get to whole nums");
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
        mdw.out("Balanced chemical equation: ");
        mdw.out(balancedCe);
        mdw.out("\n\n");
        
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
}

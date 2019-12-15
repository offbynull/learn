package com.offbynull.chemeq.parser;

import com.offbynull.chemeq.ChemicalEquationUnit;
import com.offbynull.chemeq.Bond;
import com.offbynull.chemeq.ChemicalEquation;
import com.offbynull.chemeq.BondUnit;
import com.offbynull.chemeq.ChemicalEquationSet;
import com.google.common.collect.ImmutableList;
import static com.google.common.collect.ImmutableList.toImmutableList;
import com.offbynull.chemeq.Element;
import com.offbynull.chemeq.ElementLookup;
import com.offbynull.chemeq.ChemicalEquation.ChemicalEquationDirection;
import com.offbynull.chemeq.parser.generated.ChemBaseVisitor;
import com.offbynull.chemeq.parser.generated.ChemParser;
import static java.lang.Integer.parseInt;
import java.util.List;
import static java.util.stream.Collectors.toList;


public final class DomChemVisitor extends ChemBaseVisitor<Object> {

    @Override
    public Object visitUnidirChemEq(ChemParser.UnidirChemEqContext ctx) {
        ChemicalEquationSet reactants = (ChemicalEquationSet) visit(ctx.chemEqSet(0));
        ChemicalEquationDirection direction = ChemicalEquationDirection.UNIDIRECTIONAL;
        ChemicalEquationSet products = (ChemicalEquationSet) visit(ctx.chemEqSet(1));
        return new ChemicalEquation(reactants, products, direction);
    }

    @Override
    public Object visitBidirChemEq(ChemParser.BidirChemEqContext ctx) {
        ChemicalEquationSet reactants = (ChemicalEquationSet) visit(ctx.chemEqSet(0));
        ChemicalEquationDirection direction = ChemicalEquationDirection.BIDIRECTIONAL;
        ChemicalEquationSet products = (ChemicalEquationSet) visit(ctx.chemEqSet(1));
        return new ChemicalEquation(reactants, products, direction);
    }

    @Override
    public Object visitChemEqSet(ChemParser.ChemEqSetContext ctx) {
        ImmutableList<ChemicalEquationUnit> formulaUnits = ctx.chemEqUnit().stream()
                .map(fu -> (ChemicalEquationUnit) visit(fu))
                .collect(toImmutableList());
        return new ChemicalEquationSet(formulaUnits);
    }
 
    @Override
    public Object visitChemEqUnit(ChemParser.ChemEqUnitContext ctx) {
        int count = ctx.COUNT() == null ? 1 : parseInt(ctx.COUNT().getText());
        Bond bond = (Bond) visit(ctx.bond());
        return new ChemicalEquationUnit(count, bond);
    }
    
    @Override
    public Object visitBond(ChemParser.BondContext ctx) {
        ImmutableList<BondUnit> bondUnits = ctx.bondUnit().stream()
                .map(bul -> (List<BondUnit>) visit(bul))
                .flatMap(l -> l.stream())
                .collect(toImmutableList());
        return new Bond(bondUnits);
    }

    @Override
    public Object visitGroupedBondUnit(ChemParser.GroupedBondUnitContext ctx) {
        int count = ctx.COUNT() == null ? 1 : parseInt(ctx.COUNT().getText());
        return ctx.bondUnit().stream()
                .map(bul -> (List<BondUnit>) visit(bul))
                .flatMap(l -> l.stream())
                .map(bu -> new BondUnit(bu.element, bu.count * count))
                .collect(toList());
    }

    @Override
    public Object visitSingleBondUnit(ChemParser.SingleBondUnitContext ctx) {
        Element element = ElementLookup.bySymbol(ctx.SYMBOL().getText());
        int count = ctx.COUNT() == null ? 1 : parseInt(ctx.COUNT().getText());
        return List.of(new BondUnit(element, count));
    }
}
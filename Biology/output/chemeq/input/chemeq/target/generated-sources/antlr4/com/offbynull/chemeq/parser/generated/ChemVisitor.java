// Generated from com/offbynull/chemeq/parser/generated/Chem.g4 by ANTLR 4.7.2
package com.offbynull.chemeq.parser.generated;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link ChemParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface ChemVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by the {@code UnidirChemEq}
	 * labeled alternative in {@link ChemParser#chemEq}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnidirChemEq(ChemParser.UnidirChemEqContext ctx);
	/**
	 * Visit a parse tree produced by the {@code BidirChemEq}
	 * labeled alternative in {@link ChemParser#chemEq}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBidirChemEq(ChemParser.BidirChemEqContext ctx);
	/**
	 * Visit a parse tree produced by {@link ChemParser#chemEqSet}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChemEqSet(ChemParser.ChemEqSetContext ctx);
	/**
	 * Visit a parse tree produced by {@link ChemParser#chemEqUnit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChemEqUnit(ChemParser.ChemEqUnitContext ctx);
	/**
	 * Visit a parse tree produced by {@link ChemParser#bond}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBond(ChemParser.BondContext ctx);
	/**
	 * Visit a parse tree produced by the {@code SingleBondUnit}
	 * labeled alternative in {@link ChemParser#bondUnit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSingleBondUnit(ChemParser.SingleBondUnitContext ctx);
	/**
	 * Visit a parse tree produced by the {@code GroupedBondUnit}
	 * labeled alternative in {@link ChemParser#bondUnit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGroupedBondUnit(ChemParser.GroupedBondUnitContext ctx);
}
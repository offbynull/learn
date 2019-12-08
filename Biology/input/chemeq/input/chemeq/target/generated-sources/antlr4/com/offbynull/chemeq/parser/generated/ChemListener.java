// Generated from com/offbynull/chemeq/parser/generated/Chem.g4 by ANTLR 4.7.2
package com.offbynull.chemeq.parser.generated;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link ChemParser}.
 */
public interface ChemListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by the {@code UnidirChemEq}
	 * labeled alternative in {@link ChemParser#chemEq}.
	 * @param ctx the parse tree
	 */
	void enterUnidirChemEq(ChemParser.UnidirChemEqContext ctx);
	/**
	 * Exit a parse tree produced by the {@code UnidirChemEq}
	 * labeled alternative in {@link ChemParser#chemEq}.
	 * @param ctx the parse tree
	 */
	void exitUnidirChemEq(ChemParser.UnidirChemEqContext ctx);
	/**
	 * Enter a parse tree produced by the {@code BidirChemEq}
	 * labeled alternative in {@link ChemParser#chemEq}.
	 * @param ctx the parse tree
	 */
	void enterBidirChemEq(ChemParser.BidirChemEqContext ctx);
	/**
	 * Exit a parse tree produced by the {@code BidirChemEq}
	 * labeled alternative in {@link ChemParser#chemEq}.
	 * @param ctx the parse tree
	 */
	void exitBidirChemEq(ChemParser.BidirChemEqContext ctx);
	/**
	 * Enter a parse tree produced by {@link ChemParser#chemEqSet}.
	 * @param ctx the parse tree
	 */
	void enterChemEqSet(ChemParser.ChemEqSetContext ctx);
	/**
	 * Exit a parse tree produced by {@link ChemParser#chemEqSet}.
	 * @param ctx the parse tree
	 */
	void exitChemEqSet(ChemParser.ChemEqSetContext ctx);
	/**
	 * Enter a parse tree produced by {@link ChemParser#chemEqUnit}.
	 * @param ctx the parse tree
	 */
	void enterChemEqUnit(ChemParser.ChemEqUnitContext ctx);
	/**
	 * Exit a parse tree produced by {@link ChemParser#chemEqUnit}.
	 * @param ctx the parse tree
	 */
	void exitChemEqUnit(ChemParser.ChemEqUnitContext ctx);
	/**
	 * Enter a parse tree produced by {@link ChemParser#bond}.
	 * @param ctx the parse tree
	 */
	void enterBond(ChemParser.BondContext ctx);
	/**
	 * Exit a parse tree produced by {@link ChemParser#bond}.
	 * @param ctx the parse tree
	 */
	void exitBond(ChemParser.BondContext ctx);
	/**
	 * Enter a parse tree produced by the {@code SingleBondUnit}
	 * labeled alternative in {@link ChemParser#bondUnit}.
	 * @param ctx the parse tree
	 */
	void enterSingleBondUnit(ChemParser.SingleBondUnitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code SingleBondUnit}
	 * labeled alternative in {@link ChemParser#bondUnit}.
	 * @param ctx the parse tree
	 */
	void exitSingleBondUnit(ChemParser.SingleBondUnitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code GroupedBondUnit}
	 * labeled alternative in {@link ChemParser#bondUnit}.
	 * @param ctx the parse tree
	 */
	void enterGroupedBondUnit(ChemParser.GroupedBondUnitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code GroupedBondUnit}
	 * labeled alternative in {@link ChemParser#bondUnit}.
	 * @param ctx the parse tree
	 */
	void exitGroupedBondUnit(ChemParser.GroupedBondUnitContext ctx);
}
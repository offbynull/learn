package com.offbynull.chemeq.model.equation;

public interface BinaryOperation extends Tree {
    Tree lefthand();
    Tree righthand();
    BinaryOperation invert();
}

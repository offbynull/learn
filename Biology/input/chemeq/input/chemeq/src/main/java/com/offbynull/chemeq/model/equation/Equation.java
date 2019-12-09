package com.offbynull.chemeq.model.equation;

import com.google.common.base.Preconditions;
import java.util.Objects;

public final class Equation {
    
    HOW TO ISOLATE FOR A VARIABLE:
    1. check for mul by 0 -- remove these
    1. check for mul by 1 -- remove the mul
    1. check for operations on contants -- if found simplify
    2. check for fractions -- if found, multiply both sides by the denomiators
    3. expand out out the multiplications -- THIS WILL BE A PROBLEM BECAUSE IT MAY LEAD TO EXPONENTS
    
            
            IT MAY BE A BETTER IDEA TO EXPERIMENT WITH EJMLs SIMPLEMATRIX.SOLVE() -- SEE LINKS BELOW
            
            https://github.com/lessthanoptimal/ejml
            https://www.khanacademy.org/math/precalculus/x9e81a4f98389efdf:matrices/x9e81a4f98389efdf:solving-equations-with-inverse-matrices/v/solving-matrix-equation%20%20%20%20

            
    public final Tree lefthand;
    public final Tree righthand;

    public Equation(Tree lefthand, Tree righthand) {
        Preconditions.checkNotNull(lefthand);
        Preconditions.checkNotNull(righthand);
        this.lefthand = lefthand;
        this.righthand = righthand;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 23 * hash + Objects.hashCode(this.lefthand);
        hash = 23 * hash + Objects.hashCode(this.righthand);
        return hash;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final Equation other = (Equation) obj;
        if (!Objects.equals(this.lefthand, other.lefthand)) {
            return false;
        }
        if (!Objects.equals(this.righthand, other.righthand)) {
            return false;
        }
        return true;
    }
    
}

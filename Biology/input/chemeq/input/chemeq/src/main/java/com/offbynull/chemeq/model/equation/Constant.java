package com.offbynull.chemeq.model.equation;

import com.google.common.base.Preconditions;

public final class Constant implements Tree {
    public final double value;

    public Constant(double value) {
        Preconditions.checkArgument(Double.isFinite(value));
        this.value = value;
    }

    @Override
    public int hashCode() {
        int hash = 5;
        hash = 31 * hash + (int) (Double.doubleToLongBits(this.value) ^ (Double.doubleToLongBits(this.value) >>> 32));
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
        final Constant other = (Constant) obj;
        if (Double.doubleToLongBits(this.value) != Double.doubleToLongBits(other.value)) {
            return false;
        }
        return true;
    }
    
}

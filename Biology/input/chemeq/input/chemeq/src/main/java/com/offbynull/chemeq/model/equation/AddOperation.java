package com.offbynull.chemeq.model.equation;

import com.google.common.base.Preconditions;
import java.util.Objects;

public final class AddOperation implements BinaryOperation {
    
    private final Tree lefthand;
    private final Tree righthand;

    public AddOperation(Tree lefthand, Tree righthand) {
        Preconditions.checkNotNull(lefthand);
        Preconditions.checkNotNull(righthand);
        this.lefthand = lefthand;
        this.righthand = righthand;
    }

    @Override
    public Tree lefthand() {
        return this.lefthand;
    }

    @Override
    public Tree righthand() {
        return this.righthand;
    }

    @Override
    public BinaryOperation invert() {
        return new SubtractOperation(righthand, lefthand);
    }

    @Override
    public int hashCode() {
        int hash = 3;
        hash = 11 * hash + Objects.hashCode(this.lefthand);
        hash = 11 * hash + Objects.hashCode(this.righthand);
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
        final AddOperation other = (AddOperation) obj;
        if (!Objects.equals(this.lefthand, other.lefthand)) {
            return false;
        }
        if (!Objects.equals(this.righthand, other.righthand)) {
            return false;
        }
        return true;
    }
}

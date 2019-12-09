package com.offbynull.chemeq.model.equation;

import com.google.common.base.Preconditions;
import java.util.Objects;

public final class Variable implements Tree {
    public final String id;

    public Variable(String id) {
        Preconditions.checkNotNull(id);
        this.id = id;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 37 * hash + Objects.hashCode(this.id);
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
        final Variable other = (Variable) obj;
        if (!Objects.equals(this.id, other.id)) {
            return false;
        }
        return true;
    }
    
}

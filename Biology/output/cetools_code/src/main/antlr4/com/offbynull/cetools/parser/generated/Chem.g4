grammar Chem;

chemEq:
        chemEqSet '->' chemEqSet                 #UnidirChemEq     // e.g. 2H2 + O2 ->  2H2O
        | chemEqSet '<->' chemEqSet              #BidirChemEq      // e.g. 2H2 + O2 <-> 2H2O
        ;

chemEqSet: (chemEqUnit '+')* chemEqUnit;                           // e.g. 2H2O + NaCl
chemEqUnit: COUNT? bond;                                           // e.g. 2H2O

bond: bondUnit+;                                                   // e.g. Fe2(HO)3
bondUnit:
        SYMBOL COUNT?                           # SingleBondUnit   // e.g. Fe2
        | '(' bondUnit+ ')' COUNT?              # GroupedBondUnit  // e.g. (H2O)3
        ;                                            

UNIDIRECTIONAL: '->';
BIDIRECTIONAL: '<->';
PLUS: '+';
COUNT: [0-9]+;
SYMBOL: [A-Z] [a-z]*;
WS: [ \t\n\r]+ -> skip;
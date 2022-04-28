
edgecardinality(C) :- C = #count { U,V : edge((U,V)), U < V }.

1 { walk((1,V),I) : edge((1,V)) } 1 :- mintime(I).
1 { walk((V,W),I+1) : edge((V,W)) } 1 :- walk((U,V), I), mintime(I).
1 { walk((V,W),T) : edge((V,W)), walk((_,V),T-1) } 1 :- T <= E, edgecardinality(E), walk(_,T-1), maxtime(A), T<=A.
0 { walk((V,W),T) : edge((V,W)), walk((_,V),T-1) } 1 :- T > E, edgecardinality(E), walk(_,T-1), maxtime(A), T<=A.

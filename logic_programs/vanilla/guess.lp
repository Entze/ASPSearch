
1 { walk(E,I)   : edge(E) } 1 :- mintime(I).
1 { walk(E,I+1) : edge(E) } 1 :- mintime(I).
  { walk(E,T)   : edge(E) } 1 :- walk(_,T-1), maxtime(A), T<=A.

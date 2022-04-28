
time(I..A) :- mintime(I), maxtime(A).

0 { walk(E,T) : edge(E) } 1 :- time(T).


walk(E,T) :-
  edge(E), time(T),
  continue(T),
  not else(E,T).

else(E1,T) :-
 time(T), edge(E1), edge(E2),
 E1 != E2,
 walk(E2,T).

time(I..A) :- mintime(I), maxtime(A).

continue(I) :- mintime(I).

continue(T) :-
 time(T),
 continue(T-1),
 not stop(T).

stop(T+1) :-
  time(T+1),
  stop(T).

stop(T) :-
 time(T),
 not continue(T).

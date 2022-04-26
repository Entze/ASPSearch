#program always.

walk(E) :-
  edge(E),
  not else(E).

else(E1) :-
  edge(E1), edge(E2), E1 != E2,
  walk(E2).

cost(C+W) :- 'cost(C), walk(E), edge_weight(E,W).

#show walk/1.
#show cost/1.

#program initial.

else((U,V)) :-
  edge((U,V)), U != 1.

:- edge((U,V)), edge((V,U)), not &tel { >? (walk((U,V)) | walk((V,U))) }.

cost(W) :- walk(E), edge_weight(E,W).

#program dynamic.

else((W,X)) :-
  edge((W,X)),
  'walk((U,V)), V != W.

#program final.

else((W,X)) :-
  edge((W,X)), X != 1.

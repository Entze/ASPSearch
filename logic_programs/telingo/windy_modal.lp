#program always.

walk(E) :-
  edge(E),
  not else(E).

else(E1) :-
  edge(E1), edge(E2), E1 != E2,
  walk(E2).

#show walk/1.

#program initial.

:- edge((U,V)), edge((V,U)), not &del { * &true .>? walk((U,V)) }, not &del { * &true .>? walk((V,U)) }.

else((U,V)) :-
  edge((U,V)), U != 1.

#program dynamic.

%                             :- not &del{ * &t      .>* ?load        ;; &t    .>* loaded}.
:- edge((U,V)), edge((W,X)), V != W, &del { * &true .>* ? walk((U,V)) ;; &true .>* walk((W,X)) }.

#program final.

else((W,X)) :-
  edge((W,X)), X != 1.

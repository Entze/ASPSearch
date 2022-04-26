lasttime(L) :- walk(_,L), not walk(_,L+1).

:- edge((U,V)), edge((V,U)), not walk((U,V), _), not walk((V,U), _).
:-                          edge((U,V)), walk((U,V), T), walk((V,W), T+1), not edge((V,W)).
:- mintime(I), lasttime(A), edge((U,V)), walk((U,V), A), walk((V,W),   I), not edge((V,W)).
:-                          walk((U,V),T), walk((W,X), T+1), V != W.
:- mintime(I), lasttime(A), walk((U,V),A), walk((W,X),   I), V != W.

:- mintime(I), not walk((1,_), I).
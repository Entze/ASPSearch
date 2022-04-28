
lastwalk(L) :- walk(_,L), not walk(_,L+1).

:- mintime(I), not walk((1,_), I).
:- lastwalk(L), not walk((_,1), L).
:- edge((U,V)), edge((V,U)), not walk((U,V), _), not walk((V,U), _).
:- lastwalk(L), walk(_,T), L < T.

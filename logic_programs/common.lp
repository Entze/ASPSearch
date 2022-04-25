attr(edge, E, label, W) :- edge(E), edge_weight(E, W).
attr(edge, E, dir, forward) :- edge(E).

attr(edge, E, color, red) :- edge(E), walk(E, T).
attr(edge, E, style, dotted) :- edge(E), not walk(E, _).

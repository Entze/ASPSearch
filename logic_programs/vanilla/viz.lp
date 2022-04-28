
attr(edge, E, label, W) :- edge(E), edge_weight(E, W).
attr(edge, E, dir, forward) :- edge(E).

attr(edge, E, color, gray) :- edge(E), #count { T : walk(E, T) } = 0.
attr(edge, E, color, red) :- edge(E), #count { T : walk(E, T) } = W, W >= 1.
attr(edge, E, width, W) :- edge(E), #count { T : walk(E, T) } = W, W >= 1.
attr(edge, E, style, dashed) :- edge(E), not walk(E, _).

attr(graph, default, model, "circuit").

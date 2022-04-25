
cost(C) :- C = #sum{ W,T : walk(E,T), edge_weight(E,W) }.

#minimize { C : cost(C) }.
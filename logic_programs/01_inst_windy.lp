
node(1).
node(2).
node(3).

edge((1,2)).
edge((1,3)).
edge((2,1)).
edge((2,3)).
edge((3,1)).
edge((3,2)).

edge_weight((1,2), 10).
edge_weight((2,3), 10).
edge_weight((3,1), 10).
edge_weight((2,1), 100).
edge_weight((3,2), 100).
edge_weight((1,3), 100).

mintime(1).
%maxtime(3).

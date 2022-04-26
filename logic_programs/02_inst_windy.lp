node(1).
node(2).
node(3).
node(4).

edge((1,2)).
edge((1,3)).
edge((1,4)).
edge((2,1)).
edge((2,3)).
edge((3,1)).
edge((3,2)).
edge((3,4)).
edge((4,1)).
edge((4,3)).

edge_weight((1,2), 10).
edge_weight((2,3), 10).
edge_weight((3,1), 10).
edge_weight((3,4), 10).
edge_weight((4,1), 10).
edge_weight((1,4), 100).
edge_weight((2,1), 100).
edge_weight((3,2), 100).
edge_weight((1,3), 100).
edge_weight((4,3), 100).

mintime(1).
maxtime(50).
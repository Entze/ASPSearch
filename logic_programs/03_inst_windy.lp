
% ( 1, 2)   coste      17       16
% ( 1,13)   coste      35       15
% ( 2, 3)   coste      11        8
% ( 2,14)   coste      18        3
% ( 3, 4)   coste       1        3
% ( 3, 5)   coste       4        3
% ( 4, 5)   coste       7        5
% ( 5, 6)   coste       2        1
% ( 5, 7)   coste       3        2
% ( 6, 7)   coste       2        2
% ( 6,14)   coste      14       11
% ( 7, 8)   coste      12        8
% ( 8, 9)   coste       6        2
% ( 8,12)   coste      18       20
% ( 9,10)   coste       6        7
% ( 9,11)   coste      26       30
% ( 9,12)   coste       8       14
% (10,11)   coste      11        5
% (12,13)   coste       9       15
% (12,14)   coste       6        9
% (13,14)   coste       7        5

node(1..14).

edge(( 1, 2)).
edge(( 1,13)).
edge(( 2, 3)).
edge(( 2,14)).
edge(( 3, 4)).
edge(( 3, 5)).
edge(( 4, 5)).
edge(( 5, 6)).
edge(( 5, 7)).
edge(( 6, 7)).
edge(( 6,14)).
edge(( 7, 8)).
edge(( 8, 9)).
edge(( 8,12)).
edge(( 9,10)).
edge(( 9,11)).
edge(( 9,12)).
edge((10,11)).
edge((12,13)).
edge((12,14)).
edge((13,14)).
edge((U,V)) :- edge((V,U)).

edge_weight(( 1, 2),17). edge_weight(( 2, 1),16).
edge_weight(( 1,13),35). edge_weight((13, 1),15).
edge_weight(( 2, 3),11). edge_weight(( 3, 2),8).
edge_weight(( 2,14),18). edge_weight((14, 2),3).
edge_weight(( 3, 4),1). edge_weight(( 4, 3),3).
edge_weight(( 3, 5),4). edge_weight(( 5, 3),3).
edge_weight(( 4, 5),7). edge_weight(( 5, 4),5).
edge_weight(( 5, 6),2). edge_weight(( 6, 5),1).
edge_weight(( 5, 7),3). edge_weight(( 7, 5),2).
edge_weight(( 6, 7),2). edge_weight(( 7, 6),2).
edge_weight(( 6,14),14). edge_weight((14, 6),11).
edge_weight(( 7, 8),12). edge_weight(( 8, 7),8).
edge_weight(( 8, 9),6). edge_weight(( 9, 8),2).
edge_weight(( 8,12),18). edge_weight((12, 8),20).
edge_weight(( 9,10),6). edge_weight((10, 9),7).
edge_weight(( 9,11),26). edge_weight((11, 9),30).
edge_weight(( 9,12),8). edge_weight((12, 9),14).
edge_weight((10,11),11). edge_weight((11,10),5).
edge_weight((12,13),9). edge_weight((13,12),15).
edge_weight((12,14),6). edge_weight((14,12),9).
edge_weight((13,14),7). edge_weight((14,13),5).

mintime(1).
%maxtime(30).

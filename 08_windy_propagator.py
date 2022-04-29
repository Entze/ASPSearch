import time
from threading import Lock
from typing import Tuple, MutableMapping, Set, Dict, List

import clingo
from clingo import Propagator, PropagateInit

inst1 = """

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
maxtime(6).

"""
inst2 = """

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
maxtime(10).

"""

inst3 = """
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
maxtime(30).
"""

inst4 = """

ground_edges(   1, 129,   471,      579).
ground_edges(   1, 174,   601,      706).
ground_edges(   1, 256,   893,      798).
ground_edges(   1, 436,   661,      632).
ground_edges(   2, 125,   898,     1028).
ground_edges(   3,  19,   716,      633).
ground_edges(   4, 180,   145,      127).
ground_edges(   4, 266,   372,      507).
ground_edges(   4, 498,   658,      594).
ground_edges(   5, 168,   174,      286).
ground_edges(   5, 287,   843,      689).
ground_edges(   5, 306,   151,      114).
ground_edges(   6,   8,   341,      248).
ground_edges(   6, 154,   446,      368).
ground_edges(   6, 170,   612,      585).
ground_edges(   6, 391,   393,      374).
ground_edges(   7, 156,   643,      728).
ground_edges(   7, 204,   706,      761).
ground_edges(   7, 330,   217,      316).
ground_edges(   7, 406,   527,      652).
ground_edges(   8,  71,   409,      303).
ground_edges(   8, 403,   306,      278).
ground_edges(   8, 416,   399,      570).
ground_edges(   8, 476,   702,      691).
ground_edges(   8, 482,   106,      199).
ground_edges(   9,  42,   547,      506).
ground_edges(   9,  94,   456,      379).
ground_edges(   9, 482,   781,      865).
ground_edges(   9, 500,   593,      596).
ground_edges(  10, 288,   1028,      935).
ground_edges(  10, 457,   482,      500).
ground_edges(  11,  15,   149,      278).
ground_edges(  11,  32,   638,      707).
ground_edges(  11, 175,   458,      466).
ground_edges(  11, 356,   442,      532).
ground_edges(  11, 384,   848,      696).
ground_edges(  11, 407,   906,      827).
ground_edges(  12, 294,   1,       72).
ground_edges(  12, 460,   247,      271).
ground_edges(  13, 331,   223,      312).
ground_edges(  14, 298,   270,      216).
ground_edges(  14, 456,   304,      307).
ground_edges(  15,  25,   678,      847).
ground_edges(  15, 361,   28,       72).
ground_edges(  16, 102,   568,      691).
ground_edges(  16, 116,   282,      303).
ground_edges(  16, 184,   460,      386).
ground_edges(  16, 215,   218,      231).
ground_edges(  16, 328,   600,      424).
ground_edges(  16, 447,   372,      357).
ground_edges(  17,  65,   595,      455).
ground_edges(  17,  87,   648,      757).
ground_edges(  17, 118,   693,      748).
ground_edges(  17, 122,   561,      645).
ground_edges(  17, 177,   583,      402).
ground_edges(  17, 246,   598,      534).
ground_edges(  17, 251,   510,      487).
ground_edges(  17, 372,   547,      457).
ground_edges(  18,  56,   254,      199).
ground_edges(  18,  77,   373,      275).
ground_edges(  18,  91,   421,      319).
ground_edges(  18, 187,   19,      104).
ground_edges(  18, 218,   656,      665).
ground_edges(  19, 443,   260,      297).
ground_edges(  20,  62,   675,      668).
ground_edges(  20,  74,   418,      570).
ground_edges(  20,  97,   149,      286).
ground_edges(  20, 238,   539,      559).
ground_edges(  20, 288,   769,      648).
ground_edges(  20, 289,   567,      522).
ground_edges(  21, 168,   140,      312).
ground_edges(  21, 188,   48,      201).
ground_edges(  21, 299,   641,      778).
ground_edges(  21, 440,   760,      748).
ground_edges(  21, 457,   332,      287).
ground_edges(  22, 234,   828,      695).
ground_edges(  22, 371,   910,      736).
ground_edges(  23,  25,   259,      280).
ground_edges(  23, 238,   541,      586).
ground_edges(  23, 261,   550,      567).
ground_edges(  24,  34,   280,      356).
ground_edges(  24, 145,   435,      537).
ground_edges(  24, 158,   108,      186).
ground_edges(  24, 177,   1009,      888).
ground_edges(  25, 397,   667,      666).
ground_edges(  26, 174,   851,      986).
ground_edges(  27,  67,   951,      906).
ground_edges(  27, 312,   513,      505).
ground_edges(  27, 373,   934,      950).
ground_edges(  27, 464,   539,      476).
ground_edges(  28, 105,   348,      411).
ground_edges(  28, 116,   285,      244).
ground_edges(  28, 312,   495,      377).
ground_edges(  29, 149,   177,      126).
ground_edges(  30,  42,   560,      632).
ground_edges(  30, 207,   611,      413).
ground_edges(  30, 252,   674,      700).
ground_edges(  30, 334,   737,      819).
ground_edges(  31,  82,   496,      408).
ground_edges(  31, 286,   335,      263).
ground_edges(  31, 375,   879,      722).
ground_edges(  31, 392,   500,      405).
ground_edges(  31, 438,   204,      121).
ground_edges(  32,  34,   396,      592).
ground_edges(  32, 488,   627,      434).
ground_edges(  33,  87,   723,      647).
ground_edges(  33, 476,   83,        1).
ground_edges(  33, 495,   706,      672).
ground_edges(  34, 122,   567,      561).
ground_edges(  34, 261,   979,     1032).
ground_edges(  34, 298,   703,      611).
ground_edges(  34, 351,   554,      570).
ground_edges(  34, 460,   481,      500).
ground_edges(  35, 281,   319,      395).
ground_edges(  35, 414,   434,      517).
ground_edges(  36, 115,   515,      540).
ground_edges(  36, 210,   415,      364).
ground_edges(  36, 495,   369,      418).
ground_edges(  37,  45,   836,      848).
ground_edges(  37, 228,   514,      496).
ground_edges(  38, 386,   1023,      998).
ground_edges(  38, 465,   459,      321).
ground_edges(  39, 128,   372,      477).
ground_edges(  39, 277,   952,     1021).
ground_edges(  39, 424,   585,      537).
ground_edges(  40,  62,   399,      440).
ground_edges(  40, 120,   838,     1013).
ground_edges(  41, 112,   430,      437).
ground_edges(  41, 435,   484,      580).
ground_edges(  41, 484,   237,      278).
ground_edges(  42, 232,   624,      589).
ground_edges(  42, 332,   829,      849).
ground_edges(  43, 115,   409,      282).
ground_edges(  43, 207,   247,      264).
ground_edges(  43, 255,   562,      544).
ground_edges(  43, 319,   250,      230).
ground_edges(  44, 187,   644,      688).
ground_edges(  44, 311,   1017,     1146).
ground_edges(  44, 475,   146,      207).
ground_edges(  45, 470,   278,      333).
ground_edges(  46, 100,   92,      195).
ground_edges(  46, 102,   1068,     1049).
ground_edges(  46, 407,   744,      659).
ground_edges(  46, 460,   614,      543).
ground_edges(  47, 261,   378,      315).
ground_edges(  47, 277,   293,      441).
ground_edges(  47, 312,   432,      335).
ground_edges(  47, 479,   385,      417).
ground_edges(  48,  59,   906,     1025).
ground_edges(  48,  80,   547,      527).
ground_edges(  48, 371,   632,      608).
ground_edges(  49, 114,   505,      514).
ground_edges(  49, 297,   267,      359).
ground_edges(  49, 354,   534,      505).
ground_edges(  50, 157,   432,      287).
ground_edges(  50, 211,   814,      685).
ground_edges(  50, 248,   837,      788).
ground_edges(  51,  55,   194,      368).
ground_edges(  52, 225,   690,      643).
ground_edges(  52, 291,   363,      354).
ground_edges(  52, 316,   546,      455).
ground_edges(  52, 374,   250,      256).
ground_edges(  52, 457,   417,      365).
ground_edges(  52, 492,   630,      526).
ground_edges(  53, 247,   132,      171).
ground_edges(  53, 270,   664,      681).
ground_edges(  54,  94,   277,      394).
ground_edges(  54,  97,   784,      669).
ground_edges(  54, 104,   470,      460).
ground_edges(  54, 135,   346,      321).
ground_edges(  54, 346,   290,      208).
ground_edges(  54, 457,   387,      400).
ground_edges(  55, 252,   144,       45).
ground_edges(  55, 388,   767,      589).
ground_edges(  55, 414,   651,      581).
ground_edges(  56, 172,   899,      861).
ground_edges(  57, 408,   782,      860).
ground_edges(  57, 448,   400,      504).
ground_edges(  57, 452,   680,      706).
ground_edges(  58, 201,   647,      668).
ground_edges(  58, 246,   696,      724).
ground_edges(  59, 213,   438,      407).
ground_edges(  59, 227,   1017,      858).
ground_edges(  59, 357,   360,      280).
ground_edges(  60, 211,   1088,     1178).
ground_edges(  60, 378,   902,      868).
ground_edges(  61, 236,   156,      150).
ground_edges(  61, 280,   695,      503).
ground_edges(  61, 496,   473,      528).
ground_edges(  62, 280,   697,      794).
ground_edges(  62, 301,   558,      659).
ground_edges(  63, 146,   107,        2).
ground_edges(  63, 190,   344,      316).
ground_edges(  63, 446,   792,      662).
ground_edges(  64, 189,   400,      378).
ground_edges(  64, 259,   316,      214).
ground_edges(  64, 453,   133,      193).
ground_edges(  65, 181,   332,      276).
ground_edges(  65, 376,   622,      671).
ground_edges(  65, 451,   771,      800).
ground_edges(  66,  92,   1035,     1143).
ground_edges(  66, 345,   869,      821).
ground_edges(  66, 433,   539,      428).
ground_edges(  67, 111,   552,      610).
ground_edges(  67, 181,   414,      448).
ground_edges(  67, 451,   268,      340).
ground_edges(  68, 151,   657,      491).
ground_edges(  68, 183,   526,      498).
ground_edges(  69, 201,   473,      527).
ground_edges(  70, 114,   549,      593).
ground_edges(  70, 466,   287,      373).
ground_edges(  72, 181,   611,      626).
ground_edges(  72, 193,   440,      337).
ground_edges(  72, 242,   224,      226).
ground_edges(  72, 370,   451,      500).
ground_edges(  72, 396,   463,      306).
ground_edges(  72, 408,   1206,     1102).
ground_edges(  72, 411,   1001,      863).
ground_edges(  72, 435,   711,      667).
ground_edges(  72, 500,   570,      550).
ground_edges(  73, 220,   276,      307).
ground_edges(  73, 221,   279,      408).
ground_edges(  74, 268,   71,       54).
ground_edges(  74, 381,   691,      700).
ground_edges(  74, 386,   925,      829).
ground_edges(  75, 159,   632,      490).
ground_edges(  75, 308,   930,      914).
ground_edges(  75, 454,   598,      663).
ground_edges(  75, 493,   763,      731).
ground_edges(  76, 152,   611,      678).
ground_edges(  76, 166,   306,      409).
ground_edges(  76, 317,   296,      448).
ground_edges(  76, 375,   856,     1023).
ground_edges(  78, 161,   325,      308).
ground_edges(  78, 215,   700,      667).
ground_edges(  78, 248,   488,      617).
ground_edges(  78, 303,   633,      636).
ground_edges(  78, 364,   610,      536).
ground_edges(  79, 258,   449,      446).
ground_edges(  79, 394,   352,      210).
ground_edges(  79, 413,   327,      263).
ground_edges(  80, 259,   791,      732).
ground_edges(  81, 151,   753,      781).
ground_edges(  81, 368,   271,      218).
ground_edges(  81, 384,   868,      938).
ground_edges(  81, 444,   675,      600).
ground_edges(  82, 165,   579,      671).
ground_edges(  82, 352,   144,      204).
ground_edges(  83, 147,   516,      445).
ground_edges(  84, 127,   662,      821).
ground_edges(  84, 128,   118,      161).
ground_edges(  84, 405,   316,      324).
ground_edges(  84, 418,   638,      651).
ground_edges(  84, 443,   510,      481).
ground_edges(  84, 456,   233,      383).
ground_edges(  85, 405,   24,      130).
ground_edges(  86, 103,   954,     1007).
ground_edges(  86, 343,   531,      579).
ground_edges(  87, 316,   872,      667).
ground_edges(  88, 137,   622,      614).
ground_edges(  88, 213,   191,      264).
ground_edges(  88, 240,   362,      380).
ground_edges(  88, 340,   230,      260).
ground_edges(  89, 127,   49,      194).
ground_edges(  89, 128,   997,     1024).
ground_edges(  89, 418,   799,      841).
ground_edges(  90, 401,   5,        1).
ground_edges(  91, 456,   811,      820).
ground_edges(  92, 327,   944,      851).
ground_edges(  93, 277,   900,      962).
ground_edges(  94, 211,   395,      322).
ground_edges(  94, 367,   243,      288).
ground_edges(  94, 369,   358,      325).
ground_edges(  94, 410,   164,      169).
ground_edges(  95, 133,   787,      739).
ground_edges(  95, 450,   269,      300).
ground_edges(  96, 480,   248,      212).
ground_edges(  97, 250,   915,      920).
ground_edges(  97, 284,   710,      696).
ground_edges(  97, 447,   331,      403).
ground_edges(  98, 144,   297,      403).
ground_edges(  98, 253,   1012,      922).
ground_edges(  99, 182,   1006,     1126).
ground_edges(  99, 389,   1170,     1286).
ground_edges(  99, 402,   276,      407).
ground_edges(  99, 454,   757,      559).
ground_edges(  99, 481,   901,      875).
ground_edges( 100, 131,   795,      817).
ground_edges( 100, 296,   639,      707).
ground_edges( 101, 271,   539,      635).
ground_edges( 102, 293,   502,      573).
ground_edges( 102, 405,   564,      697).
ground_edges( 103, 315,   309,      255).
ground_edges( 103, 432,   652,      647).
ground_edges( 103, 464,   933,      916).
ground_edges( 103, 489,   876,      742).
ground_edges( 105, 463,   823,      857).
ground_edges( 105, 489,   606,      604).
ground_edges( 106, 224,   151,       76).
ground_edges( 106, 477,   745,      823).
ground_edges( 107, 278,   62,      222).
ground_edges( 107, 427,   282,      466).
ground_edges( 107, 447,   786,      813).
ground_edges( 107, 490,   86,      251).
ground_edges( 108, 177,   1289,     1370).
ground_edges( 108, 253,   1068,     1029).
ground_edges( 108, 263,   271,      209).
ground_edges( 109, 424,   931,      795).
ground_edges( 110, 146,   871,      888).
ground_edges( 110, 191,   264,      284).
ground_edges( 110, 213,   201,      326).
ground_edges( 111, 149,   221,      251).
ground_edges( 111, 364,   192,      160).
ground_edges( 111, 415,   853,      890).
ground_edges( 112, 120,   394,      530).
ground_edges( 112, 190,   284,      270).
ground_edges( 112, 241,   303,      369).
ground_edges( 113, 170,   648,      628).
ground_edges( 113, 349,   538,      485).
ground_edges( 114, 241,   353,      431).
ground_edges( 114, 380,   642,      562).
ground_edges( 114, 384,   673,      617).
ground_edges( 114, 441,   364,      510).
ground_edges( 114, 479,   452,      354).
ground_edges( 116, 419,   471,      432).
ground_edges( 116, 483,   347,      395).
ground_edges( 117, 459,   371,      531).
ground_edges( 118, 187,   671,      742).
ground_edges( 118, 355,   609,      584).
ground_edges( 118, 500,   460,      359).
ground_edges( 119, 209,   399,      398).
ground_edges( 119, 239,   613,      708).
ground_edges( 119, 353,   747,      785).
ground_edges( 120, 366,   588,      742).
ground_edges( 120, 482,   970,      992).
ground_edges( 121, 366,   193,      299).
ground_edges( 121, 466,   201,      141).
ground_edges( 122, 204,   597,      527).
ground_edges( 122, 229,   904,      785).
ground_edges( 122, 377,   44,       97).
ground_edges( 123, 413,   314,      405).
ground_edges( 124, 477,   280,      125).
ground_edges( 125, 136,   595,      526).
ground_edges( 125, 218,   843,      667).
ground_edges( 125, 440,   82,      152).
ground_edges( 125, 455,   536,      655).
ground_edges( 126, 440,   388,      374).
ground_edges( 127, 196,   920,      912).
ground_edges( 127, 225,   911,     1015).
ground_edges( 127, 421,   470,      395).
ground_edges( 128, 458,   791,      659).
ground_edges( 129, 307,   776,      809).
ground_edges( 130, 456,   619,      714).
ground_edges( 131, 324,   494,      314).
ground_edges( 131, 380,   526,      543).
ground_edges( 132, 274,   865,      907).
ground_edges( 132, 324,   717,      633).
ground_edges( 132, 380,   897,      849).
ground_edges( 132, 440,   841,      802).
ground_edges( 133, 200,   111,      193).
ground_edges( 133, 232,   433,      473).
ground_edges( 133, 428,   356,      351).
ground_edges( 134, 360,   95,      155).
ground_edges( 135, 265,   184,      227).
ground_edges( 135, 432,   898,      699).
ground_edges( 136, 261,   512,      501).
ground_edges( 136, 438,   165,      184).
ground_edges( 137, 256,   338,      342).
ground_edges( 137, 284,   894,      850).
ground_edges( 137, 306,   708,      552).
ground_edges( 137, 356,   625,      652).
ground_edges( 137, 443,   934,      908).
ground_edges( 138, 403,   449,      606).
ground_edges( 138, 426,   214,      359).
ground_edges( 138, 454,   733,      803).
ground_edges( 138, 462,   410,      435).
ground_edges( 139, 210,   249,      334).
ground_edges( 139, 479,   353,      413).
ground_edges( 139, 487,   469,      459).
ground_edges( 139, 493,   433,      424).
ground_edges( 140, 162,   523,      600).
ground_edges( 140, 193,   122,       46).
ground_edges( 140, 223,   271,      213).
ground_edges( 140, 496,   473,      470).
ground_edges( 141, 186,   387,      244).
ground_edges( 141, 305,   857,      938).
ground_edges( 141, 311,   871,      876).
ground_edges( 142, 164,   417,      404).
ground_edges( 142, 194,   544,      542).
ground_edges( 142, 305,   119,      270).
ground_edges( 143, 170,   795,      951).
ground_edges( 143, 298,   381,      452).
ground_edges( 143, 385,   146,       12).
ground_edges( 144, 182,   479,      541).
ground_edges( 144, 412,   119,      234).
ground_edges( 144, 478,   460,      454).
ground_edges( 145, 251,   830,      869).
ground_edges( 145, 439,   615,      553).
ground_edges( 146, 413,   285,      309).
ground_edges( 147, 430,   496,      662).
ground_edges( 148, 264,   401,      397).
ground_edges( 148, 287,   660,      605).
ground_edges( 149, 171,   828,      824).
ground_edges( 149, 172,   574,      639).
ground_edges( 149, 439,   491,      507).
ground_edges( 150, 212,   342,      348).
ground_edges( 150, 235,   156,      211).
ground_edges( 150, 340,   614,      651).
ground_edges( 150, 417,   603,      545).
ground_edges( 150, 436,   191,      163).
ground_edges( 150, 449,   491,      335).
ground_edges( 151, 271,   86,      192).
ground_edges( 151, 400,   775,      784).
ground_edges( 152, 270,   196,      179).
ground_edges( 152, 473,   200,      144).
ground_edges( 153, 176,   647,      531).
ground_edges( 154, 320,   614,      554).
ground_edges( 154, 338,   406,      420).
ground_edges( 155, 258,   738,      755).
ground_edges( 156, 166,   897,      933).
ground_edges( 156, 416,   125,      301).
ground_edges( 157, 240,   532,      402).
ground_edges( 157, 359,   329,      470).
ground_edges( 158, 184,   499,      546).
ground_edges( 158, 388,   692,      790).
ground_edges( 159, 323,   670,      663).
ground_edges( 159, 405,   379,      395).
ground_edges( 160, 392,   113,        1).
ground_edges( 160, 439,   573,      657).
ground_edges( 160, 476,   370,      340).
ground_edges( 162, 222,   718,      753).
ground_edges( 163, 248,   667,      603).
ground_edges( 163, 251,   750,      683).
ground_edges( 163, 267,   526,      703).
ground_edges( 163, 465,   350,      246).
ground_edges( 164, 240,   443,      521).
ground_edges( 164, 253,   530,      520).
ground_edges( 165, 173,   966,      984).
ground_edges( 166, 197,   273,      312).
ground_edges( 167, 442,   361,      254).
ground_edges( 168, 276,   666,      642).
ground_edges( 168, 283,   629,      457).
ground_edges( 168, 367,   183,      132).
ground_edges( 169, 217,   423,      450).
ground_edges( 169, 237,   95,        1).
ground_edges( 169, 247,   638,      580).
ground_edges( 169, 371,   1031,     1092).
ground_edges( 169, 378,   600,      619).
ground_edges( 171, 351,   196,      165).
ground_edges( 172, 282,   1068,     1080).
ground_edges( 172, 499,   348,      344).
ground_edges( 173, 187,   774,      626).
ground_edges( 173, 194,   1198,     1303).
ground_edges( 173, 429,   873,      851).
ground_edges( 173, 476,   722,      768).
ground_edges( 173, 487,   762,      745).
ground_edges( 174, 296,   491,      478).
ground_edges( 174, 374,   538,      403).
ground_edges( 174, 449,   863,      762).
ground_edges( 174, 498,   551,      545).
ground_edges( 175, 260,   429,      450).
ground_edges( 176, 245,   526,      488).
ground_edges( 176, 421,   111,       37).
ground_edges( 177, 288,   655,      782).
ground_edges( 177, 294,   878,      813).
ground_edges( 177, 491,   820,      856).
ground_edges( 178, 406,   741,      655).
ground_edges( 178, 482,   395,      418).
ground_edges( 179, 268,   773,      689).
ground_edges( 179, 286,   281,      285).
ground_edges( 179, 302,   311,      382).
ground_edges( 180, 279,   697,      692).
ground_edges( 180, 443,   901,      911).
ground_edges( 180, 482,   21,      120).
ground_edges( 181, 318,   186,      232).
ground_edges( 181, 402,   580,      638).
ground_edges( 182, 196,   305,      199).
ground_edges( 185, 321,   822,      872).
ground_edges( 186, 339,   395,      246).
ground_edges( 186, 422,   537,      454).
ground_edges( 186, 484,   403,      533).
ground_edges( 188, 307,   873,      812).
ground_edges( 188, 401,   792,      752).
ground_edges( 188, 434,   459,      451).
ground_edges( 189, 197,   155,      194).
ground_edges( 189, 288,   489,      549).
ground_edges( 189, 393,   528,      524).
ground_edges( 191, 443,   442,      463).
ground_edges( 191, 467,   720,      657).
ground_edges( 192, 273,   831,      923).
ground_edges( 192, 295,   804,      937).
ground_edges( 194, 364,   600,      677).
ground_edges( 194, 437,   1125,     1179).
ground_edges( 195, 379,   832,      840).
ground_edges( 196, 304,   39,       58).
ground_edges( 196, 450,   244,      299).
ground_edges( 197, 352,   402,      381).
ground_edges( 197, 374,   319,      358).
ground_edges( 198, 379,   744,      674).
ground_edges( 199, 259,   922,      875).
ground_edges( 199, 269,   429,      421).
ground_edges( 199, 319,   810,      702).
ground_edges( 199, 470,   625,      754).
ground_edges( 199, 490,   328,      286).
ground_edges( 200, 203,   793,      606).
ground_edges( 200, 471,   836,      825).
ground_edges( 201, 311,   465,      580).
ground_edges( 201, 324,   528,      486).
ground_edges( 201, 424,   192,      207).
ground_edges( 201, 485,   728,      594).
ground_edges( 202, 315,   221,      316).
ground_edges( 202, 440,   816,      914).
ground_edges( 203, 264,   782,      923).
ground_edges( 203, 297,   506,      544).
ground_edges( 203, 454,   215,      169).
ground_edges( 204, 393,   660,      675).
ground_edges( 204, 498,   409,      409).
ground_edges( 205, 249,   313,      381).
ground_edges( 205, 280,   351,      310).
ground_edges( 205, 431,   246,      209).
ground_edges( 205, 443,   487,      453).
ground_edges( 206, 253,   347,      356).
ground_edges( 208, 263,   835,      842).
ground_edges( 208, 369,   742,      807).
ground_edges( 209, 314,   667,      494).
ground_edges( 209, 354,   676,      592).
ground_edges( 210, 215,   450,      298).
ground_edges( 210, 369,   95,       78).
ground_edges( 210, 481,   554,      623).
ground_edges( 211, 358,   650,      660).
ground_edges( 211, 480,   656,      666).
ground_edges( 213, 325,   123,      308).
ground_edges( 213, 377,   550,      503).
ground_edges( 213, 441,   336,      305).
ground_edges( 214, 237,   722,      710).
ground_edges( 215, 262,   489,      493).
ground_edges( 215, 296,   780,      596).
ground_edges( 215, 425,   795,      700).
ground_edges( 216, 483,   546,      675).
ground_edges( 217, 234,   418,      326).
ground_edges( 219, 257,   377,      455).
ground_edges( 221, 342,   391,      407).
ground_edges( 221, 344,   425,      511).
ground_edges( 221, 347,   618,      645).
ground_edges( 222, 310,   607,      554).
ground_edges( 223, 303,   364,      290).
ground_edges( 223, 413,   278,      334).
ground_edges( 223, 450,   356,      202).
ground_edges( 224, 277,   1085,      902).
ground_edges( 225, 379,   295,      346).
ground_edges( 226, 435,   515,      444).
ground_edges( 227, 229,   860,      714).
ground_edges( 228, 293,   362,      545).
ground_edges( 228, 384,   342,      371).
ground_edges( 229, 343,   306,      208).
ground_edges( 230, 247,   935,      805).
ground_edges( 230, 283,   838,      806).
ground_edges( 230, 295,   334,      316).
ground_edges( 230, 468,   918,      901).
ground_edges( 231, 398,   214,      253).
ground_edges( 233, 387,   78,      143).
ground_edges( 234, 306,   770,      734).
ground_edges( 234, 350,   389,      354).
ground_edges( 234, 364,   449,      563).
ground_edges( 234, 423,   612,      607).
ground_edges( 235, 307,   489,      602).
ground_edges( 235, 361,   480,      351).
ground_edges( 235, 398,   341,      430).
ground_edges( 235, 422,   124,      186).
ground_edges( 235, 497,   123,      165).
ground_edges( 236, 254,   273,      355).
ground_edges( 236, 293,   705,      697).
ground_edges( 236, 413,   58,      118).
ground_edges( 237, 287,   807,      802).
ground_edges( 238, 310,   266,      166).
ground_edges( 238, 333,   174,      262).
ground_edges( 238, 356,   378,      359).
ground_edges( 238, 392,   161,      236).
ground_edges( 239, 363,   217,      315).
ground_edges( 239, 371,   911,     1008).
ground_edges( 241, 453,   319,      336).
ground_edges( 243, 250,   621,      471).
ground_edges( 243, 397,   335,      354).
ground_edges( 244, 317,   542,      488).
ground_edges( 245, 252,   561,      501).
ground_edges( 245, 272,   239,      231).
ground_edges( 245, 357,   143,      120).
ground_edges( 246, 394,   426,      308).
ground_edges( 247, 329,   864,      870).
ground_edges( 247, 345,   665,      775).
ground_edges( 247, 355,   78,      244).
ground_edges( 247, 365,   906,      768).
ground_edges( 248, 301,   438,      427).
ground_edges( 248, 308,   711,      643).
ground_edges( 249, 332,   792,      775).
ground_edges( 250, 452,   652,      605).
ground_edges( 251, 351,   660,      607).
ground_edges( 251, 468,   622,      506).
ground_edges( 252, 283,   97,      252).
ground_edges( 252, 300,   799,      755).
ground_edges( 252, 301,   368,      438).
ground_edges( 252, 333,   518,      605).
ground_edges( 253, 277,   943,     1026).
ground_edges( 254, 261,   606,      753).
ground_edges( 254, 443,   193,      311).
ground_edges( 257, 435,   383,      340).
ground_edges( 257, 486,   461,      332).
ground_edges( 258, 305,   543,      604).
ground_edges( 258, 367,   145,      186).
ground_edges( 258, 483,   778,      704).
ground_edges( 259, 385,   776,      571).
ground_edges( 259, 467,   436,      479).
ground_edges( 261, 360,   794,      889).
ground_edges( 262, 351,   196,       31).
ground_edges( 262, 367,   256,      239).
ground_edges( 262, 404,   709,      654).
ground_edges( 263, 331,   697,      719).
ground_edges( 263, 333,   636,      754).
ground_edges( 263, 443,   868,      907).
ground_edges( 263, 494,   485,      543).
ground_edges( 264, 274,   863,      903).
ground_edges( 264, 383,   772,      724).
ground_edges( 265, 433,   231,      230).
ground_edges( 267, 334,   669,      775).
ground_edges( 267, 454,   330,      243).
ground_edges( 267, 494,   486,      393).
ground_edges( 270, 384,   816,      825).
ground_edges( 270, 441,   378,      386).
ground_edges( 271, 296,   662,      833).
ground_edges( 271, 399,   381,      497).
ground_edges( 273, 284,   770,      796).
ground_edges( 273, 332,   536,      554).
ground_edges( 273, 359,   252,      291).
ground_edges( 273, 363,   182,      188).
ground_edges( 273, 457,   690,      550).
ground_edges( 274, 368,   606,      575).
ground_edges( 274, 381,   255,      160).
ground_edges( 274, 470,   221,      154).
ground_edges( 275, 378,   451,      521).
ground_edges( 275, 484,   880,      849).
ground_edges( 278, 403,   736,      565).
ground_edges( 278, 407,   865,      905).
ground_edges( 278, 459,   1007,     1006).
ground_edges( 280, 460,   287,      300).
ground_edges( 283, 387,   270,      321).
ground_edges( 283, 448,   506,      606).
ground_edges( 283, 449,   666,      662).
ground_edges( 285, 410,   222,      216).
ground_edges( 286, 296,   215,      188).
ground_edges( 286, 326,   706,      747).
ground_edges( 286, 379,   328,      158).
ground_edges( 287, 436,   785,      754).
ground_edges( 290, 403,   60,      222).
ground_edges( 290, 445,   569,      597).
ground_edges( 291, 298,   205,      122).
ground_edges( 291, 348,   510,      453).
ground_edges( 291, 380,   503,      673).
ground_edges( 291, 381,   526,      584).
ground_edges( 291, 459,   469,      519).
ground_edges( 292, 329,   166,       91).
ground_edges( 292, 332,   672,      623).
ground_edges( 293, 296,   208,      222).
ground_edges( 293, 462,   581,      418).
ground_edges( 293, 477,   226,      102).
ground_edges( 295, 322,   244,      272).
ground_edges( 295, 334,   544,      455).
ground_edges( 295, 411,   893,      797).
ground_edges( 295, 428,   398,      375).
ground_edges( 297, 345,   729,      646).
ground_edges( 298, 352,   122,       91).
ground_edges( 298, 415,   455,      581).
ground_edges( 298, 470,   30,       38).
ground_edges( 299, 361,   790,      774).
ground_edges( 299, 390,   304,      274).
ground_edges( 300, 343,   803,      621).
ground_edges( 300, 393,   271,      428).
ground_edges( 300, 451,   783,      717).
ground_edges( 301, 355,   540,      365).
ground_edges( 302, 366,   53,       76).
ground_edges( 303, 399,   62,      115).
ground_edges( 303, 442,   508,      661).
ground_edges( 304, 419,   254,      148).
ground_edges( 304, 427,   303,      189).
ground_edges( 305, 348,   316,      398).
ground_edges( 305, 386,   444,      619).
ground_edges( 306, 312,   774,      939).
ground_edges( 306, 460,   877,      913).
ground_edges( 306, 479,   699,      674).
ground_edges( 307, 358,   526,      522).
ground_edges( 307, 359,   661,      539).
ground_edges( 307, 415,   765,      772).
ground_edges( 307, 450,   835,      852).
ground_edges( 307, 454,   330,      272).
ground_edges( 308, 461,   344,      245).
ground_edges( 308, 499,   464,      510).
ground_edges( 309, 325,   527,      503).
ground_edges( 309, 333,   784,      652).
ground_edges( 309, 479,   701,      673).
ground_edges( 312, 429,   782,      798).
ground_edges( 313, 333,   665,      715).
ground_edges( 313, 449,   395,      327).
ground_edges( 315, 442,   798,      675).
ground_edges( 316, 436,   884,      957).
ground_edges( 316, 482,   904,      973).
ground_edges( 318, 381,   314,      398).
ground_edges( 318, 413,   453,      454).
ground_edges( 318, 455,   524,      402).
ground_edges( 318, 462,   434,      440).
ground_edges( 319, 450,   672,      586).
ground_edges( 321, 344,   379,      379).
ground_edges( 321, 366,   553,      610).
ground_edges( 321, 412,   374,      428).
ground_edges( 323, 327,   154,      154).
ground_edges( 323, 389,   390,      418).
ground_edges( 324, 380,   355,      411).
ground_edges( 324, 383,   140,      227).
ground_edges( 325, 352,   351,      338).
ground_edges( 325, 470,   242,      442).
ground_edges( 326, 373,   866,      872).
ground_edges( 327, 330,   561,      479).
ground_edges( 327, 369,   724,      728).
ground_edges( 328, 449,   678,      688).
ground_edges( 328, 474,   621,      629).
ground_edges( 329, 334,   275,      271).
ground_edges( 329, 438,   479,      351).
ground_edges( 330, 336,   753,      582).
ground_edges( 330, 400,   930,      879).
ground_edges( 333, 393,   296,      368).
ground_edges( 334, 433,   200,      240).
ground_edges( 335, 436,   759,      643).
ground_edges( 336, 399,   741,      675).
ground_edges( 337, 354,   527,      414).
ground_edges( 338, 470,   163,      181).
ground_edges( 338, 488,   387,      432).
ground_edges( 339, 364,   573,      510).
ground_edges( 341, 397,   811,      750).
ground_edges( 341, 473,   964,      969).
ground_edges( 342, 390,   839,      910).
ground_edges( 342, 497,   457,      567).
ground_edges( 343, 390,   233,      343).
ground_edges( 344, 449,   245,      183).
ground_edges( 345, 395,   408,      359).
ground_edges( 346, 459,   665,      479).
ground_edges( 347, 445,   461,      433).
ground_edges( 348, 396,   417,      432).
ground_edges( 349, 380,   296,      456).
ground_edges( 350, 439,   429,      315).
ground_edges( 351, 366,   264,      334).
ground_edges( 351, 446,   291,      314).
ground_edges( 351, 451,   64,        7).
ground_edges( 352, 416,   225,      152).
ground_edges( 353, 465,   720,      637).
ground_edges( 354, 365,   136,      106).
ground_edges( 354, 411,   657,      740).
ground_edges( 355, 358,   298,      330).
ground_edges( 359, 435,   56,       65).
ground_edges( 359, 457,   338,      388).
ground_edges( 362, 371,   901,     1008).
ground_edges( 362, 398,   986,      808).
ground_edges( 362, 456,   756,      808).
ground_edges( 363, 436,   429,      417).
ground_edges( 364, 444,   671,      517).
ground_edges( 364, 469,   541,      594).
ground_edges( 365, 432,   830,      899).
ground_edges( 366, 415,   345,      281).
ground_edges( 369, 498,   339,      226).
ground_edges( 370, 475,   797,      856).
ground_edges( 370, 497,   529,      551).
ground_edges( 372, 411,   6,       92).
ground_edges( 374, 396,   495,      570).
ground_edges( 375, 453,   560,      697).
ground_edges( 382, 484,   579,      590).
ground_edges( 382, 494,   321,      282).
ground_edges( 383, 426,   703,      743).
ground_edges( 383, 455,   243,      245).
ground_edges( 385, 466,   261,      207).
ground_edges( 388, 451,   831,      721).
ground_edges( 389, 440,   1152,     1118).
ground_edges( 390, 462,   530,      506).
ground_edges( 392, 498,   161,      259).
ground_edges( 394, 482,   732,      678).
ground_edges( 395, 472,   120,       82).
ground_edges( 397, 499,   578,      700).
ground_edges( 402, 427,   644,      660).
ground_edges( 402, 430,   885,      778).
ground_edges( 402, 494,   576,      505).
ground_edges( 402, 500,   646,      537).
ground_edges( 403, 496,   373,      479).
ground_edges( 405, 458,   748,      792).
ground_edges( 407, 432,   213,      205).
ground_edges( 408, 409,   491,      385).
ground_edges( 412, 477,   571,      672).
ground_edges( 414, 431,   811,      840).
ground_edges( 415, 434,   51,      165).
ground_edges( 416, 428,   162,      344).
ground_edges( 417, 426,   694,      760).
ground_edges( 419, 490,   450,      488).
ground_edges( 420, 450,   564,      502).
ground_edges( 421, 475,   361,      369).
ground_edges( 423, 437,   355,      365).
ground_edges( 426, 482,   991,      866).
ground_edges( 430, 500,   515,      527).
ground_edges( 432, 449,   430,      264).
ground_edges( 434, 458,   768,      699).
ground_edges( 443, 479,   471,      518).
ground_edges( 446, 474,   545,      546).
ground_edges( 446, 492,   467,      659).
ground_edges( 449, 461,   193,      132).
ground_edges( 452, 458,   716,      708).
ground_edges( 456, 492,   663,      697).
ground_edges( 467, 495,   286,      255).
ground_edges( 474, 498,   393,      417).
ground_edges( 477, 489,   1135,     1067).

edge((U,V)) :- ground_edges(U,V,_,_).
edge((V,U)) :- ground_edges(U,V,_,_).

edge_weight((U,V),W) :- ground_edges(U,V, W, _).
edge_weight((V,U),W) :- ground_edges(U,V, _, W).

node(V) :- ground_edges(V,_,_,_).
node(V) :- ground_edges(_,V,_,_).

mintime(1).
maxtime(700).

"""

reasoning = """

time(I..A) :- mintime(I), maxtime(A).

lastwalk(L) :- walk(_,L), not walk(_,L+1).

%1 { walk(E,I)   : edge(E) } 1 :- mintime(I).
%1 { walk(E,I+1) : edge(E) } 1 :- mintime(I).
%  { walk(E,T)   : edge(E) } 1 :- walk(_,T-1), maxtime(A), T<=A.

0 { walk(E,T) : edge(E) } 1 :- time(T).

:- mintime(I), not walk((1,_), I).
:- lastwalk(L), not walk((_,1), L).
%:- edge((U,V)), edge((V,U)), not walk((U,V), _), not walk((V,U), _).

:~ walk(E,T), edge_weight(E,W).[W@1,E,T]
:~ walk(E,T). [1@0,E,T]

#show walk/2.
"""

debug = True


def print_debug(*args, **kwargs):
    if debug:
        print("[DEBUG]:", *args, **kwargs)


def get_time(atom: clingo.Symbol):
    if len(atom.arguments) == 2:
        if atom.arguments[-1].type is clingo.SymbolType.Number:
            return atom.arguments[-1].number
    return float('Inf')


class WindyPropagator(Propagator):

    def __init__(self):
        self._e2l: MutableMapping[Tuple[int, int], int] = {}  # {(int,int): literal}
        self._l2e: MutableMapping[int, Tuple[int, int]] = {}  # {literal: (int,int)}
        self._e2w: MutableMapping[int, Set[int]] = {}  # {literal: {literal}}
        self._t2w: MutableMapping[int, Set[int]] = {}
        self._incidents: MutableMapping[int, Set[int]] = {}  # {literal: {literal}}
        self._w2s: MutableMapping[int, int] = {}
        self._s2w: MutableMapping[int, int] = {}
        self._decisions: List[Dict[int, Tuple[Tuple[int, int], int]]] = []  # {time: ((node,node),walk_lit)}
        self._clauses: Set[Tuple[int]] = set()
        self._clauses_lock: Lock = Lock()

    @staticmethod
    def symbolic_atom_to_edge(edge: clingo.SymbolicAtom) -> Tuple[int, int]:
        return WindyPropagator.symbol_to_edge(edge.symbol)

    @staticmethod
    def symbol_to_edge(edge: clingo.Symbol) -> Tuple[int, int]:
        u = edge.arguments[0].arguments[0].number
        v = edge.arguments[0].arguments[1].number
        return u, v

    def _get_decisions(self, thread_id: int) -> Dict[int, Tuple[Tuple[int, int], int]]:
        while len(self._decisions) <= thread_id:
            self._decisions.append({})
        return self._decisions[thread_id]

    def __sol_lit_to_edge_lit(self, sol_lit: int) -> int:
        return self.__walk_lit_to_edge_lit(self._s2w[sol_lit])

    def __walk_lit_to_edge_lit(self, walk_lit: int) -> int:
        for (edge_lit, walk_lits) in self._e2w.items():
            if walk_lit in walk_lits:
                return edge_lit
        assert False, "Should have found walk literal {}".format(walk_lit)

    def __sol_lit_to_edge(self, sol_lit: int) -> Tuple[int, int]:
        return self._l2e[self.__sol_lit_to_edge_lit(sol_lit)]

    def __walk_lit_to_edge(self, walk_lit: int) -> Tuple[int, int]:
        return self._l2e[self.__walk_lit_to_edge_lit(walk_lit)]

    def __sol_lit_to_time(self, sol_lit: int) -> int:
        return self.__walk_lit_to_time(self._s2w[sol_lit])

    def __walk_lit_to_time(self, walk_lit: int) -> int:
        for (time, walk_lits) in self._t2w.items():
            if walk_lit in walk_lits:
                return time
        assert False, "Should have found walk literal {}".format(walk_lit)

    def init(self, init: PropagateInit) -> None:
        print_debug("Initializing Propagator")
        edges = init.symbolic_atoms.by_signature('edge', 1)
        print_debug("Building edge dict")
        for edge in edges:
            u, v = WindyPropagator.symbolic_atom_to_edge(edge)
            edge_lit = edge.literal
            self._e2l[(u, v)] = edge_lit
            self._l2e[edge_lit] = (u, v)
        walks = init.symbolic_atoms.by_signature('walk', 2)
        print_debug("Building walks dict")
        for walk in walks:
            self._w2s[walk.literal] = init.solver_literal(walk.literal)
            self._s2w[self._w2s[walk.literal]] = walk.literal
            init.add_watch(self._w2s[walk.literal])
            t = get_time(walk.symbol)
            self._t2w.setdefault(t, set()).add(walk.literal)
            u = walk.symbol.arguments[0].arguments[0].number
            v = walk.symbol.arguments[0].arguments[1].number
            walk_lit = walk.literal
            self._e2w.setdefault(self._e2l[u, v], set()).add(walk_lit)

        print_debug("Building incidents dict")
        for (edge_lit1, (u, v)) in self._l2e.items():
            for (edge_lit2, (w, x)) in self._l2e.items():
                if v == w:
                    self._incidents.setdefault(edge_lit1, set()).add(edge_lit2)

        print_debug("Adding walk clauses")
        for (edge1_lit, walk1_lits) in self._e2w.items():
            (u, v) = self._l2e[edge1_lit]
            if u <= v:
                for (edge2_lit, walk2_lits) in self._e2w.items():
                    (w, x) = self._l2e[edge2_lit]
                    if u == x and w == v:
                        print_debug(
                            "Adding clause of {} literals for {}|{}".format(len(walk1_lits) + len(walk2_lits), (u, v),
                                                                            (w, x)))
                        clause = []
                        clause.extend(map(self._w2s.get, walk1_lits))
                        clause.extend(map(self._w2s.get, walk2_lits))
                        init.add_clause(clause)

        print_debug("Add stop at conditions")
        stop_at = {}
        for t, walks in self._t2w.items():
            stop_at[t] = init.add_literal()
            for walk in walks:
                clause = (-stop_at[t], -self._w2s[walk])
                init.add_clause(clause)

        for t1 in self._t2w:
            for t2 in self._t2w:
                if t1 < t2:
                    stop_clause = (-stop_at[t1], stop_at[t2])
                    init.add_clause(stop_clause)

        print_debug("Adding edge constraints")
        for (t1, walks1) in self._t2w.items():
            t2 = t1 + 1
            if t1 == len(self._t2w):
                t2 = 1
            walks2 = self._t2w[t2]
            if t1 + 1 == t2 or (t1 == len(self._t2w) and t2 == 1):
                for walk1 in walks1:
                    stop_here = stop_at[t2]
                    successor_clause = [-self._w2s[walk1], stop_here]
                    successors = []
                    for walk2 in walks2:
                        u, v = self.__walk_lit_to_edge(walk1)
                        w, x = self.__walk_lit_to_edge(walk2)
                        if v != w:
                            clause = (-self._w2s[walk1], -self._w2s[walk2])
                            init.add_clause(clause)
                        else:
                            successors.append(self._w2s[walk2])
                    successor_clause.extend(successors)
                    init.add_clause(successor_clause)

        init.propagate()

        print_debug("e2l", self._e2l)
        print_debug("l2e", self._l2e)
        print_debug("w2e", self._e2w)
        print_debug("t2e", self._t2w)
        print_debug("w2s", self._w2s)
        print_debug("s2w", self._s2w)
        print_debug("incidents", self._incidents)

        print_debug("Finished initializing")

    # def propagate(self, control: PropagateControl, changes: Sequence[int]) -> None:
    #    print_debug("Reached fixpoint")
    #    for change in changes:
    #        sol2_lit = change
    #        walk2_lit = self._s2w[sol2_lit]
    #        time = self.__walk_lit_to_time(walk2_lit)
    #        edge2 = self.__walk_lit_to_edge(walk2_lit)
    #        print_debug("Chose", edge2, "at", time)
    #        decisions = self._get_decisions(control.thread_id)
    #        decisions[time] = (edge2, sol2_lit)
    #        print_debug(decisions)
    #        (u, v) = edge2
    #        if time - 1 in decisions:
    #            edge1, sol1_lit = decisions[time - 1]
    #            (s, t) = edge1
    #            if t != u:
    #                print_debug("Conflict {} -> {}".format(edge1, edge2))
    #                if not control.add_nogood((sol1_lit, sol2_lit)) or not control.propagate():
    #                    return
    #        if time + 1 in decisions:
    #            edge3, sol3_lit = decisions[time + 1]
    #            (w, x) = edge3
    #            if v != w:
    #                print_debug("Conflict {} -> {}".format(edge2, edge3))
    #                if not control.add_nogood((sol2_lit, sol3_lit)) or not control.propagate():
    #                    return
    #    print_debug("Consistent")

    # def decide(self, thread_id: int, assignment: Assignment, fallback: int) -> int:
    #    decisions = self._get_decisions(thread_id)
    #    for time in range(2, len(decisions) + 2):
    #        if time not in decisions and time - 1 in decisions:
    #            candidates = self._t2w[time]
    #            (u,v), walk_lit = decisions[time - 1]
    #            available = []
    #            for candidate in candidates:
    #                if assignment.is_free(candidate):
    #                    (w,x) = self.__walk_lit_to_edge(candidate)
    #                    if v == w:
    #                        available.append(candidate)
    #            if available:
    #                guess = choice(available)
    #                edge = self.__walk_lit_to_edge(guess)
    #                print_debug("Guessed", edge, "at", time)
    #                return guess

    #    return 0

    # def undo(self, thread_id: int, assignment: Assignment, changes: Sequence[int]) -> None:
    #    print_debug("Backtrack")
    #    decisions = self._get_decisions(thread_id)
    #    for change in changes:
    #        sol_lit = change
    #        walk_lit = self._s2w[sol_lit]
    #        edge = self.__walk_lit_to_edge(walk_lit)
    #        time = self.__walk_lit_to_time(walk_lit)
    #        print_debug("Revert", edge, "at", time)
    #        if time in decisions:
    #            del decisions[time]
    #    print_debug(decisions)

    # def check(self, control: PropagateControl) -> None:
    #    print_debug("Checking assignment")
    #    walks = {}
    #    for sol_lit in control.assignment:
    #        if sol_lit in self._s2w and control.assignment.is_true(sol_lit):
    #            time = self.__sol_lit_to_time(sol_lit)
    #            walks[time] = sol_lit

    #    print_debug("Assignment", walks)
    #    conflicts = set()
    #    for time in walks:
    #        if time > len(walks) or (time > 1 and time - 1 not in walks) or time - 1 in conflicts:
    #            conflicts.add(time)

    #    if conflicts:
    #        print_debug("Found {} conflicts {}".format(len(conflicts), conflicts))
    #        for conflict in conflicts:
    #            sol_lit = walks[conflict]
    #            edge_lit = self.__sol_lit_to_edge_lit(sol_lit)
    #            edge = self._l2e[edge_lit]
    #            print_debug("Conflict {} at {}".format(edge, conflict))
    #            possibilities = set()
    #            for possibility in self._t2w[conflict - 1]:
    #                possible_edge_lit = self.__walk_lit_to_edge_lit(possibility)
    #                if edge_lit in self._incidents[possible_edge_lit]:
    #                    possible_edge = self._l2e[possible_edge_lit]
    #                    print_debug("Possible {} at {}".format(possible_edge, conflict - 1))
    #                    possibilities.add(self._w2s[possibility])
    #            clause = []
    #            clause.append(-sol_lit)
    #            clause.extend(possibilities)
    #            self._clauses.add(tuple(clause))

    #    print_debug("Adding up to {} clauses".format(len(self._clauses)))
    #    while self._clauses:
    #        print_debug("Adding clause")
    #        clause = None
    #        with self._clauses_lock:
    #            if self._clauses:
    #                clause = self._clauses.pop()
    #        if clause is not None:
    #            if not control.add_clause(clause) or not control.propagate():
    #                return


print_debug("Creating WindyPropagator")
windy_propagator = WindyPropagator()
print_debug("Creating Control Object")
ctl = clingo.Control()
ctl.configuration.solve.models = 0
ctl.configuration.solve.parallel_mode = '16,compete'
print_debug("Registering propagator")
ctl.register_propagator(windy_propagator)
print_debug("Adding logic programs")
ctl.add('base', (), inst4)
ctl.add('base', (), reasoning)
print_debug("Starting to ground")
ctl.ground([('base', [])])
print_debug("Finished grounding")

print("Starting to solve")
start = time.monotonic()
last = start
with ctl.solve(yield_=True) as solve_handle:
    for model in solve_handle:
        last = time.monotonic()
        atoms = model.symbols(shown=True)
        print("[{:.2f}] Answer {}:".format(last - start, model.number), end=' ')
        if model.cost:
            print("{}".format(model.cost), end=' ')
        print("{} {} {}".format('{', ' '.join(map(str, sorted(sorted(atoms), key=get_time))),
                                '}'))

    print(solve_handle.get())
end = time.monotonic()
print("Searched for {:.2f}s, found optimal solution in {:.2f}s, verifying for {:.2f}s".format(end - start, last - start,
                                                                                              end - last))

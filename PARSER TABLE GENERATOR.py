# -*- coding: utf-8 -*-
from tabulate importtabulate
import re
fromcollectionsimport OrderedDict
importsys
import os
grammar_pattern = re.compile(r"(.+?)[=-]>\|?(.+)")
END = '$'
EMPTY = ''
EMPTY_IN = '€'
EMPTY_OUT = 'ε'
OR = '|'
AND = ' '
def grammar(g):
G = OrderedDict()
def add(k, v):
m = G.get(k, [])
m += v
G[k] = m
15
for i, match in enumerate(grammar_pattern.finditer(g)):
t,s2 = match.group(1), match.group(2)
t = t.strip()
s2 = [s.strip().split(AND) forsin s2.split(OR)]
add(t,s2)
K = list(G.keys())
for i in range(len(K)):
G[i] = G[K[i]]
del G[K[i]]
mp = lambda s: K.index(s) if s in K else sif s!= EMPTY_IN else EMPTY
for k in G:
G[k] = [[mp(s) for s in n] for n in G[k]]
return G, K
def first_set(G):
first = dict()
def add(k, v):
m = first.get(k,set())
m.add(v)
first[k] = m
16
def f(k):
r = []
for X in G[k]:
for x in X:
if isinstance(x,str):
add(x, x)
r.insert(0, x)
if x == EMPTY:
add(k, x)
else:
break
else:
Z = f(x)
for x in {Z[i] fori in range(Z.index(EMPTY) if EMPTY in Z else len(Z))}:
r.insert(0, x )
add(k, x )
for n in r:
add(k,n)
return r
17
for k in G:
f(k)
return first
def follow_set(G, S, first=None):
first = first or first_set(G)
follow = dict()
def add(k, v):
m = follow.get(k,set())
m.add(v)
follow[k] = m
add(S, '$')
def f(A):
for X in G[A]:
for i, x in enumerate(X):
if not isinstance(x,str):
fst = []
for y in X[i + 1:]:
m = first.get(y, {y})
18
fst += m
if EMPTY not in m:
break
for y in fst:
if y != EMPTY:
add(x, y)
if len(fst) == 0 or EMPTY in fst:
for a in follow.get(A, {}):
add(x, a)
h = lambda f: hash(n for v in f.values() for n in v)
f_old = h(follow)
while True:
for k in G:
f(k)
if f_old == h(follow):
break
else:
f_old = h(follow)
return follow
19
def parse_table(G,first=None, follow=None):
first = first or first_set(G)
follow = follow orfollow_set(G, 0, first)
M = dict()
def add(N, k, F,t):
m = M.get(N, dict())
hm =m.get(k,set())
hm.add((F, t))
m[k] = hm
M[N] = m
def frst(a):
frs = set()
for x in a:
f = first[x]
frs = frs.union(f)
if EMPTY not in f:
break
return frs- {EMPTY}
def P(A):
fori, X in enumerate(G[A]):
20
for a in frst(X):
add(A, a, A, i)
for x in X:
if isinstance(x,str):
if x == EMPTY:
for b in follow[A]:
add(A, b, A, i)
else:
break
for g in G:
P(g)
return M
def as_table(G,N, M=None, first=None, follow=None, **kwargs):
first = first or first_set(G)
follow = follow orfollow_set(G, 0, first)
terminals = set(n for v in first.values() for n in v).union(set(n for v in
follow.values() for n in v))
terminals-= {EMPTY}
21
nonterminals = set(v for v in follow.keys())
M = M or parse_table(G, first, follow)
s = lambda s:s ifs != EMPTY else EMPTY_OUT
z = sorted(list(terminals))
z.reverse()
if len(z) > 4:
z[4],z[3] = z[3],z[4]
data = []
for n in nonterminals:
data2 = [N[n]]
for t in z:
l3 = ""
if M.get(n) and M[n].get(t):
for i, p in enumerate(M[n][t]):
A, x = p
x = "".join([s(e) if isinstance(e,str) else N[e]for e in G[A][x]])
if i > 0:
l3 += "\n"
l3 += ("%-2s → %-2s" % (N[A], x))
data2.append(l3)
data2.append(" ".join(s(c) for c in first[n]))
22
data2.append(" ".join(s(c) for c in follow[n]))
data.append(data2)
return tabulate(data, headers=["NON -\nTERMINALS"] + z + ["FIRST",
"FOLLOW"], **kwargs)
if name == " main ":
l = len(sys.argv)
fmt = 'fancy_grid'
fmts = ["plain", "simple", "github", "grid", "fancy_grid", "pipe", "orgtbl",
"jira", "presto", "psql", "rst", "mediawiki", "moinmoin", "youtrack",
"html", "latex", "latex_raw", "latex_booktabs", "textile"]
g = """
E -> T E'
E' -> + T E' | € 
T -> F T'
T' -> * F T' | € 
F -> ( E ) | id
"""
if l >= 2:
arg = sys.argv[1]
if arg in ("--help", "-h"):
print("Give me grammar!")
print("Like this:\n%s" % g)
23
print("""€ is empty terminal
Use space (' ') asseperator in production
Seperate productions with pipe ('|') or with different arrow-productions
Any string on the left side of -> is a nonterminal
Any non-nonterminal on the rightside of -> is a terminal
""")
print("Third argument isstyle of table. Default:fancy_grid \nValid options
are:")
fori, f in enumerate(fmts):
if i % 12 == 11:
print()
print(f, end=" ")
print()
exit()
elif os.path.isfile(arg):
with open(arg, "r", encoding="utf-8") asfile:
G, N = grammar(file.read())
if len(G) == 0:
print("Invalid grammarin file.")
exit(-1)
elif re.match(grammar_pattern, arg):
G, N = grammar(arg)
else:
print("No grammar wasfound.")
exit(-1)
24
if l >= 3:
ifsys.argv[2] in fmts:
fmt = sys.argv[2]
else:
print("Invalid table style: %s\nTry withoutstyle option orsee --help for
valid options" % arg)
exit(-1)
else:
print("""
No recognized grammar!
For more info see --help
Example parse table:""")
G, N = grammar(g)
try:
table = as_table(G, N,tablefmt=fmt)
print(table)
except RecursionError:
print("Leftrecursive grammar!")
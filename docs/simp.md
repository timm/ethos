```py
import sys
from tricks import *

def about(): return  [
"""
(C) 2020, tim@menzies.us MIT, v2
Useful routines for building simple data miners and optimizers
""","""
Divide the data, find best and worst regions, find ways 
to jump between those regions.
""",
  # sway
  elp("verbose mode for DIV",        divVerbose= False),
  elp("bin min size =len**b",        b  = 0.5),
  elp("merge bins if score delta below e",  e=0.01),
  elp("coefficient for distance" ,   p  = 2),

  elp("training data (arff format",  train = "train.csv"),
  elp("testing data (csv format)",   test  = "test.csv"),
  # --------------------------------------------------------------------
  # System
  elp("Run some test function, then quit",       run       = "")
]

my = args(*about())

```

```py
def no(s)     : return  s == "?"
def nump(s)   : return "<" in s or "$" in s or ">" in s
def goalp(s)  : return "<" in s or "!" in s or ">" in s
def klassp(s) : return "!" in s
def lessp(s)  : return "<" in s

class Col(Thing):
  def __init__(i,pos,txt):
    i.n, i.pos, i.txt = 0, pos, txt
    i.w = -1 if lessp(txt) else 1
  def __add__(i,x):
    if no(x): return x
    i.n += 1
    return i.add(x)

class Num(Col):
  def __init__(i, *l):
    super().__init__(*l)
    i.mu, i.lo, i.hi = 0, 10**32, -10**32
  def add(i,x):
    x = float(x)
    i.lo,i.hi = min(i.lo,x), max(i.hi,x)
    i.mu      = i.mu + (x - i.mu)/i.n
    return x
  def norm(i,x):
    if no(x) : return x
    return (x - i.lo)  / (i.hi - i.lo + 0.000001)
  def dist(i,x,y):
    if no(x) and no(y): return 1
    if no(x): x = i.lo if y > i.mu else i.hi
    if no(y): y = i.lo if x > i.mu else i.hi
    return abs(i.norm(x) - i.norm(y))

class Sym(Col):
  def __init__(i, *l):
    super().__init__(*l)
    i.seen, i.most, i.mode = {}, 0, None
  def add(i,x):
    tmp = i.seen[x] = i.seen.get(x,0) + 1
    if tmp > i.most: i.most,i.mode = tmp,x
    return x
  def dist(i,x,y): 
    return 1 if no(x) and no(y) else x != y
 
class Cols(Thing):
  def __init__(i) : 
    i.x,i.y,i.nums,i.syms,i.all,i._klass = {},{},{},{},[],None
  def add(i,lst): 
    [ col.add( lst[col.pos] ) for col in i.all ]
  def klass(i,lst): 
    return lst[i._klass]
  def header(i,lst):
    for pos,txt in enumerate(lst):
      tmp = (Num if nump(txt) else Sym)(pos,txt)
      i.all += [tmp]
      (i.y    if goalp(txt) else i.x)[pos] = tmp
      (i.nums if nump(txt)  else i.syms)[pos] = tmp
      if klassp(txt) : i._klass  = tmp

class Tab(Thing):
  def __init__(i,rows=[]):
    i.rows, i.cols = [], Cols()
    [i.add(row) for row in rows]
  def clone(i,rows=[]):
    data = [[c.txt for c in i.cols.all]] + rows
    return Tab(data = data)
  def __add__(i,a): 
    return i.add(a) if i.cols.all else i.cols.header(a)
  def add(i,a): 
    i.rows += [[c + a[c.pos] for c in i.cols.all]]
  def read(i,data=None): 
    [i + row for row in cols(rows(data))]
    return i
  def dist(i,xs,ys,cols=None):
    d,cols = 0, cols or i.cols.x
    for col in cols.values():
      inc = col.dist( xs[col.pos], ys[col.ps] )
      d  += inc**my.p
    return (d/len(cols))**(1/my.p)
  def pairs(i,col):
    return Bins(col.pos,i.rows, lambda z: z[col.pos], 
                                lambda z: i.cols.klass(z))

class Range(Thing):
  def __init__(i,what,want):
    i.what,i.want = what, want
    i.n, i.yes, i.no = 0,0,0
  def add(i,x,y):
    i.n   += 1
    if y==i.want: i.yes += 1
    else        :  i.no += 1
  def s(i, all):
    yes   = i.yes/all.yes 
    no    = i.no/all.no
    return yes**2/(yes+no+0.0001) if yes > no else 0

class SBin(Range):
  def __init__(i, *lst):
    super().__init__(*lst)
    i.lo, i.hi       = None,None
  def add(i,x,y):
    super().add(x,y)
    i.lo = min(x,i.lo)
    i.hi = max(x,i.hi)
  def merge(i,j):
    k     = SBin(i.what, i.want)
    k.lo  = min(i.lo, j.lo) 
    k.hi  = max(i.hi, j.hi) 
    k.n   = i.n + j.n
    k.no  = i.no  + j.no
    k.yes = i.yes + j.yes
    return k
  def better(c,a,b,all):
    sa, sb, sc = a.s(all), b.s(all), c.s(all)
    return abs(sb - sa) < my.e or sc >= sb and sc >= sa

class Bins(Thing):
  def __init__(i,txt,a,x,y,goal=True, bin=SBin): 
    i.txt  = txt
    i.goal = goal
    i.bin  = bin
    i.all  = i.bin(txt, goal)  
    return i.merge( i.grow( i.pairs(x,y)))
  def pairs(i,x,y,lst):
    lst = [(x(z), y(z)) for z in a if not isinstance(x(z),str)]
    return sorted(lst, key= lambda z:z[0])
  def grow(i,a):
    min  = len(a)**my.b
    use  = len(a) - min
    bins = [i.bin(i.txt,i.goal)]
    for j,(x,y) in enumerate(a):
      if j < use and bins[-1].n > min:
        bins += [i.bin(i.txt,i.goal)]
      bins[-1].add(x,y)
      i.all.add(x,y) 
    return bins
  def merge(i,bins):
    j, tmp = 0, []
    while j < len(bins):
       a = bins[j]
       if j < len(bins) - 1:
          b = bins[j+1]
          c = a.merge(b)
          if c.better(a,b,i.all):
             a = c
             j += 1
       tmp += [a]
       j += 1
    return i.merge(tmp) if len(tmp) < len(bins) else bins
```

```py
@go
def _tab():
  t = Tab().read("data/auto93.csv")
  print(t)
```

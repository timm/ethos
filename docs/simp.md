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
def no(x) return x == "?"

class Cols():
   def __init__(i):
     i.x,i.y,i.nums,i.syms,i.head, = {},{},{},{},[]
     i.nums, i.lo, i.hi, i.w = {},{},{}
     i._klass=0 
  def nump(i,  s) : return "<" in s or "$" in s or ">" in s
  def goalp(i, s) : return "<" in s or "!" in s or ">" in s
  def klassp(i,s) : return "!" in s
  def lessp(i, s) : return "<" in s
   def header(i,txt):
     i.head = lst
     for n,s in enumerate(lst):
       (i.y   if i.goalp(s) else i.x  )[n] = s
       (i.num if i.nump(s)  else i.sym)[n] = s
       if i.klassp(s): i._klass = n
     for k in i.nums:
       i.lo[k] =  10**32
       i.hi[k] = -1*i.lo[k] 
       i.w[k]  = -1 if i.less(s) else 1
   def klass(i,lst): 
     return lst[i._klass]
   def row(i,lst):
     for k  in i.nums: 
       v = lst[k]
       if no(v):
       v = lst[k] = float(v)
       if v> i.hi[k]: i.hi[k] = v
       if v< i.lo[k]: i.lo[k] = v
     return lst

class Tab():
  def __init__(i,rows=[]):
    i.rows, i.cols = [], Cols()
    [i.add(row) for row in rows]
  def clone(i,rows=[]):
    t = Tab(data=[i.cols.head])
    [t.add(row) for row in rows]
    return t
  def __add__(i,lst):
    return i.row(lst) if i.cols else i.cols.header(lst)
  def i.row(i,lst):
    i.rows += [i.cols.row(lst)]
  def read(i,data=None):
    [i + row for row in csv(data)]
    return i
  def norm(i,n,v):
    if no(v) : return v
    return (v - i.cols.lo[v])  / (
            i.cols.hi[v] - i.cols.lo[v] + 0.000001)
  def dist(i,lst1,lst2,cols=None):
    cols  = cols or i.cols.x
    d,n,p = 0, 0.001, my.p
    for k in cols:
      n += 1
      x,y = lst1[k], lst2[k]
      if no(x) and no(y):
         d += 1
      elif k in i.cols.sym:
         d += x != y
      else:
         if no(x):
           y = i.norm(k,y); x = 0 if y > 0.5 else 1
         elif no(y):
           x = i.norm(k,x); y = 0 if x > 0.5 else 1
         else:
           x,y = i.norm(k,x), i.norm(k,y)
         d += abs(x-y)**p
    return (d/n)**(1/p)
  def pairs(i,col):
    return Bins(col,i.rows, lambda z: z[col], 
                            lambda z: i.cols.klass(z))

class SBin:
  def __init__(i, what, want):
    i.what,i.want = what, want
    i.n, i.yes, i.no = 0,0,0
    i.lo, i.hi       = None,None
  def add(i,x,y,goal):
    i.lo = min(x,i.lo)
    i.hi = max(x,i.hi)
    i.n   += 1
    (i.yes += 1) if y==i.want else (i.no += 1)
  def merge(i,j):
    k     = SBin(i.what, i.want)
    k.lo  = min(i.lo, j.lo) 
    k.hi  = max(i.hi, j.hi) 
    k.n   = i.n + j.n
    k.no  = i.no  + j.no
    k.yes = i.yes + j.yes
    return k
  def s(i, all):
    yes   = i.yes/all.yes 
    no    = i.no/all.no
    return yes**2/(yes+no+0.0001) if yes > no else 0
  def better(c,a,b,all):
    sa, sb, sc = a.s(all), b.s(all), c.s(all)
    return abs(sb - sa) < my.e or sc >= sb and sc >= sa

class Bins:
  def __init__(i,txt,a,x,y,goal=True, bin=SBin): 
    i.txt  = txt
    i.goal = goal
    i.bin  = bin
    i.all  = i.bin(txt, goal)  
    return i.merge( i.grow( i.pairs(x,y)))
  def pairs(i,x,y,lst):
    lst = [(x(z), y(z) for z in a if not isinstance(x(z),str)]
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
#@go
def _tab():
  t = Tab(i).read("data/weather4.csv")
  o(t)
```

```py
import sys,math
from tricks import *

def about(): return [
"""
Optimizer, written as a data miner.  Break the data
up into {colorful} regions of "bad" and "better". Find
ways to jump "bad" to "better".

  :-------:  
  | Ba    |  Bad ------.  to plan, find (better - bad)
  |    56 |            |  to monitor, find (bad - better)
  :-------:-------:    |  to trust, check if if bad or better
          | Be    |    v  
          |     4 |  Better  
          :-------:  
""","""
Copyright (c) 2020, Tim Menzies.
All rights reserved under the BSD 2-Clause license.
""",
  # sway
  elp("verbose mode for Tree",      treeVerbose= False),
  elp("bin min size =len**b",        b  = .5),
  elp("what columns to while tree building " ,   c  = ["x","y"]),
  elp("use at most 'd' rows for distance calcs",    d  = 256),
  elp("separation of poles (f=1 means 'max distance')",   f  = .9),
  elp("coefficient for distance" ,   p  = 2),
  elp("tree leaves must be at least n**s in size" ,   s  = 0.5),

  elp("training data (arff format",  train = "train.csv"),
  elp("testing data (csv format)",   test  = "test.csv"),
  # --------------------------------------------------------------------
  # System
  elp("Run just the tests with names matching 'S'",        t = ""),
  elp("Run all tests. ", T = False)
]

my = args(*about())

@go
def hello(): print(about()[0])

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
  def mid(i): return i.mu
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
  def mid(i): return i.mode
  def add(i,x):
    tmp = i.seen[x] = i.seen.get(x,0) + 1
    if tmp > i.most: i.most,i.mode = tmp,x
    return x
  def dist(i,x,y): 
    return 1 if no(x) and no(y) else x != y
 
class Cols(Thing):
  def __init__(i) : 
    i.x,i.y,i.nums,i.syms,i.all,i.klas = {},{},{},{},[],None
  def add(i,lst): 
    [ col.add( lst[col.pos] ) for col in i.all ]
  def klass(i,lst): 
    return lst[i.klas]
  def header(i,lst):
    for pos,txt in enumerate(lst):
      tmp = (Num if nump(txt) else Sym)(pos,txt)
      i.all += [tmp]
      (i.y    if goalp(txt) else i.x)[pos] = tmp
      (i.nums if nump(txt)  else i.syms)[pos] = tmp
      if klassp(txt) : i.klas  = tmp

class Tab(Thing):
  def __init__(i,rows=[]):
    i.rows, i.cols = [], Cols()
    [i.add(row) for row in rows]
  def clone(i,rows=[]):
    t  = Tab()
    t  + [c.txt for c in i.cols.all] 
    [t + row for row in  rows]
    return t
  def __add__(i,a): 
    return i.add(a) if i.cols.all else i.cols.header(a)
  def add(i,a): 
    i.rows += [[c + a[c.pos] for c in i.cols.all]]
  def read(i,data=None): 
    [i + row for row in cols(rows(data))]
    return i
  def pairs(i,col):
    return Bins(col.pos,i.rows, lambda z: z[col.pos], 
                                lambda z: i.cols.klass(z))
  def status(i):
    return '{' + ', '.join([('%.2f' % c.mid()) 
                     for c in i.cols.y.values()]) + '}'
  def mid(i):
    return [ col.mid() for col in i.cols.all ]
  def dom(i,row1,row2):
    s1,s2,n = 0,0,len(i.cols.y)+0.0001
    for c in i.cols.y.values():
      x   = c.norm( row1[c.pos] )
      y   = c.norm( row2[c.pos] )
      s1 -= math.e**(c.w*(x-y)/n)
      s2 -= math.e**(c.w*(y-x)/n)
    return s1/n < s2/n
```

```py
class Dist:
  def __init__(i, t,cols=None, rows=None, p=my.p):
    i.t= t
    i.p= p
    i.cols = cols or t.cols.x
    i.rows = rows or shuffle(t.rows)[:my.d]
  def dist(i,row1,row2):
    d = 0
    for col in i.cols.values():
      inc = col.dist( row1[col.pos], row2[col.pos] )
      d  += inc**my.p
    return (d/len(i.cols))**(1/my.p)
  def neighbors(i,r1):
    a = [(i.dist(r1,r2),r2) for r2 in i.rows if id(r1) != id(r2)]
    return sorted(a, key = lambda z: z[0])
  def faraway(i,row):
     a= i.neighbors(row)
     return a[ int( len(a) * my.f ) ][1]
  def poles(i):
     tmp   = random.choice(i.rows)
     left  = i.faraway(tmp)
     right = i.faraway(left)
     return left, right, i.dist(left,right)
  def project(i,row, left,right,c):
     a = i.dist(row,left)
     b = i.dist(row,right)
     d = (a**2 + c**2 - b**2) / (2*c)
     if d>1: d= 1
     if d<0: d= 0
     return d

class Tree:
   def __init__(i, t, cols=my.c, lo=None, lvl=0):
     lo = lo or 2*len(t.rows)**my.s
     if len(t.rows) > lo:
       if my.treeVerbose:
         print(('| '*lvl) + str(len(t.rows)))
       i.d         = Dist(t,cols=t.cols.__dict__[cols])
       i.l,i.r,i.c = i.d.poles()
       xs          = [i.d.project(r,i.l,i.r,i.c) for r in t.rows]
       i.mid       = sum(xs) / len(xs)
       i.kids      = [t.clone(),t.clone()]
       [i.kids[x >= i.mid].add(r)     for x,r in zip(xs, t.rows)]
       if len(i.kids[0].rows) < len(t.rows) and \
          len(i.kids[1].rows) < len(t.rows) :
          [ Tree(kid, cols=cols, lo=lo, lvl=lvl+1) 
            for kid in i.kids ]
     else:
       if my.treeVerbose:
         print(('| '*lvl) + str(len(t.rows)),t.status())
      
class Bore:
   def __init__(i, t) :
     i.rest = t.clone()
     i.best = i.div(t, 2*len(t.rows)**my.s)
   def div(i,t,lo):
     if len(t.rows) < lo: return  t
     d     = Dist(t,cols=t.cols.y)
     l,r,c = d.poles()
     xs    = [d.project(row,l,r,c) for row in t.rows]
     mid   = sum(xs) / len(xs)
     kid   = t.clone()
     if t.dom(l, r):
       for x,row in zip(xs, t.rows):
         (kid if x < mid else i.rest).add(row)
     else:
       for x,row in zip(xs, t.rows):
         (kid if x >=  mid else i.rest).add(row)
     return i.div(kid,lo)

class SRanges(Thing): 
  def __init__(i, txt, a, x, y, goal=True):
    i.txt  = txt
    i.goal = goal
    i.all  = Range(txt,x,i),
    d      = {}
    for one in a:
      x1, y1 = x(one), y(one)
      if no(x1): continue
      if not x1 in d: d[x1] = Range(txt,x,i)
      d[x].add(x1,y1)
      i.all.add(x1,y1)
    i.ranges =  d.values()

class Range:
  def __init__(i,what,xf,ranges):
    i.what,i.xf,i.ranges = what, xf, ranges
    i.n, i.yes, i.no = 0,0.0001,0.0001
    i.lo, i.hi = None,None
  def add(i,x,y):
    i.n += 1
    if y==i.ranges.goal: i.yes += 1
    else               : i.no += 1
    i.lo = min(x,i.lo)
    i.hi = max(x,i.hi)
  def merge(i,j):
    k     = i.ranges.bin()
    k.lo  = min(i.lo, j.lo) 
    k.hi  = max(i.hi, j.hi) 
    k.n   = i.n + j.n
    k.no  = i.no  + j.no
    k.yes = i.yes + j.yes
    return k
  def better(c,a,b):
    sa, sb, sc = a.s(), b.s(), c.s()
    return abs(sb - sa) < my.e or sc >= sb and sc >= sa
  def s(i):
    yes   = i.yes/i.ranges.all.yes 
    no    = i.no /i.ranges.all.no
    return  yes**2/(yes+no+0.0001) if yes > no else 0


class Ranges(Thing):
  def __init__(i,txt,a,x,y,goal=True):
    i.txt  = txt
    i.goal = goal
    i.bin  = lambda: Range(txt,x,i),
    i.all  = i.bin()
    i.ranges= i.merge( i.grow( i.pairs(x,y)))
  def pairs(i,x,y,lst):
    lst = [(x(z), y(z)) for z in a if not isinstance(x(z),str)]
    return sorted(lst, key= lambda z:z[0])
  def grow(i,a):
    min  = len(a)**my.b
    use  = len(a) - min
    bins = [i.bin()]
    for j,(x,y) in enumerate(a):
      if j < use and bins[-1].n > min:
        bins += [i.bin()]
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
def _hetab1():
  t = Tab().read("data/weather4.csv")
  assert( 4 == t.cols.x[0].seen["overcast"])
  assert(14 == t.cols.x[0].n)
  assert(14 == len(t.rows))
  assert( 4 == len(t.cols.all))
  assert( 3 == len(t.cols.syms))
  print(t)

@go
def _tab2():
  t = Tab().read("data/auto93.csv")
  assert(398 == len(t.rows))

@go
def _dist():
  t = Tab().read("data/auto93.csv")
  d = Dist(t)
  for r1 in shuffle(t.rows)[:10]:
    if not "?" in r1:
       assert(d.dist(r1,r1) == 0)
    n = d.neighbors(r1)
    r2 = n[ 0][1]
    r3 = n[-1][1]
    r4 = d.faraway(r1)
    print("")
    print(r1)
    print(r2, f'{d.dist(r1,r2):.3f}')
    print(r4, f'{d.dist(r1,r4):.3f}')
    print(r3, f'{d.dist(r1,r3):.3f}')
    print(*d.poles())

@go
def _tree():
  t = Tab().read("data/auto93.csv")
  my.treeVerbose = True
  Tree(t,cols="y")
 #go()

@go
def _bore():
  t = Tab().read("data/auto93.csv")
  b = Bore(t)
  print([col.txt for col in t.cols.y.values()])
  print("best",b.best.status())
  print("rest",b.rest.status())
  print("all",t.status())
 #go()

if __name__ == "__main__":
   if my.T: go()
   if my.t: go(use=my.t)
# ```

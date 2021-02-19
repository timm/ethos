#i!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81:
"""
Store rows from csv data , summarized in columns

- License: (c) 2021 Tim Menzies <timm@ieee.org>, MIT License  

Stores the csv data in `Row`s held in `Tab` (tables).

- Missing values in each row are denoted `?`.
- Column names are stored in row@1.
  - Numeric column names start in upper case.
  - Goals to be minimized/maximized end in -/+ (respectively).
  - Columns to be ignored have names with  symbol `?`.
     - Ignored columns are summarized in `Skip` instances (that do nothing).
- `Row` columns are summarized in `Sym`(bol) or `Num`umeric columns or
`Skip` columns (that just ignore the data passed to them).
  - `Sym`s count the symbols (and the mode, which is the most common symbol).
  - `Num`s report the median and standard deviation of the nums seen so far.
- One `Row` is better than another if
- `Num`s can also discretization their numerics into bins.
  - Spurious bins are fused with their neighbors.
  - Discretizations are stored as `Bin`s.
- `Cols` store the `x/y/all` (independent/dependent/all) columns.
 - `Skip`ed columns do not appear in the `x/y` lists.

"""
def demo():
  t=Tab().adds(csv("../data/auto93.csv"))
  print(len(t.rows))
  c=t.cols.all[4]
  print(c.txt, c.w, c.var(), c.div(t))

#-----------------------------------------------
import re, math
from it import it

DELIMITER = ','
IGNORE    = r'([\n\t\r ]|#.*)'
LESS      = '-' 
MORE      = '+'
SKIP      = '?'
      
def Tab():
  """Initializes summary columns, stores data rows, sumarizes 
  that data in columns. Optinonally , can also  marks 
  rows as `best` or not (see the `classify` function)"""
  def _row(i, lst): return Row([c.add(x) for c,x in zip(i.cols.all,lst)])
  def _cols(i,lst): return [i.cols.add(n,txt) for n,txt in enumerate(lst)]
  #--------------
  def classify(i,some=64,best=0.8):
    i.rows = sorted(i.rows, key=lambda r: r.betters(i,some))
    for n,row in enumerate(i.rows):
      row.best = n > len(i.rows)*best
  #--------------
  def adds(i,src):
    for lst in src:
      if i.cols.all: i.rows     += [_row(i,lst)]
      else:          i.cols.all  = _cols(i,lst)
    return i
  #-----------------------------------------
  return it(cols=Cols(), rows=[]) + locals()

def Row(lst):
  "Holds one record. Can report if one row is better than another."
  def ys(i,t): 
    return [i.cells[c.pos] for c in t.cols.y]
  #-----------------
  def better(i,j,t):
    s1,s2,n = 0,0,len(t.cols.y)
    for col in t.cols.y:
      pos,w = col.pos, col.w
      a,b   = i.cells[pos], j.cells[pos]
      a,b   = col.norm(a), col.norm(b)
      s1   -= math.e**(w*(a-b)/n)
      s2   -= math.e**(w*(b-a)/n)
    return s1/n < s2/n
  #---------------------
  def betters(i,t,some):
    i.n = i.n or sum(better(i,random.choice(t.rows), t)
                     for _ in range(some))/some
    return i.n
  #----------------------------------------
  return it(cells=lst, n=None, best=False) + locals()

def Cols():
  "Stored different kinds of columns in mulitple lists."
  def add(i,pos,txt):
    if   SKIP in txt                                   : f = Skip
    elif LESS in txt or MORE in txt or txt[0].isupper(): f = Num
    else                                               : f = Sym
    now = f(pos=pos, txt=txt, w=-1 if LESS in txt else 1)
    if   SKIP in txt                                   : also = []
    elif LESS in txt or MORE in txt                    : also = i.y
    else                                               : also = i.x
    also  += [now]
    return now
  #----------------------------------------
  return it(all=[], y=[], x=[]) + locals()

def Skip(pos=0, txt="", w=1):
  "The simplest column: if yo pass it data, it forgets it instantly"
  def add(i,x):
    if x != SKIP: i.n += 1; return x
  #----------------------------------------
  return it(pos=pos, txt=txt, w=w, n=0)  + locals()

def Sym(pos=0, txt="", w=1):
  "`Sym`s track symbol counts and can report mode and entropy."
  def ent(i): return -sum(v/i.n*math.log(v/i.n,2) for v in i.seen.values())
  def div(i, _): return [Bin(x,x) for x in i.seen.keys()]
  #-------
  def spurious(i, j):
    "If two syms both conclude the same thing, combine them."
    if i.mode == j.mode:
      k = Sym(pos=i.pos, txt=i.txt, w=i.w)
      for x,n in i.seen.items(): k.add(x,n)
      for x,n in j.seen.items(): k.add(x,n)
      return k
  #-------
  def add(i,x,n=1):
    if x != SKIP:
      i.n += n
      now = i.seen[x] = i.seen.get(x, 0) + n
      if now > i.most: i.most, i.mode = now, x
    return x
  #----------------------------------------
  return it(pos=pos, txt=txt, w=w, n=0, seen={}, most=0, mode=None) + locals()

def Num(pos=0, txt="", w=1):
  """`Nums`s track numerics and can report median (`mid`) and
   standard deviation `var`. They can also normalize numerics 0..1
   and report good ways to convert numeric columns into bins"""
  def mid(i)   : n,a = _all(i); return a[int(n/2)]
  def var(i)   : n,a = _all(i); return (a[int(.9*n)] - a[int(n/10)]) / 2.56
  def norm(i,x): _,a = _all(i); return (x - a[0]) / (a[-1] - a[0])
  def _all(i)   :
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return len(i._all), i._all
  #------------
  def add(i, x):
    if x != SKIP:
      i._all += [x]; i.n+= 1; i.ok = False
    return x
  #------------
  def div(i,t,cohen=.2, xchop=0.5):
    xy = sorted([(r.cells[pos], r.best) for r in t.rows
                if r.cells[pos] != SKIP])
    size = len(xy)**xchop
    while size < 4 and width < len(xy) / 2: width *= 1.2
    bins(xy, size, i.var()*cohen)
  #----------------------------------------
  return it(pos=pos, txt=txt, w=w, _all=[], ok=True, n=0) + locals()

def Bin(x, y):
  """Ranges from `down` to `up`. Can `also` stores
  the y-values seen in that range."""
  def has(i,x,y): return i.down <= x <i.up
  #----------------------------------------
  return it(down=x, up=y, also=Sym()) + locals()
 
def bins(xy,size,small):
  """Split data into  bins of size, say, sqrt(N);
  then merge adjacent bins that are spuriously different."""
  def split():
    now = Bin(xy[0][0], xy[0][0])
    tmp = [now]
    for j,(x,y) in enumerate(xy):
      if j < len(xy) - size:
        if now.also.n >= size:
          if x != xy[j+1][0] and now.up - now.down > small:
            now  = Bin(now.up, x)
            tmp += [now]
      now.up = x
      now.also.add(y)
    return tmp
  #------------
  def merge(b4):
    j, tmp, n = 0, [], len(b4)
    while j < n:
      a = b4[j]
      if j < n - 1:
        b  = b4[j+1]
        now = a.also.spurious(b.also)
        if now:
          a = Bin(a.down, b.up)
          a.also = now
          j += 1
      tmp += [a]
      j   += 1
    return merge(tmp) if len(tmp) < len(b4) else b4
  #------------------------------------------------
  out          = merge(split())
  out[ 0].down = -math.inf
  out[-1].up   =  math.inf
  return out

def csv(file):
  """Helper function: read csv rows, skip blank lines, coerce strings
     to numbers, if needed."""
  def atom(x):
    try: return int(x)
    except Exception:
      try: return float(x)
      except Exception: return x
  with open(file) as fp:
    for a in fp:
      yield [atom(x) for x in re.sub(IGNORE, '', a).split(DELIMITER)]
 
__name__ == "__main__" and demo()

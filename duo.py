#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
import re, math, random, inspect
from types import FunctionType as Fun
import argparse as arg

def duo( BEST:      'ratio of best examples'         = .75, 
         COHEN:     'min interesting xbin size'      =.2, 
         DELIMITER: 'csv column seperator='          = ',', 
         FILE:      'data file'                      = 'auto93.csv',
         IGNORE:    'characters to delete in data'   = r'([\n\t\r ]|#.*)',
         LESS:      'marker for goals to minimize'   = '-', 
         MORE:      'marker for goals to maximize'   = '+',
         PATH:      'path to data'                   = '.', 
         SEED:      'random number seed'             = 1,
         SKIP:      'data to ignore'                 = '?',
         TESTS:     'comparison size for domination' = 32,
         XCHOP:     'size of bins'                   = 5
       ): 
  """
  DUO = data miners used / used-by optimizers.  
  (c) Tim Menzies, 2021 MIT License, https://opensource.org/licenses/MIT.
  
  - Stores the csv data in `Row`s held in `Tbl` (tables).
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
      - Discretizations are stored as `Span`s.
  - `Cols` store the `x/y/all` (independent/dependent/all) columns.
   - `Skip`ed columns do not appear in the `x/y` lists.
  
  Coding standards: 
  
  - No tabs. Indent with 2 spaces.
  - Keep code <= 80 LOC
  - Use flake8 but ignore pep8 (cause its too verbose)
  - Use `small objects` (sets of local functions inside containers)
  - Use `i` to denote  a pointer to a container instances.
  
  """
  random.seed(SEED)
  
  def Counts():
    return o(f={}, h={}, n=0)
  
  def Row(lst):
    def ys(i,t): return [i.cells[c.pos] for c in t.cols.y]
    def _better(i,j,t):
      s1,s2,n = 0,0,len(t.cols.y)
      for col in t.cols.y:
        pos,w = col.pos, col.w
        a,b   = i.cells[pos], j.cells[pos]
        a,b   = col.norm(a), col.norm(b)
        s1   -= math.e**(w*(a-b)/n)
        s2   -= math.e**(w*(b-a)/n)
      return s1/n < s2/n
    def betters(i,t):
      i.n = i.n or sum(_better(i,random.choice(t.rows), t)
                       for _ in range(TESTS))/TESTS
      return i.n
    #----------------------------------------
    return o(cells=lst, n=None, _tag=False) + locals()
  
  def Tbl():
    def _row(i, lst): return Row([c.add(x) for c,x in zip(i.cols.all,lst)])
    def _cols(i,lst): return [i.cols.add(n,txt) for n,txt in enumerate(lst)]
    def _classify(i):
      i.rows = sorted(i.rows, key=lambda r: r.betters(i))
      for n,row in enumerate(i.rows):
        row.tag = n > len(i.rows)*BEST
    def adds(i,src):
      for lst in src:
        if i.cols.all: i.rows     += [_row(i,lst)]
        else:          i.cols.all  = _cols(i,lst)
      _classify(i)
      return i
    #-----------------------------------------
    #return o(cols=Cols(), rows=[]) #+ locals()
    return o(cols=Cols(), rows=[]) + locals()
  
  def Cols():
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
    return o(all=[], y=[], x=[]) + locals()
  
  def Span(x, y):
    def has(i,x,y): return i.down <= x <i.up
    #----------------------------------------
    return o(down=x, up=y, _also=Sym()) + locals()
  
  def Skip(pos=0, txt="", w=1):
    def add(i,x):
      if x != SKIP: i.n += 1; return x
    #----------------------------------------
    return o(pos=pos, txt=txt, w=w, n=0)  + locals()
  
  def Sym(pos=0, txt="", w=1):
    def ent(i): return -sum(v/i.n*math.log(v/i.n,2) for v in i.seen.values())
    def div(i, _): return [Span(x,x) for x in i.seen.keys()]
    def spurious(i, j):
      if i.mode == j.mode:
        k = Sym(pos=i.pos, txt=i.txt, w=i.w)
        for x,n in {**i.seen, **j.seen}.items(): k.add(x,n)
        return k
    def add(i,x,n=1):
      if x != SKIP:
        i.n += n
        now = i.seen[x] = i.seen.get(x, 0) + n
        if now > i.most: i.most, i.mode = now, x
      return x
    #----------------------------------------
    return o(pos=pos, txt=txt, w=w, n=0, seen={}, most=0, mode=None) + locals()
  
  def Num(pos=0, txt="", w=1):
    def mid(i)   : n,a = _all(i); return a[int(n/2)]
    def var(i)   : n,a = _all(i); return (a[int(.9*n)] - a[int(n/10)]) / 2.56
    def norm(i,x): _,a = _all(i); return (x - a[0]) / (a[-1] - a[0])
    def _all(i)   :
      i._all = i._all if i.ok else sorted(i._all)
      i.ok = True
      return len(i._all), i._all
    def add(i, x):
      if x != SKIP:
        i._all += [x]; i.n+= 1; i.ok = False
      return x
    def div(i,t):
      xy = sorted([(r.cells[pos], r.tag) for r in t.rows
                  if r.cells[pos] != SKIP])
      width = len(xy)**XCHOP
      while width < 4 and width < len(xy) / 2: width *= 1.2
      now = Span(xy[0][0], xy[0][0])
      tmp = [now]
      for j,(x,y) in enumerate(xy):
        if j < len(xy) - width:
          if now._also.n >= width:
            if x != xy[j+1][0] and now.up - now.down > i.var()*COHEN:
              now  = Span(now.up, x)
              tmp += [now]
        now.up = x
        now._also.add(y)
      out = _merge(tmp)
      out[ 0].down = -math.inf
      out[-1].up   =  math.inf
      return out
    def _merge(b4):
      j, tmp, n = 0, [], len(b4)
      while j < n:
        a = b4[j]
        if j < n - 1:
          b  = b4[j+1]
          now = a._also.spurious(b._also)
          if now:
            a = Span(a.down, b.up)
            a._also = now
            j += 1
        tmp += [a]
        j   += 1
      return _merge(tmp) if len(tmp) < len(b4) else b4
    #----------------------------------------
    return o(pos=pos, txt=txt, w=w, _all=[], ok=True, n=0) + locals()
  
  def csv(file):
    def atom(x):
      try: return int(x)
      except Exception:
        try: return float(x)
        except Exception: return x
    with open(file) as fp:
      for a in fp:
        yield [atom(x) for x in re.sub(IGNORE, '', a).split(DELIMITER)]
  
  t=Tbl().adds(csv(PATH + "/" + FILE))
  # #print(t.cols.y)
  # #print(t.cols.y)
  for row in t.rows[:5]: print(row.ys(t),row.tag,row.n)
  print("")
  for row in t.rows[-5:]: print(row.ys(t),row.tag,row.n)
  # for col in t.cols.x:
  #   print(f"\n {col.txt}", col.pos)
  #   print(col.div(t))

#-------------------------------------------------------  
class o:
  "Simple container of names fields, with methods."
  def __init__(i, **d): i.__dict__.update(d)
  def __repr__(i):
    "Pretty print, sorted keys, ignore private keys (those  with `_`)."
    return "{"+ ', '.join( [f":{k} {v}" for k, v in sorted(i.__dict__.items())
                            if  type(v) != Fun and k[0] != "_"])+"}"
  def __add__(i, maybe):
    "For all functions, add them as methods to `i`."
    def method(i,f): return lambda *lst, **kw: f(i, *lst, **kw)
    for k,v in maybe.items():
      if type(v) == Fun and k[0] != "_": i.__dict__[k] = method(i,v)
    return i

def cli(f):
  "Call `f`, first checking if any command line options override the defaults."
  def details(x,txt):
    isa, a = isinstance, None
    if isa(x, list):
      a, x = x, x[0]
    m, t = (("I", int)   if isa(x, int)   else (
            ("F", float) if isa(x, float) else ("S", str)))
    h = f"{txt}; default= {x} " + (f"range= {a}" if a else "")
    return dict(help=h, default=x, metavar=m, type=t, choices=a) if a else ( 
           dict(help=h, action='store_true')            if x is False else (
           dict(help=h, default=x, metavar=m, type=t)))
  #----------------------------------------------------
  do = arg.ArgumentParser(prog            = f.__name__,
                          description     = f.__doc__.split("\n\n")[0],
                          formatter_class = arg.RawDescriptionHelpFormatter)
  for key, v in inspect.signature(f).parameters.items():
    do.add_argument("-"+key, **details(v.default, v.annotation))
  return f(**vars(do.parse_args())) 

#-------------------------------------------------------  
if __name__ == "__main__": cli(duo)

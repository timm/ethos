#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et:   
"""
# keys.py 
(c) 2021, Tim Menzies, MIT license.     

USAGE ./keys.py [OPTIONS]  
  
 -t S  run demo functions matching S  
 -T    run all demo functions  
 -L    list all demo functions  
 -h    run help  
 -C    show copyright  

"""
from types import FunctionType as fun
import re, sys, inspect, pyfiglet, datetime
import random 

#------------------------------------------
# ## Base class
# You gotta start somewhere.
# Fast inits, print the non-private slots (those that don't start with `_`).
class o(object):
  def __init__(i, **d): i.__dict__.update(d)
  def __repr__(i): return "{"+ ', '.join([f":{k} {v}" 
    for k, v in sorted(i.__dict__.items()) if type(v)!=fun and k[0] != "_"])+"}"

#------------------------------------------
# ## Globals
# The only one.
the = o(ch = o(no="?", sep=","))

# ------------------------------------------
# ## Column Classes
# Used to summarize individual columns.
#
# - Col(txt="", pos=0). _pos is the column number_
#      - Num(all, w=1).  _If minimizing then w=-1._
#      - Sym(all, most, mode)
#      - Some(all, keep=256).  _Only keep some samples._
# ### Col
# Base object for all other columns. 
# `add()`ing items increments the `n` counter.
class Col(o):
  def __init__(i, pos=0, txt="", init=[]):  
    i.pos, i.txt, i.n, i.w = pos,txt,0,1
    i * init
  def __mul__(i, lst): [i + x for x in lst]; return i 
  def __add__(i, x) : 
    if x != the.ch.no:
      x = i._prep(x); i.n+= 1; i._add1(x)
    return x
  def _add1(i,x): return x
  def _prep(i,x): return x

# ### Num
# - `add` accumulates numbers into `_all`.
#  - `all()` returns that list, sorted. Can report
#  - `sd()` (standard deviation) and `mid()` (median point).
#  - Also knows how to `norm()` normalize numbers.
class Num(Col):
  def __init__(i, w=0, txt="", **kw):
    super().__init__(txt=txt, **kw)
    i._all=[]; i.ok=False; i.w=(-1 if "-" in txt else 1)
  def _add1(i,x) : 
    i._all += [x]
    i.ok=False
  def all(i):
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return i._all
  def mid(i):    a=i.all(); return a[int(len(a)/2)]
  def norm(i,x): a=i.all(); return (x-a[0])/(a[-1] - a[0])
  def _prep(i,x): return float(x)
  def sd(i):     a=i.all(); return (a[int(.9*len(a))] - a[int(.1*len(a))])/2.56

# ### Sym
# - `add` accumulates numbers into `_all`.
# Here, `add` tracks symbol counts, including `mode`."
class Sym(Col):
  def __init__(i, **kw): 
    i._all={}; i.mode=None; i.max=0
    super().__init__(**kw)
  def _add1(i,x):
    tmp = i._all[x] = i._all.get(x,0) + 1
    if tmp>i.max: i.max,i.mode = tmp,x
    return x
  def mid(i): return i.mode

# ### Some
# This `add` up to `max` items (and if full, sometimes replace old items).
class Some(Col):
  def __init__(i, keep=256, **kw): 
    super().__init__(**kw)
    i._all=[]; i.keep=keep
  def _add1(i,x) : 
    a, r = i._all, random.random
    if len(a) < i.keep : a += [x]
    elif r() < i.keep / i.n : a[ int(r()*len(a)) ] = x

# -------------------------------------------------
# ## Table class
# Holds rows, summarizes in columns. 
#
# - Cols(all=Col+, x=Col+, y=Col+).  _x,y &subseteq; all_
# - Row(cells=[], tag=0).  _tag is the row cluster i._
# - Tab(cols=Cols, rows=Row+, header=[]). _header is line1 of data._
# --------------------------
# Thing to store row data.
class Row(o):
  def __init__(i,cells=[]): 
    i.tag, i.cells= None, cells
  def __lt__(i,j,cols):
    "Worse if it losses more"
    s1,s2,n = 0,0,len(cols.y)
    for col in cols.y:
      pos,w = col.pos, col.w
      a,b   = i.cells[pos], j.cells[pos]
      a,b   = col.norm(a), col.norm(b)
      s1   -= math.e**(w*(a-b)/n)
      s2   -= math.e**(w*(b-a)/n)
    return s1/n < s2/n

# --------------------------------------
# Makes a `Num`,`Sym`, or `Skip`, sores 
# it in `i.all` and either `i.x` or `i.y`."""
class Cols(o):
  def __init__(i,lst): 
    i.header, i.x, i.y, i.all = lst, [], [], []
    for pos,txt in enumerate(lst):
      one = i.what(pos,txt)
      i.all.append(one)
      if the.ch.no  not in txt: 
        (i.y if txt[-1] in "+-" else i.x).append(one)
  def kind(i,txt):
    x = (Col if it.ch.no in txt else (Num if txt[0].isupper() else Sym))
    return x(pos=pos, txt=txt) 
  def ys(i,row): 
    return [row.cells[col.pos] for col in i.y]

class Tab(o):
  def __init__(i, keep=1024, div=lambda z:2*len(z)**.5):
     i.rows,i.cols= Some(), Cols()
     i.keep, i.div = keep, div
  def clone(i, rows=[]): 
    tab = Tab(keep=i.keep, div=i.div)
    tab * [i.cols.header] + rows 
    return tab
  def clusters(i): 
    return list(chunks(sorted(i.rows(), div(i.rows()))))
  def __mul__ (i, src):
    i.cols = Cols(next(src))
    for row in src:
      i.rows += [Row([col + x for col,x in zip(i.cols.all,row)])]
    return i
  def rows(i): 
    return i._rows._all

class lib:
  # print test with color
  def flair(**d):
    c=dict(
      PURPLE    = '\033[1;35;48m', CYAN   = '\033[1;36;48m',
      BOLD      = '\033[1;37;48m', BLUE   = '\033[1;34;48m',
      GREEN     = '\033[1;32;48m', YELLOW = '\033[1;33;48m',
      RED       = '\033[1;31;48m', BLACK  = '\033[1;30;48m',
      UNDERLINE = '\033[4;37;48m', END    = '\033[1;37;0m')
    for k,v in d.items(): return c["BOLD"] + c[k] + v + c["END"]

  # Standard meta trick
  def same(x): return x

  # Yield chunks of size `n`. If any left over, add to middle chunk.
  def chunks(a, n):
    n    = int(n)
    mid  = len(a)//2-n
    jump = n+n+len(a)%n
    for i in range(0, mid, n): yield a[i:i+n]
    yield a[i+n:i+jump] 
    for i in range(i+jump, len(a), n): yield a[i:i+n]

  # Read lists from  file strings (separating on commas).
  def csv(file):
    with open(file) as fp:
      for line in fp: 
        line = re.sub(r'([\n\t\r ]|#.*)','',line)
        if line: yield line.split(",")

# ------------
# ## Unit tests
class ok:
  fails = False

  def listAllTestFunctions(funs):
    for k,v in funs.items(): 
       if type(v)==fun: print(k, "\t:", v.__doc__)

  def ok(x,y):
    print(f"  -- {y} ",end=""); 
    try:              
      assert x,y   
      print(lib.flair(GREEN = "PASS"))
    except Exception: 
      ok.fails = True
      print(lib.flair(RED = "FAIL"))

  def runAllTests(funs):
    print(lib.flair(CYAN=pyfiglet.figlet_format("tests",font="larry3d")),end="")
    print(datetime.datetime.now().strftime("%c"))
    for k,f in funs.items(): ok.runOneTest(f)

  def runOneTest(one):
    if type(one)==fun:
       random.seed(1)
       print(lib.flair(YELLOW=f"\n# {fun.__name__} "+("-"*25)))
       print(f"[{one.__name__}] {one.__doc__}")
       one()

  def runSomeTests(want,funs):
    for k,f in funs.items():
      if want in k: ok.runOneTest(f)

# ------------
# ##  Tests
class tests:
  def ok1(): 
    "ok one ing?"
    ok.ok(1>2, "less-ing?")
  
  def ok2(): 
    "ok two ing?"
    ok.ok(10>2, "more-ing?")

  def chunks():
    "Divide a list into chunks"
    lst = [x for x in range(87)]
    lst = [len(a) for a in lib.chunks(lst, int(len(lst)**0.5))]
  
  def num():
    "summarising numbers"
    n=Num()
    for x in ["10","5","?","20","10","5","?","20","10","5",
               "?","20","10","5","?","20","10","5","?","20",
               "10","5","?","20"]:
      n + x
    print(n.mid(), n.sd())
  
  def sym():
    "summariing numbers"
    s=Sym(init= ["10","5","?","20","10","5","?","20","10","5",
                 "?","20","10","5","?","20","10","5","?","20",
                 "10","5","?","20"])
    ok.ok("10"==s.mid(),"mid working ?")
  
  def some():
    "summarize very large sample space"
    n=Some(keep=32)
    [n + x for x in range(10**6)]
    print(sorted(n._all))

  def csv():
    "Read a csv file."
    [print(x) for x in list(lib.csv("../data/auto93.csv"))[:5]]

  def tab():
    "make a table"
    t=Tab(lib.csv("../data/auto93.csv"))
    one = t.cols.all[1]
    t1 = Tab(iter([t.cols.header]))
    rows=[]
    t * [t.cols.header]+[row for row in t.rows]
    print(len(rows))   
    # print([len(a) for a in t.clusters()])
    # ok(395 == one.n, "summarized right?")
    # print([len(a) for a in t.clusters()])
    # ok(395 == len(t._rows._all),"kept enough?")
  
# --------------------------------
# Top-level control
def main():
  a = sys.argv
  funs = vars(tests)
  for n,c in enumerate(a):
    if c   == "-h": print(doc)                     ; continue
    if c   == "-C": print(doc.split("\n\n")[0])    ; continue
    if c   == "-L": ok.listAllTestFunctions(funs)  ; continue
    if c   == "-t": ok.runSomeTests(a[n+1], funs)  ; continue
    if c   == "-T": ok.runAllTests(funs)           ; continue
    if c[0]== "-" : print("usage: ./keys.py -[hCt:T] [args]")
  sys.exit(ok.fails)

if __name__ == "__main__":  main()

#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
"""keys.py
(c) 2021, Tim Menzies, MIT license.     

USAGE ./keys.py [OPTIONS]  
  
 -t S  run demo functions matching S  
 -T    run all demo functions  
 -L    list all demo functions  
 -h    run help  
 -C    show copyright  

-----------------------

CLASSES:

- Col(txt="", pos=0). _pos is the column number_
    - Num(all, w=1).  _If minimizing then w=-1._
    - Sym(all, most, mode)
    - Some(all, keep=256).  _Only keep some samples._
- Cols(all=Col+, x=Col+, y=Col+).  _x,y &subseteq; all_
- Row(cells=[], tag=0).  _tag is the row cluster i._
- Tab(cols=Cols, rows=Row+, header=[]). _header is line1 of data._
"""
from types import FunctionType as fun
import re, sys, inspect, pyfiglet, datetime
import random 

class t:
  "Fast inits, print the non-private slots (those that don't start with `_`."
  def __init__(i, **d): i.__dict__.update(d)
  def __repr__(i):      return "{"+ ', '.join( 
                          [f":{k} {v}" for k, v in sorted(i.__dict__.items()) 
                          if type(v)!=fun and k[0] != "_"])+"}"

the = t(ch = t(no="?", sep=","))

def column( pos=0,txt=""): 
  "Factory for generating different kinds of column."
  what = (Col if it.ch.no in txt else (Num if txt[0].isupper() else Sym))
  return what(pos=pos, txt=txt) 

class Col(t):
  """Base object for all other columns. `add()`ing items
  increments the `n` counter."""
  def __init__(i,pos=0, txt=""):  
    i.pos, i.txt, i.n, i.w = pos,txt,0,1
  def add(i,x) : 
    if x != the.ch.no:
      x = i.prep(x); i.n+= 1; i.add1(x)
    return x
  def add1(i,x):  return x
  def prep(i,x):  return x

class Num(Col):
  """
  - `add` accumulates numbers into `_all`.
  - `all()` returns that list, sorted. Can report
  - `sd()` (standard deviation) and `mid()` (median point).
  - Also knows how to `norm()` normalize numbers.
  """ 
  def __init__(i, w=0, txt="",pos=0): 
    super().__init__(txt=txt, pos=0) 
    i._all=[]; i.ok=False; i.w=(-1 if "-" in txt else 1)
  def add1(i,x) : 
    i._all += [x]
    i.ok=False
  def all(i):
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return i._all
  def mid(i):    a=i.all(); return a[int(len(a)/2)]
  def norm(i,x): a=i.all(); return (x-a[0])/(a[-1] - a[0])
  def prep(i,x): return float(x)
  def sd(i):     a=i.all(); return (a[int(.9*len(a))] - a[int(.1*len(a))])/2.56

class  Sym(Col):
  "Here, `add` tracks symbol counts, including `mode`."
  def __init__(i, **kw): 
    super().__init__(**kw)
    i._all={}; i.mode=None; i.max=0
  def add1(i,x):
    tmp = i._all[x] = i._all.get(x,0) + 1
    if tmp>i.max: i.max,i.mode = tmp,x
    return x
  def mid(i): return i.mode

class Some(Col):
  "This `add` up to `max` items (and if full, sometimes replace old items)."
  def __init__(i, keep=256, **kw): 
    super().__init__(**kw)
    i._all=[]; i.keep=keep
  def add1(i,x) : 
    r= random.random
    if len(i._all) < i.keep: i._all += [x]
    elif r() < i.keep / i.n: i._all[ int(r()*len(i._all)) ] = x

def data(src, cols=None):
  "Read data, updatiing columns as we go."
  cols = cols or Cols(next(src))
  for row in src:
    row = [col.add(x) for col,x in zip(cols.all,row)]
    yield cols,row


def Row(x):
  "Thing to store row data."
  new = on(gt=0, tag=None, cells = (x if type(x) else x.cells))
  def better(i,j,cols):
    s1,s2,n = 0,0,len(cols.y)
    for col in cols.y:
      pos,w = col.pos, col.w
      a,b   = i.cells[pos], j.cells[pos]
      a,b   = col.norm(a), col.norm(b)
      s1   -= math.e**(w*(a-b)/n)
      s2   -= math.e**(w*(b-a)/n)
    return s1/n < s2/n
  return new.has(locals())

def Cols(lst):
  """Makes a `Num`,`Sym`, or `Skip`, sores 
  it in `i.all` and either `i.x` or `i.y`."""
  new = on(header=lst, x=[], y=[], all=[])
  for pos,txt in enumerate(lst):
    one = column(pos,txt)
    new.all.append(one)
    if "?" not in txt: 
      (new.y if txt[-1] in "+-" else new.x).append(one)
  def ys(i,row): 
    return [row.cells[col.pos] for col in i.y]
  return new.has(dict(ys=ys))

def Tab(src=[], keep=1024, div=lambda z:2*len(z)**.5):
  new = on(_rows=Some(keep=keep), cols=None)
  for cols, row in  data(src):
    new.cols = cols
    new._rows.add(Row(row))
  def clone(i): 
    return Cols([i.cols.header])
  def clusters(i): 
    f= lambda a,b:(0 if id(a)==id(b) else (-1 if a.better(b,cols) else 1))
    return list(chunks(sorted(i.rows(), key=functools.cmp_to_key(f)),
                        div(i.rows())))
  def rows(i): 
    return i._rows._all
  return new.has(locals())

#----------------------------------
def test_tab():
  "make a table"
  t=Tab(csv("../data/auto93.csv"))
  one = t.cols.all[1]
  t1 = Tab(iter([t.cols.header]))
  rows=[]
  for cols, row in data([t.cols.header]+[row for row in t.rows]):
    rows += [Row(row)]
  print(len(rows))   
  # print([len(a) for a in t.clusters()])
  # ok(395 == one.n, "summarized right?")
  # print([len(a) for a in t.clusters()])
  # ok(395 == len(t._rows._all),"kept enough?")
  #

#----------------------------------------------------------------
class Lib:
  colors = dict(
    PURPLE    = '\033[1;35;48m', CYAN   = '\033[1;36;48m',
    BOLD      = '\033[1;37;48m', BLUE   = '\033[1;34;48m',
    GREEN     = '\033[1;32;48m', YELLOW = '\033[1;33;48m',
    RED       = '\033[1;31;48m', BLACK  = '\033[1;30;48m',
    UNDERLINE = '\033[4;37;48m', END    = '\033[1;37;0m')

  def same(x): return x

  def flair(**d):
    c = lib.colors
    for k,v in d.items(): return c["BOLD"] + c[k] + v + c["END"]

  def chunks(a, n):
    "Yield chunks of size `n`. If any left over, add to middle chunk."
    n    = int(n)
    mid  = len(a)//2-n
    jump = n+n+len(a)%n
    for i in range(0, mid, n): yield a[i:i+n]
    yield a[i+n:i+jump] 
    for i in range(i+jump, len(a), n): yield a[i:i+n]

  def cli(funs,doc=""):
    a = sys.argv
    for n,flag in enumerate(a):
      if flag=="-h": print(doc.split("\n\n----")[0]); continue
      if flag=="-C": print(doc.split("\n\n")[0]);     continue
      if flag=="-L": ok.listAllTestFunctions(funs);   continue
      if flag=="-t": ok.runSomeTests(a[n+1], funs);   continue
      if flag=="-T": ok.runAllTests(funs);            continue
      if flag[0] == "-" : print("usage: ./keys.py -[hCt:T] [args]")

  def csv(file):
    "Read lists from  file strings (separating on commas)."
    with open(file) as fp:
      for line in fp: 
        line = re.sub(r'([\n\t\r ]|#.*)','',line)
        if line: yield line.split(",")


class ok:
  fails = False

  def runAllTests(funs):
    print(lib.flair(CYAN=pyfiglet.figlet_format("tests", font="larry3d")), 
          end="")
    print(datetime.datetime.now().strftime("%c"))
    for k,f in funs.items(): ok.runOneTest(f)

  def runOneTest(fu):
    if type(fu)==fun:
       random.seed(1)
       print(lib.flair(YELLOW=f"\n# {fun.__name__} "+("-"*25)))
       print(f"[{fu.__name__}] {fu.__doc__}")
       fu()

  def listAllTestFunctions(funs):
    for k,v in funs.items(): 
       if type(v)==fun: print(k, "\t:", v.__doc__)

  def ok(x,y):
    print(f"  -- {y} ",end=""); 
    try:              assert x,y   ; print(lib.flair(GREEN="PASS"))
    except Exception: ok.fails=True; print(lib.flair(RED  ="FAIL"))

  def runSomeTests(want,funs):
    for k,f in funs.items():
      if want in k: ok.runOneTest(f)

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
      n.add(x)
    print(n.mid(), n.sd())
  
  def sym():
    "summariing numbers"
    s=Sym()
    for x in ["10","5","?","20","10","5","?","20","10","5",
               "?","20","10","5","?","20","10","5","?","20",
               "10","5","?","20"]:
      s.add(x)
    ok.ok("10"==s.mid(),"mid working ?")
  
  def some():
    "summarize very large sample space"
    n=Some(keep=32)
    [n.add(x) for x in range(10**6)]
    print(sorted(n._all))
   
if __name__ == "__main__": 
  lib.cli(vars(tests), __doc__)
  sys.exit(ok.fails)


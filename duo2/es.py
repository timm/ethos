#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et:   
"es.py /əˈspī/ verb LITERARY see something that is hidden, or obscure"

from types import FunctionType as fun
import pyfiglet, datetime, functools
import os, re, sys, math, time, inspect, argparse 
import random 

def espy(
    SRC      = None,
    ARGS     = sys.argv, 
    WHO      = "Tim Menzies", 
    VER      = "0.21", 
    COPYLEFT = "(c) 2021, Tim Menzies, MIT license, https://choosealicense.com/licenses/mit/",
    COHEN    : "ignore splits less than 'standard deviation*cohen'" = 0.3,
    DATA     : "csv file to load"     = "auto93.csv",
    DIR      : "path to data"         = "../data",
    KEEP     : "keep no more than 'keep' examples" = 1024,
    NO       : "missing value marker" = "?",
    SEP      : "CSV field separator"  = ",",
    SIZE     : "split 'n' numbers into bins of size 'n**size'" = 0.7, 
    DEMO     : "run one demo function"= "nothing",
    DEMOS    : "run all demo"         = False,
    LICENSE  : "show license"         = False,
    LS       : "list demo functions"  = False,
    VERSION  : "show version"         = False,
  ):
  
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
  class Col(lib.o):
    def __init__(i, pos=0, txt="", all=[]):  
      i.pos, i.txt, i.n, i.w, i.bins = pos,txt,0,1,[]
      i * all
    def __mul__(i, lst): [i + x for x in lst]; return i 
    def __add__(i, x) : 
      if x != NO:
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
      i._all, i.ok = [], False, 
      super().__init__(txt=txt, **kw)
      i.w = -1 if "-" in txt else 1
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
      i.all, i.mode, i.max = {}, None, 0
      super().__init__(**kw)
    def _add1(i,x):
      tmp = i.all[x] = i.all.get(x,0) + 1
      if tmp>i.max: i.max,i.mode = tmp,x
      return x
    def mid(i): return i.mode
    def spurious(i, j, goal):
      modei = i.mode == goal
      modej = j.mode == goal
      if modei == modej:
        k = Sym(pos=i.pos, txt=i.txt)
        for x,n in i.all.items(): k.all[x] = k.all.get(x,0) + n
        for x,n in j.all.items(): k.all[x] = k.all.get(x,0) + n
        for x,n in k.all.items():
          if n > k.max:
             k.mode, k.max = x,n
        return k
     
  # ### Some
  # This `add` up to `max` items (and if full, sometimes replace old items).
  class Some(Col):
    def __init__(i, keep=256, **kw): 
      i.all=[]; i.keep=keep
      super().__init__(**kw)
    def __add__(i,x) : 
      i.n += 1
      a, r = i.all, random.random
      if len(a) < i.keep : a += [x]
      elif r()  < i.keep / i.n : a[int(r()*len(a))] = x
  
  # -------------------------------------------------
  # ## Table class
  # Holds rows, summarizes in columns. 
  #
  # - Cols(all=Col+, x=Col+, y=Col+).  _x,y &subseteq; all_
  # - Row(cells=[], tag=0).  _tag is the row cluster i._
  # - Tab(cols=Cols, rows=Row+, header=[]). _header is line1 of data._
  # --------------------------
  # Thing to store row data.
  class Row(lib.o):
    def __init__(i,cells=[]): 
      i.tag, i.cells = 0, (cells if type(cells)==list else cells.cells)
    def better(i,j,cols):
      "Worse if it losses more"
      s1,s2,n = 0,0,len(cols.y)
      for col in cols.y:
        pos,w = col.pos, col.w
        a,b   = i.cells[pos], j.cells[pos]
        a,b   = col.norm(a), col.norm(b)
        s1   -= math.e**(w*(a-b)/n)
        s2   -= math.e**(w*(b-a)/n)
      return s1/n < s2/n
    def ys(i,tab):
      return [i.cells[col.pos] for col in tab.cols.y]
  
  # -------------------------------------------
  # Makes a `Num`,`Sym`, or `Skip`, store them 
  # in `i.all` and either `i.x` or `i.y`.
  class Cols(lib.o):
    def __init__(i,lst): 
      i.header, i.x, i.y, i.all = lst, [], [], []
      for pos,txt in enumerate(lst):
        one = i.kind(pos,txt)
        i.all.append(one)
        if NO not in txt: 
          (i.y if txt[-1] in "+-" else i.x).append(one)
    def kind(i,pos, txt):
      x = Col if NO in txt else (Num if txt[0].isupper() else Sym)
      return x(pos=pos, txt=txt) 
  
  class Tab(lib.o):
    def __init__(i, keep=1024, size=.5,opt=None, all=[]):
       i.keep, i.size  =  keep, size
       i.rows, i.cols = Some(keep = i.keep), None
       i * all
    def __add__ (i, lst)  :
      lst = (lst if type(lst)==list else lst.cells)
      if i.cols: 
        i.rows + Row([col + x for col,x in zip(i.cols.all,lst)])
      else:      
        i.cols = Cols(lst)
    def __mul__ (i, src): [i + x for x in src]; return i
    def classify(i):
      out = []
      for n,rows, in enumerate(i.clusters()):
        for row in rows: row.tag = n
        out += [n]
      return out
    def clone(i, rows=[]) : 
      return Tab(size=i.size,keep=i.keep) * ([i.cols.header] + rows) 
    def clusters(i): 
      gt   = lambda a,b: 0 if id(a)==id(b) else (-1 if a.better(b, i.cols) else 1)
      rows = i.rows.all
      rows = sorted(rows, key=functools.cmp_to_key(gt))
      return lib.chunks(rows, 2*len(rows)**i.size)
    def ys(i): 
      return [col.mid() for col in i.cols.y]
  
  # ## Discretization
  # ### Span(down, up, also)
  # Here, `also` are the class values seen between `down` and `up`.
  class Span(lib.o):
    def __init__(i,down=-math.inf, up=math.inf): 
      i.down, i.up, i.also = down, up, Sym()
    def __repr__(i):
      return f"[{i.down} .. {i.up})"
    def has(i,x):
      return x==i.down if i.down==i.up else i.down <= x < i.up
 
  # ### div
  # Return `Span`s generated by Spliting columns from `n` rows into 
  # bins of size  `n**size`. Ignore small splits (small than `sd*cohen`).
  def div(t, col):
    xy = sorted([(r.cells[col.pos], r.tag) for r in t.rows.all
                if r.cells[col.pos] != NO])
    width = len(xy)**SIZE
    while width < 4 and width < len(xy) / 2: width *= 1.2
    now = Span(xy[0][0], xy[0][0])
    out = [now]
    for j,(x,y) in enumerate(xy):
      if j < len(xy) - width:
        if now.also.n >= width:
          if x != xy[j+1][0]:
            if now.up - now.down > col.sd()*COHEN:
              now  = Span(now.up, x)
              out += [now]
      now.up = x
      now.also + y
    out[ 0].down = -math.inf
    out[-1].up   =  math.inf
    return out
 
  # ### Merge
  # Adjacent ranges that predict for sames goal are spurious.
  # If  we can find any, merge them then look for any other merges.
  def merge(b4, goal):
    j, tmp, n = 0, [], len(b4)
    while j < n:
      a = b4[j]
      if j < n - 1:
        b  = b4[j+1]
        merged = a.also.spurious(b.also, goal)
        if merged:
          a = Span(a.down, b.up)
          a.also = merged
          j += 1
      tmp += [a]
      j   += 1
    return merge(tmp, goal) if len(tmp) < len(b4) else b4
 
  # ### Counts
  # Given multiple clusters and one `goal` cluster,
  # label the clusters and `goal` and `not goal`.
  # Merge spurious adjacent bins; i.e. those that predict 
  # for the same label. Generate frequency counts of how 
  # often the merged bins appear in `goal` and `not goal`.
  # XXXX move binning and findin reevant bin into column.
  # also, need to be able to specify sets ofs goals, no-goal classes
  class Counts(lib.o):
    def __init__(i, tab, goal): 
      i.f, i.h, i.n = {}, {}, {}
      for col in tab.cols.x:
        if type(col) == Sym:
          col.bins = col.bins or [Span(down=x,up=x) for x in col.all.keys()]
          i.count(col, tab, goal, col.bins)
        else:
          col.bins = col.bins or div(tab, col)
          i.count(col, tab, goal, merge(col.bins, goal))
 
    # Update our frequency counts
    def count(i, col, tab, goal,  bins):
      def inc(d,k): d[k] = d.get(k,0) + 1
      f, h, n = i.f, i.h, i.n
      for row in tab.rows.all:
        x = row.cells[col.pos]
        if x != NO:
          for b in bins:
            if b.has(x):
              k = row.tag == goal
              inc(h, k)
              inc(f, (k, col.txt, b.down, b.up))
              inc(n, col.pos)
              break
 
  # ##  Tests
  class tests:

    def nothing(): 
      "Correctly installed"
      return 1

    def testTestEngine(): 
      "we can catch pass/fail"
      lib.ok(True,  "true-ing?")
      lib.ok(False, "false-ing?")

    def chunks87():
      "Divide a list into chunks"
      lst = [x for x in range(87)]
      lst = [len(a) for a in lib.chunks(lst, int(len(lst)**0.5))]
      lib.ok(lst[ 0] == 9, "starts with nine?")
      lib.ok(lst[-1] == 9, "ends with nine?")
      print(lst)

    def chunks100():
      "Divide a list into chunks"
      lst = [x for x in range(100)]
      lst = [len(a) for a in lib.chunks(lst, 10)]
      lib.ok(lst[ 0] == 10, "starts with ten?")
      lib.ok(lst[-1] == 10, "ends with ten?")
      print(lst)

    def num():
      "summarising numbers"
      n=Num(all=["10","5","?","20","10","5","?","20","10","5","?","20","10","5",
                  "?","20","10","5","?","20","10","5","?","20"])
      lib.ok(10.0 == n.mid(), "mid?")
      lib.ok(5.85 < n.sd() < 5.86, "sd?")

    def sym():
      "summariing numbers"
      s=Sym(all= ["10","5","?","20","10","5","?","20","10","5","?","20","10",
                  "5","?","20","10","5","?","20", "10","5","?","20"])
      lib.ok("10"==s.mid(),"mid working ?")
     
    def some():
      "summarize very large sample space"
      n=10**5
      keep=32
      lst = sorted(Some(keep=keep,all= [x for x in range(n)]).all)
      lib.ok(len(lst) ==32,"")
   
    def csv():
       "Read a csv file."
       lst = lib.csv("../data/auto93.csv")
       lib.ok(len(lst) == 399)
    
    def tab():
      "make a table"
      t = Tab() * lib.csv("../data/auto93.csv")
      lib.ok(398 == len(t.rows.all))
      one = t.cols.all[1]
      lib.ok(151 == one.mid())

    def clusters():
      "make a table"
      t = Tab() * lib.csv("../data/auto93.csv")
      all = [t.clone(rows).ys() for rows in t.clusters()]
      [print(one) for one in all]
      lib.ok(all[0][ 0] < all[-1][0])
      lib.ok(all[0][-1] > all[-1][1])

    def divs():
      "make a table"
      t = Tab() * lib.csv("../data/auto93.csv")
      t.classify()
      for col in t.cols.x:
        if type(col) == Num: 
          print(len(div(t,col)))
 
    def counts():
      t = Tab(size=.66) * lib.csv("../data/auto93.csv")
      t.classify()
      c = Counts(t, 0)
      for k,v in c.f.items():
        print(k,v)
 
## --------------------------------
  FUNS= vars(tests)
  for n,c in enumerate(ARGS):
    if c == "-data"   : DATA = ARGS[n+1]
    if c == "-dir "   : DIR  = ARGS[n+1]
    if c == "-license": print(COPYLEFT)
    if c == "-version": print(VER)
    if c == "-demo"   : [lib.run(FUNS[k]) for k in FUNS if ARGS[n+1] in k]
    if c == "-demos"  : lib.banner();  [lib.run(FUNS[k]) for k in FUNS]
    if c == "-ls"     : 
      print("\nDEMOS:"); 
      [print(lib.flair(RED=f"{k:>15}"),":",v.__doc__) 
       for k,v in FUNS.items() if type(v)==fun] 
  if SRC: main()
  sys.exit(0 if lib.fails==1 else 1)

class lib:
  fails = 0

 # Base class: easy inits, pretty print (keys sorted, skip those starting with "_")
  class o(object):
    def __init__(i, **d): i.__dict__.update(d)
    def __repr__(i): return "{"+ ', '.join([f":{k} {v}" 
      for k, v in sorted(i.__dict__.items()) if type(v)!=fun and k[0] != "_"])+"}"

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
    out =[]
    n    = int(n)
    mid  = len(a)//2-n
    jump = n+n+len(a)%n
    for i in range(0, mid, n): out += [a[i:i+n]]
    out += [a[i+n:i+jump]] 
    for i in range(i+jump, len(a), n): 
      out += [a[i:i+n]]
    return out
 
  # Read lists from  file strings (separating on commas).
  def csv(file):
    out = []
    with open(file) as fp:
      for line in fp: 
        line = re.sub(r'([\n\t\r ]|#.*)','',line)
        if line: out +=  [line.split(",")]
    return out
 
  def ok(x,y=""):
    print("--",y,end=" "); 
    try:              
      assert x,y   
      print(lib.flair(GREEN = "PASS"))
    except Exception: 
      print(lib.flair(RED = "FAIL"))
      lib.fails += 1
 
  def run(x):
    if type(x)==fun:
      random.seed(1)
      print(lib.flair(YELLOW=f"\n# {x.__name__}:"), x.__doc__)
      x()
 
  def banner():
    os.system("clear" if os.name == "posix" else "cls")
    s= datetime.datetime.now().strftime("%H  :  %M  :  %S")
    print(lib.flair(CYAN=pyfiglet.figlet_format(s,font="mini"))[:-35],end="")
    return True

  def cli(f):
   "Call `f`, first checking if any command line options override the defaults."
   arg = argparse
   def details(x,txt):
     isa, a = isinstance, None
     if isa(x, list):
       a, x = x, x[0]
     m, t,h = (("B", bool,  f"{txt}") if x is False    else (
               ("I", int,   f"{txt}") if isa(x, int)   else (
               ("F", float, f"{txt}") if isa(x, float) else 
               ("S", str,   f"{txt}"))))
     h = (h+f"; default={x}") if x is not False else h
     h = (h+f"range= {a}")    if a else h
     return dict(help=h, default=x, metavar=m, type=t, choices=a) if a else ( 
            dict(help=h, action='store_true')            if x is False else (
            dict(help=h, default=x, metavar=m, type=t)))
   #----------------------------------------------------
   do = arg.ArgumentParser(prog            = f.__name__,
                           description     = (f.__doc__ or '').split("\n\n")[0],
                           formatter_class = arg.RawDescriptionHelpFormatter)
   for key, v in inspect.signature(f).parameters.items():
     if type(v.annotation)==str:
       do.add_argument("-"+key.lower(), 
                       dest=key,**details(v.default, v.annotation))
   return f(**vars(do.parse_args())) 
 

if __name__ == "__main__": lib.cli(espy)
# 
# 

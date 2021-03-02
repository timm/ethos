#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et:   
# Data miner as optimizer
# -size .8 crashes
# need a class rule RULES
"""
es.py /əˈspī/ verb LITERARY see something that is hidden, or obscure.
Optimizer, written as a data miner.  Break the data up into regions
of 'bad' and 'better'. 'Interesting' things occur at very different
frequencies in 'bad' and 'better'. Find interesting bits. Combine
them. Repeat. Nearly all this processing takes log linear time.

     :-------:                 explore  = better==bad
     | Ba    | Bad <----.      planning = max(better - bad)
     |    56 |          |      monitor  = max(bad - better)
     :-------:------:   |      tabu     = min(bad + better)
             | B    |   v
             |    5 | Better
             :------:

Class model:
- Lib.o
  - Col(txt="", pos=0).        # Pos is the column number.
      - Num(all, w=1).         # If minimizing then w=-1.
      - Sym(all, most, mode)   # Most is the most frequently seen thing
      - Some(all, keep=256).   # Only keep some samples.

"""
from types import FunctionType as fun
import os, re, sys, math, time, random, inspect, argparse
import pyfiglet, datetime, functools, traceback

def espy(
    SRC      = None,
    ARGS     = sys.argv, 
    WHO      = "Tim Menzies", 
    VER      = "0.21", 
    COPYLEFT = "(c) 2021, Tim Menzies, MIT license, "+\
               "https://choosealicense.com/licenses/mit/",
    COHEN    : "ignore splits less than 'standard deviation*cohen'" = 0.3,
    DATA     : "csv file to load"     = "auto93.csv",
    DIR      : "path to data"         = "../data",
    KEEP     : "keep no more than 'keep' examples" = 1024,
    NO       : "missing value marker" = "?",
    SEP      : "CSV field separator"  = ",",
    SIZE     : "split 'n' numbers into bins of size 'n**size'" = 0.7, 
    EG       : "run one example function"= "nothing",
    LS       : "list all example functions"  = False,
    EGS      : "run all examples"     = False,
    LICENSE  : "show license"         = False,
    VERSION  : "show version"         = False,
  ):
  
  # ------------------------------------------
  class Span(lib.o):
    "`also` are the class values seen between `down` and `up`."
    def __init__(i,down=-math.inf, up=math.inf): 
      i.down, i.up, i.also = down, up, Sym()
    def __repr__(i):
      return f"[{i.down} .. {i.up})"
    def has(i,x):
      return x==i.down if i.down==i.up else i.down <= x < i.up
 
  # ------------------------------------------
  # ## Column Classes
  # Used to summarize individual columns.
  #
    # ### Col
  # Base object for all other columns. 
  # `add()`ing items increments the `n` counter.
  class Col(lib.o):
    def __init__(i, pos=0, txt="", all=[]):  
      i.pos, i.txt, i.n, i.w, i._bins = pos,txt,0,1,None
      i * all
    def __mul__(i, lst): [i + x for x in lst]; return i 
    def __add__(i, x) : 
      if x != NO:
        x = i._prep(x); i.n+= 1; i._add1(x)
        i._bins = None
      return x
    def _add1(i,x): return x
    def _prep(i,x): return x
    def bins(i, tab) : 
       i._bins = i._bins or i._bins1(tab)
       return i._bins
 
  # ---------------------------------------------------
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
    def _prep(i,x) : return float(x)
    def mid(i):    a=i.all(); return a[int(len(a)/2)]
    def norm(i,x): a=i.all(); return (x-a[0])/(a[-1] - a[0])
    def sd(i):     a=i.all(); return (a[int(.9*len(a))] - a[int(.1*len(a))])/2.56
    def _bins1(i,tab): return div(tab,i)
 
  # ---------------------------------------------------
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
    def _bins1(i,_): return  [Span(down=x,up=x) for x in i.all.keys()]
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
     
  # ---------------------------------------------------
  # ### Some
  # This `add` up to `max` items (and if full, sometimes replace old items).
  class Some(Col):
    def __init__(i, keep=KEEP, **kw): 
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

  #------------------------------------------------------------
  class Tab(lib.o):
    def __init__(i, all=[]):
       i.rows, i.cols = Some() , None
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
      return Tab() * ([i.cols.header] + rows) 
    def clusters(i): 
      gt   = lambda a,b: 0 if id(a)==id(b) else (-1 if a.better(b, i.cols) else 1)
      rows = i.rows.all
      rows = sorted(rows, key=functools.cmp_to_key(gt))
      return lib.chunks(rows, 2*len(rows)**SIZE)
    def ys(i): 
      return [col.mid() for col in i.cols.y]
  
  #------------------------------------------------------------
  # ## Discretization
  # Return `Span`s generated by Splitting columns from `n` rows into 
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
 
  #------------------------------------------------------------
  def counts(tab,goal):
    "Return frequency counts of ranges in different classes."
    def inc(d,k): d[k] = d.get(k,0) + 1
    def bin(x,bins):
      if x != NO:
        for b in bins:
          if b.has(x): return b
    out = lib.o(counts={},  hypotheses={}, totals={})
    for col in tab.cols.x:
      bins = col.bins(tab) if type(col)==Sym else merge(col.bins(tab),goal)
      for row in tab.rows.all:
        if b := bin(row.cells[col.pos], bins):
          k = row.tag == goal
          inc(out.hypotheses, k)
          inc(out.totals,     col.pos)
          inc(out.counts,     (k, col.txt, b.down, b.up))
    return out

  def learn(COUNTS):
    def loop(rules, here, there):
      lives = THE.lives
      while True:
        lives -= 1
        total, rules = prune(rules)
        if lives < 1 or len(rules) < 2:
          return rules
        rules += [combine(pick(rules, total),
                          pick(rules, total),
                          here, there)]
  
    def value(rule, here, there, e=2):
      b = like(rule, here, 2)
      r = like(rule, there, 2)
      return b**e / (b + r) if b > r else 0
  
    def like(rule, h, hs=None):
      hs = hs if hs else len(COUNTS.h)
      like = prior = (COUNTS.h[h] + THE.k) / (COUNTS.n + THE.k * hs)
      like = math.log(like)
      for col, values in rule:
        f = sum(COUNTS.f.get((h, col, v), 0) for v in values)
        inc = (f + THE.m * prior) / (COUNTS.h[h] + THE.m)
        like += math.log(inc)
      return math.e**like
  
    def combine(rule1, rule2, here, there):
      val1, rule1 = rule1
      val2, rule2 = rule2
      tmp = dict()
      for rule in [rule1, rule2]:
        for k, lst in rule:
          tmp[k] = tmp.get(k, set())
          for v in lst:
            tmp[k].add(v)
      rule3 = sorted([[k, sorted(list(vs))] for k, vs in tmp.items()])
      val3 = value(rule3, here, there)
      return [val3, rule3]
  
    def same(rule1, rule2):
      if rule1[0] != rule2[0]:
        return False
      for x, y in zip(rule1[1], rule2[1]):
        if x != y:
          return False
      return True
  
    def prune(old):
      ordered = [[s, r] for s, r in sorted(old, reverse=True)]
      one = ordered[0]
      unique = [one]
      for two in ordered[1:]:
        if not same(one, two):
          unique += [two]
        one = two
      pruned = [[s, r] for s, r in unique if s > 0][:THE.beam]
      return sum(s for s, _ in pruned), pruned
  
    def pick(rules, total):  # (s1, r1) (s2,r2) (s3,r3) total=s1+s2+s3
      n = r()
      for rule in rules:
        n -= rule[0] / total
        if n <= 0:
          return rule
      return rule
  
    def rule0(c, x, here, there):
      rule = [[c, [x]]]
      return [value(rule, here, there), rule]
  
    out, all = {}, list(set([(c, x) for (_, c, x) in COUNTS.f]))
    for there in COUNTS.h:
      for here in COUNTS.h:
        if here != there:
          rules = loop([rule0(c, x, here, there)
                        for c, x in all], here, there)
          out[here] = [[value(r, here, there, 1), r] for _, r in rules]
    return out
  

  #------------------------------------------------------------
  # ## Examples
  OK=lib.ok
  def eg_nothing(): 
    "Correctly installed"
    return 1

  def eg_testEngine(): 
    "we can catch pass/fail"
    OK(True,  "true-ing?")
    OK(False, "false-ing?")

  def eg_thunks87():
    "Divide a list into chunks"
    lst = [x for x in range(87)]
    lst = [len(a) for a in lib.chunks(lst, int(len(lst)**0.5))]
    OK(lst[ 0] == 9, "starts with nine?")
    OK(lst[-1] == 9, "ends with nine?")
    print(lst)

  def eg_chunks100():
    "Divide a list into chunks"
    lst = [x for x in range(100)]
    lst = [len(a) for a in lib.chunks(lst, 10)]
    OK(lst[ 0] == 10, "starts with ten?")
    OK(lst[-1] == 10, "ends with ten?")
    print(lst)

  def eg_num():
    "summarising numbers"
    n=Num(all=["10","5","?","20","10","5","?","20","10","5","?","20","10","5",
                "?","20","10","5","?","20","10","5","?","20"])
    OK(10.0 == n.mid(), "mid?")
    OK(5.85 < n.sd() < 5.86, "sd?")

  def eg_sym():
    "summariing numbers"
    s=Sym(all= ["10","5","?","20","10","5","?","20","10","5","?","20","10",
                "5","?","20","10","5","?","20", "10","5","?","20"])
    OK("10"==s.mid(),"mid working ?")
   
  def eg_some():
    "summarize very large sample space"
    n=10**5
    keep=32
    lst = sorted(Some(keep=keep,all= [x for x in range(n)]).all)
    OK(len(lst) ==32,"")
 
  def eg_csv():
     "Read a csv file."
     lst = lib.csv("../data/auto93.csv")
     OK(len(lst) == 399)
  
  
  def eg_tab():
    "make a table"
    t = Tab() * lib.csv("../data/auto93.csv")
    OK(398 == len(t.rows.all))
    one = t.cols.all[1]
    OK(151 == one.mid())

  def eg_clusters():
    "make a table"
    t = Tab() * lib.csv("../data/auto93.csv")
    all = [t.clone(rows).ys() for rows in t.clusters()]
    [print(one) for one in all]
    OK(all[0][ 0] < all[-1][0])
    OK(all[0][-1] > all[-1][1])

  def eg_divs():
    "make a table"
    t = Tab() * lib.csv("../data/auto93.csv")
    t.classify()
    for col in t.cols.x:
      if type(col) == Num: 
        print(len(div(t,col)))
 
  def eg_counts():
    t = Tab() * lib.csv("../data/auto93.csv")
    t.classify()
    c = counts(t, 0); [print(k,v) for k,v in c.counts.items()]
 
  ## --------------------------------
  EGS= {k:v for k,v in locals().items() if k[:3]=="eg_" and type(v)==fun} 
  for n,c in enumerate(ARGS):
    if c == "-data"    : DATA = ARGS[n+1]
    if c == "-dir "    : DIR  = ARGS[n+1]
    if c == "-license" : print(COPYLEFT)
    if c == "-version" : print(VER)
    if c == "-egs"     : lib.banner();  [lib.run(EGS[k]) for k in EGS]
    if c == "-eg"      : [lib.run(EGS[k]) for k in EGS if ARGS[n+1] in k]
    if c == "-ls"      : 
      print("\nEXAMPLES:"); 
      [print(lib.flair(RED=f"{k[3:]:>15}"),":",v.__doc__) 
       for k,v in EGS.items() if type(v)==fun] 
  if SRC: main()
  sys.exit(0 if lib.fails==1 else 1)

#############################################################################
class lib:
  fails = 0

  #--------------------------------------------------------------------------
  class o(object):
    "Easy inits, pretty print (keys sorted, skip those starting with '_')."
    def __init__(i, **d): i.__dict__.update(d)
    def __repr__(i): return "{"+ ', '.join([f":{k} {v}" 
      for k, v in sorted(i.__dict__.items()) 
      if type(v)!=fun and k[0] != "_"])+"}"
    def __eq__(i,j): return id(i) == id(j)

  #---------------------------------------------------------------------------
  def flair(**d):
    "flair(color=txt) return 'txt' wrapped in terminal color sequences"
    c=dict(
       PURPLE    = '\033[1;35;48m', CYAN   = '\033[1;36;48m',
       BOLD      = '\033[1;37;48m', BLUE   = '\033[1;34;48m',
       GREEN     = '\033[1;32;48m', YELLOW = '\033[1;33;48m',
       RED       = '\033[1;31;48m', BLACK  = '\033[1;30;48m',
       UNDERLINE = '\033[4;37;48m', END    = '\033[1;37;0m')
    for k,v in d.items(): return c["BOLD"] + c[k] + v + c["END"]
  
  #----------------------------------------------------------------------------
  def same(x): 
    "Standard meta trick"
    return x
  
  #----------------------------------------------------------------------------
  def chunks(a, n):
    "Yield chunks of size `n`. If any left over, add to middle chunk."
    out =[]
    n    = int(n)
    mid  = len(a)//2-n
    jump = n+n+len(a)%n
    j=None
    for i in range(0, mid, n): 
      j=i
      out += [a[i:i+n]]
    out += [a[j+n:j+jump]] 
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
    if x:             
      print(lib.flair(GREEN = "PASS"))
    else:
      print(lib.flair(RED = "FAIL"))
      lib.fails += 1
 
  def run(x):
    if type(x)==fun:
      random.seed(1)
      print(lib.flair(YELLOW=f"\n# {x.__name__}:"), x.__doc__)
      try:
        x()
      except Exception:
        print(traceback.format_exc())
        print(lib.flair(RED = "FUNCTION FAIL"))
        lib.fails ++ 1
        
 
  def banner():
    #os.system("clear" if os.name == "posix" else "cls")
    s= datetime.datetime.now().strftime("%H  :  %M  :  %S")
    print(lib.flair(CYAN=pyfiglet.figlet_format(s,font="mini"))[:-35],end="")
    return True

  def cli(f,doc=None):
   "Call `f`, first checking if any command line options override the defaults."
   arg = argparse
   doc = doc or __doc__ or ""
   def details(x,txt):
     isa, a = isinstance, None
     if isa(x, list):
       a, x = x, x[0]
     m, t = (("B", bool)  if x is False    else (
             ("I", int)   if isa(x, int)   else (
             ("F", float) if isa(x, float) else 
             ("S", str))))
     h = f"{txt}"
     h = (h+f"; default={x}") if x is not False else h
     h = (h+f"range= {a}")    if a else h
     return dict(help=h, default=x, metavar=m, type=t, choices=a) if a else ( 
            dict(help=h, action='store_true')            if x is False else (
            dict(help=h, default=x, metavar=m, type=t)))
   #----------------------------------------------------
   do = arg.ArgumentParser(prog            = f.__name__,
                           description     = doc.split("\n\n")[0],
                           formatter_class = arg.RawDescriptionHelpFormatter)
   for key, v in inspect.signature(f).parameters.items():
     if type(v.annotation)==str:
       do.add_argument("-"+key.lower(), 
                       dest=key,**details(v.default, v.annotation))
   return f(**vars(do.parse_args())) 

#-----------------------
if __name__ == "__main__": lib.cli(espy,__doc__)

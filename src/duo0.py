#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et :
# DUO = data miners used / used-by optimizers.
# (c) Tim Menzies, 2021 MIT License, https://opensource.org/licenses/MIT.
from random import seed as seed
from random import random as _r
import random,types
import re,math,random,types

def funp(x)    : return isinstance(x,types.FunctionType)
def method(i,f): return lambda *l, **kw: f(i, *l, **kw)

class o:
  def __init__(i, **d): i.__dict__.update(**d)
  def __repr__(i): return "{"+ ', '.join(
      [f":{k} {v}" for k, v in sorted(i.__dict__.items()) 
       if  not funp(v) and k[0] != "_"])+"}"
  def __add__(i, d): 
    for k in d: 
      if funp(d[k]): i.__dict__[k] = method(i,d[k])
    return i

THE = o(seed=1, skip="?", cohen=.2, id=0, betters=32,
        less="<",more=">",path="data",file="auto93.csv",
        Xchop=.5, best=.75, sep=",", ignore=r'([\n\t\r ]|#.*)')
seed(THE.seed)

def Counts(): 
  return o(f={}, h={}, n=0)

def Row(lst): 
  def ys(i,t): return [i.cells[c.pos] for c in t.cols.y]
  def better(i,j,t):
    s1,s2,n = 0,0,len(t.cols.y)
    for col in t.cols.y:
      pos,w = col.pos, col.w
      a,b   = i.cells[pos], j.cells[pos]
      a,b   = col.norm(a), col.norm(b)
      s1   -= math.e**(w*(a-b)/n)
      s2   -= math.e**(w*(b-a)/n)
    return s1/n < s2/n
  def betters(i,t):
    i.n = i.n or sum(i.better(random.choice(t.rows), t) 
                     for _ in range(THE.betters))/THE.betters
    return i.n
  return o(cells=lst, n=None, _tag=False) + locals()

def Tbl(): 
  def classify(i):
    i.rows = sorted(i.rows, key=lambda r: r.betters(i))
    for n,row in enumerate(i.rows):
      row.tag = n > len(i.rows)*THE.best 
  def adds(i,src):
    for lst in src:
      if i.cols.all: 
        i.rows += [Row( [c.add(x) for c,x in zip(i.cols.all, lst)] )]
      else: 
        i.cols.all = [ i.cols.add(pos,txt) for pos,txt in enumerate(lst) ]
    i.classify()
    return i
  return o(cols=Cols(), rows=[])+ locals()

def Cols(): 
  def add(i,pos,txt):
    if   THE.skip in txt                                       : f = Skip
    elif THE.less in txt or THE.more in txt or txt[0].isupper(): f = Num
    else                                                       : f = Sym
    now = f(pos=pos, txt=txt, w=-1 if THE.less in txt else 1)
    if   THE.skip in txt                                       : also = []
    elif THE.less in txt or THE.more in txt                    : also = i.y
    else                                                       : also = i.x
    also  += [now]
    return now
  return o(all=[], y=[], x=[]) + locals()

def Span(x, y):
  def has(i,x,y): return i.down <= x <i.up
  return o(down=x, up=y, _also=Sym()) + locals()

def Skip(pos=0, txt="", w=1):
  def add(i,x): 
    if x != THE.skip: i.n += 1; return x
  return o(pos=pos, txt=txt, w=w, n=0) + locals()

def Sym(pos=0, txt="", w=1):
  def ent(i): return -sum(v/i.n*math.log(v/i.n,2) for v in i.seen.values())
  def div(i, _): return [Span(x,x) for x in i.seen.keys()]
  def combined(i, j):
    if i.mode == j.mode:
      k = Sym(pos=i.pos, txt=i.txt, w=i.w)
      for x,n in {**i.seen, **j.seen}.items(): k.add(x,n)
      return k
  def add(i,x,n=1): 
    if x != THE.skip: 
      i.n += n
      now = i.seen[x] = i.seen.get(x, 0) + n
      if now > i.most: i.most, i.mode = now, x
    return x
  return o(pos=pos, txt=txt, w=w, n=0, seen={}, most=0, mode=None) + locals()

def Num(pos=0, txt="", w=1):
  def mid(i)   : n,a = i.all(); return a[int(n/2)]
  def var(i)   : n,a = i.all(); return (a[int(.9*n)] - a[int(n/10)]) / 2.56
  def norm(i,x): _,a = i.all(); return (x - a[0]) / (a[-1] - a[0])
  def all(i)   : 
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return len(i._all), i._all
  def add(i, x): 
    if x != THE.skip:
      i._all += [x]; i.n+= 1; i.ok = False
    return x
  #--------------------------------------------------------------
  def div(i,t): 
    xy = sorted([(r.cells[pos], r.tag) for r in t.rows 
                if r.cells[pos] != THE.skip])
    width = len(xy)**THE.Xchop
    while width < 4 and width < len(xy) / 2: width *= 1.2
    now = Span(xy[0][0], xy[0][0])
    tmp = [now]
    for j,(x,y) in enumerate(xy):
      if j < len(xy) - width:
        if now._also.n >= width:
          if x != xy[j+1][0] and now.up - now.down > i.var()*THE.cohen:
            now  = Span(now.up, x)
            tmp += [now]
      now.up = x
      now._also.add(y)
    out = i.merge(tmp)
    out[ 0].down = -math.inf
    out[-1].up   =  math.inf
    return out
  #--------------------------------------------------------------
  def merge(i, b4):
    j, tmp, n = 0, [], len(b4)
    while j < n:
      a = b4[j]
      if j < n - 1:
        b  = b4[j+1]
        if now := a._also.combined(b._also):
          a = Span(a.down, b.up)
          a._also = now
          j += 1
      tmp += [a]
      j   += 1
    return i.merge(tmp) if len(tmp) < len(b4) else b4
  #--------------------------------------------------------------
  return o(pos=pos, txt=txt, w=w, _all=[], ok=True, n=0) + locals()

def counts(t):
  i = o(n=0, h={}, k={}, spans={})
  i.spans = {id(spn):spn for c in t.cols.all for spn in c.div(t)}}

  for row in t.rows: 
    k    = row.tag
    i.n += 1
    i.h  = i.h.get(k,0) + 1
    
    h[r.tag] = h.get(r.tag,0) + 1
    n += 1
  for col in t.cols.x:
    spans = col.divs(t)
    for row in t.rows:
      x = row.cells[col.pos]
      if x != THE.skip:
        for span in spans: 
          if span.has(x): break
        v = (row.tag, col.pos, id(span))
        out.f[v] = out.f.get(v, 0) + 1
  return o(n=n, h=h, k=k)

def csv(file):
  def atom(x):
    try: return int(x)
    except Exception:
      try: return float(x)
      except Exception: return x
  with open(file) as fp:
    for a in fp: 
      yield [atom(x) for x in re.sub(THE.ignore, '', a).split(THE.sep)]

t=Tbl().adds(csv(THE.path + "/" + THE.file))
#print(t.cols.y)
#print(t.cols.y)
for row in t.rows[:5]: print(row.ys(t),row.tag,row.n)
print("")
for row in t.rows[-5:]: print(row.ys(t),row.tag,row.n)
for col in t.cols.x: 
  print(f"\n {col.txt}", col.pos)
  print(col.div(t))

  #for z in sorted(row.ys(t) for row in lst[:5]): print(z)
#print("")
#for z in sorted(row.ys(t) for row in lst[-5:]): print(z)




#i!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81:
"""
Recursive k=2 division of data. Centroids picked via
random projection.

- License: (c) 2021 Tim Menzies <timm@ieee.org>, MIT License  

"""
import re
from it import it
from csv import csv

def anExample():
  rows=[row for row in csv("../data/auto93.csv")]
  assert 399== len(rows)
  assert float is type(rows[1][4])
  assert int   is type(rows[1][0])
    
def Row(t,lst):
  def dist(i,j):
    for c in i._tab.cols[i._tab.using]:
       a,b = i.cells[c.pos], i.cells[c.pos]
       a,b = c.norm(a), c.norm(b)
       d  += (a-b)**i._tab.p
       n  += 1
    return (d/n)**(1/i._tab.p)
  return it(_tab=t,cells=lst,x=None,y=None) + locals()

def add(i,x): 
  if x != SKIP: 
    i.n += 1; i.add(x)
  return x

def Skip(pos=0, txt="", w=1):
  def add(i,x): return x
  return it(pos=pos, txt=txt, w=w, n=0)  + locals()
  
def Sym(pos=0, txt="", w=1):
  def add(i,x,n=1):
    now = i.seen[x] = i.seen.get(x, 0) + n
    if now > i.most: i.most, i.mode = now, x
    return x
  return it(pos=pos, txt=txt, w=w, n=0, seen={}, most=0, mode=None) + locals()
  
def Num(pos=0, txt="", w=1):
  def add(i, x): i._all += [x]
  def mid(i)   : n,a = _all(i); return a[int(n/2)]
  def var(i)   : n,a = _all(i); return (a[int(.9*n)] - a[int(n/10)]) / 2.56
  def norm(i,x): _,a = _all(i); return (x - a[0]) / (a[-1] - a[0])
  def _all(i)   :
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return len(i._all), i._all
  return it(pos=pos, txt=txt, w=w, n=0, _all=[]) + locals()

def Cols(): 
  def add(i,pos,txt)
    weight = -1 if "-" in txt else 1
    where  = ([]   if "?" in txt else (i.y if txt[-1] in "+-"  else i.x))
    what   = (Skip in "?" in txt else (Num if txt[0].isupper() else Sym))
    now    = what(pos,txt,weight)
    where += [now]
    return now
  return it(all=[],x=[],y=[]) + locals()

def Tab(src,using="y",p=2):
  def _row(i,lst):  return Row(i, [col.add(x) for col,x in zip(i.cols.all,lst)])
  def _cols(i,lst): return [i.cols.add(pos,xt) for pos,txt in enumerate(list)]
  def adds(i,src): [add(i,row) for row in src]
  def add(i,lst):
    if i.cols.all: 
      i.rows += [_row(i,lst)]
    else:
      i.cols.all  = _cols(i,lst)
      i.header=lst
  def projects(i):
    c = -1
    for one in i.rows:
      for two in i.rows:
        if id(one) > id(two):
          tmp = one.dist(two)
          if tmp > c:
            left, right, c = one, two, tmp
    xs, ys = {}, {}
    for row in rows():
      a,b = row.dist(left), row.dist(right)
      x   = math.max(0, math,min(1,(a**2 + c**2 - b**2)/(2*i.c)))
      y   = (x**2 - a**2)**.5
      i   = id(row)
      xs[i], ys[i] = x, y
    return xs,ys
  def split(i):
    xs,ys = projects(i)
    return _split(i.rows, [], len(i.rows**0.5), *projects(i))
  def split(rows, out, lo,xs,ys):
    mid  = int(len(rows)/2)
    rows.sorted(key=lambda z: xs[id(z)]); xcut = xs[ rows[mid ]]
    xlo, xmid, xhi = xs[rows[0]],  xs[rows[mid]], xs[rows[-1]]
    rows.sorted(key=lambda z: ys[id(z)]); ycut = ys[ rows[mid ]]
    ylo, ymid, yhi = ys[rows[0]],  ys[rows[mid]], ys[rows[-1]]
    ne, nw, se, sw = o(x=it(lo=[],hi=[][], [], [], []
    for row in rows:
      x,y   = xs[id(row)], ys[id(row)]
      lo,hi = (se,ne) if x<xmid else (sw,nw)
      one   = lo      if y<ymid else hi


    west,east = rows[:mid],rows[mid:]
    sw,se,nw,ne=[],[]
    west.sort(key=lambda z:ys[id(z)])

    out.x.mid          = xs[id(rows[mid])]
    
    out.x.lo, out.x.hi = xs[id(rows[0])], xs[id(rows[-1])]
    rows.sorted(key=lambda z: ys[id(z)])
    out.y.mid          = ys[id(rows[mid])]
    out.y.lo, out.y.hi = xs[id(rows[0])], xs[id(rows[-1])]
    nw,ne,sw,se = [],[],[],[]

    if len(i.rows) < lo or lvl < 0: return i
    poles = Poles(i)
    lefts, rights = poles.lefts, poles.rights
    i.rows = sorted(i.rows, key=lambda row: i.poles.project(row))
  return it(rows=[], using=using, p=p, header=[], cols=Cols())  + locals()

def fastmap(src):
  with open(file) as fp:
    for a in fp:
      yield [atom(x) for x in re.sub(ignore, '', a).split(sep)]

def atom(x):
  "Coerce x to the right kind of string (int, float, or string)"
  try: return int(x)
  except Exception:
    try:              return float(x)
    except Exception: return x

__name__ == "__main__" and anExample()

#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81:
"""
Recursive k=2 division of data. Centroids picked via
random projection.

- License: (c) 2021 Tim Menzies <timm@ieee.org>, MIT License  

"""
import re, math, random
from it import it
from csv import csv

def anExample():
  random.seed(1)
  t= Tab(fast=False)
  for row in csv("../data/auto93.csv"): 
     t.add(row)
  assert 398== len(t.rows)
  #print(t.rows[1].cells)
  assert int is type(t.rows[1].cells[4])
  #print(t.cols.all[1].norm(360))
  a=t.rows[1]
  c=t.rows[-1]
  #print(a.dist(c))
  b,_=a.furthest(t.rows)
  #print(a.uses())
  #print(b.uses())
  for n,rows in enumerate(leaves(t.cluster())):
    for row in rows:
      print(f"{row.x}\t{row.y}\t{n}")
      #print(f"set label '{mark}' at {row.x},{row.y}")

def Row(t,lst):
  def uses(i): return [i.cells[col.pos] for col in  i._tab.uses()]
  def dist(i,j):
    d,n = 0,0
    for c in i._tab.uses():
       a,b = i.cells[c.pos], j.cells[c.pos]
       a,b = c.norm(a), c.norm(b)
       d  += (a-b)**i._tab.p
       n  += 1
    return (d/n)**(1/i._tab.p)
  def furthest(i,rows):
    hi = -1
    for j in rows:
      tmp = i.dist(j)
      if tmp > hi: hi,out = tmp, j
    return out,hi
  return it(_tab=t,cells=lst,x=None,y=None) + locals()

def plus(i,x): 
  if x != "?": 
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
  def add(i, x): i._all += [x]; i.ok=False
  def mid(i)   : n,a = _all(i); return a[int(n/2)]
  def var(i)   : n,a = _all(i); return (a[int(.9*n)] - a[int(n/10)]) / 2.56
  def norm(i,x): _,a = _all(i); return (x - a[0]) / (a[-1] - a[0])
  def _all(i)   :
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return len(i._all), i._all
  return it(pos=pos, txt=txt, w=w, n=0, ok=False, _all=[]) + locals()

def Cols(): 
  def add(i,pos,txt):
    weight = -1 if "-" in txt else 1
    where  = ([]   if "?" in txt else (i.y if txt[-1] in "+-"  else i.x))
    what   = (Skip if "?" in txt else (Num if txt[0].isupper() else Sym))
    now    = what(pos,txt,weight)
    where += [now]
    i.all += [now]
  return it(all=[],x=[],y=[]) + locals()

def Tab(using="y",p=2, fast=False):
  def uses(i): return i.cols[i.using]
  def makeRow(i,a) : return Row(i,[plus(col,x) for col,x in zip(i.cols.all,a)])
  def makeCols(i,a): [i.cols.add(pos,txt) for pos,txt in enumerate(a)]
  def adds(i,src)  : [add(i,row) for row in src]; return i
  def cluster(i)   : 
    return tree(i.rows, fast)
  def add(i,a)   :
    if i.cols.all: 
      assert len(a) == len(i.cols.all), "wrong number of cells"
      i.rows += [i.makeRow(a)]
    else:
      a = a if type(a) == list else a.cells
      i.makeCols(a)
      i.header=a
  return it(header=[], rows=[], cols=Cols(),using=using,p=2,fast=fast) + locals()

def tree(rows0, fast):
  def find2FarPoints(rows):
    if fast:
      anyone   = random.choice(rows)
      north,_  = anyone.furthest(rows)
      south, c = north.furthest(rows)
    else:
      c=-1
      for m,one in enumerate(rows):
        for n,two in enumerate(rows):
          if n > m:
            tmp = one.dist(two)
            if tmp > c:
              north, south, c = one, two, tmp
    return north, south, c

  def map2twoDims(rows, lvl):
    north,south,c = find2FarPoints(rows)
    tmp = []
    for row in rows:
      a,b = row.dist(north), row.dist(south)
      x = max(0, min(1, (a**2 + c**2 - b**2)/(2*c)))
      y = (a**2 - x**2)**.5
      if lvl==0: row.x,row.y = x,y
      tmp += [(x, row)]
    mid         = len(tmp) // 2
    rows        = [z[-1] for z in sorted(tmp,key=lambda z:z[0])]
    north,south = rows[:mid], rows[mid:]
    xs          = sorted(tmp, key=lambda z:z[1].x)
    ys          = sorted(tmp, key=lambda z:z[1].y)
    return north, south, it(
        _rows=rows, north=north, south=south, c=c, up=None, down=None,
        x0= xs[0][0], xmid= xs[mid][0], x1= xs[-1][0],
        y0= xs[0][1], ymid= xs[mid][1], y1= xs[-1][1])

  def div(rows, lo,  lvl):
    if len(rows) > lo:
      down0, up0, here = map2twoDims(rows,  lvl)
      here.down        = div(down0, lo, lvl+1)
      here.up          = div(up0,   lo, lvl+1)
      return here
  ###################################
  return div(rows0, len(rows0)**.5, 0)

def show(here, lvl=0):
  if here:
     print(("|.. "*lvl) + f"{len(here._rows)}")
     show(here.up,   lvl+1)
     show(here.down, lvl+1)

def leaves(tree):
  if tree.up:
    for x in leaves(tree.up)  : yield x
    for x in leaves(tree.down): yield x
  else:
    yield tree._rows

def fastmap(src):
  with open(file) as fp:
    for a in fp:
      yield [atom(x) for x in re.sub(ignore, '', a).split(sep)]

__name__ == "__main__" and anExample()

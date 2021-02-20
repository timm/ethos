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
  t= Tab()
  for row in csv("../data/auto93.csv"): 
     print(row); t.add(row)
  assert 398== len(t.rows)
  print(t.rows[1])
  #assert float is type(t.rows[1].cells[4])
  #assert int   is type(t.rows[1].cells[0])
  print(len(t.rows))
    
def Row(t,lst):
  def dist(i,j):
    for c in i._tab.cols[i._tab.using]:
       a,b = i.cells[c.pos], i.cells[c.pos]
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
  def add(i,pos,txt):
    weight = -1 if "-" in txt else 1
    where  = ([]   if "?" in txt else (i.y if txt[-1] in "+-"  else i.x))
    what   = (Skip if "?" in txt else (Num if txt[0].isupper() else Sym))
    now    = what(pos,txt,weight)
    where += [now]
    return now
  return it(all=[],x=[],y=[]) + locals()

def Tab(using="y",p=2, fast=False):
  def _row(i,lst)  : return Row(i, [add(col,x) for col,x in zip(i.cols.all,lst)])
  def _cols(i,lst) : return [i.cols.add(pos,txt) for pos,txt in enumerate(lst)]
  def cluster(i)   : return cluster(i.rows, fast)
  def adds(i,src)  : [add(i,row) for row in src]; return i
  def add(i,lst)   :
    if i.cols.all: 
      i.rows += [_row(i,lst)]
    else:
      i.cols.all  = _cols(i,lst)
      i.header=lst
  return it(header=[], rows=[], cols=Cols()) + locals()

def cluster(rows0, fast):
  def find2FarPoints(rows):
    if fast:
      anyone   = random.choice(rows)
      north,_  = anyone.furthest(rows)
      south, c = north.furthest(rows)
    else:
      c=-1
      for m,one in enumerate(rows):
        for n,two in enumerate(rows):
          if n > m and (tmp := one.dist(two)) > c:
            north, south, c = one, two, tmp
    return north, south, c

  def projects(rows, lvl):
    north,south,c = find2FarPoints(rows)
    tmp = []
    for row in rows:
      a,b = row.dist(north), row.dist(south)
      x = math.max(0, math,min(1, (a**2 + c**2 - b**2)/(2*c)))
      y = (x**2 - a**2)**.5
      if lvl==0: row.x,row.y = x,y
      tmp += [(x, row.x, row.y, row)]
    mid         = len(tmp) // 2.
    rows        = [z[-1] for z in sorted(tmp)]
    north,south = rows[:mid], rows[mid:]
    xs,ys       = sorted(tmp, lambda z:z[1]), sorted(tmp, lambda z:z[2])
    return north, south, it(
        _rows=rows, north=north, south=south, c=c, up=None, down=None,
        x0= xs[0][0], xmid= xs[mid][0], x1= xs[-1][0],
        y0= xs[0][1], ymid= xs[mid][1], y1= xs[-1][1])

  def tree(rows, lo,  lvl):
    if len(rows) > lo*2:
      down0, up0, here = projects(rows,  lvl)
      here.down        = tree(down0, lo, lvl+1)
      here.up          = tree(up0,   lo, lvl+1)
      return here
  ###################################
  return tree(rows0, len(rows)**.5, 0)

def show(here, lvl=0):
  if here:
     print(("|.. "*lvl) + f"{len(here.rows)}")
     show(here.up,   lvl+1)
     show(here.down, lvl+1)

def fastmap(src):
  with open(file) as fp:
    for a in fp:
      yield [atom(x) for x in re.sub(ignore, '', a).split(sep)]

__name__ == "__main__" and anExample()

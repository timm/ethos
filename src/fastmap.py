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
    i.poles=Poles(i)
    i.rows = sorted(i.rows, key=lambda row: i.poles.project(row))
    i.poles.cut 
  return it(rows=[], using=using, p=p, header=[], cols=Cols(), poles=None)  + locals()

def Poles(tab):
  def _poles(i,rows):
    c=-1
    for one in rows:
      for two in rows:
        if id(one) > id(two):
          tmp = one.dist(two)
          if tmp > c:
            left,right,c = one,two,tmp
    rows = sorted(rows, key=lambda row: i.project(row))
    mid = rows[ int(len(rows)/2)] 
    return left,right,c, i.id[mid]
  def _project(row, left,right,c):
     a= row.dist(left)
     b= row.dist(right)
     return  math.max(0, math.min(1, (a**2 + c**2 - b**2)/(2*c)))
  def project(i,row)
    if not i.left: i.left,i.right,i.c,i.cut = _poles(i)
    if not i.x[id(row)]:  i.x[id(row)] = _project(row, *i.poles())
    return i.x[id(row)]
  return it(c=0,tab=tab,left=None,right=None,x={}) + locals()

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

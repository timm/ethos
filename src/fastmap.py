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
from functools import cmp_to_key
import matplotlib.pyplot as plt

def eg1():
  random.seed(1)
  t= Tab(fast=False)
  for row in csv("../data/auto93.csv"): t.add(row)
  rows = t.ordered()
  for row in rows[:5 ]: print(row.uses())
  print("")
  for row in rows[-5:]: print(row.uses())

def eg2():
  random.seed(1)
  t= Tab(fast=False)
  for row in csv("../data/auto93.csv"): t.add(row)
  rows = t.ordered()
  for n,row in enumerate(t.ordered()):
    row.gt = n/len(t.rows)
  show(t.cluster(),t)

def anExample():
  random.seed(1)
  t= Tab(fast=True)
  for row in csv("../data/auto93.csv"): 
     t.add(row)
  assert 398== len(t.rows)
  t1 = t.clone(t.rows)
  #print(len(t1.rows))
  assert 398== len(t1.rows)
  #print(t.ymid())
  assert int is type(t.rows[1].cells[4])
  a=t.rows[1]
  c=t.rows[-1]
  b,_=a.furthest(t.rows)
  for n,row in enumerate(t.ordered()):
     row.gt = n/len(t.rows)
  for n,rows in enumerate(leaves(t.cluster())):
    avg = sum(row.gt for row in rows)/len(rows)
    for row in rows:
       print(f"{row.x}\t{row.y}\t{avg}")

def Row(t,lst):
  def uses(i): return [i.cells[col.pos] for col in  i._tab.uses()]
  def better(i,j):
      s1,s2,n = 0,0,len(t.cols.y)
      for col in t.cols.y:
        pos,w = col.pos, col.w
        a,b   = i.cells[pos], j.cells[pos]
        a,b   = col.norm(a), col.norm(b)
        s1   -= math.e**(w*(a-b)/n)
        s2   -= math.e**(w*(b-a)/n)
      return s1/n < s2/n
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
  return it(_tab=t,cells=lst,x=None,y=None,gt=0) + locals()

def plus(i,x): 
  if x != "?": 
    i.n += 1; i.add(x)
  return x

def Skip(pos=0, txt="", w=1):
  def add(i,x): return x
  return it(pos=pos, txt=txt, w=w, n=0)  + locals()
  
def Sym(pos=0, txt="", w=1):
  def mid(i): return i.mode
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
  def adds(i,src)   : return [add(i,row) for row in src]; return i
  def cluster(i)    : return tree(i.rows, fast)
  def makeCols(i,a) : return [i.cols.add(pos,txt) for pos,txt in enumerate(a)]
  def makeRow(i,a)  : return Row(i,[plus(col,x) for col,x in zip(i.cols.all,a)])
  def mid(i)        : return [col.mid() for col in i.cols.all]
  def ordered(i)    : return sorted(i.rows, key=cmp_to_key(ordered1))
  def ordered1(a,b) : return (0 if id(a)==id(b) else (1 if a.better(b) else -1))
  def uses(i)       : return i.cols[i.using]
  def ymid(i)       : return [col.mid() for col in i.cols.y]

  def clone(i,inits=[]):
    j = Tab(using=i.using, p=i.p, fast=i.fast)
    j.add( i.header )
    [j.add(row) for row in inits]
    return j

  def add(i,a)   :
    if i.cols.all: 
      a = a if type(a) == list else a.cells
      assert len(a) == len(i.cols.all), "wrong number of cells"
      i.rows += [i.makeRow(a)]
    else:
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
    if len(rows) > lo*2:
      down0, up0, here = map2twoDims(rows,  lvl)
      here.down        = div(down0, lo, lvl+1)
      here.up          = div(up0,   lo, lvl+1)
      return here
  ###################################
  return div(rows0, len(rows0)**.5, 0)

def stats(t,rows):
  header= [Num(pos=col.pos, txt=col.txt) for col in t.cols.y]
  for row in rows:
    [col.add(row.cells[col.pos]) for col in header]
  heads= '  '.join([f"{col.txt:>5}"   
  for col in header])
  mids = '  '.join([f"{col.mid():5}" for col in header])
  return heads,mids

def show(here,t, lvl=0,all=None, id=0):
  if here:
    heads, mids= stats(t,here._rows)
  if not all:
    all = len(here._rows)
    print("\n    %n %wins "+heads+"\n")
  if here:
     if not here.up and not here.down:
       avg = int(100*sum(row.gt for row in here._rows)/len(here._rows))
       n   = int(100*len(here._rows)/all)
       c   = ("abcdefghijklmnopqrstuvwxyz"\
             +"ABCDEFGHIJKLMNOPQRSTUVWXYZ")[id]
       id += 1
       print(f"{c:2} {n:3}   {avg:3} "+mids) #"|.. "*lvl) 
     id = show(here.up,  t, lvl+1, all, id) 
     id = show(here.down,t, lvl+1, all, id) 
  return id

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

#__name__ == "__main__" and anExample()
#__name__ == "__main__" and anExample()
__name__ == "__main__" and eg2()


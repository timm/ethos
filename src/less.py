#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
from types import FunctionType as fu
from random import random as r
from random import choice
import random,sys,re

def fun(x): return type(x) == types.FunctionType

class o:
  def __init__(i, **d)   : i.__dict__.update(d)
  def __getitem__(i,k)   : return i.__dict__[k]
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __or__(i,j): 
    for k in j.__dict__: i[k] = j[k]
    return i
  def __repr__(i): return "{"+ ', '.join([f":{k} {v}" 
    for k, v in sorted(i.__dict__.items()) if type(v)!=fu and k[0] != "_"])+"}"
  def __add__(i,d):
    def method(i,f): return lambda *lst, **kw: f(i, *lst, **kw)
    for k,v in d.items():
      if type(v)==fu: i.__dict__[k] = method(i,v)
    return i

the=o(no="?", maxnum=128)

def same(x): return x

def column( pos=0,txt=""): 
  what = (Col if the.no in txt else (Num if txt[0].isupper() else Sym))
  return what(pos=pos, txt=txt) 

def Col(pos=0, txt=""): 
  new = o(pos=pos, txt=txt, n=0, w= (-1 if "-" in txt else 1))
  def add(i,x) : 
    if x != the.no: i.n+=1
    return x
  return new + locals()

def Num(pos=0, txt=""): 
  new = Col(pos,txt) | o(_all=[], max=1028, ok=False) 
  def add(i,x) : 
    if x != the.no:
      i.n += 1
      x = float(x)
      i._all += [x]
      i.ok=False
    return x
  def all(i):
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return i._all
  def mid(i):    a=i.all(); return a[int(len(a)/2)]
  def norm(i,x): a=i.all(); return (x-a[0])/(a[-1] - a[0])
  def sd(i):     a=i.all(); return (a[int(.9*len(a))] - a[int(.1*len(a))])/2.56
  return new + locals()

def Sym(pos=0, txt=""): 
  new = (Col(pos,txt) | o(_all={}, mode=None, max=0)) 
  def add(i,x):
    if x != the.no:
      i.n += 1
      tmp = i._all[x] = i._all.get(x,0) + 1
      if tmp>i.max: i.max,i.mode = tmp,x
    return x
  def mid(i): return i.mode
  return new + locals()

def Some(pos=0, txt="",max=256): 
  new = o(n=0, _all=[], max=max)
  def add(i,x) : 
     i.n += 1
     if len(i._all) < i.max: i._all += [x]
     elif r() < i.n / i.max: i._all[ int(r()*len(i._all)) ] = x
  return new + locals()

def Cols(lst):
  new = o(header=lst, x=[], y=[], all=[])
  for pos,txt in enumerate(lst):
    one = column(pos,txt)
    new.all.append(one)
    if the.no not in txt: 
      (new.y if txt[-1] in "+-" else new.x).append(one)
  return new

def dist(r1,r2,cols):
  def norms(col, x): x=col.norm(x); return x,(1 if x<0 else 0)
  d,n = 0,1E-32
  for col in cols.y:
    a,b  = r1[col.pos], r2[col.pos]
    a,b  = col.norm(a), col.norm(b)
    d   += (a-b)**2
    n   += 1
  return (d/n)**.5

def rmeans(rows0,about,want=.8):
  def far(r1, rows):
    most = -1
    for r2 in rows:
      tmp = dist(r1,r2,about)
      if tmp>most: most,out = tmp,r2
    return out
  def poles(rows):
    one = far(random.choice(rows), rows)
    two = far(one,rows)
    ones, twos = [], []
    for row in rows:
      (twos if dist(row,two,about) < dist(row,one,about) else ones).append(row)
    return o(_rows=rows,up=None,down=None,one=one,ones=ones,two=two,twos=twos) 
  def worker(rows, lo, lvl=0):
    if len(rows) > lo and lvl<10:
      here      = poles(rows)
      here.down = worker(here.twos, lo, lvl+1)
      here.up   = worker(here.ones, lo, lvl+1)
      return here
  #-------------------------------------
  return worker(rows0, len(rows0)**0.5)

def leaves(tree,lvl=0):
  if tree and tree.up:
    for x in leaves(tree.up,   lvl+1): yield x
    for x in leaves(tree.down, lvl+1): yield x
  else:
    yield lvl,tree._rows

def data(src, cols=None):
  cols = cols or Cols(next(src))
  for row in src:
    row = [col.add(x) for col,x in zip(cols.all,row)]
    yield cols,row

def rows(src):
  for line in src:
    yield re.sub(r'([\n\t\r ]|#.*)','',line).split(",")

def csv(file):
  with open(file) as fp:
    for lst in fp: yield lst

random.seed(1)
lst=[]
for about,row in data(rows(csv("../data/auto93.csv"))):
   lst+=[row]
print(about.all[0].all())
#for lvl,lst1 in leaves(rmeans(lst,about)): print("|.. "*lvl, len(lst1))


#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
import types
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
    for k, v in sorted(i.__dict__.items()) if not fun(v) and k[0] != "_"])+"}"
  def __add__(i,d):
    def method(i,f): return lambda *lst, **kw: f(i, *lst, **kw)
    for k,v in d.items():
      if fun(v): i.__dict__[k] = method(i,v)
    return i

the=o(no="?", maxnum=128)

def same(x): return x

def column( pos=0,txt=""): 
  what = (Col if the.no in txt else (Num if txt[0].isupper() else Sym))
  return what(pos=pos, txt=txt) 

def Col(pos=0, txt=""): 
  def add(i,x) : 
    if x != the.no: i.n+=1
    return x
  return o(pos=pos, txt=txt, n=0, w= (-1 if "-" in txt else 1))  + locals()

def Num(pos=0, txt=""): 
  def add(i,x) : 
    if x != the.no:
      i.n += 1
      x = float(x)
      if len(i._all) < i.max: 
        i.ok=False; i._all += [x]
      elif r() < i.n / i.max: 
        i.ok=False; i._all[ int(r()*len(i._all)) ] = x
    return x
  def all(i):
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return i._all
  def mid(i): a=i.all(); return a[int(len(a)/2)]
  return (Col(pos,txt) | o(_all=[], max=64, ok=False)) + locals()

def Sym(pos=0, txt=""): 
  def add(i,x):
    if x != the.no:
      i.n += 1
      tmp, i._all[x] = i._all.get(x,0) + 1
      if tmp>i.max: i.max,i.mode = tmp,x
    return x
  def mid(i): return i.mode
  return (Col(pos,txt) | o(_all={}, mode=None, max=0)) + locals()

def sd(i,x): 
  a=i.all(); return (a[int(.9*len(a))] - a[int(.1*len(a))])/2.56

def About(lst):
  i = o(header=lst, x=[], y=[], all=[])
  for pos,txt in enumerate(lst):
    one = column(pos,txt)
    i.all.append(one)
    if the.no not in txt: 
      (i.y if txt[0] in "+-" else i.x).append(one)
  return i

def data(src, about=None):
  about = about or About(next(src))
  for row in rows(src):
    yield about, [col.add(col,x) for col,x in zip(about.all,row)]

def rows(src):
  for line in src:
    yield re.sub(r'([\n\t\r ]|#.*)','',line).split(",")

def csv(file):
   with open(file) as fp:
     for lst in fp: yield lst

for _,row in data(rows(csv("../data/auto93.csv"))): 
  print(row)

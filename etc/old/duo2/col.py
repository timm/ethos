#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
"""
col.py : summarize streams of data     
(c) 2021, Tim Menzies, MIT license.      
https://choosealicense.com/licenses/mit/  
  
USAGE ./col.py [OPTIONS]  
  
 -t S  run demo functions matching S  
 -T    run all demo functions  
 -L    list all demo functions  
 -h    run help  
 -C    show copyright  
"""

from lib import cli,on
from ok  import ok
from random import random as r

def column( pos=0,txt=""): 
  "Factory for generating different kinds of column."
  what = (Col if "?" in txt else (Num if txt[0].isupper() else Sym))
  return what(pos=pos, txt=txt) 

def Col(pos=0, txt=""): 
  """Base object for all other columns. `add()`ing items
  increments the `n` counter."""
  new = on(pos=pos, txt=txt, n=0, w=1)
  def add(i,x) : 
    if x != "?": 
      x = i.prep(x); i.n+= 1; i.add1(x)
    return x
  def add1(i,x):  return x
  def prep(i,x):  return x
  return new.has(locals())

def Num(pos=0, txt=""): 
  """Here, `add` accumulates numbers into `_all`.
  `all()` returns that list, sorted. Can report
  `sd()` (standard deviation) and `mid()` (median point).
   Also knows how to `norm()` normalize numbers.""" 
  new = Col(pos,txt) + on(_all=[], ok=False,
            w= -1 if "-" in txt else 1)
  def add1(i,x) : 
    i._all += [x]
    i.ok=False
  def all(i):
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return i._all
  def mid(i):    a=i.all(); return a[int(len(a)/2)]
  def norm(i,x): a=i.all(); return (x-a[0])/(a[-1] - a[0])
  def prep(i,x): return float(x)
  def sd(i):     a=i.all(); return (a[int(.9*len(a))] - a[int(.1*len(a))])/2.56
  return new.has(locals())

def Sym(pos=0, txt=""): 
  "Here, `add` tracks symbol counts, including `mode`."
  new = Col(pos,txt) + on(_all={}, mode=None, max=0) 
  def add1(i,x):
    tmp = i._all[x] = i._all.get(x,0) + 1
    if tmp>i.max: i.max,i.mode = tmp,x
    return x
  def mid(i): return i.mode
  return new.has(locals())

def Some(pos=0, txt="", keep=256): 
  "This `add` up to `max` items (and if full, sometimes replace old items)."
  new = Col(pos,txt) + on(_all=[], keep=keep)
  def add1(i,x) : 
    if len(i._all) < i.keep: i._all += [x]
    elif r() < i.keep / i.n: i._all[ int(r()*len(i._all)) ] = x
  return new.has(locals())

#----------------------------------------------------------------
def test_num():
  "summarising numbers"
  n=Num()
  for x in ["10","5","?","20","10","5","?","20","10","5",
             "?","20","10","5","?","20","10","5","?","20",
             "10","5","?","20"]:
    n.add(x)
  print(n.mid(), n.sd())

def test_sym():
  "summariing numbers"
  s=Sym()
  for x in ["10","5","?","20","10","5","?","20","10","5",
             "?","20","10","5","?","20","10","5","?","20",
             "10","5","?","20"]:
    s.add(x)
  ok("10"==s.mid(),"mid working ?")

def test_some():
  "summarize very large sample space"
  import random
  random.seed(1)
  n=Some(max=32)
  [n.add(x) for x in range(10**6)]
  print(sorted(n._all))

if __name__ == "__main__": cli(locals(),__doc__)

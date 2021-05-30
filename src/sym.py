# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, tim menzies (timm@ieee.org) unlicense.org
"""Summarize numeric columns."""

from col import Col
import math

class Sym(Col):
  def __init__(i,**kw): 
    i.seen, i.mode, i.most = {}, None, 0
    super().__init__(**kw)

  def norm1(i,x)  : x
  def dist1(i,x,y): return 0 if x==y else 1
  def add1(i,x,n=1)   :
    tmp = i.seen[x] = i.seen.get(x,0) + n
    if tmp > i.most:
       i.most, i.mode = tmp,x

  def mid(i)   : return i.mode
  def spread(i): return i.entropy()

  def entropy(i):
    log2= lambda z: math.log(z)/math.log(2)
    return sum(-n/i.n*log2(n/i.n) for n in i.seen.values())

  def merged(i, j):
    k = Sym(at=i.at, txt=i.txt)
    for seen in [i.seen, j.seen]:
      for x, n in seen.items(): k.add(x, n)
    e1, n1 = i.entropy(), i.n
    e2, n2 = j.entropy(), j.n
    e, n   = k.entropy(), k.n
    if e1 + e2 < 0.01 or e * .95 < n1 / n * e1 + n2 / n * e2:
      return k

  def discretize(i, j, _):
    for k in (i.seen | j.seen):  
      yield True,  (k, k), i.seen.get(k,0)
      yield False, (k, k), j.seen.get(k,0)




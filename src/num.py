# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, tim menzies (timm@ieee.org) unlicense.org
"""Summarize numeric columns."""

from col import Col
import math
from bin import div,merge

class Num(Col):
  def __init__(i,**kw):
    i.mu = i.m2 = i.sd = 0
    i._all, i.lo, i.hi = [], 1E32, -1E32
    super().__init__(**kw)

  def mid(i): return i.mu
  def spread(i): return i.sd

  def norm1(i,x) : 
    return max(0, min(1, (x - i.lo)/(i.hi - i.lo + 1E-32)))

  def dist1(i,x,y):
    if   x=="?" : y   = i.norm1(y); x= 0 if y>.5 else 1
    elif y=="?" : x   = i.norm1(x); y= 0 if x>.5 else 1
    else        : x,y = i.norm1(x), i.norm1(y)
    return abs(x-y)

  def add1(i, x, n=1):
    i._all += [x]
    d = x - i.mu
    i.mu += d / i.n
    i.m2 += d * (x - i.mu)
    i.sd = 0 if i.n<2 else (0 if i.m2<0 else (i.m2 / (i.n-1))**0.5)
    i.lo = min(x, i.lo)
    i.hi = max(x, i.hi)

  def discretize(i, j, the):
    xy = [(better, True)  for better in i._all] + [
          (bad,    False) for bad    in j._all]
    sd = (i.sd*i.n + j.sd*j.n)/(i.n+j.n)
    tmp = div(xy, sd * the.cohen, len(xy)**the.tiny)
    for bin in merge(tmp):
      for klass, n in bin.also.seen.items():
        if not (bin.down == -math.inf and bin.up == math.inf):
          yield klass, (bin.down, bin.up), n

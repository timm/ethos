# vim: filetype=python ts=2 sw=2 sts=2 et :
from col import Col

class Num(Col):
  def __init__(i,**kw):
    i.mu = i.m2 = i.sd = 0
    i.lo, i.hi = 1E32, -1E32
    super().__init__(**kw)

  def norm1(i,x) : 
    return max(0, min(1, (x - i.lo)/(i.hi - i.lo + 1E-32)))

  def dist1(i,x,y):
    if   x=="?" : y   = i.norm1(y); x= 0 if y>.5 else 1
    elif y=="?" : x   = i.norm1(x); y= 0 if x>.5 else 1
    else        : x,y = i.norm1(x), i.norm1(y)
    return abs(x-y)

  def add1(i, x, n=1):
    d = x - i.mu
    i.mu += d / i.n
    i.m2 += d * (x - i.mu)
    i.sd = 0 if i.n<2 else (0 if i.m2<0 else (i.m2 / (i.n-1))**0.5)
    i.lo = min(x, i.lo)
    i.hi = max(x, i.hi)

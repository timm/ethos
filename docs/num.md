```py
from col import Col
import sys

class Num(Col):
  def __init__(i, *l, **d):
    super().__init__(*l, **d)
    i.mu  = i.m2 = i.sd = 0
    i.lo  = sys.maxsize - 1
    i.hi  = -1*i.lo
  def add1(i,x):
    x     = float(x)
    i.lo  = min(i.lo, x)
    i.hi  = max(i.hi, x)
    d     = x - i.mu
    i.mu += d/i.n
    i.m2 += d*(x - i.mu)
    if i.n > 1:
      i.sd = (i.m2 / (i.n - 1))**0.5
    return x
  def norm1(i,x):
    return (x - i.lo) / (i.hi - i.lo + 0.000001)
  def dist1(i, x,y):
    if x is Col.no: 
       y = i.norm(y); x = 0 if y>0.5 else 1
    elif y is Col.no: 
       x = i.norm(x); y = 0 if x>0.5 else 1
    else:
       x,y = i.norm(x), i.norm(y)
    return abs(x - y)
```

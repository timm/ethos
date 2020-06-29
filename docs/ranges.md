```py
from lib import Thing,o,dprint
from num import Num
from sym import Sym
import sys

class LoHi(Thing):
  id=0
  def __init__(i, want, min):
    i.want  = want
    i.best  = i.rest = 0.00001
    i.min   = min
    i.lo    = sys.maxsize - 1
    i.hi    = -i.lo
    i.n     = 0
    i.tag   = LoHi.id = LoHi.id + 1
    
  def add(i,x,y):
    i.lo    = min(x, i.lo)
    i.hi    = max(x, i.hi)
    i.n    += 1
    i.best += (y == i.want)
    i.rest += (y != i.want)
    return i

  def merge(i,j):
     k      = LoHi(i.want, i.min)
     k.lo   = min(i.lo, j.lo)
     k.hi   = max(i.hi, j.hi)
     k.n    = i.n    + j.n
     k.best = i.best + j.best
     k.rest = i.rest + j.rest
     return k
 
  def score(i, bs, rs):
     b = i.best  / bs
     r = i.rest  / rs
     return b**2 / (b+r)

class Ranges:
  bins = [16,8,4,2]
  min  = 4
  def __init__(i, xy, goal = True,debug=False):
    xy.sort(key = lambda z:z[0])
    i.min  = i.whatSize(xy)
    i.bs, i.rs = 0.0001, 0.0001
    i.all = i.grow(goal, xy)
    i.debug = False

  def whatSize(i,a):
    lo = 0
    least = Ranges.min if len(a) < 256 else len(a)**0.5
    for j in Ranges.bins:
      lo = int( len(a)/j )
      if lo >= least:  
        return lo
    return max(least,lo)

  def grow(i, goal, xy):
    out = [ LoHi(goal, i.min) ]
    for j,(x,y) in enumerate(xy):
      i.bs += (y == goal)
      i.rs += (y != goal)
      out[-1].add(x,y)
      if out[-1].n >= i.min: 
        if j < len(xy) - i.min:
          if x != xy[j+1][0]:
            out += [ LoHi(goal, i.min) ]
    return out

  def v(i,z): return z.score(i.bs, i.rs)

  def ranges(i):
    i.merge() 
    for z in i.all: 
      yield z.lo, z.hi, i.v(z)

  def merge(i,lvl=1):
    j, tmp, pre = 0, [], "|-- " * lvl
    if i.debug:
      print(pre +  "::",len(i.all))
    while j < len(i.all):
      a = i.all[j]
      if j< len(i.all) - 1:
        b = i.all[j+1]
        c = a.merge(b)
        if i.v(c) >= i.v(a) and i.v(c) >= i.v(b):
          tmp  += [c]
          j    += 2
          continue
      tmp  += [a]
      j    += 1
    if len(tmp) < len(i.all):
      i.all = tmp
      if i.debug:
        [ print(pre + "now", x) for x in i.all ]
      i.merge(lvl+1)
```

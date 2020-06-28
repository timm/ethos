```py
from lib import Thing,o,dprint
from num import Num
from sym import Sym
import sys

class LoHi(Thing):
  def __init__(i, want, min):
    i.want  = want
    i.best  = i.rest = 0.00001
    i.min   = min
    i._left  = None
    i._right = None
    i.lo    = sys.maxsize - 1
    i.hi    = -i.lo
    i.n     = 0

  def __repr__(i):
    left  = i._left or o(tag=0) 
    right = i._right or o(tag=0) 
    return dprint(dict(
      tag=i.tag, want= i.want, best= i.best, rest = i.rest,
      min = i.min,  left= left.tag, right= right.tag,
      lo  = i.lo,   hi  = i.hi,        n    = i.n))

  def filled(i,x,y):
    i.lo    = min(x, i.lo)
    i.hi    = max(x, i.hi)
    i.n    += 1
    i.best += (y == i.want)
    i.rest += (y != i.want)
    return i.n >= i.min

  def maybe(i,j,bs,rs) :
    b  = (i.best + j.best) / bs
    r  = (i.rest + j.rest) / rs
    s  = b**2/(b+r)
    s1 = i.score(bs,rs)
    s2 = j.score(bs,rs)
    better1 = s - s1
    better2 = s - s2
    return (better1 < 0.02 or better2 < 0.02)

  def merge(one,two, bs,rs):
     one.hi    = two.hi
     one.best += two.best
     one.rest += two.rest
     one.n    += two.n
     if two._right: 
       one._right = two._right
       two._right._left = one
     two._left = two._right = None
     return one
 
  def score(i, bs, rs):
     b       = i.best / bs
     r       = i.rest / rs
     i.scr   =  b**2 / (b+r)
     return i.scr

class Ranges:
  bins = 10
  min  =  20
  def __init__(i,pairs,goal = True):
    pairs.sort(key = lambda z:z[0])
    i.min      = i.whatSize(pairs)
    print("min",i.min)
    i.head     = LoHi(goal,i.min)
    i.bs= i.rs = 0
    i.grow(i.head, goal, pairs)

  def prune(i):
    b4  = i.size()
    now = 0
    loop=0
    while now < b4:
      loop += 1
      b4 = i.size()
      i.pruned(b4, i.head )
      now = i.size()
    for z in i.items():
      yield z.n,z.lo, z.hi, z.score(i.bs, i.bs)

  def items(i):
    z = i.head
    while z:
      yield z
      z = z._right
   
  def size(i): 
    n,x = 0, i.head
    while x: n, x = n+1, x._right
    return n 

  def whatSize(i,a):
    j, lo = Ranges.bins, 0
    while j >= 2:
      lo = int( len(a)/j )
      if lo >= len(a)**0.5: return lo
      j /= 2
    return lo

  def grow(i, lohi, goal, pairs):
    n, bs, rs = 1, 0.0001, 0.0001
    lohi.tag = n
    for j,(x,y) in enumerate(pairs):
      i.bs += (y == goal)
      i.rs += (y != goal)
      if lohi.filled( x,y ):
        if j < len(pairs)-1-i.min:
          x1 = pairs[j+1][0]
          if x != x1:
            n += 1
            tmp         = LoHi(goal, i.min)
            tmp.tag     = n
            lohi._right = tmp
            tmp._left   = lohi
            lohi        = tmp
    lohi._right = None
    return n

  def pruned(i,n, one):
    if n > 0 and one and one._right:
      if one.maybe(one._right, i.bs, i.rs):
         one.merge(one._right, i.bs, i.rs)
         i.pruned( n-1, one )
      else:
         i.pruned( n-1, one._right )
```

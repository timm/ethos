
# Why: decision list generator to explain best vs rest
Some other process has divided some sub-sample of `data`
into two tables, `best` and `rest`.  


```py
from lib  import Thing
from col  import Col
from div  import Div
from sym  import Sym
from best import Best,Tab
```
## Class Why

```py
class Why(Thing):
  min = 4
  def __init__(i, t): i.tree= i.div(t)
```
Build a tree
```py

  def div(t): 
    if len(t.rows) <= Why.min:
      return o(t=t, yes=None, no=None)
    else
      return i.recurse(t, *i.split(t, Best(t)))

  def split(i, t, br)
    most, pos, lo, hi = 0, None, None, None
    for col in t.cols.x:
      if ins(Col.nums,col.txt): f=lambda: i.nums(t,col,br)
      else                    : f=lambda: i.syms(t,col,br)
      for pos1, lo1, hi1, s in f():
        if s > most:
          pos, lo, hi, most = pos1, lo1, hi1, s
    return pos, lo, hi

  def recurse(i,all,t, pos, lo, hi)
    yes, no = all.clone(), all.clone()
    for row in all.rows:
      x = row.cells[pos]
      if x != Col.no:
        (yes if lo <= x and x<= hi else no).append(row)
    return o(t = t, col=pos, lo=lo, hi=hi
             yes = yes,
             no  = i.div(ll, no))
```
Split on symbolics
```py
  def syms(i, t, col, br):
    bs = len(br.best.rows) + 0.001
    rs = len(br.rest.rows) + 0.001
    for k,b in br.best[col.pos].seen.items():
      if b > 0:
        r  = br.rest[col.pos].seen.get(k,0)
        b  = b/bs
        r  = r/rs
        if b>r:
          yield col.pos,k,k,b**2/(b+r)
```
Split on numerics
```py

   def nums(i, t, col, br):
    f = lambda row: row.cells[col.pos]
    a = [(f(r),1) for r in br.best.rows if f(r) != Col.no]
    b = [(f(r),0) for r in br.rest.rows if f(r) != Col.no]
    for lo, hi, s in ranges(a+b):
      yield col.pos, lo, hi, s
```

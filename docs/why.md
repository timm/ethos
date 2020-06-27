# Why: decision list generator to explain best vs rest
```py
from div import Div
from sym import Sym
from best import Best,Tab

class Why(Pretty):
  def __init__(i, div):
    i.best = None
    i.rest = None
    super().__init__(*l, **d)

  def scoreSym(i,col):
    best = Sym()
    rest = Sym()
    [best.add( row.cells[col.pos] ) for row in i.best.rows]
    [rest.add( row.cells[col.pos] ) for row in i.rest.rows]
    bs = len(i.best.rows) + 0.001
    rs = len(i.rest.rows) + 0.001
    for k,b in best.seen.items():
      r = rest.seen.get(k,0)
      b = b/bs
      r = r/rs
      if b>r:
        yield col.pos,k, b**2/(b+r)
      
  def scoreNum(i,col,lo,hi):
    best = Sym()
    rest = Sym()
    [best.add( row.cells[col.pos] ) for row in i.best.rows]
    [rest.add( row.cells[col.pos] ) for row in i.rest.rows]
    bs = len(i.best.rows) + 0.001
    rs = len(i.rest.rows) + 0.001
    for k,b in best.seen.items():
      r = rest.seen.get(k,0)
      b = b/bs
      r = r/rs
      if b>r:
        yield col.pos,k, b**2/(b+r)
       
```

```py
from div import Div
from random import random as ra
from tab import Tab

class Best(Div):
  ratio = 3
  def __init__(i, t, cols=None):
    n1     = len(t.rows)
    n2     = n1**Div.min
    i.max  = Best.ratio * 4*n2 / (n1-n2)
    i.best = t.clone()
    i.rest = t.clone()
    super().__init__(t, cols=cols)


  def div(i,t,cols,rows, lvl=0):
    if Div.debug : 
      print('%s%s' % ("|.. " * lvl,len(rows)))
    if len(rows) <  i.min: 
      i.best = t.clone(rows=rows)
    else:
      z      = i.lohi(cols,  rows)
      z.tab  = Tab(rows=rows)
      i.rest = i.rest or t.clone()
      [i.rest.row(r) for r in z.kids[z.rest] if ra() < i.max]
      i.div(t,cols,           z.kids[z.best], lvl+1)
```

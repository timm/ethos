# Row

```py
from lib import Pretty
import math

class Row(Pretty):
  p=2
  def __init__(i, cells=[], tab=None):
    i.cells = cells
    i.dom = 0
    i.tab=None
    i.p = 2
```
## dom(row1, row2, cols=None): bool
Distance is calculated using `cols` which defaults to `i.tab.cols.x`.

```py
  def dist(i,j, cols=None):
    d, n, p = 0, 0.001, Row.p
    for c in  cols or i.tab.cols.x:
      x   = i.cells[c.pos]
      y   = y.cells[c.pos]
      inc = c.dist(x, y)
      d  += inc**p
      n  += 1
    return (d/n)**1/p
```
## dom(row1, row2): bool

```py
  def dom(i,j):
    s1,s2,e,n = 0,0, math.e, len(i.tab.cols.y)+0.0001
    for c in i.tab.cols.y:
      x   = i.cells[c.pos]
      y   = j.cells[c.pos]
      x   = c.norm(x)
      y   = c.norm(y)
      s1 -= e**(c.w*(x-y)/n)
      s2 -= e**(c.w*(y-x)/n)
    return s1/n < s2/n
```


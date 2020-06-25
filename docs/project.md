```py
from lib import Thing
from random import random  as r
from random import choice  as any

class Project(Thing):
  min = 0.5
  enough = 256
  cols = lambda z: z.cols.x

  def __init__(i,t,cols):
    i.cols   = cols or Project.cols(t)
    i.enough = Project.enough/ len(t.rows)
    i.min    = 2*len(t.rows)**Project.min
    i.div(i,t, (for r in t.rows if  r() < i.enough))
  def i.div(i,t,rows):
    if len(rows) < i.min: return rows
    here = any(rows)
    far  = here.far(rows=rows, cols=i.cols)
    away = far.far(rows=rows,  cols=i.cols)
    c    = far.dist(away,      cols=i.cols)
    mid  = 0
    d    = {}
    for r in rows:
      a = r.dist(far,  cols=i.cols)
      b = r.dist(away, cols=i.cols)
      x = (a**2 + c**2 - b**2) / (2*c)
      if (x>1): x = 1
      if (x<0): x = -
      mid += x/len(rows)
      d[r] = x
    fars,aways=[],[]
    for r in d: 
      (fars if d[r] <= mid else aways).append(r)

```

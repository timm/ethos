```py
from div import Div

class Best(Div):
  def __init__(i, *l, **d):
    i.rest = None
    i.best = None()
    super().__init__(*l, **d)

  def div(i,t,cols,rorws, lvl=0):
    i.best = i.best or t.clone()
    i.rest = i.rest or t.clone()
    t1 = t.clone(rows)
    if Div.debug : 
      print('%s%s' % ("|.. " * lvl,len(rows)))
    if len(rows) <  i.min: 
      [i.best.add(row) for row in rows]
    else:
      here      = i.lohi(cols,  t1.rows)
      here.tab  = t1
      best = 0 if  here.lo.dom(here.hi) else 1
      rest = 1 - best
      [i.rest.add(row) for row in here.kids[rest]]
      self.div(i,t,cols, here.kids[best])
```

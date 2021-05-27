# vim: filetype=python ts=2 sw=2 sts=2 et :
import random
from lib import rs

class Clusters:
  def __init__(i,t,the,cols=None,loud=False):
    i.all=[]
    i.div(t.rows,0, t,the,loud, 
          cols or t.cols.x, 
          len(t.rows)**the.tiny // 1)
  
  def div(i,rows,lvl,  t,the,loud,cols,tiny):
    if loud:
      print(f"{'|.. ' * lvl}{len(rows)}")
    if len(rows) < 2*tiny:
      i.all += [t.clone(rows)]
    else:
      any = random.choice(rows)
      left  = t.far(any,  the, cols=cols, rows=rows)
      right = t.far(left, the, cols=cols, rows=rows)
      c  = left.dist(right,the, cols=cols)
      for row in rows:
        a = row.dist(left,  the, cols=cols)
        b = row.dist(right, the, cols=cols)
        x = (a**2 + c**2 - b**2)/(2**c)
        row.divx = max(0, min(1, x))
      rows = sorted(rows, key=lambda row: row.divx)
      mid  = len(rows) // 2  
      i.div(rows[:mid],lvl+1, t,the,loud,cols,tiny)
      i.div(rows[mid:],lvl+1, t,the,loud,cols,tiny)
  

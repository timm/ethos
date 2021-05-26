# vim: filetype=python ts=2 sw=2 sts=2 et :
import random
from lib import rs

class Clusters:
  def __init__(i,t,the,cols=None,silent=True):
    i.all=[]
    i.div(t.rows,0, t,the,silent, 
          cols or t.cols.x, 
          len(t.rows)**the.enough // 1)
  
  def div(i,rows,lvl,t,the,silent,cols,enough):
    if not silent:
      print(f"{'|.. ' * lvl}{len(rows)}")
    if len(rows) < 2*enough:
      i.all += [t]
    else:
      any = random.choice(rows)
      left = t.far(any,the,rows=rows)
      right = t.far(left,the,rows=rows)
      c  = left.dist(right,cols,the)
      for row in rows:
        a= row.dist(left,  cols, the)
        b= row.dist(right, cols, the)
        x= (a**2 + c**2 - b**2)/(2**c)
        row.divx = max(0, min(1, x))
      rows=sorted(rows, key=lambda row: row.divx)
      #print(rs([row.divx for row in rows][::10],3))
      mid = len(rows) // 2  
      tleft=t.clone()
      tright=t.clone()
      [tleft.add(row) for row in rows[:mid]]
      [tright.add(row) for row in rows[mid:]]
      i.div(tleft.rows, lvl+1,tleft, the,silent,cols,enough)
      i.div(tright.rows,lvl+1,tright,the,silent,cols,enough)
  

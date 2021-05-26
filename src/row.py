# vim: filetype=python ts=2 sw=2 sts=2 et :
from lib import obj
import math

class Row(obj):
  def __init__(i,tab,cells): i.cells,i._tab = cells,tab

  def dist(i,j,cols,the):
    d,n = 0, 1E-31
    for col in cols:
      tmp = col.dist( i.cells[col.at], j.cells[col.at] )
      d  += tmp**the.p
      n  += 1
    return (d/n)**(1/the.p)

  def __lt__(i, j):
    s1, s2, n = 0, 0, len(i._tab.cols.y)
    for col in i._tab.cols.y:
      a   = col.norm(i.cells[col.at])
      b   = col.norm(j.cells[col.at])
      s1 -= math.e**(col.w * (a - b) / n)
      s2 -= math.e**(col.w * (b - a) / n)
    return s1 / n < s2 / n

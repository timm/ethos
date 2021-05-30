# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, Tim Menzies (timm@ieee.org) unlicense.org
"""Standard protocols for summarizing data columns."""

from lib import obj
from ako import weight

class Col(obj):
  def __init__(i,at=0,txt="",all=[]):
    i.at, i.txt, i.n = at,txt,0
    i.w = weight(txt) # -1 if we are minimizing, 1 otherwise
    i.adds(all)
  def adds(i, lst)  : 
    "Add multiple items"
    [i.add(x) for x in lst]

  def add(i, x, n=1):
    "Add one item. Ignore things we are skipping."
    if x != "?": 
      i.n += n
      i.add1(x,n)  
    return x

  def norm(i, x)  : 
    "Distance calcs: only normalize things we are not skipping"
    return x if x == "?" else i.norm1(x)
  def dist(i, x,y):
    "Distance calcs: assume  to missing values are at max distance. Else, be more detailed."
    if x == "?" and y=="?": return 1
    return i.dist1(x,y)


# vim: filetype=python ts=2 sw=2 sts=2 et :
from lib import obj
from ako import weight

class Col(obj):
  def __init__(i,at=0,txt="",all=[]):
    i.at, i.txt, i.n = at,txt,0
    i.w = weight(txt)
    i.adds(all)

  def adds(i, lst)  : [i.add(x) for x in lst]
  def norm(i, x)    : return x if x == "?" else i.norm1(x)
  def add(i, x, n=1):
    if x != "?": 
      i.n += n; i.add1(x,n)
    return x

  def dist(i, x,y):
    if x == "?" and y=="?": return 1
    return i.dist1(x,y)


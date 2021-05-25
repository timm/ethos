# vim: filetype=python ts=2 sw=2 sts=2 et :
from col import Col
import math

class Sym(Col):
  def __init__(i,**kw): 
    i.seen, i.mode, i.most = {}, None, 0
    super().__init__(**kw)

  def norm1(i,x)  : x
  def dist1(i,x,y): return 0 if x==y else 1
  def add1(i,x,n=1)   :
    tmp = i.seen[x] = i.seen.get(x,0) + n
    if tmp > i.most:
       i.most, i.mode = tmp,x

  def mid(i)   : return i.mu
  def spread(i): return i.entropy()

  def entropy(i):
    return sum(-n/i.n*log(n/i.n) for n in i.seen.values())

log = lambda z: math.log(z)/math.log(2)

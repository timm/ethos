# vim: filetype=python ts=2 sw=2 sts=2 et :
from col import Col

class Skip(Col):
  def __init__(i,**kw): super().__init__(**kw)
  def add1(i,x,n=1)      : return x


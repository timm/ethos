# vim: filetype=python ts=2 sw=2 sts=2 et :
from tab import Tab
from about import defaults
from clusters import Clusters
import random

def go(f="data/weather.csv",silent=True):
  the=defaults.clone()
  t=Tab(file=f)
  for n,here in enumerate(t.rows):
    tmp=t.around(here,the)
    me= tmp[0][1]
    close  = tmp[1][1]
    far = t.far(here,the)
    further= tmp[-1][1]
    if not silent:
      print("")
      print(n,here.cells)
      print(n,me.cells)
      print(n,far.cells)
      print(n,further.cells)
    assert tmp[0][0] <= tmp[1][0] < tmp[-1][0]

def diveg(f="data/weather.csv",silent=True):
  random.seed(1)
  the=defaults.clone()
  t=Tab(file=f)
  Clusters(t,the,silent=False)

go()
#go("data/auto93.csv")

diveg("data/auto93.csv")

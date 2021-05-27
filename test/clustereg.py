# vim: filetype=python ts=2 sw=2 sts=2 et :
from tab import Tab
import about
from clusters import Clusters
from lib import rs
import random

def diveg(f="data/weather.csv",loud=False):
  the=about.defaults()
  t=Tab(file=f)
  c=Clusters(t,the,cols=t.cols.x, loud=True)
  print([col.txt for col in t.cols.x])
  all = sorted(c.all)
  for x in all:
    print(rs(x.y()))
  for span in sorted(all[0].bins(all[-1],the)): 
    print(span)
  print(random.random(),the)

diveg("data/auto93.csv")

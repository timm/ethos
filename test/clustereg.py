# vim: filetype=python ts=2 sw=2 sts=2 et :
from tab import Tab
import about,clusters
from lib import rs
import random

def diveg(f="data/weather.csv",loud=False):
  the=about.defaults()
  t=Tab(file=f)
  if len(t.rows) > 2000: the.tiny=0.66
  all= sorted(clusters.div(t,the,cols=t.cols.x, loud=True))
  print([col.txt for col in t.cols.y])
  print(rs(t.y(),3), "<== baseline") 
  for x in all:
    print(rs(x.y(), 3))
  for span in sorted(all[0].bins(all[-1],the)): 
    print(span)
  print(round(random.random(),3),the)

#diveg("data/auto93.csv")
diveg("data/pom_dataset.csv")


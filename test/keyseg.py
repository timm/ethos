# vim: filetype=python ts=2 sw=2 sts=2 et :
from keys import keys
from tab  import Tab
import about

def diveg():
  the=about.defaults()
  t=Tab(file=the.data)
  print(the.data)
  for _ in  range(10):
    print("")
    keys(t,the)

#go()
#go("data/auto93.csv")
#diveg("data/auto93.csv")
#diveg("data/pom_dataset.csv")
#diveg("data/xomo_dataset.csv")

diveg()

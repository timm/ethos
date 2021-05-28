# vim: filetype=python ts=2 sw=2 sts=2 et :
from keys import keys
from tab  import Tab
import about

def diveg(f="data/weather.csv"):
  the=about.defaults()
  t=Tab(file=f)
  k=keys(t,the)

#go()
#go("data/auto93.csv")
diveg("data/auto93.csv")
#diveg("data/pom_dataset.csv")
#diveg("data/xomo_dataset.csv")


# vim: filetype=python ts=2 sw=2 sts=2 et :
from keys import Keys
from tab  import Tab
import about

def diveg(f="data/weather.csv"):
  the=about.defaults()
  t=Tab(file=f)
  k=Keys(t,the)

#go()
#go("data/auto93.csv")

diveg("data/auto93.csv")

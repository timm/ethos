# vim: filetype=python ts=2 sw=2 sts=2 et :
from tab import Tab
from about import defaults

def go():
  the=defaults.clone()
  t=Tab(file="data/weather.csv")
  for n,r in enumerate(t.rows):
    tmp=t.around(r,the)
    print("")
    print(n,r.cells)
    print(n,tmp[0][1].cells)
    print(n,tmp[-1][1].cells)

go()

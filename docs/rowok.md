
```py
from lib import ok
from tab import Tab
from row import Row

def tab0(f="data/weather4.csv"):
  t=Tab(f)
  for row in t.rows:
    a= row.around()
    print("")
    print(row.cells, len(a))
    print( a[ 2][2].cells, a[2 ][0] )
    print( a[-1][2].cells, a[-1][0] )

@ok
def tab1(): tab0()

@ok
def tab2(): tab0("data/auto93.csv")
```

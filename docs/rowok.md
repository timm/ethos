
```py
from lib import ok
from tab import Tab
from row import Row

@ok
def tab1():
  t=Tab("data/weather4.csv")
  for row in t.rows:
    a= row.around()
    print("l", len(a))
    print("")
    print(row.cells)
    print( a[2][2].cells, a[2][0] )
    print( a[-1][2].cells, a[-1][0] )
```

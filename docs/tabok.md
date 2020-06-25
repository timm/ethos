
```py
from lib import ok
from tab import Tab

@ok
def tab1():
  t=Tab("data/weather4.csv")
  for row in t.rows:
    print(row)
```

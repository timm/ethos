```py
from lib import ok
from div import Div
from tab import Tab

@ok
def _div1():
  t = Tab(file = "data/auto93.csv")
  Div.debug = True
  Div.cols = "x"
  Div(t)
```

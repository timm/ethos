
```py
from lib  import ok,excursion
from div  import Div
from best import Best,Tab

@ok
def _div1():
  t = Tab(file = "data/auto93.csv")
  with excursion(Div):
    Div.debug = True
    Div.cols = "y"
    b= Best(t)
    print(b.best.summary(), len(b.best.rows))
    print(b.rest.summary(), len(b.rest.rows))
```

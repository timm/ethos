```py
from rx  import ranks
from lib import ok
from random import random as r

@ok
def _rx():
  n = 1000
  ranks(dict(rx1=[r()      for _ in range(n)],
             rx2=[r()**2   for _ in range(n)],
             rx3=[r()**0.5 for _ in range(n)]))

```

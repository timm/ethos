```py
from lib import ok,within
from num import Num

@ok
def num1():
  n=Num()
  n.all([11,21,10,42,53])
  assert within(19.243, n.sd, 19.244)
  print(n)
```

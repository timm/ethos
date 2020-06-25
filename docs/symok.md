```py
from lib import ok,within
from sym import Sym

@ok
def num1():
  s=Sym()
  s.all("abbcccc")
  assert s.seen["c"] == 4
  print(s)
```

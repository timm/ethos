```py
from cocomo import Cocomo,w,u

c   = lambda: Cocomo(kloc=w(2,100), acap=6, ltex=5,
                     sced=6)
lst = [c().effort() for _ in range(1000)]
lst = sorted(lst)
q   = lambda n: '%.0f' % lst[ int(n * len(lst)) ]
#print(*[q(n) for n in [0.1, 0.3, 0.5, 0.7, 0.9]])


for _ in range(100):
  print(c().risk( ))
```

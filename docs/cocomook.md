```py
from cocomo import Cocomo,w
from cocrisk import risk

lst=[Cocomo(
            kloc = w(2,100), ltex = w(6),
            sced = w(6),     acap = w(6),
            pmat = w(6)
           ).effort() 
    for _ in range(10000)]
lst = sorted(lst)
q   = lambda n: '%.0f' % lst[int(n* len(lst))]

print(q(.1), q(.3), q(.5), q(.7), q(.9))


print(risk(Cocomo()))
```

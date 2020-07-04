```py
from lib import Thing,o
from copy import deepcopy as kopy
from x import F,I
from cocrisk import rules

class Cocomo(Thing):
  __name__ = "Cocomo"
  defaults = o(
      misc= o( kloc = F(2,1000), 
               a    = F(2.2,9.8),
               goal = F(0.1, 2)),
      pos = o( rely = I(1,5),  data = I(2,5), cplx = I(1,6),
               ruse = I(2,6),  docu = I(1,5), time = I(3,6),
               stor = I(3,6),  pvol = I(2,5)),
      neg = o( acap = I(1,5),  pcap = I(1,5), pcon = I(1,5),
               aexp = I(1,5),  plex = I(1,5), ltex = I(1,5),
               tool = I(1,5),  site = I(1,6), sced = I(1,5)),
      sf  = o( prec = I(1,6),  flex = I(1,6), arch = I(1,6), 
               team = I(1,6),  pmat = I(1,6)))
 
  def __init__(i,listofdicts=[]):
    i.x, i.y, dd = o(), o(), kopy(Cocomo.defaults)
    # set up the defaults
    for d in dd:  
      for k in dd[d] : i.x[k]  = dd[d][k] # can't +=: no background info 
    # apply any other constraints 
    for dict1 in listofdicts:  
      for k in dict1 : 
         try: i.x[k] += dict1[k] # now you can +=
         except Exception as e:
              print(k, e)
    # ----------------------------------------------------------
    for k in dd.misc:i.y[k]= i.x[k]()
    for k in dd.pos: i.y[k]= F( .073,  .21)()   * (i.x[k]() -3) +1
    for k in dd.neg: i.y[k]= F(-.178, -.078)()  * (i.x[k]() -3) +1
    for k in dd.sf : i.y[k]= F(-1.56, -1.014)() * (i.x[k]() -6)
    # ----------------------------------------------------------

  def effort(i):
    em, sf = 1, 0
    b      = (0.85-1.1)/(9.18-2.2) * i.x.a() + 1.1+(1.1-0.8)*.5 
    for k in Cocomo.defaults.sf  : sf += i.y[k]
    for k in Cocomo.defaults.pos : em *= i.y[k]
    for k in Cocomo.defaults.neg : em *= i.y[k]
    return round(i.x.a() * em * (i.x.kloc()) ** (b + 0.01*sf), 1)
 
  def risk(i, r=0):
    for k1,rules1 in rules.items():
      for k2,m in rules1.items():
        x  = i.x[k1]()
        y  = i.x[k2]()
        z  = m[x-1][y-1]
        r += z
    return round(100 * r / 104, 1)
```

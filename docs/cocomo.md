```py
from lib import Thing,o
import random
from cocrisk import rules

def u(lo, hi=None):  return random.uniform(lo, hi or lo)
def w(lo, hi=None):  return random.randint(lo, hi or lo)

class Cocomo(Thing):
  def __init__(i,**my):
    i.x, i.y, dd = o(), o(), i.defaults()
    # ----------------------------------------------------------
    for j in dd:
      for k in dd[j]: i.x[k] = dd[j][k] 
    for k in my:      i.x[k] = my[k]
    # ----------------------------------------------------------
    for k in dd.misc: i.y[k]= i.x[k]
    for k in dd.pos:  i.y[k]= u(  .073,  .21) *(i.x[k] - 3) +1
    for k in dd.neg:  i.y[k]= u( -.178, -.078)*(i.x[k] - 3) +1
    for k in dd.sf :  i.y[k]= u(-1.56, -1.014)*(i.x[k] - 6)
    # ----------------------------------------------------------
    i.b = (0.85-1.1) / (9.18-2.2) * i.x.a  + 1.1+ (1.1-0.8)*.5 

  def defaults(i):
    return o(
      misc= o( kloc = u(2,1000), a  = u(2.2,9.8)),
      pos = o( rely = w(1,5),  data = w(2,5), cplx = w(1,6),
               ruse = w(2,6),  docu = w(1,5), time = w(3,6),
               stor = w(3,6),  pvol = w(2,5)),
      neg = o( acap = w(1,5),  pcap = w(1,5), pcon = w(1,5),
               aexp = w(1,5),  plex = w(1,5), ltex = w(1,5),
               tool = w(1,5),  site = w(1,6), sced = w(1,5)),
      sf  = o( prec = w(1,6),  flex = w(1,6), arch = w(1,6), 
               team = w(1,6),  pmat = w(1,6)))
 
  def effort(i):
    em,sf = 1,0
    for k in i.defaults().sf  : sf += i.y[k]
    for k in i.defaults().pos : em *= i.y[k]
    for k in i.defaults().neg : em *= i.y[k]
    return i.x.a * em * i.x.kloc ** (i.b + 0.01 * sf) 
 
  def risk(i):
    r = 0
    for k1,rules1 in rules.items():
      for k2,m in rules1.items():
        x  = i.x[k1]
        y  = i.x[k2]
        z  = m[x-1][y-1]
        r += z
    return round(100 * r / 104,2)

  def eg(i):
    return [ i.y[k] for k in i.x ] + [ i.effort(), i.risk() ]
```

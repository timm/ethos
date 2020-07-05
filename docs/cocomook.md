```py
from cocomo import Cocomo,F,I
import sys,cocoeg
from lib import perc
from rx import group

c= lambda: Cocomo(
       [dict(goal=F(1), kloc=F(2,100), 
             acap=I(1), ltex=I(5), sced=I(5))])


# d.effort(), d.risk())
#print(perc([c().effort() for _ in range(256)]),
 #     perc([c().risk() for _ in range(256)]))

def all():
  n=1024
  for k in cocoeg.better:
    sys.stderr.write("%s\n" % k)
    c= lambda: Cocomo( 
                 [dict(kloc=F(2,100)),
                 cocoeg.better[k] ])
    print(k, perc([c().effort() for _ in range(n)]),
             perc([c().risk() for _ in range(n)]))

def one():
  n=256
  for k1 in cocoeg.projects:
    print("#")
    e = {}
    r = {}
    for k2 in cocoeg.better:
      c= lambda: Cocomo( [cocoeg.better[k2] ,
                          cocoeg.projects[k1]])
      e[k2] = [c().effort() for _ in range(n)]
      r[k2] = [c().risk()   for _ in range(n)]
    print("\n" + k1, "effort")
    group(e, width= 30, show="%6.0f",
             chops= [.1, .3,  .5, .7,  .9])
    print("\n" + k2, "risk")
    group(r, width= 30, show="%6.0f",
             chops= [.1, .3,  .5, .7,  .9])



one()
    
#o{b=1.049, em=1.076, sf=27.996}
#o{a=5.600, 

#} 1592.9 7.7

#s=3.165+ 4.505+5.647+7.705+6.974 
#em=1.266* 1.142* 1.175* 1.205* 1.209* 0.841* 1.183* 1.082* 0.749*0.791* 0.899* 1.260* 0.778* 0.839* 1.000* 1.208* 0.763
#
#k=66.371 
#b=1.049
#a=5.6
#print( s,em,a * k**(b + 0.01*s) * em)
#   
```

```py
from cocomo import Cocomo,F,I
import sys,cocoeg
from lib import perc

c   = lambda: Cocomo(
       dict(kloc=F(2,100), goal=F(.3),acap=I(1), 
                      ltex=I(5),
                      sced=I(5)))
#print(perc([c().effort() for _ in range(256)]),
 #     perc([c().risk() for _ in range(256)]))

def all():
  n=1024
  for k in cocoeg.better:
    sys.stderr.write("%s\n" % k)
    c= lambda: Cocomo( 
                 dict(kloc=F(2,100)),
                 cocoeg.better[k] )
    print(k, perc([c().effort() for _ in range(n)]),
             perc([c().risk() for _ in range(n)]))

def one():
  n=256
  for k1 in cocoeg.projects:
    for k2 in cocoeg.better:
      c= lambda: Cocomo( 
                 cocoeg.better[k2] ,
                 cocoeg.projects[k1]
          )
      print("")
      print(k1, k2,
        perc([c().effort() for _ in range(n)]),
        perc([c().risk()   for _ in range(n)]))
    
  
one()
   
```

```py
from lib import Thing,dprint
import random

class X(Thing):
   def __init__(i,lo,hi,f=random.uniform):
     i.lo, i.hi, i.f = lo,hi,f
     i.args = [i.lo, i.hi]
     i.cache = None
   def __call__(i):
     i.cache = i.cache or i.f(*i.args)
     return i.cache
   def miutate(i):
     i.cache = None

u = lambda lo,hi=None : X(lo,hi or lo)
w = lambda lo,hi=None : X(lo,hi or lo, random.randint)

class Cocomo(Thing):
  def __init__(i,**d):
    self.__dict__.update(dict(
          a    = u(2.2,9.8), kloc = u(2,1000), 
          prec = w(1,6),  flex = fw(1,6), arch = w(1,6), 
          team = w(1,6),  pmat = w(1,6),
          rely = w(1,5),  data =w(2,5), cplx = w(1,6),
          ruse = w(2,6),  docu = w(1,5), time = w(3,6),
          stor = w(3,6),  pvol = w(2,5),
          acap = w(1,5),  pcap = w(1,5), pcon = w(1,5),
          aexp = w(1,5),  plex = w(1,5), ltex = w(1,5),
          tool = w(1,5),  site = w(1,6), sced = w(1,5))
    self.__dict__.uodate(d)
    i.a    = i.a()
    i.kloc = i.kloc()
    i.b    = B(i.a)
    #  exponentially influential
    i.prec,i.flex,i.arch = Sf(i.prec), Sf(i.flex), Sf(i.arch)
    i.team,i.pmat        = Sf(i.team), Sf(i.pmat)
    #  positively linearly influential
    i.rely = Emp(i.rely); i.data = Emp(i.data); i.cplx = Emp(i.cplx)
    i.ruse = Emp(i.ruse); i.docu = Emp(i.docu); i.time = Emp(i.time)
    i.stor = Emp(i.stor); i.pvol = Emp(i.pvol);
    #  negatively linearly influential
    i.acap = Emn(i.acap); i.pcap = Emn(i.pcap); i.pcon = Emn(i.pcon)
    i.aexp = Emn(i.aexp); i.plex = Emn(i.plex); i.ltex = Emn(i.ltex)
    i.tool = Emn(i.tool); i.site = Emn(i.site); i.sced = Emn(i.sced)
  def effort(i):
    sf=   i.prec() + i.flex() + i.arch() + i.team() + i.pmat()
    em=   i.rely() * i.data() * i.cplx() * i.ruse() * i.docu() \
        * i.time() * i.stor() * i.pvol() * i.acap() * i.pcap() \
        * i.pcon() * i.aexp() * i.plex() * i.ltex() * i.tool() \
        * i.site() * i.sced()
    return i.a * i.kloc ** (i.b() + 0.01 * sf) * em
  def __repr__(i):
   return dprint(dict( prep=   i.prec(), flex=+ i.flex(),arch= i.arch(),team= i.team(), 
               pmat= i.pmat(), reply=i.rely() , data= i.data() ,cplx= i.cplx() , 
               ruse= i.ruse() , docu= i.docu() , time= i.time() , stor= i.stor() , 
              pvol= i.pvol() , acap= i.acap() , pcap= i.pcap() , pcon= i.pcon() , 
              aexp= i.aexp(), plix= i.plex() ,
               ltex= i.ltex(), tool= i.tool() , site= i.site() ,sced= i.sced()))

class Y(Thing):
   __name__ = "Y"
   def __init__(i,x): i.x = x();  i._y =  i.y()
   def __call__(i): return i._y 
   
class Emp(Y):
   def y(i): return u(0.073,   0.21)()  * (i.x - 3) + 1

class Emn(Y):
   def y(i): return u(-0.178, -0.078)() * (i.x - 3) + 1

class Sf(Y):
   def y(i): return u(-1.56,  -1.014)() * (i.x - 6) 

class B(Y):
   def y(i):
     m = (0.85 - 1.1) / (9.18 - 2.2)
     return m*i.x + 1.1+ (1.1-0.8)*.5 
```

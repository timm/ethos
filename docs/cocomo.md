```py
from lib import Cache
from random import random,uniform,randint

r = random.random
u = random.unifrom
w = random.randint

one5 = w(1,5)
one6 = w(1,6)
two5 = w(2,5)

class Cache(Thing):
  def __init__(i)
    i.cache = None
  def __call__(i): 
    if not i.cache: i.cache = i.y()
    return i.y

class Var(Cache)
  def __init__(i,f):
    super().__init__()
    i.f = f
 
class Cocomo(Fun):
  def __init__(i):
    i.a    = lambda: u(2.2,9.8)
    i.b    = B(lambda: i.a)
    i.prec,i.flex,i.arch = Sf(), Sf(), Sf()
    i.team,i.pmat        = Sf(), Sf()
    i.acap = Emp(one5)

   
class Emp(Var):
   def y(i): return u(0.073,   0.21)  * (i.x - 3) + 1

class Emn(Var):
   def y(i): return u(-0.178, -0.078) * (i.x - 3) + 1

class Sf(Var):
   def y(i): return u(-1.56,  -1.014) * (i.x - 6) 

class B(Var):
   def y(i):
     m = (0.85 - 1.1) / (9.18 - 2.2)
     return m*i.x + 1.1+ (1.1-0.8)*.5 
```

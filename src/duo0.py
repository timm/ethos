from random import seed as seed
from random import random as _r
import math

#------------------- ------------------- ------------------- ------------------
class o:
  def __init__(i, **d): i.__dict__.update(**d)
  def __repr__(i): return str(
      {k: (v.__name__ + "()" if callable(v) else v)
       for k, v in sorted(i.__dict__.items()) if k[0] != "_"})

def _of(i, methods):
  def of1(i, f): return lambda *l, **d: f(i, *l, **d)
  for k in methods:
    i.__dict__[k] = of1(i, methods[k])
  return i
#------------------- ------------------- ------------------- ------------------
THE = o(seed=1, skip="?", cohen=.35, id=0,
        Xchop=.5, best=.8, sep=",", ignore=r'([\n\t\r ]|#.*)')
#------------------- ------------------- ------------------- ------------------
def App()       : return o(tbl=Tbl(), counts=Counts())
def Counts()    : return o(f={}, h={})
def Tbl()       : return o(cols=[], rows=[])
def Row()       : return o(cells=[], n=0, tag=False)
#------------------- ------------------- ------------------- ------------------
def Span(x,y)   :
  def top(i)    : i.hi =  math.inf
  def tail(i)   : i.lo = -math.inf  
  def has(i,x,y): return i.lo <= x <=hi
  return _of(o(lo=x,hi=y),locals())
#------------------- ------------------- ------------------- ------------------
def Sym()       :
  def ent(i)    : return -sum(v/i.n*math.log(v/i.n,2) for v in i.seen.values())
  def add(i,x)  : 
    now = i.seen[x] = i.seen.get(x, 0) + 1
    if now > i.most: i.most, i.mode = now, x
  return _of(o(seen={},most=0,mode=None), locals())
#------------------- ------------------- ------------------- ------------------
def Num()       :
  def add(i, x) : i._all += [x]; i.ok = False
  def mid(i)    : n,a= i.all(); return a[int(.5 * n)]
  def var(i)    : n,a= i.all(); return (a[int(.9 * n)] - a[int(.1 * n)]) / 2.56
  def norm(i,x) : _,a= i.all(); return (x-a[0])/(a[-1]-a[0])
  def all(i)    : 
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return len(i._all), i._all
  def width(i): 
    n = len(i._all)**THE.Xchop
    while n < 4 and n < len(xy) / 2: n *= 1.2
    return int(n)
  def div(i):
    n,a = i.all()
    width, sd, x0, out = i.width(), i.var(), a[0], []
    now = width
    while now < n - width:
      now += 1
      x1, x2 = a[now], a[now+1]
      if x1 != x2 and x1 - x0 > sd*THE.cohen:
        x0   = x1
        out += [x1]
        now += width
    return out
  return _of(o(_all=[], ok=True, n=0), locals())
#------------------- ------------------- ------------------- ------------------
def _add(i,x):
  if x != THE.skip:
    i.n += 1
    i.add(x)

seed(THE.seed)
n=Num()
for _ in range(10000): _add(n,int(1000*_r()))
print(n.mid())

#print(n.var(), n.mid())
print(n.div())

def _csv(file):
  def atom(x):
    try:
      return int(x)
    except Exception:
      try:
        return float(x)
      except Exception:
        return x
  with open(file) as fp:
    for a in fp:
      yield [atom(x) for x in re.sub(THE.ignore, '', a).split(THE.sep)]


def _coladd(cols,pos,x):
  i = cols[n] = cols[n] if cols[n] else (
      Num() if isinstance(x, (float, int)) else Sym())
  return cols



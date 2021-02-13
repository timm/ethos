from random import seed as seed
from random import random as r
from math import log

class o:
  def __init__(i, **d): i.__dict__.update(**d)
  def __repr__(i): return str(
      {k: (v.__name__ + "()" if callable(v) else v)
       for k, v in sorted(i.__dict__.items()) if k[0] != "_"})

def _of(i, **methods):
  def of1(i, f): return lambda *l, **d: f(i, *l, **d)
  for k in methods:
    i.__dict__[k] = of1(i, methods[k])
  return i

def App()     : return o(tbl=Tbl(), counts=Counts())
def Counts()  : return o(f={}, h={})
def Tbl()     : return o(cols=[], rows=[])
def Row()     : return o(cells=[], n=0, tag=False)
def Sym()     :
  def ent(i)  : return -sum(v/i.n * math.log(v/i.n,2) for v in i.seen.values())
  def add(i,x):
    now = i.seen[x] = i.seen.get(x, 0) + 1
    if now > i.most: i.most, i.mode = now, x
  return _of(o(seen={},most=0,mode=None), var=ent, add=add, mid=lambda i:i.mode)

def Num()      :
  def add(i, x): i._all += [x]; i.ok = False
  def median(i): n, a = i.all(); return a[int(.5 * n)]
  def sd(i)    : n, a = i.all(); return (a[int(.9 * n)] - a[int(.1 * n)]) / 2.56
  def all(i)   :
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return len(i._all), i._all
  return _of(o(_all=[], ok=True, n=0), add=add, all=all, mid=median, var=sd)

def _add(cols, n, x):
  if x != THE.skip:
    i = cols[n] = cols[n] if cols[n] else (
      Num() if isinstance(x, (float, int)) else Sym())
    i.n += 1
    i.add(x)

THE = o(seed=1, skip="?", best=.8, sep=",", ignore=r'([\n\t\r ]|#.*)')
seed(THE.seed)
n = Num()
for _ in range(10000): _add(n, r())
print(n.var(), n.mid())

def csv(file):
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
```

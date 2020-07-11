```py
import pprint,re,random,traceback,argparse

def elp(txt,**d):
  for k in d:
    key = k
    val = d[k]
    break
  default = val[0] if isinstance(val,list)  else val
  if val is False :
    return key,dict(help=txt, action="store_true")
  m,t = "S",str
  if isinstance(default,int)  : m,t= "I",int
  if isinstance(default,float): m,t= "F",float
  if isinstance(val,list):
    return key,dict(help=txt, choices=val,          
                    default=default, metavar=m ,type=t)
  return key,dict(help=txt + ("; e.g. %s" % val), 
                 default=default, metavar=m, type=t)

def args(before, after, *lst):
  parser = argparse.ArgumentParser(epilog=after, description = before,
               formatter_class = argparse.RawDescriptionHelpFormatter)
  for key, args in lst:
    parser.add_argument("--"+key,**args)
  return parser.parse_args()

def rows(x=None):
  prep=lambda z: re.sub(r'([\n\t\r ]|#.*)','',z.strip())
  if x:
    with open(x) as f:
      for y in f: 
         z = prep(y)
         if z: yield z.split(",")
  else:
   for y in sys.stdin: 
         z = prep(y)
         if z: yield z.split(",")

def cols(src):
  todo = None
  for a in src:
    todo = todo or [n for n,s in enumerate(a) if not "?"in s]
    yield [ a[n] for n in todo]
```
```py
class Thing:
  def __repr__(i):
     s = pprint.pformat(has(i.__dict__),compact=True)
     return  re.sub(r"'",' ',s)

def has(i,seen=None):
   seen = seen or {}
   if isinstance(i,Thing)         : 
      if i in seen: return "_"
      seen[i]=i
      return dict(klass=i.__class__.__name__, slots=has(i.__dict__,seen))
   if isinstance(i,(tuple,list)): 
      return [ has(v,seen) for v in i ]
   if isinstance(i,dict): 
      return { k:has(i[k], seen) for k in i if str(k)[0] !="_"}
   return i

def o(i):
  dprint(i.__dict__)

def dprint(d, pre="",skip="_"):
  def q(z):
    if isinstance(z,float): return "%5.3f" % z
    if callable(z): return "f(%s)" % z.__name__
    return str(z)
  l = sorted([(k,d[k]) for k in d if k[0] != skip])
  return pre+'{'+", ".join([('%s=%s' % (k,q(v))) 
                             for k,v in l]) +'}'
```

```py
class Test:
  t,f = 0,0
  def score(s): 
    t,f = Test.t, Test.f
    return f"#TEST {s} passes = {t-f} fails = {f}"
  def go(fun):
    try:
      Test.t += 1
      print("### ",fun.__name__)
      random.seed(1)
      fun()
      print(Test.score("PASS"),':',fun.__name__)
    except Exception:
      Test.f += 1
      print(traceback.format_exc())
      print(Test.score("FAIL"),':',fun.__name__)

go = Test.go
```

```py
import pprint,rrandom,traceback,argparse

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
def shuffle(lst):
  random.shuffle(lst)
  return lst

def has(i,seen=None):
   seen = seen or {}
   if isinstance(i,Thing)         : 
      j =id(i) % 128021
      if i in seen: return f"#:{j}"
      seen[i]=i
      d=has(i.__dict__,seen)
      d["#"] = j
      return d
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

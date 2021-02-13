
DUO = data miners used / used-by optimizers.
(c) Tim Menzies, 2021 MIT License, https://opensource.org/licenses/MIT.

Sort the data by how much each row dominates over rows.  Split the
sort into 'bad' and 'better'. Discretize data, combining any splits
that do not comment on those splits.  Count how often ranges appear
in 'bad' or 'better'.  Sort the ranges by how likely they appear
in better.  Build rules by combining different ranges; i.e.  pick
pairs of better ranges, combine them, then sort them back into the
list.

     :-------:                 explore  = better==bad
     | Ba    | Bad <----.      planning = max(better - bad)
     |    56 |          |      monitor  = max(bad - better)
     :-------:------:   |      tabu     = min(bad + better)
             | B    |   v
             |    5 | Better
             :------:

```python
import math
from lib import args, csv, sd, mu, symsp, numsp, isa, any, r, seed
from duolib import showRule, selects, cell
from tiny import o, of
from the import THE
from tbl import table

def classify(tbl):
  """Count how often each row dominates some others.
     Classify a row as True if it scores in the top _best_ range."""
  def norm(lst, x): return (
      x - lst[0]) / (lst[-1] - lst[0] + 1E-32)

  def better(tbl, row1, row2):
    "Zitler's continous domination predicate (from IBEA, 2005)."
    s1, s2, n = 0, 0, len(tbl.y)
    for col in tbl.y.values():
      pos, w = col.pos, col.w
      a, b = row1.cells[pos], row2.cells[pos]
      a, b = norm(col.has, a), norm(col.has, b)
      s1 -= math.e**(w * (a - b) / n)
      s2 -= math.e**(w * (b - a) / n)
    return s1 / n < s2 / n
  #######################
  for row1 in tbl.rows:
    row1.score = sum(better(tbl, row1, any(tbl.rows))
                     for _ in range(THE.rowsamples)) / THE.rowsamples
  for n, row in enumerate(sorted(tbl.rows, key=lambda z: z.score)):
    row.klass = n > len(tbl.rows) * THE.best
  return tbl


#######################################################
def discretize(TBL):
  """Reports `bins` for each numeric columns. Initially,
  columns of `N` (x,y) values  into bins of size N^Xchop.
  Combines bins that are smaller than `sd(x)*xsmall`. Then combine
  bins that are different by less than `sd(y)*ysmall`. Also, if
  two adjacent bins are not not 'best', then they are dull and
  we fuse them.  For example, from ../data/auto93.csv, we
  get  learn that '-cylinders' effectively divides into 3:

    [{'hi': 4, 'lo': -inf},
     {'hi': 8, 'lo': 5},
     {'hi': inf, 'lo': 5}]

  Note that the above used 'best=.5' i.e. we were were dividing data
  half:half into best:rest. But we ran the same code with 'best=.8' then
  we find a different picture of what is interesting or not:

    [{'hi': 4, 'lo': -inf},
     {'hi': inf, 'lo': 3}]

  That is, at 'best=.8' all we care about is whether or not 'cylinders'
  is above or below 3.;

  """

  def Span(lo=-math.inf, hi=math.inf, has=None):
    return o(lo=lo, hi=hi, _has=has if has else [])

  def pairs(lst, fx, fy):
    xs, ys, xy = [], [], []
    for one in lst:
      x = fx(one)
      if x != "?":
        y = fy(one)
        xs += [x]
        ys += [y]
        xy += [(x, y)]
    ys = sorted(ys)
    return (sd(sorted(xs)) * THE.xsmall,
            sd(ys) * THE.ysmall,
            ys[int(THE.best * len(ys))],
            sorted(xy))

  def div(xsmall, ysmall, ymin, xy):
    n = len(xy)**THE.Xchop
    while n < 4 and n < len(xy) / 2:
      n *= 1.2
    n, tmp, b4, span = int(n), [], 0, Span(lo=xy[0][0])
    now = n
    while now < len(xy) - n:
      x = xy[now][0]
      span.hi = x
      now += 1
      if (now - b4 > n and now < len(xy) - 2
          and x != xy[now][0]
              and span.hi - span.lo > xsmall):
        span._has = [z[1] for z in xy[b4:now]]
        tmp += [span]
        span = Span(lo=xy[now][0])
        b4 = now
        now += n
    tmp += [Span(lo=xy[b4][0], hi=xy[-1][0],
                 has=[z[1] for z in xy[b4:]])]
    out = merge(tmp, ymin, ysmall)
    out[0].lo = -math.inf
    out[-1].hi = math.inf
    return out

  def merge(b4, ymin, ysmall):
    j, now = 0, []
    while j < len(b4):
      a = b4[j]
      if j < len(b4) - 1:
        b = b4[j + 1]
        if (abs(mu(b._has) - mu(a._has)) < ysmall
            or
                (mu(b._has) < ymin and mu(a._has) < ymin)):
          merged = Span(lo=a.lo, hi=b.hi, has=a._has + b._has)
          now += [merged]
          j += 2
      now += [a]
      j += 1
    return merge(now, ymin, ysmall) if len(now) < len(b4) else now

  for col in TBL.x.values():
    if numsp(col.has):
      col.spans = div(*pairs(TBL.rows,
                             lambda z: z.cells[col.pos],
                             lambda z: z.score))
      print(f"NUM {col.txt:12} :", [x.hi for x in col.spans])
    else:
      print(f"SYM {col.txt:12} :", sorted(col.has.keys()))
  return TBL


def counts(TBL):
  """Counts (class column attribute) inside `TBL`
   (where attributes are the discretized attributes).
   THe counts take the form: (cKass,attribute,range,col), count.
   For example, with best=.9, the counts from ../data/auto93.csv
   are as follows. Note the simplicity of the decision space:
   all that matters is displacement and horsepower is above below
   141 and 74

      (False, 'displacement', 141, 1) 154
      (False, 'displacement', inf, 1) 205
      (False, 'horsepower', 74, 2) 48
      (False, 'horsepower', inf, 2) 307
      ....
      (True, 'displacement', 141, 1) 38
      (True, 'displacement', inf, 1) 1
      (True, 'horsepower', 74, 2) 34
      (True, 'horsepower', inf, 2) 3
      ....

   """

  def Counts(): return o(f={}, h={}, n=0)
  out = Counts()
  for row in TBL.rows:
    k = row.klass
    out.n += 1
    out.h[k] = out.h.get(k, 0) + 1
    for col in TBL.x.values():
      x = cell(col, row)
      if x:
        v = (k, col.txt, x)
        out.f[v] = out.f.get(v, 0) + 1
  return out


#######################################################
def learn(COUNTS):
  def loop(rules, here, there):
    lives = THE.lives
    while True:
      lives -= 1
      total, rules = prune(rules)
      if lives < 1 or len(rules) < 2:
        return rules
      rules += [combine(pick(rules, total),
                        pick(rules, total),
                        here, there)]

  def value(rule, here, there, e=2):
    b = like(rule, here, 2)
    r = like(rule, there, 2)
    return b**e / (b + r) if b > r else 0

  def like(rule, h, hs=None):
    hs = hs if hs else len(COUNTS.h)
    like = prior = (COUNTS.h[h] + THE.k) / (COUNTS.n + THE.k * hs)
    like = math.log(like)
    for col, values in rule:
      f = sum(COUNTS.f.get((h, col, v), 0) for v in values)
      inc = (f + THE.m * prior) / (COUNTS.h[h] + THE.m)
      like += math.log(inc)
    return math.e**like

  def combine(rule1, rule2, here, there):
    val1, rule1 = rule1
    val2, rule2 = rule2
    tmp = dict()
    for rule in [rule1, rule2]:
      for k, lst in rule:
        tmp[k] = tmp.get(k, set())
        for v in lst:
          tmp[k].add(v)
    rule3 = sorted([[k, sorted(list(vs))] for k, vs in tmp.items()])
    val3 = value(rule3, here, there)
    return [val3, rule3]

  def same(rule1, rule2):
    if rule1[0] != rule2[0]:
      return False
    for x, y in zip(rule1[1], rule2[1]):
      if x != y:
        return False
    return True

  def prune(old):
    ordered = [[s, r] for s, r in sorted(old, reverse=True)]
    one = ordered[0]
    unique = [one]
    for two in ordered[1:]:
      if not same(one, two):
        unique += [two]
      one = two
    pruned = [[s, r] for s, r in unique if s > 0][:THE.beam]
    return sum(s for s, _ in pruned), pruned

  def pick(rules, total):  # (s1, r1) (s2,r2) (s3,r3) total=s1+s2+s3
    n = r()
    for rule in rules:
      n -= rule[0] / total
      if n <= 0:
        return rule
    return rule

  def rule0(c, x, here, there):
    rule = [[c, [x]]]
    return [value(rule, here, there), rule]

  out, all = {}, list(set([(c, x) for (_, c, x) in COUNTS.f]))
  for there in COUNTS.h:
    for here in COUNTS.h:
      if here != there:
        rules = loop([rule0(c, x, here, there)
                      for c, x in all], here, there)
        out[here] = [[value(r, here, there, 1), r] for _, r in rules]
  return out

def main():
  return discretize(
      classify(
          table(
              csv(THE.path2data + "/" + THE.data))))

#####################################################
def _main():
  seed(THE.seed)
  t = main()
  c = counts(t)
  for k, rules in learn(c).items():
    print("")
    print(k, f"(n={c.h[k]}) if")
    print("    N  " + ' '.join([f"  {col.txt:5}"
                                for col in t.y.values()]))
    for rule in rules:
      ys = {}
      some = selects(t, rule)
      for row in some:
        for col in t.y.values():
          ys[col.txt] = ys.get(col.txt, []) + [row.cells[col.pos]]
      print(
          f"{len(some):5}  " + ' '.join([f"{mu(ys[k]):7.2f}"
                                         for k in ys]), end="   ")
      print(showRule(rule))


#######################################################
if __name__ == "__main__":
  THE = args("duo4", __doc__.split("\n\n")[0], THE)
  _main()
```

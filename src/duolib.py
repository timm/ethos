"""
Misc python utils
(c) Tim Menzies, 2021 MIT License, https://opensource.org/licenses/MIT.
"""

def showRule(r):
  def show1(k, v): return k + " = (" + ' | '.join(map(str, v)) + ")"
  s, rule = r
  out = ""
  return ' & '.join([show1(k, v) for k, v in rule])

def selects(t, rule):
  "Return the rows selected by a rule."
  def selects1(t, row, ands):
    for txt, ors in ands:
      val = u.cell(t.cols[txt], row)
      if val:
        if val not in ors:
          return False
    return True
  s, rule = rule
  return [row for row in t.rows if selects1(t, row, rule)]

def cell(col, row):
  """HELPER.  Returns a cell value if it is not missing.
  Also, if appropriate, Discretize it first."""
  def bin(spans, x):
    for span in spans:
      if span.lo <= x < span.hi:
        return span.hi
    return span.hi
  ######################
  x = row.cells[col.pos]
  if x != "?":
    return bin(col.spans, x) if u.numsp(col.has) else x

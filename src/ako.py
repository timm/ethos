# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, Tim Menzies (timm@ieee.org) unlicense.org
"""Interpretation rules for CSV headers.
e.g.

        name, Age,Gender?,Salary+

shows 4 columns of data of  which the first is non-numeric 
and the other three contain numbers. The  third column contains
data  we will ignore and  the  fourth column  shows something
we want to maximize (so we will give that column a `weight`  of 1). 
"""

def weight(s):  return -1 if "-" in s else 1 
def isKlass(s): return "!" in s 
def isSkip(s):  return "?" in s
def isNum(s):   return s[0].isupper()
def isY(s):     return "+" in s or "-" in s or "!" in s
def isX(s):     return not isY(s)

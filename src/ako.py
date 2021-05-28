# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, Tim Menzies (timm@ieee.org) unlicense.org
"""Interpretation rules for names on row1 of a CSV file."""


def weight(s):  return -1 if "-" in s else 1 
def isKlass(s): return "!" in s 
def isSkip(s):  return "?" in s
def isNum(s):   return s[0].isupper()
def isY(s):     return "+" in s or "-" in s or "!" in s
def isX(s):     return not isY(s)

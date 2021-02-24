#!/usr/bin/env python3
# vim: ts=2 sw=2 sts=2 et tw=81 fdm=indent:
"""
kolor.py : pretty print text  
(c) 2021, Tim Menzies, MIT license.     
https://choosealicense.com/licenses/mit/
"""

all=dict(
    PURPLE    = '\033[1;35;48m', CYAN   = '\033[1;36;48m',
    BOLD      = '\033[1;37;48m', BLUE   = '\033[1;34;48m',
    GREEN     = '\033[1;32;48m', YELLOW = '\033[1;33;48m',
    RED       = '\033[1;31;48m', BLACK  = '\033[1;30;48m',
    UNDERLINE = '\033[4;37;48m', END    = '\033[1;37;0m')

def say(**d):
  for k,v in d.items(): 
    return all["BOLD"] + all[k] + v + all["END"]

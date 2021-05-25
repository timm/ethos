# vim: filetype=python ts=2 sw=2 sts=2 et :
from sym import Sym

s=Sym(all="aaaabbc")
assert 4==s.seen["a"]
assert 1.378  <= s.spread() <=1.38

"""
Config items.
(c) Tim Menzies, 2021 MIT License, https://opensource.org/licenses/MIT.
"""

from tiny import o, of

THE = o(
    best=0.5,
    beam=10,
    data="auto93.csv",
    path2data=".",
    k=1,
    m=2,
    seed=13,
    lives=128,
    rowsamples=64,
    xsmall=.35,
    ysmall=.35,
    Xchop=.5)

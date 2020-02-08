#!/usr/bin/env clisp -q
; vim: filetype=lisp: ts=2 sw=2 sts=2  et :

(load "../src/101")

(let ((d (nb "../data/weather.csv")))
  (print d)
)

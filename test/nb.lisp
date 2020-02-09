#!/usr/bin/env clisp -q
; vim: filetype=lisp: ts=2 sw=2 sts=2  et :

(load "../src/101")

(let ((n (make-nb)))
  (create n "../data/weather.csv")
  (do-hash (k d (? n parts))
     (print (? d cols klass)))
)

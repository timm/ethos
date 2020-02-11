;#!/usr/bin/env clisp -q
; vim: filetype=lisp: ts=2 sw=2 sts=2  et :

(load "../src/101")


(let ((n (adds '(85 80 83 70 68 65 
                 64 72 69 75 75 72 81))))
x  (ok 0.015 (round2 (like n 85)))
  (ok 0.057 (round2 (like n 72)))
  (ok 0.058 (round2 (like n 75)))

  )



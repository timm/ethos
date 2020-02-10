#!/usr/bin/env clisp -q
; vim: filetype=lisp: ts=2 sw=2 sts=2  et :

(load "../src/101")

(deftest weather1 ()
  (let ((d (make-data)))
    (readd d "../data/weather.csv")
    (ok 23 (length (? d rows)))
    (ok 20.332 (round2 (? (first (? d cols nums)) sd) 3))
    (ok 7.796  (round2 (? (second (? d cols nums)) sd) 3))
    (setf d (clone d))
    (ok 1 (round2 (? (first (? d cols nums)) sd) 3))
    (ok 1 (round2 (? (second (? d cols nums)) sd) 3))

    ))



(weather1)

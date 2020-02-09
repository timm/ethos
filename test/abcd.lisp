#!/usr/bin/env clisp -q
; vim: filetype=lisp: ts=2 sw=2 sts=2  et :

(load "../src/101")
(let ((a (make-abcds)))
    (dotimes (i  6) (update2 a 'y 'y))
    (dotimes (i  2) (update2 a 'n 'n))
    (dotimes (i  5) (update2 a 'm 'm))
    (update2 a 'm 'n)
    (ready  a)
    (ok 93 (p (acc a)))
    (ok 96 (p (abcd-g (gethash 'n (? a hs)))))
    (ok 83 (p (abcd-pd (gethash 'm (? a hs)))))
) 
(print 2)

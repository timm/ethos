#!/usr/bin/env clisp -q
; vim: filetype=lisp: ts=2 sw=2 sts=2  et :

(load "../src/101")


(deftest _n0() 
  (let ((n (make-nb)))
    (init n "../data/weather101.csv")
    (print (ready (? n abcds)))
    (do-hash (k d (? n klasses))
      (print `(k ,k ,(car (last (? d cols syms))))))
    )
  )

(deftest _n1() 
  (let ((n (make-nb)))
    (init n "../data/weather101n.csv")
    (print (ready (? n abcds)))
    (do-hash (k d (? n klasses))
      (print `(k ,k ,(car (last (? d cols nums))))))
    )
  )

(deftest _n2() 
  (let ((n (make-nb)))
    (init n "../data/weather.csv")
    (do-hash (k d (? n klasses))
      (print `(k ,k ,(car (last (? d cols syms))))))
    )
  )

(deftest _n3()
  (let ((n (make-nb)))
    (init n "../data/diabetes.csv")
    (print (ready (? n abcds)))
    (do-hash (k d (? n klasses))
      (print `(k ,k ,(car (last (? d cols nums))))))
    )
  )

;(_n1)
(_n3)


;#!/usr/local/bin/sbcl --script
                                        ;#!/usr/bin/env clisp -q
; vim: filetype=lisp: ts=2 sw=2 sts=2  et :
;(locally
 ;   (declare #+sbcl(sb-ext:muffle-conditions
  ;                  sb-kernel:redefinition-warning))
   ;(handler-bind ((style-warning #'muffle-warning)))) 

#+sbcl
(sb-ext:restrict-compiler-policy 'debug 3)


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

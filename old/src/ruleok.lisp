(defun square (x)
  (* x x))

(defun square-of-sum (x y)
  (square (+ x y)))

(defun sum-of-squares (x y)
  (+ (square x) (square y)))

(square-of-sum 2 3)
(sum-of-squares 2 3)



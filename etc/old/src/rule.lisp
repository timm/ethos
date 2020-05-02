(defstruct ranges 
  arr n epsilon
  (skip "?")
  (fx #'first)
  (fy #'second)
  (fxs #'make-num)
  (fys #'make-num)
  first last
  (put #'(lambda (x rank) (slot-value x 'rank) rank))
  xs
  (trivial 1.01)
  ys)


(defmethod x ((r ranges) z) (funcall (? r fx)  z))
(defmethod y ((r ranges) z) (funcall (? r fy)  z))

(defmethod x+ ((r ranges) z &optional (xs (? r xs))) (update xs (x r z)))
(defmethod y+ ((r ranges) z &optional (ys (? r ys))) (update ys (y r z)))

(defmethod x- ((r ranges) z &optional (xs (? r xs))) (dec xs (x r z)))
(defmethod y- ((r ranges) z &optional (ys (? r ys))) (dec ys (y r item)))

(defmethod at ((r ranges) i) (aref (? r arr) i))

(defmethod create ((r ranges) lst &key epsilon (cohen 0.3))
  (with-slots (n arr fxs fys epsilon xs ys first last jump) r
    (setf n   (length lst)
          arr (coerce
               (sort rows #'(lambda (a b) (< (x r a) (x r b))))
               #'vector)
          jump (sqrt n)
          xs  (funcall fxs)
          ys  (funcall fys))
    (dolist (item lst)
      (setf first (or first (x r item))
            last  (x r item))
      (x+ r item)
      (y+ r item))
    (setf epsilon (or epsilon (* cohen (spread xs))))))

(defmethod div ((r ranges) 
		&optional (xrhs (? r xs)) (yrhs (? r ys)) (lo 0) (hi (? r n)))
  (with-slots (n jump epsilon start stop trivial) r
    (let ((min   (spread yrhs))
	  (xlhs  (funcall (? r fxs)))
	  (ylhs  (funcall (? r fys)))
	  yrhs1 xrhs1 xlhs1 ylhs1 cut)
      (loop for i from lo to hi do
	(let* ((z     (at r i))
	       (z1    (at r (1+ i)))
	       (now   (x r z))
	       (after (x r z1)))
	  (x+ r z xlhs)
	  (y+ r z ylhs)
	  (x- r z xrhs)
	  (y- r z yrhs)
	  (if  (and (>   i (+ lo jump))
		    (<   i (- hi jump))
		    (not (equal now (? r skip)))
		    (not (equal after now))
		    (<   epsilon (- after start))
		    (<   epsilon (- stop  now))
		    (<=  trivial (/ (mid xrhs) (mid xlhs)))
		    (<   epsilon (- (mid xrhs) (mid xlhs)))
		    (<=  trivial (/ min (xpect ylhs yrhs))))
	    (setq cut   (1+ i)
		  min   (xpect ylhs yrhs)
		  xrhs1 (copy-structure xrhs)
		  xlhs1 (copy-structure xlhs)
		  yrhs0 (copy-structure yrhs)
		  ylhs1 (copy-structure ylhs)))))
      (cond (cut (div r xlhs1 ylhs1 lo  cut)
		 (div r xrhs1 yrhs1 cut hi)) 
	    (t   (loop for i from lo to hi do
		       (funcall (? r put) (at r i))))))))

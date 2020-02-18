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
  ys)

(defmethod x ((r ranges) z) (funcall (? r fx)  z))
(defmethod y ((r ranges) z) (funcall (? r fy)  z))

(defmethod create ((r ranges) lst &key epsilon (cohen 0.3))
  (with-slots (n arr fxs fys epsilon xs ys first last) r
    (setf n   (length lst)
          arr (coerce
               (sort rows #'(lambda (a b) (< (x r a) (x r b))))
               #'vector)
          xs  (funcall fxs)
          ys  (funcall fys))
    (dolist (item lst)
      (setf first (or first (x r item))
            last  (x r item))
      (update xs (x r item))
      (update ys (y r item)))
    (setf epsilon (or epsilon
                      (* cohen (spread xs))))))

(defmethod div ((r ranges)  &key right (lo 0) (hi (? r n)))
   (with-slots 
  (let (cut
        (min  (spread right))
        (xs1  (funcall (? r fxs)))
        (safe (copy-structure right)))
    (loop for i from lo to hi do
         (let* ((item (aref (? r arr) i)))
               (y1 (y r item)))
           (if (not (equalp x1 "?"))
               (update xs1 x1)
               (decrete,ent 
               (decrement (? 
           
      collect y)
          
        

       




(defstruct ranges arr n epsilon 
           (fx #'first)
           (fy #'second)
           (fxs #'make-num)
           (fys #'make-num)
           xs
           ys)

(defmethod x ((r ranges) z) (funcall (? r fx)  z))
(defmethod y ((r ranges) z) (funcall (? r fy)  z))

(defmethod create ((r ranges) lst &key epsilon (cohen 0.3))
  (with-slots (n arr fxs fys epsilon xs ys) r
    (setf n   (length lst)
          arr (coerce
               (sort rows #'(lambda (a b) (< (x r a) (x r b))))
               #'vector)
          xs  (funcall fxs)
          ys  (funcall fys))
    (dolist (item lst)
      (update xs (x r item))
      (update ys (y r item)))
    (setf epsilon (or epsilon
                      (* cohen (spread xs))))))

(defmethod div ((r ranges)  &key ys1 (lo 0) (hi (? r n)))
  (let (cut
        (xs1 (funcall (? r fxs)))
        (safe (copy-structure ys1)))
    (loop for i from lo to hi
       for item = (aref (? r arr) i) do
         (let ((x1 (x r item))
               (y1 (y r item)))
           (if (not (equalp x1 "?"))
               (update xs1 x1)
               (decrete,ent 
               (decrement (? 
           
      collect y)
          
        

       



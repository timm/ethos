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

(defmethod x+ ((r range) z &optional (xs (? r xs))) (update xs (x r z)))
(defmethod y+ ((r range) z &optional (ys (? r ys))) (update ys (y r z)))

(defmethod x- ((r range) z &optional (xs (? r xs))) (dec    xs (x r z)))
(defmethod y- ((r range) z &optional (ys (? r ys))) (dec    ys (y r item))))

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

(defmethod argmin ((r ranges) xright yright lo hi)
   (with-slots (n jump epsilon start stop trivial) r
     (let (cut 
           (min     (spread yright))
           (xleft   (funcall (? r fxs)))
           (yleft   (funcall (? r fys)))
           xleft1
           yleft1
           (yright1 (copy-structure yright))
           (xright1 (copy-structure xright)))
       (loop for i from lo to hi do
            (let* ((z (aref (? r arr) i)))
              (x+ r z xleft)
              (y+ r z yleft)
              (x- r z xright)
              (y- r z yright)
              (when (and (> i (+ lo jump))
                         (< i (- hi jump)))
                (let* ((z1    (aref (? r arr) (1+ i)))
                       (after (x r z1))
                       (now   (x r z)))
                  (unless (or (equal now (? r skip))
                              (equal after now))
                    (if (and (<  epsilon (- after start))
                             (<  epsilon (- stop  now))
                             (<= trivial (/ (mid xright) (mid xleft)))
                             (<  epsilon (- (mid xright) (mid xleft))))
                        (let ((new (xpect yleft yright)))
                          (if (<  (* new trivial) min)
                              (setq cut     i
                                    min     new
                                    xright1 (copy-structure xright)
                                    xleft1  (copy-structure xleft)
                                    yright1 (copy-structure yright)
                                    yleft1  (copy-structure yleft)))))))))))
     (values cut xleft1 xright1 yleft1 yright1)))

(defmethod div ((r ranges) &key (xright (? r xs))
                             (yright (? r ys))
                             (lo 0) (hi (? r n)))
  (multiple-value-bind (cut xleft1 xright1 yleft1 yright1)
      (argmin r xright yright lo hi)
    (if cut
        (progn
          (div r xleft1 yleft1 lo cut)
          (duv r xright1 yright1 (1+ cut) hi))  
        (loop for i from lo to hi do
             (funcall (? r put)  (aref (? r arr) i)))))) 

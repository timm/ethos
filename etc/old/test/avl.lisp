
(defun hashes(n)
	(let ((h (make-hash-table)))
		(deotimes (i n h) (setf (gethash i h) i))))

(defun ps(n)
	(let ((x (gensym)))
		(dotimes (i n x) (setf (get x i) (* 20 i)))))

(print (symbol-plist (ps 4)))

(loop for (k v) on (symbol-plist (ps 4))  by (function cddr)
          do (print `(k ,k v ,v)))

(defun hashes+(h n)
 (dotimes (i n)
 	(progn (setf (gethash  i h) (* i 12)))))

(defun ps+(p n)
  (dotimes (i n)
    (/ 1 0)
 	(progn (setf (get p i)  (* i 11)))))

(defun main2 (n r)
 (let (t1 t2 t3)
    (setf t1 (get-internal-real-time))
    (dotimes (i r) (hashes+ (hashes n) n))
    (setf t2 (get-internal-real-time))
    (dotimes (i r) (ps+  (ps n) n))
    (setf t3 (get-internal-real-time))
    (setf t3 (float (/ (- t3 t2 ) r)))
    (setf t2 (float (/ (- t2 t1 ) r)))
    (print `(size ,n plist ,t3 hash ,t2 diff 
        ,(float (/ t3 (+ 0.00000000000000001 t2)))))))

(main2 5 1000)
(main2 10 1000)
(main2 20 1000)

(main2 40 1000)
(main2 80 1000)
(main2 160 1000)
(main2 320 1000)
(main2 640 1000)
(defun lsts(n)
  (let (out) (dotimes (i n out) (push i out))))

(defun vectors(n)
  (let ((out (make-array  n)))
    (dotimes (i n out) (setf (aref  out i ) i))))

(defun lsts+(lst n)
 (dotimes (i n)
 	(setf (nth i lst) i)))
(defun vectors+(v n)
 (dotimes (i n)
 	(setf (aref v i)  i)))

(defun main (n r)
  (let* (t1 t2 t3 (m 0)(t0 (GET-INTERNAL-REAL-TIME)))
    (dotimes (i r) (incf m))
    (setf t1 (get-internal-real-time))
    (dotimes (i r) (lsts+ (lsts n) n))
    (setf t2 (get-internal-real-time))
    (dotimes (i r) (vectors+ (vectors n) n))
    (setf t3 (get-internal-real-time))
    (setf t3 (float (/ (- t3 t2 ) r)))
    (setf t2 (float (/ (- t2 t1 ) r)))
    (setf t1 (float (/ (- t1 t0 ) r)))
    (print `(size ,n nothing ,t1 lists ,t2 vectors ,t3 diff ,(float (/ t2 (+ 0.00000000000000001 t3)))))))

 ;(let ((n 20)) (dotimes(i 7) (setf n (* 2 n)) (main n 100)))


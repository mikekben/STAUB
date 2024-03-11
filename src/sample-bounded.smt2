; 
(set-info :status unknown)
(declare-fun z () (_ BitVec 23))
(declare-fun y () (_ BitVec 23))
(declare-fun x () (_ BitVec 23))
(assert
 (let ((?x25 (bvadd (bvadd (bvmul (bvmul x x) x) (bvmul (bvmul y y) y)) (bvmul (bvmul z z) z))))
 (= ?x25 (_ bv855 23))))
(check-sat)

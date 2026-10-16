; Binary trees: a small version of the classic benchmark for garbage
; collectors (Hans Boehm's GCBench, and "binary-trees" in the Computer
; Language Benchmarks Game).
;
; One tree of depth 10 is kept for the whole run: long-lived data.
; Then 200 more trees of depth 10 are built, counted, and dropped:
; short-lived data, 1.6 million places of it, in a heap of 65536.
; Every tree node is a block of two fields, left and right; a leaf
; has 0 in both.

main:   PUSH 10
        CALL make 1     ; local 0: the long-lived tree
        PUSH 0          ; local 1: total of all nodes counted
        PUSH 200        ; local 2: trees left to build
loop:   LOAD 2
        JZ done
        LOAD 1
        PUSH 10
        CALL make 1
        CALL count 1
        ADD
        STORE 1
        LOAD 2
        PUSH 1
        SUB
        STORE 2
        JMP loop
done:   LOAD 1
        PRINT           ; 200 trees of 2047 nodes: 409400
        LOAD 0
        CALL count 1
        PRINT           ; the long-lived tree is still all there: 2047
        HALT

; make(depth): a full tree of that depth
make:   PUSH 2
        NEW             ; local 1: the node
        LOAD 0
        JZ leaf
        LOAD 1
        PUSH 0
        LOAD 0
        PUSH 1
        SUB
        CALL make 1
        SETF            ; node.left = make(depth - 1)
        LOAD 1
        PUSH 1
        LOAD 0
        PUSH 1
        SUB
        CALL make 1
        SETF            ; node.right = make(depth - 1)
leaf:   LOAD 1
        RET

; count(tree): the number of nodes in it
count:  LOAD 0
        PUSH 0
        EQ
        JZ node
        PUSH 0
        RET
node:   PUSH 1
        LOAD 0
        PUSH 0
        GETF
        CALL count 1
        ADD
        LOAD 0
        PUSH 1
        GETF
        CALL count 1
        ADD
        RET

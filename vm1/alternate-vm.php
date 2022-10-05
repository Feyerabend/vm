<?php

class Stack {

    public $top;
    public $stack = array();

    function __construct() {
        $this->top = -1;
    }

    public function push($x) {
        $this->stack[++$this->top] = $x;
    }

    public function pop() {
        if ($this->top < 0){
            echo "error: stack empty";
        } else {
          return $this->stack[$this->top--];
        }
    }
}


class OP {
    const ADD = 1;
    const MUL = 2;
    const SUB = 3;
    const SET = 4;
    const PRNT = 5;
    const HALT = 6;
}

$code = array(
    OP::SET, 33,
    OP::SET, 44,
    OP::ADD,
    OP::PRNT,
    OP::HALT
);


function run($code): void {

    $stk = new Stack();
    $pc = 0;

    do {
        $opcode = $code[$pc];
        $pc = $pc + 1;

        switch ($opcode) {

            case OP::HALT:
                return;

            case OP::SET:
                $v = $code[$pc];
                $stk->push($v);
                break;

            case OP::ADD:
                $b = $stk->pop();
                $a = $stk->pop();
                $stk->push($a + $b);
                break;

            case OP::SUB:
                $b = $stk->pop();
                $a = $stk->pop();
                $stk->push($a - $b);
                break;

            case OP::MUL:
                $b = $stk->pop();
                $a = $stk->pop();
                $stk->push($a * $b);
                break;

            case OP::PRNT:
                $v = $stk->pop();
                echo "{$v}".PHP_EOL;
                break;

            default:
                break;
        } // switch

    } while (TRUE);
}

run($code);

# Virtual Machines

## vmenkel


Description of the language *enkel/0*. ...

```ebnf
program = block .

block = [ const ident = number {, ident = number} ; ]
        [ array ident : number {, ident : number} ; ]
        [ var ident {, ident} ; ]
        { procedure ident[ [ident {, ident}] ] ; block ; }
          statement

statement = [ ident[. index] is expression
            | call ident[ [factor {, factor}] ]
            | begin statement {; statement } end 
            | if condition then statement { else statement }
            | while condition do statement
            | return [factor]
            | print factor
            | emit factor ]

condition = expression (=|#|<|<=|>|<=) expression

expression = [-] term { (+|-|or|xor) term }

term = factor { (*|/|%|and) factor }

factor = ident[. index] | number | ( expression )

index = (ident|number)
```



![Simplified BNF for enkel/0, a simple compiler](assets/images/enkel0.png)


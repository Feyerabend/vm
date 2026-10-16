
# Fibonacci (as usual)

LET I = 3
LET N = 10  # number of

LET T1 = 0
LET T2 = 1

LET NXT = T1 + T2

PRINT "Fib serie:"
PRINT T1
PRINT T2

WHILE I <= N DO
  PRINT NXT
  LET T1 = T2
  LET T2 = NXT
  LET NXT = T1 + T2
  LET I = I + 1
ENDWHILE

END

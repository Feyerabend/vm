# GCD (as per usual) %
LET a = 15
LET b = 6

WHILE a <> b DO
  IF b < a THEN
    LET a = a - b
  ELSE
    LET b = b - a
  ENDIF
ENDWHILE

PRINT a
END

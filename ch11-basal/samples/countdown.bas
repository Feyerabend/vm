# FOR with a negative STEP, and ON ... GOSUB to pick a subroutine.

FOR N = 10 TO 0 STEP -2
  PRINT N;
  PRINT " ";
NEXT N
PRINT

FOR K = 1 TO 3
  ON K GOSUB ONE, TWO, THREE
NEXT K
PRINT "done"
END

! ONE
PRINT "one"
RETURN

! TWO
PRINT "two"
RETURN

! THREE
PRINT "three"
RETURN

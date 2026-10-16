# A counting loop with arithmetic and a subroutine, as basal/0 writes it.
LET TOTAL = 0
FOR I = 1 TO 300000
  LET X = I * 3 - 2 * 4 + 10 / 5
  IF X > 100 THEN
    GOSUB ADDIT
  ENDIF
NEXT I
PRINT TOTAL
END

! ADDIT
LET TOTAL = TOTAL + X / 1000
RETURN

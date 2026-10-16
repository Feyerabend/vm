# A multiplication table, with FOR loops and PRINT ...; to stay on a line.

FOR ROW = 1 TO 9
  FOR COL = 1 TO 9
    LET P = ROW * COL
    IF P < 10 THEN
      PRINT " ";
    ENDIF
    PRINT P;
    PRINT " ";
  NEXT COL
  PRINT
NEXT ROW

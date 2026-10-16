# The run-time print routine has to cope with every number, including
# the one that has no positive partner: -2147483648.

LET BIG = 2147483647
PRINT BIG;
PRINT " ";
PRINT BIG + 1;
PRINT " ";
PRINT -BIG;
PRINT " ";
PRINT 0;
PRINT " ";
PRINT -7;
PRINT

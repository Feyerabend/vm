# Adopted from
# https://github.com/cyningstan/TinyBASIC/blob/master/bas/hurkle.bas
# in public domain

#   Initialise the random number generator
    PRINT "Think of a number."
#   INPUT R
    LET R = 512 # simulate input
    IF R < 0 THEN
      LET R = 0
    ENDIF
    IF R > 4095 THEN
      LET R = 4095
    ENDIF

#   Initialise the game
    GOSUB RANDOM
    LET T = R / 10 * 10
    LET G = R - T
    GOSUB RANDOM
    LET U = R / 10 * 10
    LET H = R - U
    LET M = 0

#   Input player guess
!   AGAIN
    PRINT "Where is the hurkle? Enter column then row."
#   INPUT X, Y
    LET X = 2 # simulate
    LET Y = 1 # simulate

    IF X >= 0 THEN
      IF X <= 9 THEN
        IF Y >= 0 THEN
          IF Y<= 9 THEN
            GOTO PROCESS
          ENDIF
        ENDIF
      ENDIF
    ENDIF
    PRINT "That location is off the grid!"
    GOTO AGAIN

#   Process player guess
!   PROCESS
    LET M = M + 1
    PRINT "The Hurkle is..."
    IF G < X THEN
      IF H < Y THEN
        PRINT "...to the northwest."
      ENDIF
    ENDIF
    IF G = X THEN
      IF H < Y THEN
        PRINT "...to the north."
      ENDIF
    ENDIF
    IF G > X THEN
      IF H < Y THEN
        PRINT "...to the northeast."
      ENDIF
    ENDIF
    IF G > X THEN
      IF H = Y THEN
        PRINT "...to the east."
      ENDIF
    ENDIF
    IF G > X THEN
      IF H > Y THEN
        PRINT "...to the southeast."
      ENDIF
    ENDIF
    IF G = X THEN
      IF H > Y THEN
        PRINT "...to the south."
      ENDIF
    ENDIF
    IF G < X THEN
      IF H > Y THEN
        PRINT "...to the southwest."
      ENDIF
    ENDIF
    IF G < X THEN
      IF H = Y THEN
        PRINT "...to the west."
      ENDIF
    ENDIF
    IF G = X THEN
      IF H = Y THEN
        GOTO RIGHT
      ENDIF
    ENDIF
    IF M > 6 THEN
      GOTO TOOLONG
    ENDIF
    PRINT "You have taken ";
    PRINT M
    PRINT " turns so far."
    GOTO AGAIN


#   Player has won
!   RIGHT # here
    PRINT "...RIGHT HERE!"
    PRINT "You took ";
    PRINT M
    PRINT " turns to find it."
    END


#   Player has lost
!   TOOLONG # you lose
    PRINT "You have taken too long over this. You loose!"
    END


#   Random number generator
#     Input:   R - current seed
#     Outputs: R - updated seed
!   RANDOM
    LET R = 5 * R + 35
    LET E = R / 4096
    LET R = R - E * 4096
    RETURN

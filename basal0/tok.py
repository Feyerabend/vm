
from enum import Enum, unique

RSTART = 500
RSTOP = 519

@unique
class TType(Enum):

    # eof
    EOF = -1

    # meta
    NEWLINE, NUMBER, IDENT, STRING = range(0x00, 0x04)

    # arith. relops
    EQ, PLUS, MINUS, ASTERISK, SLASH, \
    NEQ, LT, LQ, GT, GQ = range(200, 210)

    # punctuations
    LPAREN, RPAREN, COLON, SEMI, EXCL, COMMA = range(300, 306)

    # reserved
    ON, GOTO, PRINT, INPUT, LET, IF, THEN, ENDIF, WHILE, DO, ENDWHILE, \
    END, GOSUB, RETURN, ELSE, FOR, TO, NEXT, STEP = range(RSTART, RSTOP)


class Token:
    def __init__(self, text, type):
        self.text = text
        self.type = type

class LexerError(Exception):
    def __init__(self, pos, msg, *args):
        self.pos = pos
        self.msg = msg
        self.args = args

    def __str__(self):
        return '%s at position %s' % (self.msg % self.args, self.pos)

class ParseError(Exception):
    def __init__(self, pos, msg, *args):
        self.pos = pos
        self.msg = msg
        self.args = args

    def __str__(self):
        return '%s at position %s' % (self.msg % self.args, self.pos)

#try:
#    raise(ParseError(2, 3 * 2, "Not Allowed"))
#except ParseError as Arg:
#    print('Exception occurred: ', Arg)

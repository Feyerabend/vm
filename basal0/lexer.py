
from tok import *
import csv
import enum
import sys

NULL = '\0'
NEWL = '\n'
RETN = '\r'
TABL = '\t'
SPAC = ' '

# slice the input, write the bits to file
class Tokenize:
    def __init__(self, file):
        with open(file, 'r') as f:
            self.input = f.read()
        f.close()
        self.lexer = Lexer(self.input + NEWL)

    def write(self, file):
        with open(file, 'w', newline = '') as f:
            fieldnames = ['type', 'text']
            writer = csv.DictWriter(f, fieldnames = fieldnames, \
                delimiter = '|', quoting = csv.QUOTE_ALL)
            token = self.lexer.gettoken()
            writer.writeheader()
            while token.type.value != -1: # TType.EOF:
                kind = token.type.value
                text = token.text
                writer.writerow({'type': kind, 'text': text})
                token = self.lexer.gettoken()
        f.close()


class Lexer:
    def __init__(self, input):
        self.input = input
        self.curr = ''  # curr character
        self.index = -1   # curr position
        self.advance()  # init

    def err(self, message):
        print("error:lexer: " + message)
        sys.exit(1)

    def advance(self):
        self.index += 1
        if self.index > len(self.input) - 1:
            self.curr = NULL # stop mark
            return False
        self.curr = self.input[self.index]
        return True

    def ahead(self):
        if self.index + 1 >= len(self.input):
            return NULL # stop mark
        return self.input[self.index + 1]

    def gettoken(self):
        self.prepare()
        token = None

        if self.curr == '*':
            token = Token(self.curr, TType.ASTERISK)

        elif self.curr == '/':
            token = Token(self.curr, TType.SLASH)

        elif self.curr == '(':
            token = Token(self.curr, TType.LPAREN)

        elif self.curr == ')':
            token = Token(self.curr, TType.RPAREN)

        elif self.curr == ';':
            token = Token(self.curr, TType.SEMI)

        elif self.curr == '!':
            token = Token(self.curr, TType.EXCL)

        elif self.curr == ',':
            token = Token(self.curr, TType.COMMA)

        elif self.curr == '=':
            token = Token(self.curr, TType.EQ)

        elif self.curr == '>':
            if self.ahead() == '=':
                self.advance()
                token = Token('>=', TType.GQ)
            else:
                token = Token(self.curr, TType.GT)

        elif self.curr == '<':
            if self.ahead() == '=':
                self.advance()
                token = Token('<=', TType.LQ)
            elif self.ahead() == '>':
                self.advance()
                token = Token('<>', TType.NEQ)
            else:
                token = Token(self.curr, TType.LT)

        elif self.curr == '+':
            token = Token(self.curr, TType.PLUS)
            if self.ahead().isdigit():
                self.advance()
                num = self.consume('0123456789')
                token = Token(num, TType.NUMBER)

        elif self.curr == '-':
            token = Token(self.curr, TType.MINUS)
            if self.ahead().isdigit():
                self.advance()
                num = self.consume('0123456789')
                token = Token(str(-int(num)), TType.NUMBER)

        elif self.curr == '\"':
            self.advance()
            start = self.index
            while self.curr != '\"':
                if self.curr in {RETN, NEWL}:
                    self.err("unexpected end of string")
                self.advance()
            text = self.input[start : self.index]
            token = Token(text, TType.STRING)

        elif self.curr == "\'":
            self.advance()
            start = self.index
            while self.curr != "\'":
                if self.curr in {RETN, NEWL}:
                    self.err("unexpected end of string")
                self.advance()
            text = self.input[start : self.index]
            token = Token(text, TType.STRING)

        elif self.curr.isdigit():
            num = self.consume('0123456789')
            token = Token(num, TType.NUMBER)

        elif self.curr.isalpha():
            text = self.consume('0123456789' +
                                'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
                                'abcdefghijklmnopqrstuvwxyz')
            token = self.reserved(text)

        elif self.curr == NEWL:
            token = Token(NEWL, TType.NEWLINE)

        elif self.curr == NULL: #'\0':
            token = Token('', TType.EOF)

        else:
            self.err("unknown token: " + self.curr)

        self.advance()
        return token

    # lookup reserved or return identifier
    def reserved(self, text):
        for name, member in TType.__members__.items():
            if str(name) == text and member.value in range(RSTART, RSTOP):
                return Token(name, member)
        return Token(text, TType.IDENT)

    # helper numbers, variables, keywords
    def consume(self, set):
        start = self.index
        while self.ahead() in set:
            self.advance()
        text = self.input[start : self.index + 1]
        return text

    def prepare(self):
        self.nowhitespace()
        self.nocomment()

    def nowhitespace(self):
        while self.curr in {SPAC, TABL, RETN}:
            self.advance()

    def nocomment(self):
        if self.curr == '#':
            while self.curr != NEWL:
                self.advance()

        '''
        raise LexerError(
            self.index + 1,
            'Expected %s, found %s',
            'character' if chars is None else '[%s]' % chars,
            next_char
        )
        '''

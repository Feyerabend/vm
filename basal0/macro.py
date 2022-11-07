
from collections import deque
from tok import *
import csv
import sys


# get tokens from file, already tokenized
class FileTokens:
    def __init__(self, file):

        # read tokens from file, put in temporary queue (store)
        self.store = deque()
        queue = []
        with open(file, 'r') as file:
            csvf = csv.DictReader(file, delimiter = '|', quoting = csv.QUOTE_ALL)
            for row in csvf:
                queue.append(dict(row))

        # reconstruct tokens, put in deque
        for line in queue:
            type = TType(int(line['type']))
            text = str(line['text'])
            token = Token(text, type)
            self.store.append(token)

    def write(self, file):
        with open(file, 'w', newline = '') as f:
            fieldnames = ['type', 'text']
            writer = csv.DictWriter(f, fieldnames = fieldnames, \
                delimiter = '|', quoting = csv.QUOTE_ALL)
            token = self.gettoken()
            writer.writeheader()
            while token.type.value != -1:
                type = token.type.value
                text = token.text
                writer.writerow({'type': type, 'text': text})
                token = self.gettoken()
        f.close()

    # pop element, return token from queue
    def gettoken(self):
        return self.store.popleft() if self.store else Token('', TType.EOF)


class Translate:
    def __init__(self, tokenfile):
        self.lexer = FileTokens(tokenfile)
        self.out = deque()

        self.curr = self.lexer.gettoken()
        self.next = self.lexer.gettoken()

    def err(self, message):
        sys.exit("error:macro: " + message)

    def out(self):
        return self.out

    def advance(self):
        self.curr = self.next
        self.next = self.lexer.gettoken()

    def recognize(self, type):
        return type == self.curr.type

    def expect(self, type):
        if not self.recognize(type):
            self.err("expected " + type.name + \
                     ", found " + self.curr.type.name)
        self.advance()

    def push(self):
        self.out.append(self.curr)

    def program(self):
        while not self.recognize(TType.EOF):
            self.statement()
        self.out.append(Token('', TType.EOF))

    def statement(self):

        # table jumps
        #   ON identifier GOTO label1, label2, ..
        # and
        #   ON identifier GOSUB label1, label2, ..

        if self.recognize(TType.ON):

            self.advance()
            iter = self.curr.text
            self.expect(TType.IDENT)
            if self.recognize(TType.GOTO):
                instr = TType.GOTO
            elif self.recognize(TType.GOSUB):
                instr = TTYPE.GOSUB
            else:
                self.err("unrecognized instruction in ON statement")
            self.advance()

            # now the translation
            count = 0
            while not self.recognize(TType.NEWLINE):
                count += 1
                label = self.curr.text
                self.out.append(Token('IF', TType.IF))
                self.out.append(Token(iter, TType.IDENT))
                self.out.append(Token('=', TType.EQ))
                self.out.append(Token(count, TType.NUMBER))
                self.out.append(Token('THEN', TType.THEN))
                self.out.append(Token('\n', TType.NEWLINE))
                if instr == TType.GOTO:
                    self.out.append(Token('GOTO', TType.GOTO))
                elif instr == TType.GOSUB:
                    self.out.append(Token('GOSUB', TType.GOSUB))
                self.out.append(Token(label, TType.IDENT))
                self.out.append(Token('\n', TType.NEWLINE))
                self.out.append(Token('ENDIF', TType.ENDIF))
                self.out.append(Token('\n', TType.NEWLINE))
                self.advance()
                if not self.recognize(TType.COMMA):
                    break
                self.expect(TType.COMMA)


        # simple impl

        # from
        # FOR I = 1 TO 100 STEP 1
        # ..
        # NEXT I

        # to
        # LET I = 1
        # WHILE I <= 100 DO
        # ...
        # I = I + 1
        # ENDWHILE


        # NEXT identifier
        elif self.recognize(TType.NEXT):

            self.advance()
            iter = self.curr.text
            self.expect(TType.IDENT)

            self.out.append(Token('LET', TType.LET))
            self.out.append(Token(iter, TType.IDENT))
            self.out.append(Token('=', TType.EQ))
            self.out.append(Token(iter, TType.IDENT))
            self.out.append(Token('+', TType.PLUS))
            self.out.append(Token('STEP', TType.IDENT))
            self.out.append(Token('\n', TType.NEWLINE))

            self.out.append(Token('ENDWHILE', TType.ENDWHILE))
            self.out.append(Token('\n', TType.NEWLINE))

        # FOR identifier = start TO end STEP step
        elif self.recognize(TType.FOR):

            self.advance()
            iter = self.curr.text
            self.expect(TType.IDENT)
            self.expect(TType.EQ)
            start = self.curr.text
            self.expect(TType.NUMBER)
            self.expect(TType.TO)
            end = self.curr.text
            self.expect(TType.NUMBER)

            step = '1'
            if self.recognize(TType.STEP):
                self.expect(TType.STEP)
                step = self.curr.text
                self.expect(TType.NUMBER)
                if int(step) < 0:
                    token = Token('>=', TType.GQ)
                elif int(step) > 0:
                    token = Token('<=', TType.LQ)
                else:
                    self.err("STEP in FOR statement can not be 0")

            self.out.append(Token('LET', TType.LET))
            self.out.append(Token('STEP', TType.IDENT))
            self.out.append(Token('=', TType.EQ))
            self.out.append(Token(step, TType.NUMBER))
            self.out.append(Token('\n', TType.NEWLINE))

            self.out.append(Token('LET', TType.LET))
            self.out.append(Token(iter, TType.IDENT))
            self.out.append(Token('=', TType.EQ))
            self.out.append(Token(start, TType.NUMBER))
            self.out.append(Token('\n', TType.NEWLINE))

            self.out.append(Token('WHILE', TType.WHILE))
            self.out.append(Token(iter, TType.IDENT))
            self.out.append(token)
            self.out.append(Token(end, TType.NUMBER))
            self.out.append(Token('DO', TType.DO))
            self.out.append(Token('\n', TType.NEWLINE))

        else:
            self.push()
            self.advance()

class Filter:
    def __init__(self, tokenfile):
        parse = Translate(tokenfile)
        parse.program()
        parse.lexer.store = parse.out
        parse.lexer.write(tokenfile)


import sys
import enum
import csv
from collections import deque
from tok import *


# get tokens from file, already tokenized
class LoadTokens:
    def __init__(self, file):
        self.store = deque()

        # read tokens from file, put in temporary queue
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

    # pop element, return token from queue
    def gettoken(self):
        return self.store.popleft() if self.store else Token('', TType.EOF)


class Parser:
    def __init__(self, tokenfile):
        self.lexer = LoadTokens(tokenfile)
        self.out = deque()

        self.vars = [] # vars
        self.decl = [] # labels declared
        self.dest = [] # destinations of GOTO/GOSUB
        self.labelcounter = 0 # each label unique (increment counter)

        self.curr = self.lexer.gettoken()
        self.next = self.lexer.gettoken()

    def err(self, message):
        print("error:parse: " + message)
        sys.exit(1)

    def advance(self):
        self.curr = self.next
        self.next = self.lexer.gettoken()

    def recognize(self, type):
        return type == self.curr.type

    def expect(self, type):
        if not self.recognize(type):
            self.err("expected " + type.name + ", found " + self.curr.type.name)
        self.advance()

    def createlabel(self):
        self.labelcounter += 1
        label = 'LAB_' + str(self.labelcounter) + '-L'
        return label

    def newlabel(self):
        label = self.createlabel()
        while label in self.decl:
            label = self.createlabel()
        self.decl.append(label)
        return label

    def relop(self, op):
        if op == '<':
            return '\tLT\t'
        elif op == '>':
            return '\tGT\t'
        elif op == '<=':
            return '\tLQ\t'
        elif op == '>=':
            return '\tGQ\t'
        elif op == '=':
            return '\tEQ\t'
        elif op == '<>':
            return '\tNEQ\t'
        else:
            return None

    def eatspace(self):
        while self.recognize(TType.NEWLINE):
            self.advance()

    # entry and exit
    def program(self):
        self.out.append("START:")
        self.eatspace()
        while not self.recognize(TType.EOF):
            self.statement() # main dish
        self.out.append("END:")
        self.out.append("\tHALT")
        return self.out

    # spend most time looping through the stmts
    def statement(self):

        # LET identifier = expression
        if self.recognize(TType.LET):
            self.advance()
            if self.curr.text not in self.vars:
                self.vars.append(self.curr.text)
            store = str(self.vars.index(self.curr.text))
            self.expect(TType.IDENT)
            self.expect(TType.EQ)
            self.expression()
            self.out.append('\tSTORE\t' + store)

        # PRINT string or expression
        elif self.recognize(TType.PRINT):
            self.advance()
            if self.recognize(TType.STRING):
                string = self.curr.text
                self.advance()
                self.out.append(self.printstr(string))
            else:
                self.expression()
                self.out.append('\tPRINT')

        # GOTO label
        elif self.recognize(TType.GOTO):
            self.advance()
            label = self.curr.text
            self.dest.append(label)
            self.out.append('\tJP\t:' + label)
            self.expect(TType.IDENT)

        # ! label
        elif self.recognize(TType.EXCL):
            self.advance()
            label = self.curr.text
            if label in self.decl:
                self.err("label " + label + " exist")
            self.decl.append(label)
            self.out.append(label + ':')
            self.expect(TType.IDENT)

        # END
        elif self.recognize(TType.END):
            self.advance()
            self.out.append('\tHALT')

        # RETURN
        elif self.recognize(TType.RETURN):
            self.advance()
            self.out.append('\tRET')

        # IF condition THEN stmts {ELSE stmts} ENDIF
        elif self.recognize(TType.IF):
            self.advance()
            self.condition()
            labela = self.newlabel()
            self.out.append('\tJPZ\t:' + labela)
            self.expect(TType.THEN)
            self.eatspace()
            while True:
                if self.recognize(TType.ENDIF):
                    self.expect(TType.ENDIF)
                    self.out.append(labela + ':')
                    break
                if self.recognize(TType.ELSE):
                    self.expect(TType.ELSE)
                    labelb = self.newlabel()
                    self.out.append('\tJP\t:' + labelb)
                    self.out.append(labela + ':')
                    self.advance()
                    while not self.recognize(TType.ENDIF):
                        self.statement()
                    self.expect(TType.ENDIF)
                    self.out.append(labelb + ':')
                    break
                self.statement()

        # GOSUB label
        elif self.recognize(TType.GOSUB):
            self.advance()
            label = self.curr.text
            self.dest.append(label)
            self.out.append('\tCALL\t:' + label)
            self.expect(TType.IDENT)

        # WHILE condition DO stmts ENDWHILE
        elif self.recognize(TType.WHILE):
            self.advance()
            labela = self.newlabel()
            labelb = self.newlabel()
            self.out.append(labela + ':')
            self.condition()
            self.out.append('\tJPZ\t:' + labelb)
            self.expect(TType.DO)
            self.eatspace()
            while not self.recognize(TType.ENDWHILE):
                self.statement()
            self.out.append('\tJP\t:' + labela)
            self.expect(TType.ENDWHILE)
            self.out.append(labelb + ':')

        else:
            self.err("syntax error " + self.curr.text + \
            " (" + self.curr.type.name + ")")

        self.expect(TType.NEWLINE)
        self.eatspace()

    # helper: print string through emit
    def printstr(self, item):
        string = ''
        res = []
        for elem in item:
            res.extend(ord(n) for n in elem)
        for el in res:
            string += '\tSET\t' + str(el) + '\n'
            string += '\tEMIT\n'
        if not self.recognize(TType.SEMI):
            string += '\tSET\t10\n\tEMIT\n'
            string += '\tSET\t13\n\tEMIT'
        else:
            self.advance()
        return string

    # helper: condition
    def condition(self):
        self.expression()
        self.cmp()
        while self.curr.text in {'>', '>=', '<', '<=', '=', '<>'}:
            self.cmp()

    # helper helper: condition
    def cmp(self):
        comp = self.relop(self.curr.text)
        self.advance()
        self.expression()
        self.out.append(comp)

    def expression(self):
        self.term()
        sign = None

        while self.recognize(TType.PLUS) or \
                self.recognize(TType.MINUS):
            if self.recognize(TType.PLUS):
                sign = 'ADD'
            elif self.recognize(TType.MINUS):
                sign = 'SUB'
            self.advance()
            self.term()
            self.out.append('\t' + sign + '\t')

    def term(self):
        self.factor()
        sign = None

        while self.recognize(TType.ASTERISK) or \
                self.recognize(TType.SLASH):
            if self.recognize(TType.ASTERISK):
                sign = 'MUL'
            elif self.recognize(TType.SLASH):
                sign = 'DIV'
            self.advance()
            self.factor()
            self.out.append('\t' + sign + '\t')

    def factor(self):

        if self.recognize(TType.NUMBER):
            self.out.append("\tSET\t" + self.curr.text)
            self.advance()

        elif self.recognize(TType.IDENT):
            if self.curr.text not in self.vars:
                self.vars.append(self.curr.text)
                self.out.append("\tSET\t0")
                store = str(self.vars.index(self.curr.text))
                self.out.append('\tSTORE\t' + store)
            num = str(self.vars.index(self.curr.text))
            self.out.append("\tLOAD\t" + num)
            self.advance()

        elif self.recognize(TType.LPAREN):
            self.advance()
            self.expression()
            if not self.recognize(TType.RPAREN):
                self.err("expected ')' not found")
            self.advance()

        else:
            self.err("unrecognized token '" + self.curr.text + "'")


        '''
        raise ParseError(
            self.pos + 1,
            'Expected %s but got %s',
            'character' if chars is None else '[%s]' % chars,
            next_char
        )
        '''

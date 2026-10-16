import re
import sys
import getopt

TOKEN_SPECIFICATION = [
    ('NUMBER', r'\d+'),        # integer
    ('PLUS', r'\+'),           # addition
    ('MINUS', r'-'),           # subtraction
    ('TIMES', r'\*'),          # multiplication
    ('DIVIDE', r'/'),          # division
    ('LPAREN', r'\('),         # left parenthesis
    ('RPAREN', r'\)'),         # right parenthesis
    ('PERIOD', r'\.'),         # period
    ('SKIP', r'[ \t]+'),       # skip spaces, tabs
    ('MISMATCH', r'.'),        # any other character
]

EOF_TOKEN = ('EOF', None, -1, -1, -1, -1)

def lex(characters):
    tokens = []
    line_num = 1
    line_start = 0
    for mo in re.finditer('|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION), characters):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = int(value)
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            tokens.append(('ERROR', value, line_num, column, mo.start(), mo.end()))
            continue
        tokens.append((kind, value, line_num, column, mo.start(), mo.end()))
    return tokens

class Parser:
    def __init__(self, tokens, input_string):
        self.tokens = tokens
        self.input_string = input_string
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def error(self, message):
        token = self.current_token
        line_num = token[2]
        column = token[3]
        lines = self.input_string.splitlines()
        if line_num - 1 < len(lines):
            line = lines[line_num - 1]
            pointer = ' ' * column + '^'
        else:
            line = ""
            pointer = '^'
        suggestion = self.get_suggestion(token)
        raise Exception(f'Syntax error: {message} at line {line_num}, column {column}\n{line}\n{pointer}\nSuggestion: {suggestion}')

    def get_suggestion(self, token):
        if token[0] == 'PERIOD':
            return 'Expected end of expression or term. Check for missing operators or terms.'
        elif token[0] == 'NUMBER':
            return 'Check for missing operators or parentheses around numbers.'
        elif token[0] in ('PLUS', 'MINUS', 'TIMES', 'DIVIDE'):
            return 'Check for valid terms before or after the operator.'
        elif token[0] == 'LPAREN':
            return 'Check for matching closing parenthesis.'
        elif token[0] == 'RPAREN':
            return 'Check for matching opening parenthesis and correct expression inside.'
        else:
            return 'Check syntax near the indicated position.'

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = EOF_TOKEN
#            self.current_token = ('EOF', None, self.tokens[-1][2], self.tokens[-1][3] + 1, -1, -1)

    def expect(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()
        else:
            self.error(f'Expected {token_type}, got {self.current_token[0]}')

    def parse_expression(self):
        self.parse_term()
        while self.current_token[0] in ('PLUS', 'MINUS'):
            self.advance()
            self.parse_term()

    def parse_term(self):
        self.parse_factor()
        while self.current_token[0] in ('TIMES', 'DIVIDE'):
            self.advance()
            self.parse_factor()

    def parse_factor(self):
        if self.current_token[0] == 'NUMBER':
            self.advance()
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            self.parse_expression()
            self.expect('RPAREN')
        else:
            self.error('Expected number or parenthesis')

    def parse(self):
        self.parse_expression()
        self.expect('PERIOD')
        if self.current_token[0] != 'EOF':
            self.error('Unexpected tokens at the end')

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def check(code):
    tokens = lex(code)
    parser = Parser(tokens, code)
    try:
        parser.parse()
        print("Syntax is correct.")
    except Exception as e:
        print(e)

def main(argv):
    inputfile = ''

    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print('check.py -i <inputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('usage: check.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg

    code = read_file(inputfile)
    check(code)

if __name__ == "__main__":
   main(sys.argv[1:])

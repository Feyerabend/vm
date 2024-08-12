import re

# combinator parsers

def char(c):
    def parser(text, pos):
        if pos < len(text) and text[pos] == c:
            return c, pos + 1
        return None, pos
    return parser

def string(s):
    def parser(text, pos):
        end = pos + len(s)
        if text[pos:end] == s:
            return s, end
        return None, pos
    return parser

def regex(pattern):
    compiled = re.compile(pattern)
    def parser(text, pos):
        match = compiled.match(text, pos)
        if match:
            return match.group(0), match.end()
        return None, pos
    return parser

def sequence(*parsers):
    def parser(text, pos):
        results = []
        for p in parsers:
            res, pos = p(text, pos)
            if res is None:
                return None, pos
            results.append(res)
        return results, pos
    return parser

def choice(*parsers):
    def parser(text, pos):
        for p in parsers:
            res, pos = p(text, pos)
            if res is not None:
                return res, pos
        return None, pos
    return parser

def many(parser):
    def parse(text, pos):
        results = []
        while True:
            res, pos = parser(text, pos)
            if res is None:
                return results, pos
            results.append(res)
    return parse

def many1(parser):
    def parse(text, pos):
        results, pos = many(parser)(text, pos)
        if results:
            return results, pos
        return None, pos
    return parse

def between(opening, closing, parser):
    return sequence(opening, parser, closing)

def map_parser(parser, func):
    def parse(text, pos):
        res, pos = parser(text, pos)
        if res is None:
            return None, pos
        return func(res), pos
    return parse

def whitespace():
    return many(choice(char(' '), char('\t'), char('\n')))

# token parsers
digit = regex(r'[0-9]')
constant = map_parser(many1(digit), lambda d: int(''.join(d)))
variable = choice(string('x'), string('y'), string('z'))

def factor():
    return sequence(
        whitespace(),
        choice(between(char('('), char(')'), expression()),
               variable,
               constant),
        whitespace())

def term():
    def parse(text, pos):
        res, pos = factor()(text, pos)
        if res is None:
            return None, pos
        while True:
            op, pos = sequence(whitespace(), choice(string('*'), string('/')))(text, pos)
            if op is None:
                break
            right, pos = factor()(text, pos)
            if right is None:
                return None, pos
            res = (op, res, right)
        return res, pos
    return parse

def expression():
    def parse(text, pos):
        res, pos = term()(text, pos)
        if res is None:
            return None, pos
        while True:
            op, pos = sequence(whitespace(), choice(string('+'), string('-')))(text, pos)
            if op is None:
                break
            right, pos = term()(text, pos)
            if right is None:
                return None, pos
            res = (op, res, right)
        return res, pos
    return parse

# main
def parse_expression(expression_str):
    parser = expression()
    result, pos = parser(expression_str, 0)
    if pos != len(expression_str):
        raise ValueError(f"Parsing error at position {pos}.")
    return result


# back to infix
def convert_expression(expr):
    # remove extra quotes and brackets
    expr = expr.replace("'", "").replace("[", "").replace("]", "")
    
    # add spaces around operators
    expr = re.sub(r'([+\-*/()])', r' \1 ', expr)

    # replace comma with space
    expr = re.sub(r',\s*', ' ', expr)

    # no parenthesis or spaces
    expr = expr.replace("(", "").replace(")", "").replace(' ', '')

    return expr

def parse_prefix_expression(expr):
    if isinstance(expr, list):

        # nothing
        if len(expr) == 0:
            return ''

        # parse first
        if len(expr) == 1:
            return parse_prefix_expression(expr[0])

        # empty lists
        if isinstance(expr[0], list) and len(expr[0]) == 0:
            return parse_prefix_expression(expr[1])

        # make infix
        if len(expr) == 3 and expr[1] in ['+', '-', '*', '/']:
            operator = expr[1]
            left = parse_prefix_expression(expr[0])
            right = parse_prefix_expression(expr[2])
            return f'({left} {operator} {right})'

        # nested parentheses, recursion
        if expr[0] == '(' and expr[-1] == ')':
            inner_expr = parse_prefix_expression(expr[1:-1])
            return f'({inner_expr})'
        return ' '.join(parse_prefix_expression(subexpr) for subexpr in expr)

    elif isinstance(expr, str):
        return expr

    return str(expr)

# parse from prefix to infix
def prefix_infix(expr):
    stack = []
    i = len(expr) - 1
    while i >= 0:
        s = expr[i]
        if not s in ['+', '-', '*', '/', '(', ')']:
            stack.append(s)
        else:
            stack.append('(' + stack.pop() + s + stack.pop() + ')')
        i -= 1
    return stack.pop()


# evaluator
def evaluate_expression(expression_str, variable_values):
    # replace variable names with values
    for var, value in variable_values.items():
        expression_str = re.sub(rf'\b{var}\b', str(value), expression_str)
    # remove unnecessary spaces and evaluate
    expression_str = re.sub(r'\s+', ' ', expression_str).strip()
    try:
        return eval(expression_str) # scary
    except Exception as e:
        return str(e)

# sample run
if __name__ == "__main__":
    expr = "3 + 2 * (x - 4) / y"
    try:
        result = parse_expression(expr)
        print("Parsed result:", result)

        parsed_expr = parse_prefix_expression(result)
        converted_expr = convert_expression(parsed_expr)
        recon_expr = prefix_infix(converted_expr)
        print("Reconstructed expression:", recon_expr)

        evaluate = evaluate_expression(recon_expr, {'x': 5, 'y': 2})
        print("Evaluated result:", evaluate, "  with x = 5 and y = 2")

    except ValueError as e:
        print("Parsing error:", e)

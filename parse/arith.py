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


# main
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
            print(f"Term parsing failed at position {pos}")
            return None, pos
        results = [res]
        while True:
            op, pos = sequence(whitespace(), choice(string('*'), string('/')))(text, pos)
            if op is None:
                break
            res, pos = factor()(text, pos)
            if res is None:
                print(f"Term continuation parsing failed at position {pos}")
                return None, pos
            results.append((op, res))
        return results, pos
    return parse

def expression():
    def parse(text, pos):
        res, pos = term()(text, pos)
        if res is None:
            print(f"Expression parsing failed at position {pos}")
            return None, pos
        results = [res]
        while True:
            op, pos = sequence(whitespace(), choice(string('+'), string('-')))(text, pos)
            if op is None:
                break
            res, pos = term()(text, pos)
            if res is None:
                print(f"Expression continuation parsing failed at position {pos}")
                return None, pos
            results.append((op, res))
        return results, pos
    return parse

def parse_expression(expression_str):
    parser = expression()
    result, pos = parser(expression_str, 0)
    if pos != len(expression_str):
        raise ValueError(f"Parsing error at position {pos}.")
    return result


if __name__ == "__main__":
    expr = "3 + 2 * (x - 4) / y"
    try:
        result = parse_expression(expr)
        print("Parsed result:", result)
    except ValueError as e:
        print("Parsing error:", e)

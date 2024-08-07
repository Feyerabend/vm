# combinator parsers

The fundamental components of combinator parsers and their operations
can be formalized using concepts from *category theory* and *formal grammar
theory*.

### Mathematical formalism for 'Combinator Parsers'

#### *Basics*:

   - *Parser*: A parser is a function that, given an input string,
     returns a *set of possible parses*. Each parse is typically a
     pair consisting of the parsed result and the remaining unparsed
     portion of the input (pointing at a position in the remaining
     input).

   - *Combinator*: A combinator is a higher-order function that takes
     one or more parsers as arguments and returns *a new parser*.

#### *Formally defined parsers*:

   Let $\( P \)$ be a parser with the type signature:
   *P: Σ* → P(R × Σ*)*
   where $\( \Sigma^* \)$ is the set of all possible input strings,
   $\( \mathcal{R} \)$ is the set of parse results, and $\( \mathcal{P} \)$
   denotes the power set.

   This means that a parser $\( P \)$ takes an input string and
   returns a set of pairs. Each pair consists of a result and the
   remaining unparsed part of the input.

#### *Combinators*:

*Choice*:
The choice combinator $\( \text{alt} \)$ tries two parsers
and returns the result of the first successful parser.

```math
alt(P, Q) = λ s . filter results from (P(s) ∪ Q(s))
```

*Sequence*:
The sequence combinator $\( \text{seq} \)$ combines two
parsers such that the second parser is applied to the
remaining input after the first parser succeeds.

```math
seq(P, Q) = λ s . { (r1 ∘ r2, s'') | (r1, s') ∈ P(s) and (r2, s'') ∈ Q(s') }
```
where $\( \oplus \)$ denotes some combination of the results $\( r_1 \)$ and $\( r_2 \)$.

*Many*:
The many combinator $\( \text{many} \)$ applies a parser
zero or more times.

```math
many(P) = λ s . { (results, s') | results is a list of results from zero or more applications of P and s' is the remaining input }
```

*Many1*:
     The many1 combinator $\( \text{many1} \)$ applies a parser one or more times.
     \[
     \text{many1}(P) \text{ is defined as } \text{seq}(P, \text{many}(P))
     \]

   - *Option*:
     The option combinator \( \text{opt} \) applies a parser and returns a default value if the parser fails.
     \[
     \text{opt}(P, d) \text{ is defined as } \lambda s . \{ (r, s) \mid (r, s) \in P(s) \} \cup \{ (d, s) \mid \text{if } P(s) \text{ fails} \}
     \]

4. *Formal definitions using Category Theory*:

   In *category theory*, parsers can be modeled as functors between categories.
   For instance:

   - *Category of parsers*:
     - Objects: Parsers.
     - Morphisms: Combinators.

   - *Functorial composition*:
     - A parser combinator can be viewed as a functor that maps parsers to new
       parsers. For example, the sequence combinator is a functor that maps a
       pair of parsers to a new parser.



The mathematical formalism of combinator parsers involves defining parsers as
functions that map input strings to sets of parse results and remaining input
(position). Combinators are higher-order functions that combine parsers in
various ways. This formalism can be described using set theory, formal language
theory, and category theory.



## ebnf

Extended Backus-Naur Form (EBNF) is a notation used to express
context-free grammars, which are often used to describe the syntax
of languages. Let's write the EBNF for both the prefix expression
and the infix expression as described in the examples.

### prefix

Prefix notation (Polish notation) is where operators precede their
operands. The EBNF for the given prefix notation would look like this:

```ebnf
expression  ::= "(" operator expression expression ")" | operand
operator    ::= "+" | "-" | "*" | "/"
operand     ::= variable | number
variable    ::= "x" | "y"  // extend this to include other variable names if needed
number      ::= digit {digit}
digit       ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

### infix

Infix notation is the more conventional form where operators are
placed between operands. The EBNF for infix notation that corresponds
to the previous prefix examples would look like this:

```ebnf
expression  ::= term {("+" | "-") term}
term        ::= factor {("*" | "/") factor}
factor      ::= "(" expression ")" | operand
operand     ::= variable | number
variable    ::= "x" | "y"  // extend this to include other variable names if needed
number      ::= digit {digit}
digit       ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

### description

- *Prefix Notation EBNF*:
  - `expression` can be either an operator followed by two expressions enclosed in parentheses, or it can be an operand.
  - `operator` includes the basic arithmetic operators: `+`, `-`, `*`, and `/`.
  - `operand` can be either a variable or a number.
  - `variable` is restricted to `x` and `y` for simplicity, but this can be extended.
  - `number` consists of one or more digits.

- *Infix Notation EBNF*:
  - `expression` consists of `term` optionally followed by a sequence of `term`s separated by `+` or `-`.
  - `term` consists of `factor` optionally followed by a sequence of `factor`s separated by `*` or `/`.
  - `factor` can be an `expression` enclosed in parentheses or an `operand`.
  - `operand` can be either a variable or a number.
  - `variable` is restricted to `x` and `y` for simplicity, but this can be extended.
  - `number` consists of one or more digits.

These EBNF rules define the syntax of the prefix and infix expressions
as used in the examples, ensuring the correct structure and order of operations.

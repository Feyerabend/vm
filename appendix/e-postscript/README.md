# E: PostScript

<p align="center"><img src="samples/tree.svg" width="320" alt="a tree, drawn by a recursive PostScript procedure"></p>

In 1985 Apple's LaserWriter printer had a more powerful processor than
the Macintosh that sent it pages. It needed one: a page was not sent as
dots, but as a *program*, in Adobe's new language PostScript, and the
printer ran it. The same program printed the same page on any
PostScript printer, at whatever resolution it had. That promise,
device independence, is the promise of a virtual machine, made for
paper.

## The machine

PostScript is a stack machine, like ours, and its programs look like
assembly language for one, written backwards from what most languages
do:

```
3 4 add 5 mul =
```

Each number is pushed on the operand stack; `add` and `mul` pop two
and push the result; `=` pops and prints. But it is a far richer
machine. Its values are typed: numbers, strings, names, arrays,
dictionaries, and procedures, written in braces. And there is a second
stack, of *dictionaries*, where names get their meaning:

```
/square { dup mul } def
12 square =
```

`/square` is a literal name, and is pushed. `{ dup mul }` is a
procedure, and is pushed too, not run. `def` puts the name and the
procedure in the dictionary on top of the dictionary stack. When the
interpreter then meets the name `square`, it looks it up, finds a
procedure, and runs it.

`if`, `ifelse`, `for` and `repeat` are not syntax but operators, which
take procedures from the stack:

```
/fact {
    dup 2 lt
    { pop 1 }
    { dup 1 sub fact mul }
    ifelse
} def
```

[`ps.py`](ps.py) is an interpreter for a subset of PostScript, about
600 lines: the arithmetic, the stack, dictionaries, procedures,
control, arrays, strings for printing, and enough painting for paths,
fills and colour. It writes the painted page as an SVG file.

## Painting

The painting operators build a *path*, `moveto` and `lineto` and
`arc`, and then `stroke` or `fill` it. Every coordinate goes through
the *current transformation*, which `translate`, `rotate` and `scale`
change, and `gsave` and `grestore` save and bring back.

[`samples/tree.ps`](samples/tree.ps) draws the tree above with that
alone. A branch is a line; at its end the coordinate system is turned
and shrunk, and a smaller tree is drawn in it, twice. The program never
works out where any point is on the page, or how thick a twig should
be: the transformation does it, since the line width shrinks with the
scale. [`samples/star.ps`](samples/star.ps) draws one petal twelve
times, turning between each.

<p align="center"><img src="samples/star.svg" width="200" alt="twelve petals, from black to light gray"></p>

## Compared with ours

PostScript and our machine are both stack machines, but they differ
in when a name gets its meaning. Our assembler turns every label into
an address before the program runs, and chapter 10's compiler turns
every variable into a memory address. PostScript looks a name up in
the dictionary stack each time it is run. In
[`samples/calc.ps`](samples/calc.ps), `fourth` is defined as
`square square`; after `square` is redefined, `fourth` does something
else. This is *dynamic binding*: flexible, and slow, since every name
is a search.

A procedure is just an array of objects, kept as data until something
runs it, so a PostScript program can build, print and change its own
procedures. And because the program is text, read and run token by
token, there is no compile step at all.

Its errors will look familiar. `stackunderflow`, `typecheck`,
`rangecheck`, `undefinedresult` for division by zero: the traps of
chapters 4 and 13, under other names. Typed values, checked on every
operation, are what chapter 13's tags were for.

PostScript's descendant, PDF, made the opposite choice. A PDF page is a
description, not a program: the painting operators are kept, and the
loops, procedures and dictionaries are gone. A program can take any
time to run, or never finish, and a document reader should not have
to run one to show a page.

## Run it

```
make test
python3 ps.py samples/calc.ps
python3 ps.py samples/tree.ps tree.svg
```

The page size comes from the `%%BoundingBox:` comment, as printers
took it. Any web browser shows the SVG.
[`archive/ps`](../../archive/ps) has another interpreter for a smaller
subset, in JavaScript, which paints on a canvas in the browser.

## Exercises

1. Add `curveto`, which draws a Bézier curve. SVG has the same curve,
   so it can be passed straight through, after the transformation.
   (An arc can be made of curves too, as real PostScript does.)
2. Add `show`, to paint text: `/Helvetica findfont 12 scalefont setfont`
   and then `(Hello) show`. How should a font get into the SVG?
3. Real PostScript has `bind`, which replaces each name in a procedure
   with the operator it names now, once. Implement it, and measure
   `samples/tree.ps` with and without. Which names must not be bound?
4. Write a small PostScript program that prints a table of the
   squares and cubes of 1 to 10, right-aligned, using only `=`,
   `print`, `cvs` and `string`.

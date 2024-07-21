# Virtual Machines

[PostScript](POSTSCRIPT.md) is a versatile, widely-used page
description language and __programming language__ specifically
designed for creating graphics but also fancy "typographical"
(or typeset) text. As it is a programmming language, it is also
Turing complete. It operates *as a* virtual machine, which allows
for device-independent graphics rendering, meaning it can produce
*consistent results across different printers and displays*.
Although finding general-purpose graphics APIs in languages like
Python or C can be challenging and uncommon[^h], JavaScript’s
Canvas API stands out as a robust and accessible platform for
rendering vector graphics. This makes it an excellent choice for
those seeking functionality similar to PostScript. Therefore,
implementing a simple PostScript interpreter in JavaScript using
the Canvas API is both practical and straightforward.[^rip]

[^h]: This is especially relevant for our goal of being as
universally applicable as possible, selecting programming
languages that require minimal installations, additional
tools, or dependencies.

[^rip]: As most outputs are today based on dots or pixels,
somewhere the vectors have to be translated. In a laser printer
this is traditionally done through a RIP, a raster image processor
(https://en.wikipedia.org/wiki/Raster_image_processor).
Finding out how to draw a line, it calculates where to draw the
dot next looping through all the possible dots of the vector line.
A vector graphics display or a graphics plotter would on the other
hand, would probably be an easier conversion.

![Make and move ps for view](../assets/images/moveps.png)

### psmaker

Your web browser may almost certainly support viewing local HTML
pages. Open the `psmaker.html` with a browser and draw something,
choosing between lines, rectangles and circles -- to make things
easy. Nothing fancy here, to keep to simple code and clear aim.

Generate PostScript with the click of the button. Copy the result
and ..

### psviewer

.. open the web browser with the HTML page `psviewer.html`, then
paste the result in the textbox. The result should look like the
drawing you made in `psmaker.html`.


### the vm in psviewer

The `interpretPostScript` function in `psviewer.html` parses and
interprets a simplified PostScript-like script to draw on an HTML
canvas. The function reads commands from the script, manipulates
a stack for operand storage, and issues drawing commands to the
canvas context (`ctx`).


#### Stack

```javascript
   const stack = [];
```
A stack is used to store operands (numbers) for PostScript commands.

#### Commands

```javascript
   const commands = script.split('\n').flatMap(line => line.trim().split(/\s+/));
```
The input script is split into lines, and each line is further
split into commands and operands, creating an array of tokens.

#### Interpretation

```javascript
   commands.forEach(command => {
       if (!isNaN(command)) {
           stack.push(parseFloat(command)); // push number
       } else {
           switch (command) {
               ..
           }
       }
   });
```

Each token is processed in turn:
- If the token is a number, it is pushed onto the stack.
- If the token is a command, it is interpreted through
a `switch` statement.

#### newpath

```javascript
  case 'newpath':
      ctx.beginPath(); // new path
      break;
```
Starts a new path on the canvas.

#### moveto

```javascript
  case 'moveto':
      const yMove = stack.pop();
      const xMove = stack.pop();
      ctx.moveTo(xMove, yMove); // move to new point
      break;
```
Moves the drawing cursor to a new point without
drawing a line. The coordinates are popped from
the stack.

#### lineto

```javascript
  case 'lineto':
      const yLine = stack.pop();
      const xLine = stack.pop();
      ctx.lineTo(xLine, yLine); // draw line to new point
      break;
```
Draws a line from the current position to a new
point, with coordinates taken from the stack.

#### rect

```javascript
  case 'rect':
      const height = stack.pop();
      const width = stack.pop();
      const yRect = stack.pop();
      const xRect = stack.pop();
      ctx.rect(xRect, yRect, width, height); // draw rectangle
      break;
```
Draws a rectangle with the specified width, height,
and position.

#### arc

```javascript
  case 'arc':
      const endAngle = stack.pop() * (Math.PI / 180); // to radians
      const startAngle = stack.pop() * (Math.PI / 180); // to radians
      const radi = stack.pop();
      const yArc = stack.pop();
      const xArc = stack.pop();
      ctx.arc(xArc, yArc, radi, startAngle, endAngle); // draw arc
      break;
```
Draws an arc with the given center, radius, and
angles (converted from degrees to radians).

#### closepath

```javascript
  case 'closepath':
      ctx.closePath(); // close current path
      break;
```
Closes the current path by drawing a straight line
back to the starting point.

#### gsave / grestore

```javascript
  case 'gsave':
      graphicsStateStack.push({
          lineWidth: ctx.lineWidth,
          fillStyle: ctx.fillStyle,
          strokeStyle: ctx.strokeStyle
      });
      break;
  case 'grestore':
      if (graphicsStateStack.length > 0) {
          const state = graphicsStateStack.pop();
          ctx.lineWidth = state.lineWidth;
          ctx.fillStyle = state.fillStyle;
          ctx.strokeStyle = state.strokeStyle;
      }
      break;
```
`gsave` saves the current graphics state onto
a stack, while `grestore` restores the most
recently saved state.

#### setlinewidth

```javascript
  case 'setlinewidth':
      const linewidth = stack.pop();
      ctx.lineWidth = linewidth; // set line width
      break;
```
Sets the line width for subsequent drawing commands.

#### setgray

```javascript
  case 'setgray':
      const grayValue = stack.pop();
      ctx.fillStyle = `rgba(${grayValue * 255}, ${grayValue * 255}, ${grayValue * 255}, 1)`;
      ctx.strokeStyle = ctx.fillStyle; // set stroke color to same gray
      break;
```
Sets the fill and stroke color to a shade of gray
based on the given value (0 to 1).

#### fill / stroke

```javascript
  case 'fill':
      ctx.fill(); // fill current path
      break;
  case 'stroke':
      ctx.stroke(); // render path
      break;
```
`fill` fills the current path with the current
fill color, while `stroke` renders the path
outline with the current stroke color.

#### showpage

```javascript
  case 'showpage':
      // no-op for this impl.
      break;
```
A no-op in this implementation, typically used
to finalize and display the page in PostScript.
It is also dropped in ESP[^eps] when more documents
are glued together, as it renders which makes
the rest of the document (if there is) obsolete
as the rest is not rendered.

[^eps]: https://en.wikipedia.org/wiki/Encapsulated_PostScript

### integration with HTML

The function `interpret` is designed to be
triggered by a button to process the input
PostScript code from a textarea:

```javascript
function interpret() {
    const postScript = document.getElementById('input').value;
    interpretPostScript(postScript);
}
```
This function reads the PostScript code from
a textarea elemen with id `input`, and then
calls `interpretPostScript` to render it on
the canvas.

### changing the coordinate system

As PostScript has a different coordintate system
than Canvas, some convertions has to be made.
The initial coordinate system for PostScript has
the x axis to the right and y axis upwards, the
origin is located at the bottom left hand corner
of the page. Canvas on the other hand, has the
upper-left corner of the screen as origin, so x
and y goes instead downwards increasing their
values.

So one way to handle this is to do what can be
seen in `psmaker.html` where each point gets
transformed easily through an 'arithmetical
geometry' process, while in `psviewer.html`
the whole canvas is transformed before drawing
through rather standard rotations and flipping
through 2D matrices. They may have different
results partly due to such things as precision
in numbers when calculating.

## postscript: the language

> The three most important aspects of the PostScript programming
> language are that it is *interpreted*, that it is *stack-based*,
> and that it uses a unique data structure called a *dictionary*.[^design]

[^design]: Reid, Glenn C., *PostScript language program design*,
Addison-Wesley, Reading, Mass., 1988, p.2.

PostScript’s interpreted nature parallels the concept of virtual
machines introduced in computing, where execution doesn’t rely on
binary or bytecode representations. Instead it directly interprets
*source code*. In PostScript, the source code serves a role akin
to our familiar *bytecodes* in other contexts.

PostScript employs multiple *stacks*—general, graphics, dictionary,
etc.—alongside a dictionary reminiscent of *procedures* seen in other
languages. This setup allows named entities to be invoked and yield
results.

When PostScript source code is transported and interpreted, or along
the line rasterized, it’s notable that the program’s text isn’t manually
crafted by a programmer. Instead, it’s typically *generated* by software
like PageMaker. Indeed, while programmers can write in PostScript, it's
not typically practical to manually create complex documents such as
book layouts directly in PostScript unless the goal is to build a rasterizer,
debugger, driver, or similar tool. For creating professional layouts
efficiently, designers would use specialized software like InDesign,
QuarkXPress, PageMaker, Illustrator, or similar tools tailored for graphic
design and publishing. These applications provide user-friendly interfaces
and powerful features that streamline the layout and design process,
offering more efficient workflows compared to manually coding in PostScript.

### samples

As there are over 250 commands (instructions) in PostScript,
there are a lot to go through, but as this is not a reference
manual, we will though take some illustrative and simple examples.
Test the following with `psviewer.html`.

You might recognize how numbers are added or substracted for
instance, leaving its result on the stack.

```postscript
40 67 add
90 543 sub
```

To swap the two top numbers on the stack, instead of `swap` we
used previously, it is here called `exch` for 'exchange'.

```postscript
23 90 exch
````

The stack would be '90 23' after the operation. But mostly
it is naturally for graphics.

```postscript
%!PS
newpath
100 200 moveto
200 450 lineto
stroke
showpage
```

Draws a from left to right a steep line. It starts from where
the point of deeparture is set with `moveto` which uses the
two top numbers from the stack. Next two other numbers are put
on the stack and the line is drawn starting from 
`moveto` to where it ends with `lineto`. The line itself
is determined by `stroke` (there can be other commands here).

```postscript
%!PS
newpath
100 200 moveto
200 450 lineto
100 400 lineto
closepath
3 setlinewidth
0.5 setgray
stroke
showpage
```

This draws a triangle but with a slightly gray stroke which have
a thickness of 3. It also ends all the 'legs' by connecting the
last `lineto` with the start of `moveto` by `closepath`.


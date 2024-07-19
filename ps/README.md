# Virtual Machines

[PostScript](POSTSCRIPT.md) is a versatile and widely-used page
description language and programming language specifically designed
for creating graphics but also fancy "typographical" text.
It operates *as a* virtual machine, which allows
for device-independent graphics rendering, meaning it can produce
*consistent results across different printers and displays*.
Although general APIs for graphics in languages like Python or C
are hard to come by and not very common, JavaScript’s Canvas API
offers a reasonable robust and accessible platform for rendering
vector graphics similar to PostScript. Therefore, implementing a
simple PostScript interpreter in JavaScript using the Canvas API
is both practical and effective.


### psmaker

Your web browser may almost certainly support viewing local HTML pages.
Open the `psmaker.html` with a browser and draw something, choosing between
lines, rectangles and circles -- to make things easy. Nothing fancy
here, to keep to simple code and clear aim.

Generate PostScript with the click of the button. Copy the result and ..

### psviewer

.. open the web browser with the HTML page `psviewer.html`, then paste
the result in the textbox. The result should look like the drawing you
made in `psmaker.html`.


### the vm in psviewer

The `interpretPostScript` function in `psviewer.html` parses and interprets
a simplified PostScript-like script to draw on an HTML canvas. The function
reads commands from the script, manipulates a stack for operand storage,
and issues drawing commands to the canvas context (`ctx`).


#### Stack

```javascript
   const stack = [];
```
A stack is used to store operands (numbers) for PostScript commands.

#### Commands

```javascript
   const commands = script.split('\n').flatMap(line => line.trim().split(/\s+/));
```
The input script is split into lines, and each line is further split into
commands and operands, creating an array of tokens.

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
Moves the drawing cursor to a new point without drawing a line.
The coordinates are popped from the stack.

#### lineto

```javascript
  case 'lineto':
      const yLine = stack.pop();
      const xLine = stack.pop();
      ctx.lineTo(xLine, yLine); // draw line to new point
      break;
```
Draws a line from the current position to a new point,
with coordinates taken from the stack.

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
Draws an arc with the given center, radius, and angles (converted
from degrees to radians).

#### closepath

```javascript
  case 'closepath':
      ctx.closePath(); // close current path
      break;
```
Closes the current path by drawing a straight line back to the
starting point.

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
`gsave` saves the current graphics state onto a stack,
while `grestore` restores the most recently saved state.


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
`fill` fills the current path with the current fill color,
while `stroke` renders the path outline with the current stroke color.


#### showpage

```javascript
  case 'showpage':
      // no-op for this impl.
      break;
```
A no-op in this implementation, typically used to finalize and
display the page in PostScript. It is also dropped in PDF when
more documents are glued together, as it renders which makes
the rest of the document (if there is) obsolete as the rest
is not rendered.


### Integration with HTML

The function `interpret` is designed to be triggered by a button
to process the input PostScript code from a textarea:

```javascript
function interpret() {
    const postScript = document.getElementById('input').value;
    interpretPostScript(postScript);
}
```
This function reads the PostScript code from a textarea elemen
with id `input`, and then calls `interpretPostScript` to render
it on the canvas.

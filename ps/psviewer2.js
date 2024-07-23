// global init of canvas ..
let canvas, ctx

canvas = document.getElementById('canvas');
ctx = canvas.getContext('2d');

ctx.translate(0, canvas.height);
ctx.scale(1, -1);

// other globals
let graphicsStateStack, dictionaryStack, logArea, currentX, currentY;


function initialize() {
    graphicsStateStack = [];
    dictionaryStack = [{}];

    currentX = 0;
    currentY = 0;

    logArea = document.getElementById('log');
    logArea.value = '';
}

function log(message) {
    logArea.value += message + '\n';
}

function logStack(stack) {
    log(`Current stack: [${stack.join(', ')}] (Length: ${stack.length})`);
}

function interpret() {
    const postScript = document.getElementById('input').value;
    initialize();
    let definitions = {};
    collectDefinitions(postScript, definitions);
    executeScript(postScript, definitions);
}

function collectDefinitions(script, definitions) {
    const commands = script.split('\n').flatMap(line => line.trim().split(/\s+/));
    let inDef = false;
    let defName = '';
    let defCommands = [];

    commands.forEach(command => {
        if (inDef) {
            if (command === '}') {
                definitions[defName] = defCommands.join(' ');
                log(`Defined name: ${defName}`);
                log(`        commands: ${definitions[defName]}`);
                defName = '';
                defCommands = [];
                inDef = false;
            } else {
                defCommands.push(command);
            }
        } else if (command.startsWith('/')) {
            defName = command.substring(1);
            inDef = true;
            log(`Starting definition of: ${defName}`);
        }
    });
    log(`- - - - -`);
}

function executeScript(script, definitions) {
    const stack = [];
    const commands = script.split('\n').flatMap(line => line.trim().split(/\s+/));

    commands.forEach(command => {
        if (!isNaN(command)) {
            stack.push(parseFloat(command));
            log(`Pushed number (execute): ${command}`);
        } else if (definitions[command]) {
            log(`Executing defined: ${command}`);
            interpretDefined(definitions[command], stack);
        } else {
            executeGraphicsCommand(command, stack);
        }
        logStack(stack);
    });
}

function interpretDefined(script, stack) {
    const commands = script.split(' ');

    commands.forEach(command => {
        if (!isNaN(command)) {
            stack.push(parseFloat(command));
            log(`Pushed number (defined): ${command}`);
        } else {
            executeGraphicsCommand(command, stack);
        }
    });
}

function executeGraphicsCommand(command, stack) {
    log(`Executing command: ${command}`);
    switch (command) {

        case 'newpath':
            ctx.beginPath();
            break;

        case 'moveto':
            const yMove = stack.pop();
            const xMove = stack.pop();
            ctx.moveTo(xMove, yMove);
            currentX = xMove;
            currentY = yMove;
            log(`Moved to: (${xMove}, ${yMove})`);
            break;

        case 'rlineto':
            const yRelLine = stack.pop();
            const xRelLine = stack.pop();
            ctx.lineTo(currentX + xRelLine, currentY + yRelLine);
            currentX += xRelLine;
            currentY += yRelLine;
            log(`Relative line to: (${currentX}, ${currentY})`);
            break;

        case 'lineto':
            const yLine = stack.pop();
            const xLine = stack.pop();
            ctx.lineTo(xLine, yLine);
            currentX = xLine;
            currentY = yLine;
            log(`Line to: (${xLine}, ${yLine})`);
            break;

        case 'arc':
            const endAngle = stack.pop() * (Math.PI / 180);
            const startAngle = stack.pop() * (Math.PI / 180);
            const radius = stack.pop();
            const yArc = stack.pop();
            const xArc = stack.pop();
            ctx.arc(xArc, yArc, radius, startAngle, endAngle);
            log(`Arc with center: (${xArc}, ${yArc}), radius: ${radius}, startAngle: ${startAngle}, endAngle: ${endAngle}`);
            break;

        case 'closepath':
            ctx.closePath();
            log('Path closed');
            break;

        case 'gsave':
            saveGraphicsState();
            log('Graphics state saved');
            break;

        case 'grestore':
            restoreGraphicsState();
            log('Graphics state restored');
            break;

        case 'setlinewidth':
            const lineWidth = stack.pop();
            ctx.lineWidth = lineWidth;
            log(`Line width set to: ${lineWidth}`);
            break;

        case 'setgray':
            const grayValue = stack.pop();
            ctx.fillStyle = ctx.strokeStyle = `rgba(${grayValue * 255}, ${grayValue * 255}, ${grayValue * 255}, 1)`;
            log(`Gray color set to: ${grayValue}`);
            break;

        case 'setrgbcolor':
            const b = stack.pop() * 255;
            const g = stack.pop() * 255;
            const r = stack.pop() * 255;
            ctx.fillStyle = ctx.strokeStyle = `rgba(${r}, ${g}, ${b}, 1)`;
            log(`RGB color set to: (${r}, ${g}, ${b})`);
            break;

        case 'fill':
            ctx.fill();
            log('Filled current path');
            break;

        case 'stroke':
            ctx.stroke();
            log('Stroked current path');
            break;

        case 'translate':
            const yTranslate = stack.pop();
            const xTranslate = stack.pop();
            ctx.translate(xTranslate, yTranslate);
            currentX += xTranslate;
            currentY += yTranslate;
            log(`Translated by: (${xTranslate}, ${yTranslate})`);
            break;

        case 'scale':
            const yScale = stack.pop();
            const xScale = stack.pop();
            ctx.scale(xScale, yScale);
            log(`Scaled by: (${xScale}, ${yScale})`);
            break;

        case 'showpage':
            log('Showpage (no-op)');
            break;

        case '#!PS':
            log('PostScript header (no-op)');
            break;
    }
}

function saveGraphicsState() {
    graphicsStateStack.push({
        lineWidth: ctx.lineWidth,
        fillStyle: ctx.fillStyle,
        strokeStyle: ctx.strokeStyle,
        transform: ctx.getTransform(),
        currentX: currentX,
        currentY: currentY
    });
}

function restoreGraphicsState() {
    if (graphicsStateStack.length > 0) {
        const state = graphicsStateStack.pop();
        ctx.lineWidth = state.lineWidth;
        ctx.fillStyle = state.fillStyle;
        ctx.strokeStyle = state.strokeStyle;
        ctx.setTransform(state.transform);
        currentX = state.currentX;
        currentY = state.currentY;
    }
}
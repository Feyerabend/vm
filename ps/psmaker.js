const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;
let tool = 'line';
let startX, startY;
const shapes = [];

function setTool(selectedTool) {
    tool = selectedTool;
}

function startDraw(e) {
    drawing = true;
    startX = e.offsetX;
    startY = e.offsetY;
}

function draw(e) {
    if (!drawing) return;

    const currentX = e.offsetX;
    const currentY = e.offsetY;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    redrawShapes();

    ctx.beginPath();
    if (tool === 'line') {
        ctx.moveTo(startX, startY);
        ctx.lineTo(currentX, currentY);

    } else if (tool === 'rectangle') {
        ctx.rect(startX, startY, currentX - startX, currentY - startY);

    } else if (tool === 'circle') {
        const radius = Math.sqrt((currentX - startX) ** 2 + (currentY - startY) ** 2);
        ctx.arc(startX, startY, radius, 0, 2 * Math.PI);
    }
    ctx.stroke();
}

function endDraw(e) {
    if (!drawing) return;

    drawing = false;
    const endX = e.offsetX;
    const endY = e.offsetY;

    let shape = {};
    if (tool === 'line') {
        shape = { type: 'line', startX, startY, endX, endY };

    } else if (tool === 'rectangle') {
        shape = { type: 'rectangle', startX, startY, width: endX - startX, height: endY - startY };

    } else if (tool === 'circle') {
        const radius = Math.sqrt((endX - startX) ** 2 + (endY - startY) ** 2);
        shape = { type: 'circle', centerX: startX, centerY: startY, radius };
    }
    shapes.push(shape);
    ctx.__currentPath = [];
}

function redrawShapes() {
    for (const shape of shapes) {
        ctx.beginPath();

        if (shape.type === 'line') {
            ctx.moveTo(shape.startX, shape.startY);
            ctx.lineTo(shape.endX, shape.endY);

        } else if (shape.type === 'rectangle') {
            ctx.rect(shape.startX, shape.startY, shape.width, shape.height);

        } else if (shape.type === 'circle') {
            ctx.arc(shape.centerX, shape.centerY, shape.radius, 0, 2 * Math.PI);
        }
        ctx.stroke();
    }
}

function generatePostScript() {
    let psCode = "%!PS-Adobe-3.0\n";
    for (const shape of shapes) {
        if (shape.type === 'line') {
            psCode += `${shape.startX} ${canvas.height - shape.startY} moveto ${shape.endX} ${canvas.height - shape.endY} lineto stroke\n`;
        } else if (shape.type === 'rectangle') {
            psCode += `${shape.startX} ${canvas.height - shape.startY} moveto\n`;
            psCode += `${shape.startX + shape.width} ${canvas.height - shape.startY} lineto\n`;
            psCode += `${shape.startX + shape.width} ${canvas.height - (shape.startY + shape.height)} lineto\n`;
            psCode += `${shape.startX} ${canvas.height - (shape.startY + shape.height)} lineto\n`;
            psCode += "closepath stroke\n";
        } else if (shape.type === 'circle') {
            psCode += `newpath ${shape.centerX} ${canvas.height - shape.centerY} ${shape.radius} 0 360 arc closepath stroke\n`;
        }
    }
    // document.getElementById('postscript-output').innerText = psCode;
    document.getElementById('postscript-output').value = psCode;
}

canvas.addEventListener('mousedown', startDraw);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', endDraw);
canvas.addEventListener('mouseleave', endDraw);
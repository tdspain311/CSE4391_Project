var canvas;
var gl;

var Vertices_Buffer;
//var VerticesColorBuffer;
var cubeVerticesIndexBuffer;
var Rotation = 0.0;
//var XOffset = 0.0;
//var YOffset = 0.0;
//var Offset = 0.0;
//var lastUpdateTime = 0;
//var xIncValue = 0.2;
//var yIncValue = -0.4;
//var zIncValue = 0.3;

var mvMatrix;
var shaderProgram;
var vertexPositionAttribute;
//var vertexColorAttribute;
var perspectiveMatrix;

// start
// Called when the canvas is created to get started
function start()
{
    canvas = document.getElementById("glcanvas");
    initWebGL(canvas);      // Initialize the GL context
    // Only continue if WebGL is available and working
    if (gl)
    {
        gl.clearColor(0.0, 0.0, 0.0, 1.0);  // Clear to black, fully opaque
        gl.clearDepth(1.0);                 // Clear everything
        gl.enable(gl.DEPTH_TEST);           // Enable depth testing
        gl.depthFunc(gl.LEQUAL);            // Near things obscure far things

        // Initialize the shaders; this is where all the lighting for the
        // vertices and so forth is established.
        initShaders();
        // Here's where we call the routine that builds all the objects
        // we'll be drawing.
        initBuffers();
        // Set up to draw the scene periodically.
        setInterval(drawScene, 15); // 15 milliseconds
    }
}


// initWebGL
// Initialize WebGL, returning the GL context or null if
// WebGL isn't available or could not be initialized.
function initWebGL() {
    gl = null;
    try {
        gl = canvas.getContext("experimental-webgl");
        gl.viewportWidth = canvas.width/2;
        gl.viewportHeight = canvas.height/2;
    }
    catch(e) {
    }
    // If we don't have a GL context, give up now
    if (!gl) {
        alert("Unable to initialize WebGL. Your browser may not support it.");
    }
}

// initBuffers
// Initialize the buffers we'll need.
function initBuffers()
{
    // Create a buffer for the cube's vertices.
    Vertices_Buffer = gl.createBuffer();

    // Select the Vertices_Buffer as the one to apply vertex
    // operations to from here out.
    gl.bindBuffer(gl.ARRAY_BUFFER, Vertices_Buffer);

    // Now create an array of vertices for the cube.
    var vertices = [
        0, 0, 0,
        1, 0, 0,
        0, 1, 0,
        1, 1, 0,
        0.5, 0.5, 1
    ];

    // Now pass the list of vertices into WebGL to build the shape. We
    // do this by creating a Float32Array from the JavaScript array,
    // then use it to fill the current vertex buffer.
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);

    Vertices_Buffer.itemSize = 3;
    Vertices_Buffer.numItems = 5;
    // Now set up the colors for the faces. We'll use solid colors
    // for each face.

    var colors = [
        1.0, 0.0, 0.0, 1.0,
        0.0, 1.0, 0.0, 1.0,
        0.0, 0.0, 1.0, 1.0,

        // Right face
        1.0, 0.0, 0.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 1.0, 0.0, 1.0,

        // Back face
        1.0, 0.0, 0.0, 1.0,
        0.0, 1.0, 0.0, 1.0,
        0.0, 0.0, 1.0, 1.0,

        // Left face
        1.0, 0.0, 0.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 1.0, 0.0, 1.0
        //[1.0,  1.0,  1.0,  1.0],    // Front face: white
        //[1.0,  0.0,  0.0,  1.0],    // Back face: red
        //[0.0,  1.0,  0.0,  1.0],    // Top face: green
        //[0.0,  0.0,  1.0,  1.0],    // Bottom face: blue
        //[1.0,  1.0,  0.0,  1.0],    // Right face: yellow
        //[1.0,  0.0,  1.0,  1.0]     // Left face: purple
    ];
    //
    //// Convert the array of colors into a table for all the vertices.
    //var generatedColors = [];
    //for (j=0; j<6; j++)
    //{
    //    var c = colors[j];
    //    // Repeat each color four times for the four vertices of the face
    //    for (var i=0; i<4; i++)
    //    {
    //        generatedColors = generatedColors.concat(c);
    //    }
    //}
    //
    VerticesColorBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, VerticesColorBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colors), gl.STATIC_DRAW);
    VerticesColorBuffer.itemsize = 4;
    VerticesColorBuffer.numItems = 12;


    // Build the element array buffer; this specifies the indices
    // into the vertex array for each face's vertices.
    cubeVerticesIndexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, cubeVerticesIndexBuffer);

    // This array defines each face as two triangles, using the
    // indices into the vertex array to specify each triangle's
    // position.

    // THESE ARE MY FACES AND THIS IS WHERE I WOULD HAVE TO MODIFY MY PROGRAM

    var faces = [
        3, 1, 0,
        2, 3, 0,
        1, 4, 0,
        4, 2, 0,
        1, 3, 4,
        2, 4, 3
    ]

    // Now send the element array to GL
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(faces), gl.STATIC_DRAW);
}

// drawScene
// Draw the scene.
function drawScene()
{
    // Clear the canvas before we start drawing on it.
    gl.viewport(0, 0, gl.viewportWidth, gl.viewportHeight);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // Establish the perspective with which we want to view the
    // scene. Our field of view is 45 degrees, with a width/height
    // ratio of 640:480, and we only want to see objects between 0.1 units
    // and 100 units away from the camera.

    perspectiveMatrix = makePerspective(45, 640.0/480.0, 0.1, 100.0);

    // Set the drawing position to the "identity" point, which is
    // the center of the scene.
    loadIdentity();

    // Now move the drawing position a bit to where we want to start
    // drawing the cube.
    mvTranslate([-1.5, 0.0, -6.0]);

    // Save the current matrix, then rotate before we draw.
    mvPushMatrix();
    mvRotate(Rotation, [1, 0, 1]);
    //mvTranslate([cubeXOffset, cubeYOffset, cubeZOffset]);

    // Draw the cube by binding the array buffer to the cube's vertices
    // array, setting attributes, and pushing it to GL.
    gl.bindBuffer(gl.ARRAY_BUFFER, Vertices_Buffer);
    gl.vertexAttribPointer(vertexPositionAttribute, 3, gl.FLOAT, false, 0, 0);

    // Set the colors attribute for the vertices.
    //gl.bindBuffer(gl.ARRAY_BUFFER, cubeVerticesColorBuffer);
    //gl.vertexAttribPointer(vertexColorAttribute, 4, gl.FLOAT, false, 0, 0);

    // Draw the cube.
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, cubeVerticesIndexBuffer);
    setMatrixUniforms();
    // the number 18 comes from the n*m of the faces
    gl.drawElements(gl.TRIANGLES, 18, gl.UNSIGNED_SHORT, 0 );
   //gl.drawArrays(gl.TRIANGLES, 0, 3);

    // Restore the original matrix
    //mvPopMatrix();

    // Update the rotation for the next draw, if it's time to do so.
    //var currentTime = (new Date).getTime();
    //if (lastCubeUpdateTime) {
    //    var delta = currentTime - lastCubeUpdateTime;
    //    cubeRotation += (30 * delta) / 1000.0;
    //    cubeXOffset += xIncValue * ((30 * delta) / 1000.0);
    //    cubeYOffset += yIncValue * ((30 * delta) / 1000.0);
    //    cubeZOffset += zIncValue * ((30 * delta) / 1000.0);
    //
    //    if (Math.abs(cubeYOffset) > 2.5) {
    //        xIncValue = -xIncValue;
    //        yIncValue = -yIncValue;
    //        zIncValue = -zIncValue;
    //    }
    //}
    //
    //lastCubeUpdateTime = currentTime;
}


// initShaders
// Initialize the shaders, so WebGL knows how to light our scene.
function initShaders()
{
    var fragmentShader = getShader(gl, "shader-fs");
    var vertexShader = getShader(gl, "shader-vs");

    // Create the shader program
    shaderProgram = gl.createProgram();
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);

    // If creating the shader program failed, alert
    if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS))
    {
        alert("Unable to initialize the shader program.");
    }

    // now use the shader program
    gl.useProgram(shaderProgram);

    // defines the vertex position attribute
    vertexPositionAttribute = gl.getAttribLocation(shaderProgram, "aVertexPosition");
    gl.enableVertexAttribArray(vertexPositionAttribute);

    // defines the color attribute
    //vertexColorAttribute = gl.getAttribLocation(shaderProgram, "aVertexColor");
    //gl.enableVertexAttribArray(vertexColorAttribute);
}

// getShader
// Loads a shader program by scouring the current document,
// looking for a script with the specified ID.
function getShader(gl, id)
{
    var shaderScript = document.getElementById(id);
    // Didn't find an element with the specified ID; abort.
    if (!shaderScript)
    {
        return null;
    }

    // Walk through the source element's children, building the
    // shader source string.
    var theSource = "";
    var currentChild = shaderScript.firstChild;

    while(currentChild)
    {
        if (currentChild.nodeType == 3)
        {
            theSource += currentChild.textContent;
        }
        currentChild = currentChild.nextSibling;
    }

    // Now figure out what type of shader script we have,
    // based on its MIME type.
    var shader;

    if (shaderScript.type == "x-shader/x-fragment") {
        shader = gl.createShader(gl.FRAGMENT_SHADER);
    } else if (shaderScript.type == "x-shader/x-vertex") {
        shader = gl.createShader(gl.VERTEX_SHADER);
    } else {
        return null;  // Unknown shader type
    }

    // Send the source to the shader object
    gl.shaderSource(shader, theSource);

    // Compile the shader program
    gl.compileShader(shader);

    // See if it compiled successfully
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        alert("An error occurred compiling the shaders: " + gl.getShaderInfoLog(shader));
        return null;
    }
    return shader;
}

// Matrix utility functions
function loadIdentity()
{
    mvMatrix = Matrix.I(4);
}

function multMatrix(m)
{
    mvMatrix = mvMatrix.x(m);
}

function mvTranslate(v)
{
    multMatrix(Matrix.Translation($V([v[0], v[1], v[2]])).ensure4x4());
}

function setMatrixUniforms()
{
    var pUniform = gl.getUniformLocation(shaderProgram, "uPMatrix");
    gl.uniformMatrix4fv(pUniform, false, new Float32Array(perspectiveMatrix.flatten()));

    var mvUniform = gl.getUniformLocation(shaderProgram, "uMVMatrix");
    gl.uniformMatrix4fv(mvUniform, false, new Float32Array(mvMatrix.flatten()));
}

var mvMatrixStack = [];

function mvPushMatrix(m)
{
    if (m) {
        mvMatrixStack.push(m.dup());
        mvMatrix = m.dup();
    } else {
        mvMatrixStack.push(mvMatrix.dup());
    }
}

function mvPopMatrix()
{
    if (!mvMatrixStack.length) {
        throw("Can't pop from an empty matrix stack.");
    }

    mvMatrix = mvMatrixStack.pop();
    return mvMatrix;
}

function mvRotate(angle, v)
{
    var inRadians = angle * Math.PI / 180.0;

    var m = Matrix.Rotation(inRadians, $V([v[0], v[1], v[2]])).ensure4x4();
    multMatrix(m);
}
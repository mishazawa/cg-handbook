# WebGL pipeline

![image](https://user-images.githubusercontent.com/7611372/202558392-b0f29dae-56d7-48f2-a74d-25d9c96322d2.png)

1. Create the **data representing the geometry** (JavaScript) and pass it to shaders (GLSL).
 
2. The data is fed to a **vertex shader** and the rendering process starts, each vertex position is calculated and stored along with its color and textures coordinates.
 
3. **Primitives are assembled** (WebGl primitives are _lines, points and triangles_). This step creates vectorial shapes for the geometry;
 
4. Rasterization, where **pixels are mapped from the primitives**. Every not visible primitives or out of the view area are discarded. Vertex attributes are interpolated across the pixel they enclose;
 
5. **Fragment shader** takes input from the vertex shader and the rasterization stage and calculates the color for each pixel. Other calculations can be done after determining the color;
 
6. The **image is displayed** on the 2D screen and the frame buffer (part of graphic memory) holds the scene data.

## [WebGL state diagram](https://webglfundamentals.org/webgl/lessons/resources/webgl-state-diagram.html)

## Clip space, matrices

We go from coordinates defined in a space to a result on a screen. Our data must be brought to the WebGL space also called clip space coordinate system. This space is 2 units wide. We can visualize it as a cube going from –1 to 1 in three dimensions with a center of (0,0,0). It does not take any other factor into account such as screen ratio. The vertex shader returns a calculated position into this space through a variable called `gl_Position`. To do so, positions are multiplied by [several matrices](https://developer.mozilla.org/fr/docs/Web/API/WebGL_API/WebGL_model_view_projection%2520http://www.opengl-tutorial.org/fr/beginners-tutorials/tutorial-3-matrices/):

* **Model matrix**: translate the object reference coordinates to the WebGL 3D space (at first, vertices origin is based on the object center, after that calculation, they are based on the 3D WebGL word origin);

* **View matrix**: translate the origin of the vertices coordinates to a point that will be considered as a camera coordinates;

* **Projection Matrix**: Used to introduce the perspective notion. The farthest we are, the smaller objects are.

![image](https://user-images.githubusercontent.com/7611372/202559602-e77f18f7-a4b8-4ed1-8be2-c79eefd67db3.png)

### Clip space coordinates always go from -1 to +1 no matter what size your canvas is.

![image](https://user-images.githubusercontent.com/7611372/202559701-cae6ae50-cbdc-4f92-a1f8-28ed2c885627.png)

WebGL only cares about 2 things: **clip space coordinates and colors**. Your job as a programmer using WebGL is to provide WebGL with those 2 things. You provide your 2 "shaders" to do this. _**A Vertex shader which provides the clip space coordinates, and a fragment shader that provides the color.**_

# Shaders

**Attributes and Buffers**: Buffers are arrays of normalized data you upload to the GPU. Usually buffers contain things like positions, normals, texture coordinates, vertex colors. Attributes are used to specify how to pull data out of your buffers and provide them to your vertex shader.

**Uniforms**: Uniforms are effectively global variables you set before you execute your shader program.

**Textures**: Textures are arrays of data you can randomly access in your shader program. The most common thing to put in a texture is image data but textures are just data and can just as easily contain something other than colors.

**Varyings**: Varyings are a way for a vertex shader to pass data to a fragment shader. Depending on what is being rendered, points, lines, or triangles, the values set on a varying by a vertex shader will be interpolated while executing the fragment shader.

## Shader data

Vertex shaders:

1. [Attributes](https://webglfundamentals.org/webgl/lessons/webgl-shaders-and-glsl.html#attributes) (data pulled from buffers)
2. [Uniforms](https://webglfundamentals.org/webgl/lessons/webgl-shaders-and-glsl.html#uniforms) (values that stay the same for all vertices of a single draw call)
3. [Textures](https://webglfundamentals.org/webgl/lessons/webgl-shaders-and-glsl.html#textures-in-vertex-shaders) (data from pixels/texels)

Fragment shaders:

1. [Uniforms](https://webglfundamentals.org/webgl/lessons/webgl-shaders-and-glsl.html#uniforms) (values that stay the same for every pixel of a single draw call)
2. [Textures](https://webglfundamentals.org/webgl/lessons/webgl-shaders-and-glsl.html#textures-in-fragment-shaders) (data from pixels/texels)
3. [Varyings](https://webglfundamentals.org/webgl/lessons/webgl-shaders-and-glsl.html#varyings) (data passed from the vertex shader and interpolated)

### Attributes and buffers
```ts
const geometry = new BufferGeometry();
// create a simple square shape. We duplicate the top left and bottom right
// vertices because each vertex needs to appear once per triangle.
const vertices = new Float32Array([
	-1.0, -1.0,  1.0,
	 1.0, -1.0,  1.0,
	 1.0,  1.0,  1.0,

	 1.0,  1.0,  1.0,
	-1.0,  1.0,  1.0,
	-1.0, -1.0,  1.0
]);

// itemSize = 3 because there are 3 values (components) per vertex
geometry.setAttribute('position', new BufferAttribute(vertices, 3));

// Create shader material
const material = new ShaderMaterial({
      wireframe: true,
      side: DoubleSide,
      fragmentShader, // string
      vertexShader,   // string
      uniforms: {
        texture: new Uniform(new DataTexture(new Uint8Array(4 * /* len */),  32, 32)),
        resolution: new Uniform(new Vector2(32, 32))
      }
    });

const mesh = new Mesh(geometry, material);
```

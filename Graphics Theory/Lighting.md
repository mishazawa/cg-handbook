The basic light model is called `Ambient/Diffuse/Specular`. 

# Ambient

Ambient light is the type of light you see when you go outside in a usual sunny day. Even though the sun is traveling across the sky and its light rays hit the world at different angles in different parts of the day, most of the stuff will be visible, even if it is in shadow. Since light bounces off everything it eventually hits everything so objects that are not in the direct path of the sun are also lit. Even a light bulb in a room behaves like the sun in that sense and spreads ambient light because if the room is not too big everything is lit equally. _The ambient light is modeled as light that has no origin, no direction and has an equal effect on all objects in the scene._

![image](https://user-images.githubusercontent.com/7611372/204507647-f3657271-6492-41b3-87ba-f55bf350ce74.png)

# Diffuse

Diffuse lighting emphasizes the fact that the angle by which the light hits the surface affects the brightness by which the object is lit. When light hits an object on one side that side is brighter than the other side (the side not directly in front of the light source). We just saw that the sun spreads ambient light which has no specific direction. However, the sun also has diffuse properties in its light. When it hits a tall building you can usually see that one side of the building is lighter than the other side. _The most important property of diffuse light is its direction. _

The model of diffuse light is actually based on **Lambert's cosine law** that says that _the intensity of light reflected from a surface is directly proportional to the cosine of the angle between the observer's line of sight and the surface normal_. Note that we changed this a bit by using the direction of light instead of the observer's line of sight (which we will use in specular light).

To calculate the intensity of light in the diffuse model we are going to simply use the cosine of the angle between the light and the surface normal (whereas Lambert's law refers to the more general concept of 'directionally proportional').

![image](https://user-images.githubusercontent.com/7611372/204507988-84ed485b-0d7f-485e-a222-ceefadbdcd36.png)

A **vertex normal** is the average of the normals of all the triangles that share the vertex. Instead of having the vertex shader calculate the diffuse light we only pass through the vertex normal as an attribute to the fragment shader and nothing more. The rasterizer will get three different normals and will need to interpolate between them. The fragment shader will be invoked for each pixel with the specific normal for this pixel. We can then calculate the diffuse light at the pixel level using that specific normal. The result will be a lighting effect which nicely changes across the triangle face and between neighboring triangles. This technique is known as Phong Shading.

The vertices and their normals are specified in a local coordinate space and are transformed in the vertex shader all the way to clip space by the WVP matrix that we supply to the shader. However, specifying the direction of light in world space is the most logical course of action. After all, the direction of light is the result of some light source which is positioned in the world somewhere (even the sun is located in the "world", albeit many miles away) and sheds its light in a particular direction. Therefore, we will need to transform the normals to world space before the calculation.

```glsl
// vertex shader 

// general
mat4 normalMatrix = transpose(inverse(modelView));
// three js
uniform vec3 normalMatrix;

varying vec3 Normal0;

// ...
Normal0 = normalize(normalMartix * vec4(Normal, .0))

// fragment shader

float DiffuseFactor = dot(Normal0, directionalLight.Direction);
// multiply it by color, intensity and add to ambient light
```
There are many sources online that tell you that you need the transpose of the inverse of the world matrix in order to transform the normal vector. This is correct, however, we usually don't need to go that far. Our world matrices are always orthogonal (their vectors are always orthogonal). Since the inverse of an orthogonal matrix is equal to its transpose, the transpose of the inverse is actually the transpose of the transpose, so we end up with the original matrix. 

# Specular

Specular lighting is more a property of the object, rather than the light itself. This is what makes parts of things shine when light hits them at a very specific angle and the viewer is positioned at a specific point. Metallic objects often have some kind of specular property. For example, a car in a bright sunny day can sometimes shine off its edges. Calculating specular lighting must take into consideration both the direction the light hits (and bounces off) as well as the position of the viewer.

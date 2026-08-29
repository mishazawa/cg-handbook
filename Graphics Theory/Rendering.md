# Forward rendering

FR is a rendering pipeline that performs the shading of pixels as it processes the geometric information for a frame. In a forward renderer, the rendering process is typically done in a single pass, where the renderer traverses the geometric primitives in the scene and performs the necessary shading calculations for each pixel as it goes.

In contrast to [deferred rendering](#deferred-rendering), a forward renderer does not store the geometric and material information for a frame in intermediate buffers. Instead, it performs the shading calculations directly on the final pixel colors for the frame. This can make forward rendering more efficient for simple scenes with few light sources, as there is no need to perform an additional lighting pass.

However, forward rendering becomes less efficient as the complexity of the scene increases, particularly in the presence of many light sources. In these cases, the renderer may need to perform the shading calculations multiple times for each pixel, leading to slower rendering times. Forward rendering also tends to be less flexible in terms of the types of lighting and shading effects that can be achieved, as the renderer does not have access to as much information about the geometry and materials in the scene.

Forward rendering is still widely used in many rendering applications, particularly for real-time rendering in games and other interactive applications. However, it has largely been superseded by more advanced rendering techniques such as deferred rendering and physically based rendering, which offer improved performance and visual quality for more complex scenes.

## Implementation details (Unity)

In FR, some number of brightest lights that affect each object are rendered in fully per-pixel lit mode. Then, up to 4 point lights are calculated per-vertex. The other lights are computed as **Spherical Harmonics (SH)**, which is much faster but is only an approximation.

_Whether a light will be a per-pixel light or not is dependent on this:_

* Lights that have their `Render Mode` set to `Not Important` are always per-vertex or SH.
* Brightest directional light is always per-pixel.
* Lights that have their `Render Mode` set to Important are always per-pixel.
* If the above results in fewer lights than current `Pixel Light Count` [Quality Setting](https://docs.unity3d.com/Manual/class-QualitySettings.html), then more lights are rendered per-pixel, in order of decreasing brightness.

_Rendering of each object happens as follows:_

* Base Pass applies one per-pixel directional light and all per-vertex/SH lights.
* Other per-pixel lights are rendered in additional passes, one pass for each light.

## Execution order (`CameraEvent` and `LightEvent`)

* Unity renders depth for opaque geometry.
* Unity renders depth normals for opaque geometry.
* Unity renders shadows.
  1. Unity renders all shadow casters for the current pass.
  2. Unity repeats the previous step for each pass.
  3. Unity gathers the shadow map into a screen space buffer and performs filtering.
* Unity renders opaque geometry.
* Unity renders the skybox.
* Unity renders halos.
* Unity applies opaque-only post-processing effects.
* Unity renders transparent geometry, and UI Canvases with a Rendering Mode of Screen Space - Camera.
* Unity renders lens flares.
* Unity applies post-processing effects.
* Unity renders UI Canvases with a Rendering Mode that is not Screen Space - Camera.

# Deferred rendering

DR is a rendering pipeline that delays the shading of pixels until all geometric and lighting information for a frame has been processed. In a deferred renderer, the rendering process is typically split into two stages: a geometry pass and a lighting pass.

In the geometry pass, the renderer processes all the geometric information for a frame and stores it in a set of buffers known as g-buffers. These g-buffers typically store information such as surface normals, depth, and material properties for each pixel in the frame.

In the lighting pass, the renderer uses the information stored in the g-buffers to compute the final pixel colors for the frame. This process involves calculating the lighting contributions from all the light sources in the scene, as well as any other visual effects such as shadows and reflections.

Deferred rendering has several advantages over traditional forward rendering pipelines. It allows for more efficient rendering of complex scenes with many light sources, as the lighting calculations can be done independently for each pixel and parallelized on modern graphics hardware. It also allows for greater flexibility in the types of lighting and shading effects that can be achieved, as all the necessary geometric and material information is available during the lighting pass.

Deferred rendering can also be more complex to implement and may not be well-suited for certain types of rendering tasks, such as those that require real-time alpha blending or transparent rendering.

## Overview (Unity)

When using deferred shading, there is no limit on the number of lights that can affect a `GameObject`. All lights are evaluated per-pixel, which means that they all interact correctly with normal maps, etc. Additionally, all lights can have cookies and shadows.

Deferred shading has the advantage that the processing overhead of lighting is proportional to the number of pixels the light shines on. This is determined by the size of the light volume in the Scene regardless of how many `GameObjects` it illuminates. Therefore, performance can be improved by keeping lights small. Deferred shading also has highly consistent and predictable behaviour. The effect of each light is computed per-pixel, so there are no lighting computations that break down on large triangles.

On the downside, deferred shading has no real support for anti-aliasing and can't handle semi-transparent `GameObjects` (these are rendered using [forward rendering](#forward-rendering)). There is also no support for the `Mesh Renderer`'s _Receive Shadows_ flag and culling masks are only supported in a limited way. You can only use up to four culling masks. That is, your culling layer mask must at least contain all layers minus four arbitrary layers, so 28 of the 32 layers must be set. Otherwise you get graphical artifacts.

**Note**: Deferred rendering isn't supported when using Orthographic projection. If the Camera's projection mode is set to `Orthographic`, the Camera falls back to Forward rendering.

## Performance considerations

The rendering overhead of real-time lights in deferred shading is proportional to the number of pixels illuminated by the light and **not dependent** on Scene complexity. So small `Point Lights` or `Spot Lights` are very cheap to render and if they are fully or partially occluded by Scene GameObjects then they are even cheaper.

Of course, lights with shadows are much more expensive than lights without shadows. In deferred shading, shadow-casting `GameObjects` still need to be rendered once or more for each shadow-casting light. Furthermore, the lighting shader that applies shadows has a higher rendering overhead than the one used when shadows are disabled.

## Execution order (`CameraEvent` and `LightEvent`)

* Unity renders opaque geometry.
* Unity resolves depth.
* Unity renders default reflections, and Reflection Probe reflections.
* Unity copies reflections to the Emissive channel of the G-buffer.
* Unity renders shadows.
  1. Unity renders all shadow casters for the current pass.
  2. Unity repeats the previous step for each pass.
  3. Unity gathers the shadow map into a screen space buffer and performs filtering.
* Unity processes the final pass.
* Unity renders opaque geometry that cannot be rendered with deferred rendering.
* Unity renders the skybox.
* Unity renders halos.
* Unity applies opaque-only post-processing effects.
* Unity renders transparent geometry, and UI Canvases with a Rendering Mode of Screen Space - Camera.
* Unity renders lens flares.
* Unity applies post-processing effects.
* Unity renders UI Canvases with a Rendering Mode that is not Screen Space - Camera.

# Miscellaneous

## Path tracing

Path tracing is a technique used in computer graphics to generate photorealistic images of 3D scenes. It is a type of ray tracing, which is a rendering technique that simulates the way light travels through a 3D environment by tracing the paths of rays from the eye of the viewer through the scene.

In path tracing, the renderer traces rays from the eye through the scene and records the color and intensity of the light that is scattered or absorbed by the objects in the scene. The renderer then uses this information to compute the final pixel colors for the image, taking into account the lighting, shading, and surface properties of the objects in the scene.

Path tracing is known for producing highly realistic images with accurate lighting and shadow effects, but it can be computationally intensive and may require a significant amount of time to render a single frame. As a result, it is typically used for offline rendering, where the time required to generate a final image is not a limiting factor. However, advances in graphics hardware and rendering techniques have made it possible to use path tracing in real-time rendering applications as well.

## Raymarching

Raymarching is a technique used in computer graphics to render 3D scenes that involve shapes and objects that cannot be efficiently represented using traditional polygonal meshes. It works by tracing rays through the 3D scene and evaluating the distance from the ray to the nearest surface at each step.

In raymarching, the renderer starts from a point in 3D space and marches the ray a small distance forward at each step, until it hits a surface or exceeds a maximum distance threshold. The renderer can then use the distance information to compute the color and other visual properties of the pixel corresponding to the ray.

Raymarching is particularly well-suited for rendering volumetric and procedural geometry, as it allows the renderer to efficiently evaluate complex shapes and patterns without the need to explicitly store and manipulate large meshes. It is also often used to render complex visual effects such as fog, smoke, and atmospheric effects.

Raymarching can be computationally intensive and may require a significant amount of time to render a single frame, particularly for scenes with a high level of detail. It is also more difficult to implement than some other rendering techniques, as it requires the use of specialized distance functions to evaluate the distance from the ray to the nearest surface.

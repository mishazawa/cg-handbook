# GameObject

GameObjects are the fundamental objects in Unity that represent characters, props and scenery. They do not accomplish much in themselves but they act as containers for Components, which implement the functionality.

The Transform is used to store a GameObject's position, rotation, scale and parenting state and is thus very important. A GameObject will always have a Transform component attached - it is not possible to remove a Transform or to create a GameObject without one.

Parenting is one of the most important concepts to understand when using Unity. When a GameObject is a Parent of another GameObject, the Child GameObject will move, rotate, and scale exactly as its Parent does.

When parenting Transforms, it is useful to set the parent's location to <0,0,0> before adding the child. This means that the local coordinates for the child will be the same as global coordinates making it easier to be sure you have the child in the right position.

> The position, rotation and scale values of a Transform are measured relative to the Transform's parent. If the Transform has no parent, the properties are measured in world space.

## Importance of Scale

The scale of the Transform determines the difference between the size of a mesh in your modeling application and the size of that mesh in Unity. The mesh's size in Unity (and therefore the Transform's scale) is very important, especially during physics simulation. By default, the physics engine assumes that one unit in world space corresponds to one meter. If an object is very large, it can appear to fall in "slow motion"; the simulation is actually correct since effectively, you are watching a very large object falling a great distance.

Ideally, you should not adjust the Scale of your object in the Transform Component. The best option is to create your models at real-life scale so you won't have to change your Transform's scale. The next best option is to adjust the scale at which your mesh is imported in the Import Settings for your individual mesh. Certain optimizations occur based on the import size, and instantiating an object that has an adjusted scale value can decrease performance.

## Limitations with Non-Uniform Scaling

Non-uniform scaling is when the Scale in a Transform has different values for x, y, and z; for example (2, 4, 2). In contrast, uniform scaling has the same value for x, y, and z; for example (3, 3, 3). Non-uniform scaling can be useful in a few specific cases but it introduces a few oddities that don't occur with uniform scaling:

- Certain components do not fully support non-uniform scaling. For example, some components have a circular or spherical element defined by a radius property, among them Sphere Collider, Capsule Collider, Light and Audio Source. In cases like this the circular shape will not become elliptical under non-uniform scaling as you would expect and will simply remain circular.
- When a child object has a non-uniformly scaled parent and is rotated relative to that parent, it may appear skewed or "sheared". There are components that support simple non-uniform scaling but don't work correctly when skewed like this. For example, a skewed Box Collider will not match the shape of the rendered mesh accurately.
- For performance reasons, a child object of a non-uniformly scaled parent will not have its scale automatically updated when it rotates. As a result, the child's shape may appear to change abruptly when the scale eventually is updated, say if the child object is detached from the parent.

## Deactivate GameObjects

To temporarily remove a GameObject from your scene, you can mark the GameObject as inactive. To deactivate a GameObject through script, use the `SetActive` method. To see if an object is active or inactive, check the `activeSelf` property.

If you deactivate a parent GameObject, you also deactivate all of its child GameObjects because the deactivation overrides the activeSelf setting on all child GameObjects. The child GameObjects return to their original state when you reactivate the parent.

To know if a child GameObject is active in your scene, use the `activeInHierarchy` property.

> Note: The `activeSelf` property is not always accurate if you check a child GameObject because even if it is set to active, you might have set one of its parent GameObjects to inactive.

## Static GameObjects

If a GameObject does not move at runtime, it is known as a static GameObject. If a GameObject moves at runtime, it is known as a dynamic GameObject. Many systems in Unity can precompute information about static GameObjects in the Editor. Because the GameObjects do not move, the results of these calculations are still valid at runtime. This means that Unity can save on runtime calculations, and potentially improve performance.

Static systems: Contribute GI, Occluder Static, Occludee Static, Batching Static, Navigation Static, Off Mesh Link Generation, Reflection Probe

# Tags

A Tag is a reference word which you can assign to one or more GameObjects. Tags help you identify GameObjects for scripting purposes. They ensure you don't need to manually add GameObjects to a script's exposed properties using drag and drop, thereby saving time when you are using the same script code in multiple GameObjects.

# Prefabs

Unity's Prefab system allows you to create, configure, and store a GameObject complete with all its components, property values, and child GameObjects as a reusable Asset. The Prefab Asset acts as a template from which you can create new Prefab instances in the Scene.

Any edits that you make to a Prefab Asset are automatically reflected in the instances of that Prefab, allowing you to easily make broad changes across your whole Project without having to repeatedly make the same edit to every copy of the Asset.

You can nest Prefabs inside other Prefabs to create complex hierarchies of objects that are easy to edit at multiple levels.

However, this does not mean all Prefab instances have to be identical. You can override settings on individual prefab instances if you want some instances of a Prefab to differ from others. You can also create variants of Prefabs which allow you to group a set of overrides together into a meaningful variation of a Prefab.

You should also use Prefabs when you want to instantiate GameObjects at runtime that did not exist in your Scene at the start - for example, to make powerups, special effects, projectiles, or NPCs appear at the right moments during gameplay.

## Instance overrides

Instance overrides allow you to create variations between Prefab instances, while still linking those instances to the same Prefab Asset.

There are four different types of instance override:
- Overriding the value of a property
- Adding a component
- Removing a component
- Adding a child GameObject

There are some limitations with Prefab instances: you cannot reparent a GameObject that is part of a Prefab, and you cannot remove a GameObject that is part of the Prefab. You can, however, deactivate a GameObject, which is a good substitute for removing a GameObject (this counts as a property override).

> Overrides take precedence

An overridden property value on a Prefab instance always takes precedence over the value from the Prefab Asset. This means that if you change a property on a Prefab Asset, it doesn't have any effect on instances where that property is overridden.

If you make a change to a Prefab Asset, and it does not update all instances as expected, you should check whether that property is overridden on the instance. It is best to only use instance overrides when strictly necessary, because if you have a large number of instance overrides throughout your Project, it can be difficult to tell whether your changes to the Prefab Asset will or won't have an effect on all of the instances.

The alignment of a Prefab instance is a special case, and is handled differently to other properties. The alignment values are never carried across from the Prefab Asset to the Prefab instances. This means they can always differ from the Prefab Asset's alignment without it being an explicit instance override. Specifically, the alignment means the Position and Rotation properties on the root Transform of the Prefab instance, and for a Rect Transform this also includes the Width, Height, Margins, Anchors and Pivot properties.

## Prefab Variants

Prefab Variants are useful when you want to have a set of predefined variations of a Prefab. A Prefab Variant inherits the properties of another Prefab, called the base. Overrides made to the Prefab Variant take precedent over the base Prefab's values. A Prefab Variant can have any other Prefab as its base, including Model Prefabs or other Prefab Variants.

As with any Prefab instance, you can use prefab overrides in a Prefab Variant, such as modified property values, added components, removed components, and added child GameObjects. There are also the same limitations: you cannot reparent GameObjects in the Prefab Variant which come from its base Prefab. You also cannot remove a GameObject from a Prefab Variant which exists in its base Prefab. You can, however, deactivate GameObjects (as a property override) to achieve the same effect as removing a GameObject.

> The point of a Prefab Variant is to provide a convenient way to store a meaningful and reusable collection of overrides, which is why they should normally remain as overrides and not get applied to the base Prefab Asset.

## Unpacking Prefab instances

You can unpack a Prefab instance by right-clicking on it in the Hierarchy and selecting Unpack Prefab. The resulting GameObject in the Scene no longer has any link to its former Prefab Asset. The Prefab Asset itself is not affected by this operation and there may still be other instances of it in your Project

# Layers

> Layers are a tool that allows you to separate GameObjects in your scenes.

You can render only the objects in a particular layer, or selection of layers, if you use the Camera's culling mask. UI elements and screen space canvas children are exceptions to this and render regardless.

You can use layers to specify which GameObjects that a ray cast can intersect with. To make a ray cast ignore a GameObject, you can assign it to the Ignore Raycast layer, or pass a LayerMask to the ray cast API call. If you don't pass a LayerMask to the ray cast API call, Unity uses `Physics.DefaultRaycastLayers` which matches every layer except Ignore Raycast.

```c#
var combinedLayerMask = (1 << layerMask1 | (1 << layerMask2);

/*
~ inverse
| or
& and
*/

// add to existing

combinedLayerMask |= (1 << layerMask3);

// remove from existing

combinedLayerMask &= ~(1 << layerMask3);

```

# Constraints

A Constraint component links the position, rotation, or scale of a GameObject to another GameObject. A constrained GameObject moves, rotates, or scales like the GameObject it is linked to.

Unity supports the following types of Constraint components:

- Aim: Rotate the constrained GameObject to face the linked GameObject.
- Look At: Rotate the constrained GameObject to the linked GameObject (simplified Aim Constraint).
- Parent: Move and rotate the constrained GameObject with the linked GameObject.
- Position: Move the constrained GameObject like the linked GameObject.
- Rotation: Rotate the constrained GameObject like the linked GameObject.
- Scale: Scale the constrained GameObject like the linked GameObject.

Avoid creating a cycle of Constraints, because this causes unpredictable updates during gameplay.

There are two aspects to working with Constraints: activating and locking.

You activate a Constraint to allow it to evaluate the position, rotation, or scale of the constrained GameObject. Unity does not evaluate inactive Constraints.

You lock a Constraint to allow it to move, rotate, or scale the GameObject. A locked Constraint takes control of the relevant parts of the Transform of the GameObject. You cannot manually move, rotate, or scale a GameObject with a locked Constraint. You also cannot edit the Constraint Settings.

# Rotation and orientation in Unity

In Unity, you can use both Euler angles and quaternions to represent rotations and orientation. These representations are equivalent but have different uses and limitations.

Typically, you rotate objects in your scene using the Transform component, which displays orientation as a Euler angle. However, Unity stores rotations and orientations internally as quaternions, which can be useful for more complex motions that might otherwise lead to gimbal lock.

## Euler angles
In the Transform coordinate, Unity displays rotation with the vector property Transform.eulerAngles X, Y, and Z. Unlike a normal vector, these values actually represent the angle (in degrees) of rotation about the X, Y, and Z axes.

Euler angle rotations perform three separate rotations around the three axes. Unity performs the Euler rotations sequentially around the z-axis, the x-axis and then the y-axis. This method of rotation is extrinsic rotation; the original coordinate system doesn't change while the rotations occur.

To rotate a GameObject, you can enter angle values of how far you want each axis to rotate into the Transform component. To rotate your GameObjects with script, use Transform.eulerAngles. If you convert to Euler angles to do calculations and rotations, you risk problems with gimbal lock.

## Gimbal lock
When an object in 3D space loses a degree of freedom and can only rotate within two dimensions, it's called gimbal lock. Gimbal lock can occur with Euler angles if two axes become parallel. If you don't convert the rotational values to Euler angles in your script, the use of quaternions should prevent gimbal lock.

If you do have problems with gimbal lock, you can avoid Euler angles if you use Transform.RotateAround for rotations. You can also use Quaternion.AngleAxis on each axis and multiply them together (quaternion multiplication applies each rotation in turn).

## Quaternions

Quaternions provide mathematical notation for unique representations of spatial orientation and rotation in 3D space. A quaternion uses four numbers to encode the direction and angle of rotation around unit axes in 3D. These four values are complex numbers rather than angles or degrees.

Unity converts rotational values to quaternions to store them because quaternion rotations are efficient and stable to compute. The Editor doesn't display rotations as quaternions because a single quaternion can't represent a rotation greater than 360 degrees about any axis.

## Convert between Euler angles and quaternions

- To convert from Euler angles to quaternions, you can use the `Quaternion.Euler` function.
- To convert a quaternion to Euler angles, you can use the `Quaternion.eulerAngles` function.

# Cross-Platform Considerations

## Input

### Keyboard and joypad

The `Input.GetAxis` function is convenient on desktop platforms to consolidate keyboard and joypad input. This function isn't suitable for mobile platforms that rely on touchscreen input. The standard desktop keyboard input is only suitable for porting typed text to mobile devices.

### Touches and clicks

The `Input.GetMouseButtonXXX` functions are designed to have an obvious interpretation on mobile devices. The screen reports a simple touch as a left click and the `Input.mousePosition` property gives the position of the touch, as long as the finger is touching the screen. Games with simple mouse interactions can often work transparently between the desktop and mobile platforms.

### Memory, storage and CPU performance

Mobile devices have less storage, memory and CPU power available than desktop machines and so a game may be difficult to port simply because its performance isn't acceptable on lower powered hardware. If you are pushing the limits of your desktop hardware, then the game probably isn't a good candidate for porting to a mobile platform.

### Storage requirements
Video, audio, and textures can use a lot of storage space. You need to manage storage effectively if you want to port your game. Storage space (which often also corresponds to download time) is usually not an issue on desktop machines, but it can be limited on mobile devices. Mobile app stores often impose a limit on the maximum size of a submitted product. It might require some planning to address these concerns during your game development.

For example, you may need to provide cut-down versions of assets for mobiles to save space. Another possibility is that the game may need to be designed so that large assets can be downloaded on demand rather than being part of the initial download of the application.

- Unity re-codes imported Assets into its own internal formats, so the choice of source Asset type is not relevant. For example, if you have a multi-layer Photoshop Texture in the Project, it is flattened and compressed before building. Exporting the Texture as a .png file does not make any difference to build size, so you should stick to the format that is most convenient for you during development.

- Unity strips most unused Assets during the build, so you don't gain anything by manually removing Assets from the Project. The only Assets that are not removed are scripts (which are generally very small anyway) and Assets in the Resources folder (because Unity can't determine which of these are needed and which are not). With this in mind, you should make sure that the only Assets in the Resources folder are the ones you need for the game. You might be able to replace Assets in the Resources folder with AssetBundles - this means that Unity loads Assets dynamically, thereby reducing the player size.

- Mesh and Animation compression uses quantization, which means it takes less space, but the compression can introduce some inaccuracies.

- Mesh compression only produces smaller data files, and does not use less memory at run time. Animation keyframe reduction produces smaller data files and uses less memory at run time; generally you should always have it enabled.

### Automatic memory management
Unity automatically handles the recovery of unused memory from "dead" objects and often happens unnoticed on desktop machines. However, the lower memory and CPU power on mobile devices means that garbage collections can be more frequent, impacting performance and causing unwanted pauses in gameplay. Even if the game runs in the available memory, it might be necessary to optimize code to avoid garbage collection pauses

### CPU power
A game that runs well on a desktop machine might experience poor framerate on a mobile device because the mobile CPU struggles with the game complexity. Pay attention to code efficiency when a project is ported to a mobile platform.

A script makes its connection with the internal workings of Unity by implementing a class which derives from the built-in class called MonoBehaviour.

An initialization of an object **is not** done using a constructor function. This is because the construction of objects is handled by the editor and does not take place at the start of gameplay as you might expect. If you attempt to define a constructor for a script component, it will interfere with the normal operation of Unity and can cause major problems with the project.

# Variables and the Inspector

- The way to see a variable in the Inspector is to declare it as `public`.
- An alternative method is to use `SerializeField`.
- `HideInInspector` to prevent a public variable from being displayed in the Inspector.

# Coroutines

A coroutine allows you to spread tasks across several frames. In Unity, a coroutine is a method that can pause execution and return control to Unity but then continue where it left off on the following frame.

In most situations, when you call a method, it runs to completion and then returns control to the calling method, plus any optional return values. This means that any action that takes place within a method must happen within a single frame update.

In situations where you would like to use a method call to contain a procedural animation or a sequence of events over time, you can use a coroutine.

However, it's important to remember that coroutines aren't threads. Synchronous operations that run within a coroutine still execute on the main thread. If you want to reduce the amount of CPU time spent on the main thread, it's just as important to avoid blocking operations in coroutines as in any other script code. If you want to use multi-threaded code within Unity, consider the C# Job System.

It's best to use coroutines if you need to deal with long asynchronous operations, such as waiting for HTTP transfers, asset loads, or file I/O to complete.

A coroutine is a method that you declare with an `IEnumerator` return type and with a `yield return` statement included somewhere in the body. The `yield return null` line is the point where execution pauses and resumes in the following frame.

Correct values over the lifetime of the coroutine, and any variable or parameter is preserved between `yield` statements.

```c#
IEnumerator Func() {
  yield return null;
}

StartCoroutine(Func());
```

## Coroutine time delay

By default, Unity resumes a coroutine on the frame after a yield statement. If you want to introduce a time delay, use `WaitForSeconds` to spread an effect over a period of time, and you can use it as an alternative to including the tasks in the `Update` method. Unity calls the `Update` method several times per second, so if you don't need a task to be repeated quite so often, you can put it in a coroutine to get a regular update but not every single frame. This reduces the number of checks that Unity carries out without any noticeable effect on gameplay.

## Stopping coroutines

To stop a coroutine, use `StopCoroutine` and `StopAllCoroutines`. A coroutine also stops if you've set `SetActive` to false to disable the GameObject the coroutine is attached to. Calling `Destroy(example)` (where example is a MonoBehaviour instance) immediately triggers `OnDisable` and Unity processes the coroutine, effectively stopping it. Finally, `OnDestroy` is invoked at the end of the frame.

> Note: If you've disabled a MonoBehaviour by setting `enabled` to false, Unity doesn't stop coroutines.

## Analyzing coroutines

It's best practice to condense a series of operations down to the fewest number of individual coroutines possible. Nested coroutines are useful for code clarity and maintenance, but they impose a higher memory overhead because the coroutine tracks objects.

If a coroutine runs every frame and doesn't yield on long-running operations, it's more performant to replace it with an `Update` or `LateUpdate` callback. This is useful if you have long-running or infinitely looping coroutines.

All the initial code in a coroutine, from the start of the coroutine method until the first `yield` statement, appears in the trace whenever Unity starts a coroutine. The initial code most often appears whenever the `StartCoroutine` method is called. Coroutines that Unity callbacks generate (such as `Start` callbacks that return an `IEnumerator`) first appear within their respective Unity callback.

The rest of a coroutine's code (from the first time it resumes until it finishes executing) appears within the `DelayedCallManager` line that's inside Unity's main loop.

This happens because of the way that Unity executes coroutines. The C# compiler auto generates an instance of a class that backs coroutines. Unity then uses this object to track the state of the coroutine across multiple invocations of a single method. Because local-scope variables within the coroutine must persist across `yield` calls, Unity hoists the local-scope variables into the generated class, which remain allocated on the heap during the coroutine. This object also tracks the internal state of the coroutine: it remembers at which point in the code the coroutine must resume after yielding.

_Because of this, the memory pressure that happens when a coroutine starts is equal to a fixed overhead allocation plus the size of its local-scope variables._

The code which starts a coroutine constructs and invokes an object, and then Unity's `DelayedCallManager` invokes it again whenever the coroutine's yield condition is satisfied. Because coroutines usually start outside of other coroutines, this splits their execution overhead between the `yield` call and `DelayedCallManager`.

# UnityEvents

UnityEvents are a way of allowing user driven callback to be persisted from edit time to run time without the need for additional programming and script configuration.

UnityEvents are useful for a number of things:

- Content driven callbacks
- Decoupling systems
- Persistent callbacks
- Preconfigured call events

UnityEvents can be added to any MonoBehaviour and are executed from code like a standard .net delegate. When a UnityEvent is added to a MonoBehaviour it appears in the Inspector and persistent callbacks can be added.

> UnityEvents have similar limitations to standard delegates. That is, they hold references to the element that is the target and this stops the target being garbage collected. If you have a `UnityEngine.Object` as the target and the native representation disappears the callback will not be invoked.

```c#
// add and remove event listener

void OnEnable()
{
    ScriptWithEventsInside.StaticEventName += FunctionToRun;
}
void OnDisable()
{
    ScriptWithEventsInside.StaticEventName -= FunctionToRun;
}
```

# Null Reference Exceptions

A `NullReferenceException` happens when you try to access a reference variable that isn't referencing any object. If a reference variable isn't referencing an object, then it'll be treated as `null`. The run-time will tell you that you are trying to access an object, when the variable is `null` by issuing a `NullReferenceException`.

Reference variables in c# and JavaScript are similar in concept to pointers in C and C++. Reference types default to `null` to indicate that they are not referencing any object. Hence, if you try and access the object that is being referenced and there isn't one, you will get a `NullReferenceException`.

Summary:

- `NullReferenceException` happens when your script code tries to use a variable which isn't set (referencing) and object.
- `NullReferenceException` can be avoided by writing code that checks for `null` before accessing an object, or uses `try/catch` blocks.

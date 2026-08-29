# GameObject

> `GameObject` class is used to represent anything which can exist in a Scene.

GameObjects are the building blocks for scenes in Unity, and act as a container for functional components which determine how the GameObject looks, and what the GameObject does.

GameObjects are active by default, but can be deactivated, which turns off all components attached to the GameObject. This generally means it will become invisible, and not receive any of the normal callbacks or events such as `Update` or `FixedUpdate`.

The GameObject's active status is represented by the checkbox to the left of the GameObject's name. You can control this using `GameObject.SetActive`.

You can also read the current active state using `GameObject.activeSelf`, and whether or not the GameObject is actually active in the scene using `GameObject.activeInHierarchy`. The latter of these two is necessary because whether a GameObject is actually active is determined by its own active state, plus the active state of all of its parents. If any of its parents are not active, then it will not be active despite its own active setting.

Some of Unity's systems, such as _Global Illumination, Occlusion, Batching, Navigation, and Reflection Probes_, rely on the **static** status of a GameObject. You can control which of Unity's systems consider the GameObject to be static by using `GameObjectUtility.SetStaticEditorFlags`.

Tags provide a way of marking and identifying types of GameObject in your scene and Layers provide a similar but distinct way of including or excluding groups of GameObjects from certain built-in actions, such as rendering or physics collisions.

You can modify tag and layer values via script using the `GameObject.tag` and `GameObject.layer` properties. You can also check a GameObject's tag efficiently by using the `CompareTag` method, which includes validation of whether the tag exists, and does not cause any memory allocation.

## Creating and Destroying GameObjects (derrived from `UnityEditor.Object`)

- GameObject can be created using the `Instantiate` method which makes a new copy of an existing object.

- `Destroy` method that will destroy an object after the frame update. Note that the 'Destroy' function can destroy individual components without affecting the GameObject itself.

``` c#
Destroy(this); // destroy script

Destroy(gameObject); // destroy game object
```
To create instances of Unity's built-in primitives, use `GameObject.CreatePrimitive`, which instantiates a primitive of the type that you specify. The available primitive types are `Sphere`, `Capsule`, `Cylinder`, `Cube`, `Plane` and `Quad`.

```c#
GameObject.CreatePrimitive(PrimitiveType.Cube);
```

## Access to components

```c#

AddComponent<Type>();

GetComponent<Type>();

```

## Finding child GameObjects

```c#

// because all GameObjects implicitly have a Transform
foreach (Transform t in transform) {}

```

You can also locate a specific child object by name using the `Transform.Find` method:

```c#
transform.Find("Frying Pan");
```

## Finding GameObjects by Name or Tag

```c#
GameObject player;
GameObject chef;
GameObject[] stoves;

player = GameObject.Find("MainHeroCharacter");
chef   = GameObject.FindWithTag("Chef");
stoves = GameObject.FindGameObjectsWithTag("Stove");
```

## Sending and Broadcasting messages

`BroadcastMessage` allows you to send out a call to a named method, without being specific about where that method should be implemented. You can use it to call a named method on every MonoBehaviour on a particular GameObject or any of its children. You can optionally choose to enforce that there must be at least one receiver (or an error is generated).

`SendMessage` is a little more specific, and only sends the call to a named method on the GameObject itself, and not its children.

`SendMessageUpwards` is similar, but sends out the call to a named method on the GameObject and all its parents.

# MonoBehaviour

> The `MonoBehaviour` class is the base class from which every Unity script derives, by default. It provides the framework which allows you to attach your script to a GameObject in the editor, as well as providing hooks into useful Events such as `Start` and `Update`.

- Allows you to start, stop, and manage Coroutines.
- Provides access to a large collection of event messages, which allows you to execute your code based on what is currently happening in your project.

# Object

> `Object` acts as a base class for all objects that Unity can reference in the editor. Classes which inherit from `UnityEngine.Object` have special functionality which means they can be dragged and dropped into fields in the Inspector, or picked using the Object Picker next to an Object field.

The `Object` class provides a few methods which allow you to `Instantiate` and `Destroy` them properly, as well as finding references to Objects of a specific type.

When creating your own objects via scripting, you typically do not want to inherit directly from `Object`. Instead, you should inherit from a class designed to be more specific to your goal:

- `MonoBehaviour` if you want to write a custom component which you can add to a GameObject, to control what the GameObject does or provide some functionality relating to it.

- `ScriptableObject` if you want to create custom assets which can store serialized data.

Both of these inherit from Unity's `Object` class, but provide extra functionality to suit those purposes.

# Vectors

Unity provides `Vector2`, `Vector3` and `Vector4` for 2D, 3D and 4D vectors. For the underlying math — addition, subtraction, scalar multiplication, dot/cross product, normalization — see [CG Math Handbook § Vector math](<../Graphics Theory/CG Math Handbook.md#vector-math>). This section covers the Unity-specific API and a few practical tips.

## Distance checks without the square root

Getting a vector's magnitude involves a square root, which is relatively slow. If you only need the distance for a comparison (a proximity check, say), skip the square root entirely and compare squared values instead via `sqrMagnitude`:

```c#
// This is much more efficient than using the true magnitude in the comparison.
vec.sqrMagnitude < dist * dist
```

## Dot product — isolating directional speed

```c#
/*
For example, a car's speedometer typically works by measuring the rotational speed of the wheels. The car may not be moving directly forward (it may be skidding sideways, for example) in which case part of the motion will not be in the direction the car is facing - and so won't be measured by the speedometer. The magnitude of an object's rigidbody.velocity vector will give the speed in its direction of overall motion but to isolate the speed in the forward direction, you should use the dot product
*/
var fwdSpeed = Vector3.Dot(rigidbody.velocity, transform.forward);
```

> The direction vector must always be normalized for this calculation. Not only is the result more correct than the magnitude of the velocity, it also **avoids the slow square root operation involved in finding the magnitude**.

## Cross product

```c#
Vector3.Cross(v1, v2);
```

## Computing a Normal/Perpendicular vector

A "normal" vector (ie. a vector perpendicular to a plane) is required frequently during mesh generation and is also useful in path following and other situations.

Given three points in the plane, say the corner points of a mesh triangle, you can find the normal as follows:

- Pick one of the three points
- Subtract it from each of the two other points separately (resulting in two new vectors, "Side 1" and "Side 2")
- Calculate the cross product of the vectors "Side 1" and "Side 2"
- The result of the cross product is a new vector that is perpendicular to the plane.

![image](https://user-images.githubusercontent.com/7611372/187892399-bd158483-2ff3-42ae-9b01-83b3a89694a1.png)

```c#
Vector3 a;
Vector3 b;
Vector3 c;

Vector3 side1 = b - a;
Vector3 side2 = c - a;

Vector3 normal = Vector3.Cross(side1, side2);
```

For meshes, the normal vector must also be normalized. This can be done with the normalized property, but there is another trick which is occasionally useful. You can also normalize the perpendicular vector by dividing it by its magnitude:

```c#
float perpLength = perp.magnitude;
perp /= perpLength;
```

> The area of the triangle is equal to `perpLength / 2`.

# Quaternion

Unity uses the `Quaternion` class to store the three dimensional orientation of GameObjects, as well as using them to describe a relative rotation from one orientation to another.

When dealing with handling rotations in your scripts, you should use the `Quaternion` class and its functions to create and modify rotational values. There are some situations where it is valid to use Euler angles, but you should bear in mind:

- You should use the Quaternion Class functions that deal with Euler angles
- Retrieving, modifying, and re-applying Euler values from a rotation can cause unintentional side-effects

When you read the `.eulerAngles` property, Unity converts the Quaternion's internal representation of the rotation to Euler angles. Because, there is more than one way to represent any given rotation using Euler angles, the values you read back out may be quite different from the values you assigned. This can cause confusion if you are trying to gradually increment the values to produce animation.

## Creating Rotations:

- `Quaternion.LookRotation`
- `Quaternion.Angle`
- `Quaternion.AngleAxis`
- `Quaternion.FromToRotation`

## Manipulating Rotations:

- `Quaternion.Slerp`
- `Quaternion.Inverse`
- `Quaternion.RotateTowards`

`Transform` class also provides methods which allow you to work with the `Quaternion` rotations:

- `Transform.Rotate`
- `Transform.RotateAround`

Wrong:

```c#
// rotation scripting mistake #1
// the mistake here is that we are modifying the x value of a quaternion
// this value does not represent an angle, and does not produce desired results

void Update ()
{
    var rot = transform.rotation;
    rot.x += Time.deltaTime * 10;
    transform.rotation = rot;
}

// rotation scripting mistake #2
// Read, modify, then write the Euler values from a Quaternion.
// Because these values are calculated from a Quaternion,
// each new rotation might return very different Euler angles, which might suffer from gimbal lock.

void Update ()
{
    var angles = transform.rotation.eulerAngles;
    angles.x += Time.deltaTime * 10;
    transform.rotation = Quaternion.Euler(angles);
}
```

Correct:

```c#
// Rotation scripting with Euler angles correctly.
// Store the Euler angle in a class variable, and only use it to
// apply it as an Euler angle, but never rely on reading the Euler back.

float x;
void Update ()
{
    x += Time.deltaTime * 10;
    transform.rotation = Quaternion.Euler(x,0,0);
}
```

# ScriptableObject

A ScriptableObject is a data container that you can use to save large amounts of data, independent of class instances. One of the main use cases for ScriptableObjects is to reduce your Project's memory usage by avoiding copies of values. This is useful if your Project has a Prefab that stores unchanging data in attached MonoBehaviour scripts.

Every time you instantiate that Prefab, it will get its own copy of that data. Instead of using the method, and storing duplicated data, you can use a ScriptableObject to store the data and then access it by reference from all of the Prefabs. This means that there is one copy of the data in memory.

Just like MonoBehaviours, ScriptableObjects derive from the base Unity object but, unlike MonoBehaviours, you can not attach a ScriptableObject to a GameObject. Instead, you need to save them as Assets in your Project.

The main use cases for ScriptableObjects are:

- Saving and storing data during an Editor session
- Saving data as an Asset in your Project to use at run time


# Time

The Time class has a few properties which provide you with numeric values that allow you to measure time elapsing while your game or app is running. For example:

- `Time.time` returns the amount of time in seconds since your project started playing.
- `Time.deltaTime` returns the amount of time in seconds that elapsed since the last frame completed. This value varies depending on the frames per second (FPS) rate at which your game or app is running.

The Time class also provides you with properties which allow you to control and limit how time elapses, for example:

- `Time.timeScale` controls the rate at which time elapses. You can read this value, or set it to control how fast time passes, allowing you to create slow-motion effects.
- `Time.fixedDeltaTime` controls the interval of Unity's fixed timestep loop (used for physics, and if you want to write deterministic time-based code).
- `Time.maximumDeltaTime` sets an upper limit on the amount of time the engine will report as having passed by the "delta time" properties above.

## Variable and Fixed time steps

Unity has two systems which track time, one with a variable amount of time between each step, and one with a fixed amount of time between each step.

The variable time step system operates on the repeated process of drawing a frame to the screen, and running your app or game code once per frame.

The fixed time step system steps forward at a pre-defined amount each step, and is not linked to the visual frame updates. It is more commonly associated with the physics system, which runs at the rate specified by the fixed time step size, but you can also execute your own code each fixed time step if necessary.

## Variable frame rate management

The frame rate of your game or app can vary because of the time it takes to display and execute the code for each frame. This is is affected by the capabilities of the device on which it is running, and also on the varying amount of complexity of the graphics displayed and computation required each frame. For example, your game may run at a slower frame rate when there are one hundred characters active and on-screen, compared to when there is only one. This variable rate is often referred to as "frames per second", or FPS.

Unless otherwise constrained by your quality settings or by the Adaptive Performance package, Unity tries to run your game or app at the **fastest frame rate possible**.

As the frame rate varies, the the object's apparent speed also varies. If the game is running at 100 frames per second, the object moves one hundred times per second. But if the frame rate slows to 60 frames per second (due to CPU load, say) then it only steps forward sixty times a second and therefore covers a shorter distance over the same amount of time.

In most cases this is undesirable, particularly with games and animation. It is much more common to want your in-game objects to move at steady and predictable speeds regardless of the frame rate. The solution is to scale the amount of the movement each frame by the amount of time elapsed each frame, which you can read from the `Time.deltaTime` property.

> Depending on your target platform, use either `Application.targetFrameRate` or `QualitySettings.vSyncCount` to set the frame rate of your application.

## Fixed Timestep

Unlike the main frame update, Unity's physics system works to a fixed timestep, which is important for the accuracy and consistency of the simulation. At the start of the each frame, Unity performs as many fixed updates as necessary to catch up with the current time.

You can also execute your own code in sync with the fixed timestep, if necessary. This is most commonly used for executing your own physics-related code, such as applying a force to a Rigidbody.

The `fixedDeltaTime` property controls the interval of Unity's fixed timestep loop, and is specified in seconds.

> Note: A lower timestep value means more frequent physics updates and more precise simulations, which leads to higher CPU load.

## Controlling and handling variations in time

Elapsed time variations can be slight. For example, in a game running at 60 frames per second, the actual number of frames per second may vary slightly, so that each frame lasts between 0.016 and 0.018 seconds. Larger variations can occur when your app performs heavy computations or garbage collection, or when the resources it needs to maintain its frame rate are being used by a different app.

- `Time.time` indicates the amount of time elapsed since the player started, and so usually continuously and steadily rises.

- `Time.deltaTime` indicates the amount of time elapsed since the last frame, and so ideally remains fairly constant.

Both these values are subjective measures of time elapsed within your app or game. This means they take into account any scaling of time that you apply.

The unscaled versions of each of these properties (`Time.unscaledTime` and `Time.unscaledDeltaTime`) ignore subjective variations and limitations, and report the actual time elapsed in both cases. This is useful for anything that should respond at a fixed speed even when the game is playing in slow-motion. An example of this is UI interaction animation.

When a frame delay of larger than the `maximumDeltaTime` value occurs, Unity limits the value reported by `deltaTime`, and the amount added to the current time. The purpose of this limit is to avoid undesirable side-effects that might occur if the timestep exceeded that amount. If there was no limit, an object whose movement was scaled by `deltaTime` would be able to "glitch" through a wall in a game during a frame rate spike, because there would theoretically be no limit to how far an object could move from one frame to the next, so it could possibly jump from one side of an obstacle to another in a single frame without intersecting with it at all.

The `Time.smoothDeltaTime` property reports an approximation of the recent `deltaTime` values with all variations smoothed out according to an algorithm. This is another technique to avoid undesirably large steps or fluctuations in movement or other time-based calculations. In particular, those which fall below the threshold set by `maximumDeltaTime`. The smoothing-out algorithm cannot predict future variations, but it gradually adapts its reported value to smooth out variations in the recently elapsed delta time values, so that the average reported time remains approximately equivalent to the actual amount of time elapsed.

## Time variation and the physics system

The `maximumDeltaTime` value also affects the physics system. The physics system uses the `fixedTimestep` value to determine how much time to simulate in each step. Unity tries to keep the physics simulation up-to-date with the amount of time that has elapsed and, as mentioned above, sometimes performs multiple physics updates per frame. However if the physics simulation fall too far behind, for example because of some heavy computation or a delay of some kind, the physics system may require a large number of steps to catch up with the current time. This large number of steps may then itself cause a further slow-down.

To avoid this cyclic feedback of slowing down due to attempting to catch up, the `maximumDeltaTime` value also acts as a limit on the amount of time the physics system will simulate between any given two frames.

If a frame update takes longer than `maximumDeltaTime` to process, the physics engine will not try to simulate any time beyond the `maximumDeltaTime`, and instead lets the frame processing catch up. Once the frame update has finished, the physics resumes as though no time has passed since it stopped. The result of this is that physics objects will not move perfectly in real time as they usually do, but will be slowed slightly. However, the physics "clock" will still track them as though they were moving normally. The slowing of physics time is usually not noticeable and is often an acceptable trade-off against gameplay performance.

## Time Scale
For special time effects such as slow-motion, it's sometimes useful to slow the passage of game time so that animations and time-based calculations in your code happen at a slower pace. Furthermore, you may sometimes want to freeze game time completely, as when the game is paused. Unity has a Time Scale property that controls how fast game time proceeds relative to real time.

> Note that the time scale doesn't actually slow execution but instead changes the time step reported to the `Update` and `FixedUpdate` functions with `Time.deltaTime` and `Time.fixedDeltaTime`. Your `Update` function may be called just as often when you reduce your time scale, but the value of `deltaTime` each frame will be less. Other script functions aren't affected by the time scale, so you can for example display a GUI with normal interaction when the game is paused.

## Capture frame rate

A special case of time management is where you want to record gameplay as a video. Since the task of saving screen images takes considerable time, the game's normal frame rate is reduced, and the video doesn't reflect the game's true performance.

To improve the video's appearance, use the Capture Framerate property. The property's default value is 0, for unrecorded gameplay. For recording. When you set the property's value to anything other than zero, game time is slowed and the frame updates are issued at precise regular intervals. The interval between frames is equal to `1 / Time.captureFramerate`, so if you set the value to 5.0 then updates occur every fifth of a second. With the demands on frame rate effectively reduced, you have time in the Update function to save screenshots or take other actions:

```c#
void Start () {
    // Set the playback frame rate (real time will not relate to game time after this).
    Time.captureFramerate = frameRate;

    // Create the folder
    System.IO.Directory.CreateDirectory(folder);
}


void Update () {
    // Append filename to folder name (format is '0005 shot.png"')
    string name = string.Format("{0}/{1:D04} shot.png", folder, Time.frameCount );

    // Capture the screenshot to the specified file.
    Application.CaptureScreenshot(name);
}
```

Using this technique improves the video, but can make the game much harder to play. Try different values of `Time.captureFramerate` to find a good balance.

# Mathf

Unity's Mathf class provides a collection of common math functions, including trigonometric, logarithmic, and other functions commonly required in games and app development.

## Trigonometric

All Unity's trigonometry functions work in radians.

- `Sin`
- `Cos`
- `Tan`
- `Asin`
- `Acos`
- `Atan`
- `Atan2`

`PI` is available as a constant, and you can multiply by the static values `Rad2Deg` or `Deg2Rad` to convert between radians and degrees.

```c#

var deg = .5f * Rad2Deg; // 360 / (PI * 2)

var rad = 180f * Deg2Rad; // (PI * 2) / 360

```

## Powers and Square Roots

- `Pow`
- `Sqrt`
- `Exp`

These are useful when working with common binary data sizes, which are often constrained or optimized to power-of-two values (such as texture dimensions):

- `ClosestPowerOfTwo`
- `NextPowerOfTwo`
- `IsPowerOfTwo`

## Interpolation

Interpolation functions allows you to calculate a value that is some way between two given points.

- `Lerp`
- `LerpAngle`
- `LerpUnclamped`
- `InverseLerp`
- `MoveTowards`
- `MoveTowardsAngle`
- `SmoothDamp`
- `SmoothDampAngle`
- `SmoothStep`

> The `Vector` classes and the `Quaternion` class all have their own interpolation functions (such as `Quaternion.Lerp`) which allow you to interpolate positions, directions and rotations in multiple dimensions.

## Limiting and repeating values

These simple helper functions are often useful in games or apps and can save you time when you need to limit values to a certain range or repeat them within a certain range.

- `Max` and `Min`
- `Repeat` and `PingPong`
- `Clamp` and `Clamp01`
- `Ceil` and `Floor`

## Logarithmic

The `Log` function allows you to calculate the logarithm of a specified number, either the natural logarithm or in a specified base. Additionally the `Log10` function returns the base–10 logarithm of the specified number.


# Random

The Random class provides you with easy ways of generating various commonly required types of random values.

## Simple random numbers

- `Random.value` gives you a random floating point number between 0.0 and 1.0. A common usage is to convert it to a number between zero and a range of your choosing by multiplying the result.

- `Random.Range` gives you a random number between a minimum and maximum value that you provide. It returns either an integer or a float, depending on whether the min and max values provided are integers or floats.

## Random points within Circles or Spheres

- `Random.insideUnitCircle` returns a randomly selected point inside a circle with a radius of 1 (Again you can multiply the result to get a random point within a circle of any size).

- `Random.insideUnitSphere` returns a randomly selected point inside a sphere with a radius of 1.

- `Random.onUnitSphere` returns a randomly selected point on the surface of a sphere with a radius of 1.

## Other types of random values

- `Random.rotation` to generate a random rotation.

- `Random.ColorHSV` to generate a random color.

## Choosing a Random Item from an Array

> `Random.Range` returns a value from a range that includes the first parameter but excludes the second, so using `myArray.Length` here gives the correct result.

```c#

var element = myArray[Random.Range(0, myArray.Length)];

```

## Shuffling a List

```c#
void Shuffle (int[] deck) {
    for (int i = 0; i < deck.Length; i++) {
        int temp = deck[i];
        int randomIndex = Random.Range(i, deck.Length);
        deck[i] = deck[randomIndex];
        deck[randomIndex] = temp;
    }
}
```

## Choosing from a Set of Items Without Repetition

A common task is to pick a number of items randomly from a set without picking the same one more than once. This can be done by iterating through the items in sequence, making a random decision for each as to whether or not it gets added to the chosen set. As each item is visited, the probability of its being chosen is equal to the number of items still needed divided by the number still left to choose from.

```c#

float probability = needToPick / itemsLeftInSet;

// check rand > probability...
```

> Note that although the selection is random, items in the chosen set will be in the same order they had in the original array. If the items are to be used one at a time in sequence then the ordering can make them partly predictable, so it may be necessary to shuffle the array before use.

<details>
  <summary>Full code</summary>

  ```c#
  Random randomGen = new Random();

  float rand () {
    return (float)randomGen.NextDouble ();
  }

  int randRange(int a, int b) {
   return randomGen.Next(a, b);
  }

  void Shuffle (int[] deck) {
      for (int i = 0; i < deck.Length; i++) {
          int temp = deck[i];
          int randomIndex = randRange(i, deck.Length);
          deck[i] = deck[randomIndex];
          deck[randomIndex] = temp;
      }

  }


  int[] ChooseSet (int[] pickFrom, int numRequired) {
    var res  = new int[numRequired];
    int rest = numRequired;

    for (var left = pickFrom.Length; left > 0; left--) {

      float prob = (float)rest/(float)left;

      if (rand() <= prob) {
        rest--;
        res[rest] = pickFrom[left - 1];
      }

      if (left == 0) break;
    }

    return res;
  }

  void Main()
  {

    var arr = new int[]{1,2,3,4,5,6,7,8,9};
    Shuffle(arr);
    var asd = ChooseSet(arr, 5);
    foreach (var i in asd) {

      Console.WriteLine($"{i}");
    }
  }

  ```
</details>

## Random Points in Space

```c#
var randVec = Vector3(Random.value, Random.value, Random.value);
```

This gives a point inside a cube with sides one unit long. The cube can be scaled simply by multiplying the X, Y and Z components of the vector by the desired side lengths. If one of the axes is set to zero, the point will always lie within a single plane.


When the volume is a sphere (ie, when you want a random point within a given radius from a point of origin), you can use `Random.insideUnitSphere` multiplied by the desired radius:

```c#
var randWithinRadius = Random.insideUnitSphere * radius;
```

Note that if you set one of the resulting vector's components to zero, you will not get a correct random point within a circle. Although the point is indeed random and lies within the right radius, the probability is heavily biased toward the center of the circle and so points will be spread very unevenly. You should use `Random.insideUnitCircle` for this task instead:

```c#
var randWithinCircle = Random.insideUnitCircle * radius;
```

# Debug

The Debug class allows you to visualise information in the Editor that may help you understand or investigate what is going on in your project while it is running.

## Logging errors, warnings and messages

```c#
Debug.Log("This is a log message.");
Debug.LogWarning("This is a warning message!");
Debug.LogError("This is an error message!");
```

> You can also optionally provide a second parameter to these log methods to indicate that the message is associated with a particular GameObject

The Debug class also offers two methods for drawing lines in the Scene view and Game view.

- `Debug.DrawLine`
- `Debug.DrawRay`


# Gizmos & Handles

The Gizmos and Handles classes allows you to draw lines and shapes in the Scene view and Game view, as well as interactive handles and controls. These two classes together provide a way for you to extend what is shown in these views and build interactive tools to edit your project in any way you like.

The Gizmos class allows you to draw lines, spheres, cubes, icons, textures and meshes into the Scene view to use as debugging, set-up aids, or tools while developing your project.

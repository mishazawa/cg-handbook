# Vector math

Vector - expression of direction and length. 
```ts
const vector = vec(x, y, z);
vector.length
```

> For Unity's vector API (`Vector2`/`Vector3`/`Vector4`) and practical usage tips, see [Scripting (Important Classes) § Vectors](<../Unity/Scripting (Important Classes).md#vectors>).

## Operations with vectors
### Addition

Adding two vectors is like taking each as a "step" and following them one after another — order doesn't matter, `v1 + v2` gives the same result as `v2 + v1`. If the first vector represents a point in space, the second can be read as an offset (a "jump") from that position.

![image](https://user-images.githubusercontent.com/7611372/202461509-4fc881d6-ad2c-4e74-b994-fb48d59ac6fb.png)


```js
v1 = vec(1, 0, 0);
v2 = vec(0, 1, 0);

/*
v3.x = v1.x + v2.x
v3.y = v1.y + v2.y
v3.z = v1.z + v2.z
*/

v3 = v1 + v2;
// 1, 1, 0
```
### Subtraction

Subtracting one vector from another gives you the direction and distance between two points: `v2 - v1` is a vector that "points" from `v1` toward `v2`, and its length is the distance between them. Unlike addition, order matters here — `v2 - v1` and `v1 - v2` point in opposite directions.

![image](https://user-images.githubusercontent.com/7611372/187888426-36bedea2-1ef4-4251-b24e-83959c5b7c0c.png)

```js
v1 = vec(1, 0, 0);
v2 = vec(4, 0, 0);

v3 = v2 - v1;
// 3, 0, 0 — points from v1 to v2, length 3
```

### Multiplication / division
Changing length of vector. Multiplying/dividing by a scalar keeps the direction the same (a negative scalar flips it) and scales the length.
```js
v1 = vec(10, 10, 0);

v2 = v1 / 10; // or v1 * 0.1
// 1, 1, 0
```

### Normalization and magnitude
Normalized vector which is 1 unit length.

Magnitude - length/size of vector.

```js
v = vec(5, 5, 5)
v.length // 8.66025

v1 = normalize(v)// 0.57735, 0.57735, 0.57735
v1.length // 1
```
### Dot product

Dot product is projection of length of vector to another vector — the amount of one vector's length that lies in the direction of another. For normalized vectors, it's essentially the cosine of the angle between them (1 = same direction, 0 = perpendicular, -1 = opposite), but much cheaper to compute than an actual cosine — a useful substitute when you just need "how aligned are these two directions", not the angle itself.

![image](https://user-images.githubusercontent.com/7611372/202464977-18c9a3d6-ee87-4491-a1a4-5530a85ac782.png)

```js
v1 = vec(1, 0, 0);
v2 = vec(0, 1, 0);
v3 = vec(-1, 0, 0);

dot(v1, v2); // 0
dot(v1, v1); // 1
dot(v1, v3); // -1
```

### Cross product

Cross product calculates perpendicular vector to another two vectors (3D only). Use the "right-hand rule" to remember the output direction: point your right hand's fingers along the first vector, curl them toward the second, and your thumb points along the result.

![image](https://user-images.githubusercontent.com/7611372/202467877-50be9ed2-7171-4c9b-923a-eff29785cb2d.png)

```js
v1 = vec(1, 0, 0);
v2 = vec(0, 1, 0);
v3 = cross(v1, v2); // 0, 0, 1
```

# Trigonometry
## Radians/degrees

PI = length of circle divided by its diameter.

```js
PI rad = 180 degrees
2PI = 360
```

### Conversion

```js
rad = deg * PI / 180

deg = rad * 180 / PI
```
## `sin`, `cos` & `tan`

![image](https://user-images.githubusercontent.com/7611372/202475393-f1efca6d-5d7c-4484-af3b-961bb0c6097d.png)

### `secant`, `cosecant` & `cotan`
Just inverted `sin`, `cos` and `tan`.

```js
secant   = 1/sin(rad)
cosecant = 1/cos(rad)
cotan    = 1/tan(rad)
```

### Unit circle 
![image](https://user-images.githubusercontent.com/7611372/202477157-989816ad-88f8-4cd3-a75c-d17688e4ceb7.png)

```js
x = radius * cos(sampled_angle);
y = radius * sin(sampled_angle);
```

![image](https://user-images.githubusercontent.com/7611372/202478478-714d452d-1c82-4427-b0e8-cae6fd4ceb91.png)

```js 
// draw circle
for (let i = 0; i < 360; i++) {
  const irad = degToRad(i);
  pos = r * vec(cos(irad), sin(irad));
  point(pos);
}
```

![image](https://user-images.githubusercontent.com/7611372/202481295-56e1d56f-d00e-4ffc-9c61-ecc734b82d9d.png)

```js
// draw wave
for (let i = 0; i < 360; i++) {
  const irad = degToRad(i);
  pos = amp * vec(irad, sin(irad));
  point(pos);
}
```

## Inverse trigonometry (estimating an angle from a ratio)

`sin`, `cos` and `tan` take an angle and give you a ratio of sides. The inverse functions — `asin`, `acos`, `atan` — go the other way: give them a ratio, they give you back an angle. That's what lets you convert a point from Cartesian coordinates (x, y) to polar coordinates (r, θ) — e.g. to find the angle needed to rotate a point, apply the rotation, then convert back to Cartesian.

![image](https://user-images.githubusercontent.com/7611372/202486524-14449b98-7cd9-434d-a8ec-5984dbe82fd6.png)

For a right triangle with hypotenuse `a`, opposite side `b`, and adjacent side `c`:

```js
angle = asin(b / a); // sin, range 0 - 90
angle = acos(c / a); // cos, range 0 - 180
angle = atan(b / c);  // tan, range 0 - 90 — but see below
```

`atan` only sees the ratio `b / c`, not the actual signs of `b` and `c`, so it can't tell which quadrant the angle is really in — two different points can produce the same ratio and the same `atan` result. That's what `atan2` fixes.

### Atan2 — full 0-360° range

`atan2(y, x)` computes the angle of a point `(x, y)` relative to the origin. Unlike `atan`, it takes `x` and `y` as separate arguments, so it can use their individual signs to return the correct angle anywhere around the full circle, not just within one quadrant.

```js
angle = atan2(b, c); // atan2(y, x)

// examples
atan2(1, 0);  // point straight up   → 90°  (PI / 2)
atan2(0, -1); // point straight left → 180° (PI)
atan2(-1, 0); // point straight down → -90° (-PI / 2)
```

# Quaternion

A quaternion represents a rotation with 4 numbers: an axis (x, y, z), and a scalar w.

```js
vec4(x, y, z, w)
```
### Houdini

```vex
v@v = {1, 0, 0};                          // vector to rotate
vector4 q = quaternion($PI/2, {0, 1, 0}); // 90° rotation around the Y axis

@N = qrotate(q, @v); // apply the rotation
```

![image](https://user-images.githubusercontent.com/7611372/202493177-c346cd5e-46f5-4ff5-a4d2-ad28c2c7509f.png)


### Three.js

```js
const quaternion = new THREE.Quaternion();
quaternion.setFromAxisAngle( new THREE.Vector3( 0, 1, 0 ), Math.PI / 2 ); // 90° around Y

const vector = new THREE.Vector3( 1, 0, 0 );
vector.applyQuaternion( quaternion ); // rotate the vector
```

### Dihedral

A dihedral rotation is the shortest rotation that takes one vector and points it in the direction of another. Houdini exposes it as a single built-in function rather than something you build by hand from a reflection + rotation:

```
vector v1 = {1, 0, 0};
vector v2 = {0, 1, 0};

vector4 q = dihedral(v1, v2); // rotation that takes v1 onto v2

@P = qrotate(q, @P); // apply it to a point
```
![image](https://user-images.githubusercontent.com/7611372/202494756-a5dd486e-58e0-4fd4-b8c3-90a5ef8a9b87.png)

# Matrices / Transformations

A matrix is a grid of numbers used to represent a transformation. In 2D space a transformation matrix is 3x3; in 3D space it's 4x4.

### Identity matrix

Doing nothing: multiplying any vector or matrix by the identity matrix leaves it unchanged.

```
1 0 0 0
0 1 0 0
0 0 1 0
0 0 0 1
```

```vex
matrix m = ident();
```

```js
const m = new THREE.Matrix4();
```

## Operations with matrices

### Determinant

A single number that tells you whether a matrix has an inverse. A determinant of 0 means the matrix has no inverse — it's "singular" (e.g. it collapses space into a lower dimension, like scaling by 0).

### Inverse

The inverse of a transformation matrix is the matrix that undoes it — e.g. the inverse of a rotation matrix rotates back the other way.

Computing a general inverse is expensive, so in computer graphics it's common to use a cheaper shortcut instead where possible — like the transpose below, which for a pure rotation matrix happens to equal the inverse.

```
@P *= inverse(4@mat);
```

### Transpose

Swap rows with columns.

For a pure rotation matrix, the transpose *is* the inverse. This is because rotation matrices are orthogonal, and the inverse of an orthogonal matrix always equals its transpose — so "inverting" a rotation is just a cheap transpose, no real matrix inversion needed.

That shortcut breaks once translation is mixed in — a matrix that also encodes position doesn't have transpose == inverse. In that case, use a simplified inversion that handles the translation term separately, or fall back to a full matrix inversion for anything more complex.

### Multiplying by a scalar

Every number in the matrix gets multiplied by the scalar:

```
[A A A]       [kA kA kA]
[A A A] * k = [kA kA kA]
[A A A]       [kA kA kA]
```

### Multiplying by a vector

This is how a matrix actually transforms a point or direction. Order matters, and different engines put the vector on a different side of the matrix by convention:

```
// column vector, matrix on the left (OpenGL)
M * vec = result

// row vector, matrix on the right (DirectX, Houdini)
vec * M = result
```

### Multiplying two matrices

Order matters here too: combining a translate (T), rotate (R) and scale (S) gives a different result depending on the order you multiply them in — `TRS ≠ RTS ≠ SRT`.

Each cell of the result is a row of the left matrix "dotted" with a column of the right matrix:

**ROW x COLUMN**

```
[a b] * [e f] = [a*e + b*g][a*f + b*h]
[c d]   [g h]   [c*e + d*g][c*f + d*h]
```

Multiplying by the identity matrix leaves the other matrix unchanged:

```
[a b] * [1 0] = [a b]
[c d]   [0 1]   [c d]
```

### Transformation matrix

To transform a point, represent it as a vector and multiply it by the transformation matrix. Translation, rotation and scale each have a characteristic layout of numbers within the matrix. The examples below use row vectors (as in Houdini/DirectX — see "Multiplying by a vector" above), so the translation values sit along the bottom row:

```js
// Translation — moves the point by (x, y, z)
1 0 0 0
0 1 0 0
0 0 1 0
x y z 1

// Rotation — the r values encode the rotation
r r r 0
r r r 0
r r r 0
0 0 0 1

// Scale — scales by (x, y, z)
x 0 0 0
0 y 0 0
0 0 z 0
0 0 0 1
```

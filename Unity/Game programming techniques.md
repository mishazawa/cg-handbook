# GPU instancing

Draw many copies of the same mesh in a single draw call instead of one draw call per object. The CPU sends the mesh once, plus a list of per-instance data (usually just a transform matrix, sometimes color etc.), and the GPU draws all copies from that. Cuts CPU overhead when you have lots of identical objects — grass, rocks, crowds, particles.

```
// naive: one draw call per object, expensive with many objects
for pos in positions:
  draw(mesh, material, pos)

// instanced: one draw call for all of them
draw_instanced(mesh, material, positions)
```

# Object pool

Reuse objects instead of creating/destroying them constantly. Creating and destroying objects at runtime is relatively expensive (allocation, garbage collection). Instead, pre-allocate a batch of objects up front, keep the inactive ones in a pool, and hand them out/take them back as needed.

```
pool = []
for i in 1..N:
  obj = create(Bullet)
  obj.active = false
  pool.push(obj)

function spawn():
  for obj in pool:
    if not obj.active:
      obj.active = true
      obj.reset()
      return obj
  return null // pool empty — grow it, or just don't spawn

function despawn(obj):
  obj.active = false // back in the pool, ready to reuse
```

Common for bullets, enemies, particles, pickups — anything spawned/removed often.

# Conditional compilation

Include or exclude code at compile time based on a flag (platform, build config, debug vs release), instead of checking it at runtime. The excluded branch isn't just skipped — it's never compiled into the build, so there's zero runtime cost and no dead code shipped.

```
#if DEBUG
  log("debug info")
#endif

#if PLATFORM_MOBILE
  use_low_res_textures()
#else
  use_high_res_textures()
#endif
```

Useful for debug-only tooling, platform-specific code paths, and stripping things out of release builds entirely.

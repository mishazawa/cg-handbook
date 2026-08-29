## Create and animate model

Example animation

![image](https://user-images.githubusercontent.com/7611372/207697924-fd4f06b4-e680-4689-b989-0a23365a6f48.png)

In Non-linear animation editor create NLA Track
[Blender NLA](https://docs.blender.org/manual/en/latest/editors/nla/tracks.html#action-track)

![image](https://user-images.githubusercontent.com/7611372/207698548-ce83e8dd-3b07-4ae5-80a4-4ab5511587ce.png)

Export model(scene)

![image](https://user-images.githubusercontent.com/7611372/207699036-36028542-8cbf-49b4-b3b7-957c213765fd.png)

## Load glb

[project template](https://github.com/mishazawa/Shreh/tree/2aa42da24c80fd700361caa625024fcf5073386e)

```ts
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

// helper fn
// to load glb model
// https://threejs.org/docs/#examples/en/loaders/GLTFLoader
const load = url => new Promise((res, rej) => new GLTFLoader().load(url, data => res(data), null, rej));

// ...

// inside scene initialization

// load model
const model = await load(URL_MODEL) as Object3D;

// extract mesh from glb (it can be array of meshes or tree)
const mesh = model['scene'] as Mesh;

// f.e. extract clip by name 
// model.animations -> Array<THREE.AnimationClip>
// https://threejs.org/docs/#api/en/animation/AnimationClip
const currentClip = AnimationClip.findByName(model.animations, "ExampleAnimation");

// attach mesh to animation
// https://threejs.org/docs/#api/en/animation/AnimationMixer
const mixer = new AnimationMixer(mesh);

// get reference for clip to use his methods
// https://threejs.org/docs/#api/en/animation/AnimationMixer.clipAction
const action = mixer.clipAction(currentClip);

// add mesh to scene
scene.add(mesh);

// ...

// to play animation it should be updated each frame
// https://threejs.org/docs/#api/en/animation/AnimationMixer.update
function update(deltaTime) {
    mixer.update(deltaTime);
}

// ...

// somewhere in code trigger animation
// https://threejs.org/docs/#api/en/animation/AnimationAction
action.reset().play();
```

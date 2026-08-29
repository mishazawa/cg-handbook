## Draw line through 2 points

```ts
const R = ...renderer...;

function line(coords1: Coords, coords2: Coords) {
  const slope = (coords1.y - coords2.y) / (coords1.x - coords2.x);
  const b = coords1.y - slope * coords1.x;

  const xmin = -R.width;
  const xmax = R.width;

  const ymin = slope * xmin + b;
  const ymax = slope * xmax + b;

  R.line(xmin, ymin, xmax, ymax);
}
```

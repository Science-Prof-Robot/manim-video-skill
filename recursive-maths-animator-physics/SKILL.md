---
name: recursive-maths-animator-physics
description: Create verified Manim physics animations using manim-physics for rigid mechanics, pendulums, electromagnetism, optics, waves, and custom deterministic physics models.
---

# Recursive maths animator — physics compatibility skill

Physics is now part of the main `recursive-maths-animator` skill. Read
[`../recursive-maths-animator/SKILL.md`](../recursive-maths-animator/SKILL.md)
first; this file remains as a detailed compatibility entry point for hosts that
discover physics separately.

## Dependency and supported scope

The project pins `manim-physics==0.4.0` in `recursive-maths-animator/requirements.txt`.
Install or refresh the environment with:

```bash
pip install -r recursive-maths-animator/requirements.txt
```

The package is imported with:

```python
from manim import *
from manim_physics import *
```

The supported built-in families are:

- Rigid mechanics: `SpaceScene`, gravity, rigid/static bodies, collisions,
  elasticity, density, friction, and pendulums.
- Electromagnetism: `Charge`, `ElectricField`, `Wire`, and `MagneticField`.
- Optics: lenses and rays.
- Waves: `LinearWave`, `RadialWave`, and `StandingWave`.

Do not imply that a visual simulation is physically exact. State assumptions,
units, dimensionality, integration method, and omitted effects in the scene or
accompanying notes.

## Scene selection

Use the narrowest scene base that matches the model:

| Need | Base/pattern |
| --- | --- |
| Gravity, body interactions, or collisions | `SpaceScene` |
| A swinging pendulum without collisions | `Scene` plus `Pendulum` |
| Field visualization | `Scene` or `ThreeDScene` plus field objects |
| 2D/3D wave propagation | `Scene` or `ThreeDScene` plus wave objects |
| A custom ODE/PDE or particle model | Main Manim scene plus a deterministic updater |

For rigid mechanics, register movable objects with
`self.make_rigid_body(...)` and boundaries with `self.make_static_body(...)`.
Set `self.GRAVITY` explicitly when the direction or magnitude is part of the
explanation. Tune `elasticity`, `density`, and `friction` deliberately rather
than relying on defaults.

Example:

```python
from manim import *
from manim_physics import SpaceScene


class TwoObjectsFalling(SpaceScene):
    GRAVITY = DOWN * 9.8

    def construct(self):
        ball = Circle(radius=0.25, color=BLUE, fill_opacity=1).shift(UP * 2)
        floor = Line(LEFT * 5 + DOWN * 3, RIGHT * 5 + DOWN * 3)
        self.add(floor, ball)
        self.make_static_body(floor)
        self.make_rigid_body(ball, elasticity=0.8, density=1, friction=0.8)
        self.wait(4)
```

For pendulums, add the pendulum's bobs as rigid bodies before starting the
swing. For waves and fields, make start/stop behavior explicit so the final
frame is stable during verification.

## Physics workflow

1. Write a short physical thesis: what is moving, what causes the motion, and
   what the viewer should notice.
2. Record assumptions: 2D vs 3D, units, constants, initial conditions,
   boundary conditions, timestep/frame rate, and whether the result is
   qualitative or quantitative.
3. Choose a built-in `manim-physics` object where it fits. Use a custom updater
   or numerical integrator only for behavior the package does not provide.
4. Keep the model deterministic. Seed random initial conditions, avoid live
   network data, and do not make simulation results depend on wall-clock time.
5. Render a low-quality approval GIF, then a high-quality MP4 using the main
   animator skill's commands.
6. Extract frames and complete the main skill's visual verification loop. Check
   for tunneling, unstable energy, excessive jitter, field discontinuities,
   clipping, and labels that imply more precision than the model supports.
7. Only after verification, upload the MP4 using the local ignored S3 publisher.

## Numerical and visual guardrails

### Layout and overlap guardrails

- Treat the scene as a responsive layout, not a fixed pile of labels. Reserve
  explicit regions for the physical construction, live values, graph, and
  status text before placing objects.
- Use the minimum words needed to identify the idea. Remove duplicate captions,
  subtitles, and labels that the geometry already makes obvious.
- Keep labels outside moving paths and keep the graph in a reserved region that
  moving objects and rays cannot enter. If a moving object can approach a text
  element, make the text or its container resize/reposition with the state.
- After every render, inspect beginning, middle, and end frames at the target
  resolution. Reject the scene if any label, ray, object, graph, or title
  overlaps, clips, or becomes unreadable; shrink or reposition the affected
  group and rerender.

- Keep the render frame rate high enough for collision detection; low frame
  rates can allow bodies to pass through static objects.
- Use normalized or clearly labeled units when showing quantities.
- For custom integration, prefer a fixed timestep and document the integrator.
- Separate simulation state from visual state so a re-render is reproducible.
- Do not use exaggerated gravity, mass, or field strength without labeling it
  as a visual scale.
- Verify conservation claims empirically; do not call a model energy-conserving
  unless the implementation and measured error support that claim.

## References

The implementation is based on the official `manim-physics` v0.4.0
documentation:

- https://manim-physics.readthedocs.io/en/latest/
- https://manim-physics.readthedocs.io/en/latest/reference/manim_physics.optics.lenses.Lens.html
- https://manim-physics.readthedocs.io/en/latest/reference/manim_physics.optics.rays.Ray.html
- https://manim-physics.readthedocs.io/en/latest/reference/manim_physics.rigid_mechanics.rigid_mechanics.html
- https://manim-physics.readthedocs.io/en/latest/reference/manim_physics.wave.html

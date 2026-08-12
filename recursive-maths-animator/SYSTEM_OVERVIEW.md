# System overview

## Canonical workflow

1. Read `SKILL.md`.
2. Define the visual thesis and scene beats.
3. Record assumptions, dependencies, and layout regions.
4. Implement the Manim scene.
5. Render a low-quality smoke test.
6. Extract and inspect frames for alignment, overlap, clipping, and physical
   correctness.
7. Fix issues and repeat.
8. Render the final MP4.
9. Upload only after verification.

## Supported modes

- Mathematical explainers and graphs.
- Voiceover scenes, when explicitly needed.
- Physics: mechanics, optics, electromagnetism, waves, and custom deterministic
  models through `manim-physics`.

## Source of truth

- Agent behavior: [`SKILL.md`](SKILL.md)
- Commands: [`QUICK_START.md`](QUICK_START.md)
- Frame review: [`references/video_verification_rubric.md`](references/video_verification_rubric.md)
- Physics example: [`examples/convex_lens_object_to_infinity.py`](examples/convex_lens_object_to_infinity.py)

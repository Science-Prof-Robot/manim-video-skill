# Recursive Maths Animator

Manim-based animations for mathematics, technical explainers, and physics.
The project is designed for reproducible MP4s with a verification loop that
catches layout, overlap, clipping, and motion problems before delivery.

## What it includes

- LaTeX-free Manim examples using `Text`, lines, paths, and custom graphing.
- Optional voiceover through `manim-voiceover`.
- Physics through `manim-physics` 0.4.0: mechanics, optics, fields, waves,
  and deterministic custom models.
- Smoke tests, high-quality renders, frame extraction, and visual review.
- Optional S3 publishing through the ignored local publisher. Video files and
  credentials must never be committed to a public repository.

## Quick install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r recursive-maths-animator/requirements.txt
```

Install `ffmpeg` and `ffprobe` with your operating system package manager.
LaTeX and SoX are not required for the included silent examples.

### Codex prompt

> Read `recursive-maths-animator/SKILL.md` and use it as the project workflow. Use the physics section for physics scenes. Start with a low-quality render, extract verification frames, fix all overlap/clipping issues, then render the final MP4.

### Claude Code prompt

> Read `recursive-maths-animator/SKILL.md` before editing. Follow its Manim, physics, responsive-layout, verification, and S3 rules. Do not commit rendered videos, credentials, or ignored upload tooling.

## Render an example

```bash
source .venv/bin/activate
.venv/bin/manim -ql recursive-maths-animator/examples/convex_lens_object_to_infinity.py \
  ConvexLensObjectToInfinity --format mp4 --disable_caching
.venv/bin/manim -qh recursive-maths-animator/examples/convex_lens_object_to_infinity.py \
  ConvexLensObjectToInfinity --format mp4 --disable_caching
```

## Video examples

The original verified examples are committed under [`videos/`](videos/):

<p><strong>Table to bar chart</strong></p>
<video width="640" controls muted loop playsinline><source src="https://raw.githubusercontent.com/Science-Prof-Robot/recursive-math-animator/main/videos/TableToBarChartPattern.mp4" type="video/mp4"></video>

<p><strong>Table to line graph</strong></p>
<video width="640" controls muted loop playsinline><source src="https://raw.githubusercontent.com/Science-Prof-Robot/recursive-math-animator/main/videos/TableToLineGraphPattern.mp4" type="video/mp4"></video>

<p><strong>Table to scatter plot</strong></p>
<video width="640" controls muted loop playsinline><source src="https://raw.githubusercontent.com/Science-Prof-Robot/recursive-math-animator/main/videos/TableToScatterPlotPattern.mp4" type="video/mp4"></video>

<p><strong>Distribution animation</strong></p>
<video width="640" controls muted loop playsinline><source src="https://raw.githubusercontent.com/Science-Prof-Robot/recursive-math-animator/main/videos/DistributionAnimation.mp4" type="video/mp4"></video>

<p><strong>Formula derivation</strong></p>
<video width="640" controls muted loop playsinline><source src="https://raw.githubusercontent.com/Science-Prof-Robot/recursive-math-animator/main/videos/FormulaDerivation.mp4" type="video/mp4"></video>

<p><strong>Sampling visualization</strong></p>
<video width="640" controls muted loop playsinline><source src="https://raw.githubusercontent.com/Science-Prof-Robot/recursive-math-animator/main/videos/SamplingVisualization.mp4" type="video/mp4"></video>

<p><strong>Basic pie chart</strong></p>
<video width="640" controls muted loop playsinline><source src="https://raw.githubusercontent.com/Science-Prof-Robot/recursive-math-animator/main/videos/BasicPieChart.mp4" type="video/mp4"></video>

<p><strong>Staggered pie chart</strong></p>
<video width="640" controls muted loop playsinline><source src="https://raw.githubusercontent.com/Science-Prof-Robot/recursive-math-animator/main/videos/StaggeredPieChart.mp4" type="video/mp4"></video>

<p><strong>Pie-to-bar transition</strong></p>
<video width="640" controls muted loop playsinline><source src="https://raw.githubusercontent.com/Science-Prof-Robot/recursive-math-animator/main/videos/PieToBarTransition.mp4" type="video/mp4"></video>

<p><strong>Physics: convex lens — object beside lens to infinity</strong></p>
<video width="800" controls muted loop playsinline><source src="https://ashish-random-videos.s3.amazonaws.com/exponential-curve/convex-lens-object-to-infinity.mp4" type="video/mp4"></video>

## Physics example

The convex-lens example moves the object from beside the lens through the
focal transition and outward toward infinity. It shows virtual/upright and
real/inverted regimes, a taller lens, and a synchronized `u–v` graph confined
to the bottom-left quarter.

- Source: [`convex_lens_object_to_infinity.py`](recursive-maths-animator/examples/convex_lens_object_to_infinity.py)
- Local output: `media/videos/convex_lens_object_to_infinity/1080p60/`

The scene is qualitative/paraxial and uses `1/f = 1/u + 1/v`; it is a visual
example, not a full optical simulation.

## Verify a render

```bash
.venv/bin/python recursive-maths-animator/scripts/extract_verification_frames.py \
  media/videos/convex_lens_object_to_infinity/1080p60/ConvexLensObjectToInfinity.mp4 \
  --count 8
```

Inspect start, middle, transition, and end frames. Check that no text, rays,
images, graph elements, or titles overlap; graph content stays inside its
frame; labels remain readable; and the visual state matches the physics.

## Project map

```text
recursive-maths-animator/
├── README.md
├── recursive-maths-animator/
│   ├── SKILL.md              # canonical agent instructions
│   ├── QUICK_START.md        # command-first setup
│   ├── requirements.txt
│   ├── examples/
│   ├── scripts/
│   └── references/
└── recursive-maths-animator-physics/
    └── SKILL.md              # compatibility/detail entry point
```

## License

MIT — see [LICENSE](LICENSE).

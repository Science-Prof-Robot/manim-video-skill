# Recursive Maths Animator

> Production-ready Manim animations with zero LaTeX dependencies

[![Patterns](https://img.shields.io/badge/Patterns-9%20Verified-success)](./recursive-maths-animator/references/pattern_library/)
[![Success Rate](https://img.shields.io/badge/Success%20Rate-100%25-brightgreen)](./recursive-maths-animator/.training/)
[![LaTeX Free](https://img.shields.io/badge/LaTeX-Free-blue)](./recursive-maths-animator/SKILL.md)

Create beautiful, narrated mathematical animations in minutes — not hours.

This repository is a **Cursor / Claude Code agent skill** for **technical and mathematical animations** using [Manim Community](https://www.manim.community/). It teaches compatible agents how to structure projects, version scenes with git, add optional narration, and run a **vision review loop** after each render.

### 1-Shot Demo (Single Prompt)

https://github.com/user-attachments/assets/e8976362-ad4f-4655-a41b-e21f86bcd253

---

## Quick Start (30 Seconds)

```bash
# 1. Activate environment
source recursive-maths-animator/.training/.venv-3.12/bin/activate

# 2. Render a pattern
python recursive-maths-animator/references/pattern_library/table_transforms_tested.py TableToBarChartPattern -ql --format mp4

# 3. Get your video
# Output: media/videos/1080p60/TableToBarChartPattern.mp4
```

No LaTeX installation. No complex setup. Just working animations.

---

## The 9 Verified Patterns

### Table-to-Graph Transformations

| Pattern | Use Case | Video |
|---------|----------|-------|
| **TableToBarChartPattern** | Quarterly reports, category comparisons | [▶️ Watch](videos/TableToBarChartPattern.mp4) |
| **TableToLineGraphPattern** | Time series, trends over months | [▶️ Watch](videos/TableToLineGraphPattern.mp4) |
| **TableToScatterPlotPattern** | Correlation analysis, relationships | [▶️ Watch](videos/TableToScatterPlotPattern.mp4) |

```python
from references.pattern_library import TableToBarChartPattern
scene = TableToBarChartPattern()
scene.data = [("Q1", 2500), ("Q2", 3200), ("Q3", 2800), ("Q4", 4100)]
scene.bar_colors = [BLUE, GREEN, YELLOW, RED]
scene.render()   # → 19.3s animated video with voiceover
```

📹 **See it in action:** [TableToBarChartPattern.mp4](videos/TableToBarChartPattern.mp4)

### Statistical Visualizations

| Pattern | Use Case | Video |
|---------|----------|-------|
| **DistributionAnimation** | Normal/Gaussian curves, statistics education | [▶️ Watch](videos/DistributionAnimation.mp4) |
| **FormulaDerivation** | Step-by-step math proofs, theorem explanations | [▶️ Watch](videos/FormulaDerivation.mp4) |
| **SamplingVisualization** | Central Limit Theorem, sampling demos | [▶️ Watch](videos/SamplingVisualization.mp4) |

```python
from references.pattern_library import FormulaDerivation
scene = FormulaDerivation()
scene.formula_steps = ["a² + b² = c²", "c = √(a² + b²)"]
scene.render()   # → 17.2s video showing derivation with narration
```

📹 **See it in action:** [FormulaDerivation.mp4](videos/FormulaDerivation.mp4)

### Pie Chart Animations

| Pattern | Use Case | Video |
|---------|----------|-------|
| **BasicPieChart** | Market share, percentage breakdowns | [▶️ Watch](videos/BasicPieChart.mp4) |
| **StaggeredPieChart** | Exploded segments, emphasis | [▶️ Watch](videos/StaggeredPieChart.mp4) |
| **PieToBarTransition** | Same data, two perspectives | [▶️ Watch](videos/PieToBarTransition.mp4) |

```python
from references.pattern_library import StaggeredPieChart
scene = StaggeredPieChart()
scene.data = [("Product A", 40), ("Product B", 30), ("Product C", 30)]
scene.explode_index = 0
scene.render()   # → 21.8s video with sequential reveals and explode effect
```

📹 **See it in action:** [StaggeredPieChart.mp4](videos/StaggeredPieChart.mp4)

### Video Gallery

| # | Pattern | Duration | Size |
|---|---------|----------|------|
| 1 | TableToBarChartPattern | 19.3s | 845KB |
| 2 | TableToLineGraphPattern | 19.5s | 872KB |
| 3 | TableToScatterPlotPattern | 20.1s | 1.0MB |
| 4 | DistributionAnimation | 18.8s | 1.1MB |
| 5 | FormulaDerivation | 17.2s | 910KB |
| 6 | SamplingVisualization | 22.4s | 1.6MB |
| 7 | BasicPieChart | 19.4s | 874KB |
| 8 | StaggeredPieChart | 21.8s | 1.4MB |
| 9 | PieToBarTransition | 23.1s | 1.7MB |

**Total:** 9.4MB of production-ready animations — 1920x1080 @ 60fps, H.264, AAC audio with auto-generated voiceover and SRT captions.

---

## Key Features

### Zero LaTeX Dependencies

| Instead of | We Use | Benefit |
|------------|--------|---------|
| `Axes()` | `Line()` + `Text()` | -2GB dependency |
| `MathTex()` | `Text()` | No compilation |
| `FunctionGraph()` | `VMobject()` | Full control |
| `PieChart()` | `AnnularSector()` | No internal deps |

### Auto-Generated Voiceover

- GTTSService generates audio automatically
- 5-7 sync points per video
- SRT captions auto-generated

### Evidence-Based Timing

- 0.5s per staggered element, 2.0s for transitions, 2.0s final pause
- Total: 17-23 seconds (ideal for explainers / TikTok / Reels)

### Customizable in 3 Lines

```python
scene = TableToBarChartPattern()
scene.data = [("Your", 100), ("Data", 200)]
scene.bar_colors = ["#3498db", "#2ecc71"]
```

---

## Two Layers

| What | Where | Purpose |
|------|--------|---------|
| **Git repository root** | This folder (`README.md`, `LICENSE`, `scripts/`) | Clone, issues, and optional **ClawHub** publishing helpers. |
| **Installable skill** | **`recursive-maths-animator/`** (contains **`SKILL.md`**) | What agents actually load: copy this folder into your tool's skills path, or install via **ClawHub**. |

---

## What the skill does

| Piece | Role |
|-------|------|
| **`SKILL.md`** | When to use Manim, **brief-first** pitch + user-chosen palettes, **design theme**, folder layout, rendering, GIF/MP4 guidance, and the **verification loop**. |
| **`references/pattern_library/`** | 9 verified LaTeX-free animation patterns (table transforms, statistical viz, pie charts). |
| **`references/manim_versioning.py`** | Optional Python helper: git-backed **scene versions**, branches, rollbacks, and render helpers. |
| **`references/soft_enterprise_palette.py`** | Example color and easing helpers for consistent visuals. |
| **`references/video_verification_rubric.md`** | Checklist for reviewing **still frames** (padding, logic vs storyboard, theme, glitches). |
| **`references/gemini_tts_service.py`** | Optional: Gemini TTS for `manim-voiceover` (needs API key and `google-genai`). |
| **`scripts/extract_verification_frames.py`** | Uses **ffmpeg/ffprobe** to slice a video into frames + `manifest.json` for multimodal review. |
| **`scripts/run_pipeline.py`** | Optional render + subtitle burn-in pipeline. |
| **`scripts/check_environment.py`** | Prints whether Manim, ffmpeg, git, and common Python deps are available. |
| **`requirements.txt`** | Template copied into **new animation projects** by `ManimProject.init()`. |

### End-to-end flow

1. Agent gives a **short animation brief** and **2-3 palette / format options**; user approves before heavy coding (`ANIMATION_BRIEF.md` + `DESIGN_THEME.md`).
2. Agent writes or updates **Manim** scene code (prefer engine-native motion; see `SKILL.md`); optional **manim-voiceover** for narration.
3. User or agent **renders** MP4/GIF (Manim CLI or `ManimProject.render*`).
4. **`extract_verification_frames.py`** pulls evenly spaced stills into `exports/verification/`.
5. The **same agent session** reads those frames against the rubric and writes **`VERIFICATION_FEEDBACK.md`** with concrete fixes.
6. Iterate on code and re-render until quality is acceptable.

---

## What you need on your machine

**To use the skill** (teach the agent): Nothing beyond your editor's skill support; the agent only needs to **read** `SKILL.md` and referenced files.

**To actually render animations:**

| Requirement | Why |
|-------------|-----|
| **Python 3.9+** | Manim and scripts. |
| **[Manim Community](https://docs.manim.community/en/stable/installation.html)** | Scene rendering. |
| **ffmpeg** and **ffprobe** | Video I/O; frame extraction for verification. |
| **git** | If you use `ManimProject` versioning. |
| **manim-voiceover** (+ a TTS backend such as gTTS) | Optional narration. |
| **google-genai** + **`GEMINI_API_KEY`** | Only if you use the Gemini TTS helper. |

Quick check:

```bash
python3 recursive-maths-animator/scripts/check_environment.py
```

---

## Install the skill

Agents expect a **directory** whose name matches the skill (`recursive-maths-animator`) containing **`SKILL.md`**.

### From Git (recommended)

```bash
git clone https://github.com/Science-Prof-Robot/recursive-math-animator.git
cd recursive-math-animator
```

Then copy or symlink the **inner** skill folder to your tool's skills location.

**Cursor - all projects**

```bash
mkdir -p ~/.cursor/skills
cp -R recursive-maths-animator ~/.cursor/skills/
```

**Cursor - one repo**

```bash
mkdir -p .cursor/skills
cp -R recursive-maths-animator .cursor/skills/
```

**Claude Code - all projects**

```bash
mkdir -p ~/.claude/skills
cp -R recursive-maths-animator ~/.claude/skills/
```

**Claude Code - one repo**

```bash
mkdir -p .claude/skills
cp -R recursive-maths-animator .claude/skills/
```

Restart the editor or start a **new** agent chat so the skill is picked up.

---

## OpenClaw / ClawHub (registry install and updates)

[ClawHub](https://clawhub.ai) is the public registry for **OpenClaw** skills. This skill is published there as slug **`recursive-maths-animator`**.

| Path | What tracks the install | Typical commands |
|------|-------------------------|------------------|
| **OpenClaw workspace** | OpenClaw records ClawHub installs under your configured workspace. | `openclaw skills install ...`, `openclaw skills update ...` |
| **Standalone clawhub CLI** | A **`.clawhub/lock.json`** next to the directory you run from. | `npx clawhub@latest install ...`, `npx clawhub@latest update ...` |

### OpenClaw: `openclaw skills install` / `openclaw skills update`

```bash
# Install (first time; --force overwrites existing)
openclaw skills install recursive-maths-animator --force

# Update
openclaw skills update recursive-maths-animator
```

**If `openclaw skills update` says the skill is "not tracked"** — run `openclaw skills install recursive-maths-animator --force` once, then `openclaw skills update` will work.

### Standalone: `clawhub` CLI

```bash
# Install
npx --yes clawhub@latest install recursive-maths-animator --force

# Update
npx --yes clawhub@latest update recursive-maths-animator --force
```

### Why `clawhub` often needs `--force` (VirusTotal / "suspicious" skills)

ClawHub runs **VirusTotal Code Insight** on published skills. This repo legitimately documents API keys and optional cloud helpers, so the bundle can be **flagged as "suspicious."** Then `clawhub install` fails in non-interactive mode unless you pass `--force`. Heuristic rows in VirusTotal reports (non-standard port, sleep during execution, URLs in memory) often come from the sandbox itself or Python/Windows DLLs, not hidden endpoints. For a clean static review, prefer file hash / contents checks against this GitHub source.

**Maintainers:** publish a new semver with `CLAWHUB_TOKEN` set and `./scripts/publish_to_clawhub.sh <version> "changelog text"`.

---

## Example: Cursor

After the skill is under `.cursor/skills/` or `~/.cursor/skills/`:

1. Open the repo where you want the animation (or an empty folder).
2. Start **Agent** chat and mention you are using the **recursive maths animator** skill.
3. Point the agent at this clone if it needs scripts.

**Sample message:**

> Use the recursive maths animator skill. I want a 20-second Manim animation: derive the quadratic formula on a dark background with a "midnight + neon" palette, 16:9. Start with a short brief and 2-3 palette options; after I pick one, create `ANIMATION_BRIEF.md` and `DESIGN_THEME.md`, then implement the scene. When we have an MP4, run frame extraction and vision review per the skill.

---

## Example: Claude Code

Same layout under `~/.claude/skills/recursive-maths-animator/` or `.claude/skills/` in a project.

**Sample message:**

> Follow the recursive-maths-animator skill in my skills folder. Animate the unit circle definition of sine and cosine: circle, point moving, projecting to axes, `sin(θ)` and `cos(θ)` labels. Offer calm vs punchy motion and 1:1 vs 16:9; wait for my choices before writing scene code.

**Lighter sample:**

> Using recursive maths animator: 15-second clip showing why the sum 1 + 2 + ... + n is n(n+1)/2 with stacked blocks transforming into a rectangle. No voiceover. After render, extract verification frames and list fixes in `VERIFICATION_FEEDBACK.md`.

---

## Using helpers inside an animation project

New projects created with `ManimProject.init()` get `requirements.txt`, `ANIMATION_BRIEF.md`, `DESIGN_THEME.md`, `assets/`, `exports/`, etc. Scene code must be able to import `references/`; **`SKILL.md`** shows the usual `sys.path` pattern.

For verification after a render:

```bash
python3 path/to/recursive-maths-animator/scripts/extract_verification_frames.py path/to/output.mp4 --count 8
```

---

## What You Can Build

- **Educational Content** — Math tutorials, statistics explanations, data visualization lessons
- **Business Presentations** — Quarterly reports, market share breakdowns, trend analysis
- **Social Media** — Short-form explainers (17-23s, perfect for TikTok/Reels), animated infographics
- **Documentation** — API visualization, process flows, feature explanations

---

## Repository Layout

```text
recursive-math-animator/              # git repo root
├── LICENSE
├── README.md                          # this file
├── .gitignore
├── scripts/                           # publish_to_clawhub.sh (maintainers)
└── recursive-maths-animator/          # the installable skill
    ├── SKILL.md                       # agent instructions
    ├── README.md                      # inner docs
    ├── requirements.txt               # copied into new Manim projects by init()
    ├── references/
    │   ├── pattern_library/           # 9 verified LaTeX-free patterns
    │   │   ├── table_transforms_tested.py
    │   │   ├── statistical_viz_tested.py
    │   │   ├── pie_charts_tested.py
    │   │   └── QUICK_REFERENCE.md
    │   ├── manim_versioning.py
    │   ├── soft_enterprise_palette.py
    │   ├── gemini_tts_service.py
    │   └── video_verification_rubric.md
    ├── scripts/
    │   ├── extract_verification_frames.py
    │   ├── run_pipeline.py
    │   └── check_environment.py
    ├── .training/                     # evidence & learnings (gitignored)
    └── media/                         # rendered videos (gitignored)
```

---

## Smoke test

```bash
printf '%s\n' 'from manim import *' 'class Smoke(Scene):' '    def construct(self): self.play(Write(Text("ok")))' > smoke.py
manim -ql smoke.py Smoke
```

## Quick Commands Cheat Sheet

```bash
# Render specific pattern
python recursive-maths-animator/references/pattern_library/table_transforms_tested.py TableToBarChartPattern -ql --format mp4

# List all patterns
python -c "from references.pattern_library import __all__; print('\n'.join(__all__))"

# Render all patterns
for p in TableToBarChartPattern TableToLineGraphPattern TableToScatterPlotPattern DistributionAnimation FormulaDerivation SamplingVisualization BasicPieChart StaggeredPieChart PieToBarTransition; do
  python recursive-maths-animator/references/pattern_library/table_transforms_tested.py $p -ql --format mp4
done
```

## License

MIT — see [LICENSE](LICENSE).

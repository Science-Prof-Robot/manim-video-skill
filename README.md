# recursive-maths-animator (agent skill)

Portable **Cursor** and **Claude Code** skill for [Manim](https://www.manim.community/) animations with optional **manim-voiceover**, git-based **scene versioning** (`references/manim_versioning.py`), palette helpers, optional **Gemini TTS** (`references/gemini_tts_service.py`), and a **vision verification loop**.

The agent-facing instructions live in [`recursive-maths-animator/SKILL.md`](recursive-maths-animator/SKILL.md). Install by placing the **`recursive-maths-animator`** directory (the folder that contains `SKILL.md`) in a skills path (see below), or install from **ClawHub** (see below).

**Behavior highlights:** `ManimProject.init()` seeds **`requirements.txt`**, **`DESIGN_THEME.md`**, **`assets/{images,svgs,fonts}`**, **`exports/approvals/`**, and **`exports/verification/`**. Agents confirm a **design theme** first, keep **`requirements.txt`** accurate, use **GIF previews** where useful, then run **frame extraction** + multimodal review per **`SKILL.md`**.

## Prerequisites

- Python 3.9+
- [Manim Community](https://docs.manim.community/en/stable/installation.html) (`pip install manim`)
- [ffmpeg](https://ffmpeg.org/) and **ffprobe** (with `libx264`; add `libass` if you burn subtitles; **ffprobe** is used for frame extraction)
- [git](https://git-scm.com/) (for `ManimProject` versioning)
- Optional: `pip install "manim-voiceover[gtts]"` for narrated scenes
- Optional: `pip install google-genai` and `GEMINI_API_KEY` for Gemini TTS
- [Node.js](https://nodejs.org/) (for ClawHub CLI: `npx clawhub`)

Check dependencies:

```bash
python recursive-maths-animator/scripts/check_environment.py
```

## Install from ClawHub

If the skill is published (slug: **`recursive-maths-animator`**):

```bash
# Cursor / generic — use a skills directory you configure for your agent
npx --yes clawhub@latest install recursive-maths-animator --workdir /path/to/parent
# Skill is installed to /path/to/parent/skills/recursive-maths-animator/
```

For **nanobot**, use your workspace:

```bash
npx --yes clawhub@latest install recursive-maths-animator --workdir ~/.nanobot/workspace
```

Then point your agent at `skills/recursive-maths-animator/SKILL.md` (or the folder) per your tool’s skill discovery rules.

**Publish / update** (owner — requires `npx clawhub@latest login` once):

```bash
cd /path/to/manim-video-skill
npx --yes clawhub@latest publish recursive-maths-animator --slug recursive-maths-animator --version 1.0.0 --changelog "Your release notes"
```

Bump `--version` on each publish (semver).

## Install from Git

Clone this repository, then copy or symlink only the inner **`recursive-maths-animator`** directory into the target path.

### Cursor (all projects)

```bash
mkdir -p ~/.cursor/skills
cp -R recursive-maths-animator ~/.cursor/skills/
# or: ln -s "$(pwd)/recursive-maths-animator" ~/.cursor/skills/recursive-maths-animator
```

### Cursor (single project)

```bash
mkdir -p .cursor/skills
cp -R /path/to/manim-video-skill/recursive-maths-animator .cursor/skills/
```

### Claude Code (all projects)

```bash
mkdir -p ~/.claude/skills
cp -R recursive-maths-animator ~/.claude/skills/
```

### Claude Code (single project)

```bash
mkdir -p .claude/skills
cp -R /path/to/manim-video-skill/recursive-maths-animator .claude/skills/
```

Restart the IDE or start a new agent session so the skill is picked up.

## Vision verification loop

After a render (prefer **MP4** for final QA):

```bash
python recursive-maths-animator/scripts/extract_verification_frames.py path/to/scene.mp4 --count 8
```

The agent reads the frames + `DESIGN_THEME.md` + storyboard, applies [`recursive-maths-animator/references/video_verification_rubric.md`](recursive-maths-animator/references/video_verification_rubric.md), and produces **`VERIFICATION_FEEDBACK.md`** in the project. See **`SKILL.md`** for the full loop and iteration cap.

## Repository layout

```text
recursive-maths-animator/
├── SKILL.md              # Instructions for the agent
├── requirements.txt      # Template copied into new animation projects by ManimProject.init()
├── scripts/              # run_pipeline.py, check_environment.py, extract_verification_frames.py
└── references/           # manim_versioning, palette, rubric, manim_guide, optional Gemini TTS
```

Generated Manim projects should add `references/` (from this skill or a copy inside the project) to `sys.path` as described in `SKILL.md`.

## Smoke test (Manim only)

After installing Manim, from an empty folder:

```bash
printf '%s\n' 'from manim import *' 'class Smoke(Scene):' '    def construct(self): self.play(Write(Text("ok")))' > smoke.py
manim -ql smoke.py Smoke
```

## License

MIT — see [LICENSE](LICENSE).

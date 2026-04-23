# manim-video (agent skill)

Portable **Cursor** and **Claude Code** skill for [Manim](https://www.manim.community/) animations with optional **manim-voiceover**, git-based **scene versioning** (`references/manim_versioning.py`), palette helpers, and optional **Gemini TTS** (`references/gemini_tts_service.py`).

The agent-facing instructions live in [`manim-video/SKILL.md`](manim-video/SKILL.md). Install by placing the `manim-video` folder in a skills directory (see below).

## Prerequisites

- Python 3.9+
- [Manim Community](https://docs.manim.community/en/stable/installation.html) (`pip install manim`)
- [ffmpeg](https://ffmpeg.org/) (with `libx264`; add `libass` if you burn subtitles)
- [git](https://git-scm.com/) (for `ManimProject` versioning)
- Optional: `pip install "manim-voiceover[gtts]"` for narrated scenes
- Optional: `pip install google-genai` and `GEMINI_API_KEY` for Gemini TTS

Check dependencies:

```bash
python manim-video/scripts/check_environment.py
```

## Install as a skill

Clone this repository, then copy or symlink only the inner **`manim-video`** directory (the folder that contains `SKILL.md`) into the target path.

### Cursor (all projects)

```bash
mkdir -p ~/.cursor/skills
cp -R manim-video ~/.cursor/skills/
# or: ln -s "$(pwd)/manim-video" ~/.cursor/skills/manim-video
```

### Cursor (single project)

```bash
mkdir -p .cursor/skills
cp -R /path/to/manim-video-skill/manim-video .cursor/skills/
```

### Claude Code (all projects)

```bash
mkdir -p ~/.claude/skills
cp -R manim-video ~/.claude/skills/
```

### Claude Code (single project)

```bash
mkdir -p .claude/skills
cp -R /path/to/manim-video-skill/manim-video .claude/skills/
```

Restart the IDE or start a new agent session so the skill is picked up.

## Repository layout

```text
manim-video/
├── SKILL.md              # Instructions for the agent
├── scripts/              # run_pipeline.py, check_environment.py
└── references/           # manim_versioning, palette, manim_guide, optional Gemini TTS
```

Generated Manim projects should add `references/` (from this skill or a copy inside the project) to `sys.path` as described in `SKILL.md`.

## Optional: ClawHub

To publish or install via [ClawHub](https://clawhub.ai), use their CLI from a workspace root; this repo is structured as a single skill directory plus top-level docs.

## Smoke test (Manim only)

After installing Manim, from an empty folder:

```bash
printf '%s\n' 'from manim import *' 'class Smoke(Scene):' '    def construct(self): self.play(Write(Text("ok")))' > smoke.py
manim -ql smoke.py Smoke
```

## License

MIT — see [LICENSE](LICENSE).

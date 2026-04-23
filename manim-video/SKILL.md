---
name: manim-video
description: Create Manim animations with optional voiceover (manim-voiceover), subtitles, and git-based scene versioning. Use for educational or technical motion graphics with narration, or when you need versioned Manim scenes with rollback and branch workflows.
---

# Manim video (animation + voiceover + versioning)

This skill ships helper code under `references/` (palette, optional Gemini TTS adapter, `manim_versioning.ManimProject`) and utilities under `scripts/`. Agents should point users at those paths when generating projects.

## Requirements

- **Python** 3.9+
- **manim** — `pip install manim`
- **manim-voiceover** with a TTS backend — e.g. `pip install "manim-voiceover[gtts]"` (uses network for gTTS unless you switch engine)
- **ffmpeg** — with `libx264` and `libass` if you burn subtitles (see `scripts/run_pipeline.py`)
- **git** — for `ManimProject` versioning commands

Optional:

- **google-genai** — only if using `references/gemini_tts_service.py` (set `GEMINI_API_KEY`)

## Using `references/` from your project

The Quick Start imports `ManimProject` from `manim_versioning`. Add this skill’s `references` directory to `sys.path` (or copy the files into your repo).

```python
from pathlib import Path
import sys

# Path to the installed skill’s references/ folder (adjust if you symlink or copy the skill).
SKILL_REF = Path.home() / ".cursor/skills/manim-video/references"  # example: Cursor user skill
# SKILL_REF = Path("path/to/manim-video-skill/manim-video/references")

sys.path.insert(0, str(SKILL_REF.resolve()))
from manim_versioning import ManimProject
```

Scene files should use the same pattern so `soft_enterprise_palette` and optional `gemini_tts_service` resolve:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "references"))
```

(Adjust the relative path if your layout differs.)

## Quick Start

```python
from pathlib import Path
import sys

REF = Path("/path/to/manim-video/references").resolve()
sys.path.insert(0, str(REF))
from manim_versioning import ManimProject

project = ManimProject("my_animation")
project.init()  # Creates git repo, scenes/ folder, structure

# Create Scene 1
project.create_scene("scene_1", """
class Scene1(Scene):
    def construct(self):
        # Your animation code
        pass
""")

# Render and commit
project.render("scene_1")  # Auto-commits as "scene_1 v1"

# Make changes, create new version
project.update_scene("scene_1", "# updated code...")
project.render("scene_1")  # Auto-commits as "scene_1 v2"

# Rollback if needed
project.rollback("scene_1", version=1)  # Restores v1

# Create provisional branch for review
project.branch("scene_1", "review-alice")  # Creates branch, doesn't affect main
```

## Project structure

```
my_animation/
├── .git/
├── scenes/
│   ├── scene_1/
│   │   ├── scene_1.py
│   │   ├── versions/
│   │   │   ├── v1.py
│   │   │   └── v2.py
│   │   └── branches/
│   │       └── review-alice/
│   ├── scene_2/
│   └── shared/
│       ├── palette.py
│       └── utils.py
├── media/
│   └── scene_1_v2.mp4
└── project.json
```

## Versioning commands

| Action | Command | Result |
|--------|---------|--------|
| Initialize project | `project.init()` | Git repo + folder structure |
| Create scene | `project.create_scene(name, code)` | Scene file + initial commit |
| Update scene | `project.update_scene(name, code)` | New version committed |
| Render | `project.render(name)` | Video + auto-commit |
| List versions | `project.versions(name)` | Shows v1, v2, v3... |
| Rollback | `project.rollback(name, version)` | Restores code to version |
| Create branch | `project.branch(name, branch_name)` | Provisional copy |
| Merge branch | `project.merge(name, branch_name)` | Merges into main |
| Compare | `project.diff(name, v1, v2)` | Shows code differences |
| Tag approved | `project.tag(name, version, "approved")` | Marks final version |

## Provisional branch workflow

```python
project.update_scene("scene_1", "# version 1 code")
project.render("scene_1")

project.branch("scene_1", "alt-animation")
project.update_scene("scene_1", "# alternative code", branch="alt-animation")
project.render("scene_1", branch="alt-animation")

# Review outputs, then merge or delete_branch as needed
project.merge("scene_1", "alt-animation")
```

## Scene template (voiceover + soft palette)

```python
"""
SCENE {N}: {TITLE}
{Description}
~{duration}s, {orientation}
"""

import sys
sys.path.insert(0, '{project_path}/references')

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from soft_enterprise_palette import SoftColors, EASE_GAS_SPRING


class Scene{N}_{Title}(VoiceoverScene):
    """{Description}"""

    def __init__(self, **kwargs):
        config.pixel_width = {width}
        config.pixel_height = {height}
        config.frame_width = {frame_w}
        config.frame_height = {frame_h}
        config.frame_rate = 60

        super().__init__(**kwargs)

        self.set_speech_service(GTTSService(lang='en', slow=True))

    def construct(self):
        bg = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=SoftColors.BACKGROUND,
            fill_opacity=1
        )
        self.add(bg)

        section_title = Text(
            "{SECTION_TITLE}",
            font="IBM Plex Mono",
            font_size=14,
            color=SoftColors.TEXT_SECONDARY
        )
        section_title.to_edge(UP, buff=0.5)
        self.add(section_title)

        with self.voiceover(
            text="{VOICEOVER_LINE_1}"
        ) as tracker:
            pass

        self.wait(0.5)

    def create_token(self, text, is_active=False):
        token = Text(
            text,
            font="Monospace",
            font_size=24,
            color=SoftColors.TEXT_PRIMARY if is_active else SoftColors.TEXT_SECONDARY,
            weight=MEDIUM
        )

        if is_active:
            bg = RoundedRectangle(
                corner_radius=0.12,
                width=token.width + 0.35,
                height=token.height + 0.25,
                fill_color=SoftColors.CONTAINER,
                fill_opacity=0.85,
                stroke_color=SoftColors.BORDER,
                stroke_width=1
            )
            bg.move_to(token.get_center())
            token = VGroup(bg, token)

        return token


if __name__ == "__main__":
    config.quality = "high_quality"
    scene = Scene{N}_{Title}()
    scene.render()
```

## Soft enterprise palette

Defined in `references/soft_enterprise_palette.py` — import `SoftColors` and `EASE_GAS_SPRING` after adding `references` to `sys.path`.

## Rendering

```bash
# Draft quality
manim -ql scene.py SceneClass --disable_caching

# High quality
manim -qh scene.py SceneClass --disable_caching

# Versioning helper
project.render("scene_1", quality="high")
```

## Pipeline helper (optional)

`scripts/run_pipeline.py` wraps render + optional subtitle burn-in. `scripts/check_environment.py` verifies common dependencies.

## Output locations

- **Draft**: `media/videos/scene_1/480p15/Scene1.mp4`
- **Final**: `media/videos/scene_1/1080p60/Scene1.mp4`
- **Versioned**: `media/scene_1_v{N}.mp4` (when using `ManimProject`; see implementation)

## Best practices

1. Version deliberately: use commits per meaningful render.
2. Use branches for experiments before merging to main line.
3. Tag approvals when a cut is final.
4. Keep scenes independently renderable.
5. Shared utilities live under `scenes/shared/`.
6. Keep voiceover text TTS-friendly (plain punctuation, avoid noisy symbols).
7. Target ~10–15s per scene for short-form vertical if that is the deliverable.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Git not initialized | Run `project.init()` first |
| Import errors for helpers | Add this skill’s `references/` to `sys.path` or copy files into your project |
| Branch merge conflict | Resolve in scene file, then commit via project helpers |
| Cache issues | Use `--disable_caching` |
| TTS / API limits | Fall back to gTTS or another `SpeechService` |

## Optional follow-on

- **Remotion** or other compositors for captions, UI chrome, or multi-track polish.
- **General video editing** (FFmpeg, DaVinci, etc.) for final assembly.

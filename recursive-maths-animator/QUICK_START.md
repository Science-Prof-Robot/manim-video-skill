# Quick start

Run from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r recursive-maths-animator/requirements.txt
```

Install `ffmpeg` and `ffprobe` separately. Then render a smoke test:

```bash
.venv/bin/manim -ql recursive-maths-animator/examples/convex_lens_object_to_infinity.py \
  ConvexLensObjectToInfinity --format mp4 --disable_caching
```

Render the final MP4:

```bash
.venv/bin/manim -qh recursive-maths-animator/examples/convex_lens_object_to_infinity.py \
  ConvexLensObjectToInfinity --format mp4 --disable_caching
```

Verify frames:

```bash
.venv/bin/python recursive-maths-animator/scripts/extract_verification_frames.py \
  media/videos/convex_lens_object_to_infinity/1080p60/ConvexLensObjectToInfinity.mp4 \
  --count 8
```

## Install as an agent skill

Codex:

```bash
mkdir -p ~/.codex/skills
cp -R recursive-maths-animator ~/.codex/skills/
```

Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R recursive-maths-animator ~/.claude/skills/
```

Start a new agent session and ask it to read `SKILL.md` before editing.

Codex prompt:

> Read `recursive-maths-animator/SKILL.md` first. Set up the venv from `requirements.txt`, use the physics workflow when relevant, verify frames for overlap/clipping, and render the final MP4 only after the smoke test passes.

Claude Code prompt:

> Read `recursive-maths-animator/SKILL.md` before editing. Follow its Manim, physics, responsive-layout, verification, and S3 rules. Keep videos, credentials, and upload helpers out of git.

## Next prompt

> Create or update a Manim scene using the recursive-maths-animator skill. Use the physics workflow when relevant, reserve layout regions, keep every element inside safe margins, run a smoke render, inspect extracted frames for overlap, and only then render the final MP4.

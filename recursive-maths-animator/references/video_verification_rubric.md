# Video verification rubric (agent vision review)

Use this checklist when reviewing **extracted frames** from a render (see `scripts/extract_verification_frames.py`) together with **`DESIGN_THEME.md`** and the agreed **storyboard / scene plan**.

For each issue, cite **which frame** (`filename`, `t_seconds`, or `pct` from `manifest.json`).

## 1. Layout, padding, and safe margins

- [ ] Text and important shapes stay inside a **comfortable safe area** (not hugging edges unless intentional).
- [ ] **Padding** between titles, body copy, and diagrams is consistent with the theme (not cramped, not floating too far from content).
- [ ] Nothing is **accidentally cropped** by the frame (partial letters, clipped circles).
- [ ] **Alignment** looks deliberate: centered vs left-aligned blocks match the plan.

## 2. Typography and readability

- [ ] Font sizes are **legible** at the target delivery size (social vs full HD).
- [ ] **Contrast** between text and background matches the theme (light-on-light mistakes, etc.).
- [ ] Line length and label density are not overwhelming in wide shots.

## 3. Color and theme fidelity

- [ ] Colors match **locked palette** in `DESIGN_THEME.md` (background, primary, accent).
- [ ] No accidental default Manim colors leaking in where the theme specified otherwise.
- [ ] Highlights and de-emphasized elements read clearly as **primary vs secondary**.

## 4. Logical progression and planned function

For each storyboard beat, ask: **does this frame support the beat it sits in?**

- [ ] **Order of reveals** matches the plan (A before B, no reversed causality).
- [ ] Each scene or segment **proves one idea**; frames do not show contradictory states.
- [ ] Arrows, graphs, and state transitions match the **narrative logic** (e.g. before/after, prune vs keep).
- [ ] If voiceover exists: **visuals at this timestamp** plausibly match what should be on screen for that line (spot-check key frames).

## 5. Motion hints (from sparse frames)

Still frames cannot prove timing, but they can flag:

- [ ] **Overlaps / clutter** that suggest elements are stacked confusingly at mid-motion.
- [ ] **Ghosting** or half-drawn states that look like bugs rather than intentional progressive reveal.
- [ ] **Jarring jumps** between consecutive sample frames (large unexplained layout changes).

## 6. Technical glitches

- [ ] No obvious **render errors** (black frames, solid color flash, missing expected objects).
- [ ] Subtitles or captions (if any) are **on-screen and not cut off**.

## Severity guide

| Level | Meaning |
|-------|---------|
| **P0** | Wrong fact, unreadable core message, or theme-breaking mistake; must fix before ship. |
| **P1** | Layout/padding/logic issue that confuses the story; fix before final. |
| **P2** | Polish: minor spacing, color tweak, optional clarity improvement. |

After review, write **`VERIFICATION_FEEDBACK.md`** in the project root with concrete Manim fixes (objects, `buff=`, `to_edge`, colors, reordering `play` calls), ordered **P0 → P1 → P2**.

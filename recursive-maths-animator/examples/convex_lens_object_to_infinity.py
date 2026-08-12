"""Convex-lens ray construction with a synchronized u-v graph.

Run from the repository root with:

    .venv/bin/manim -qh recursive-maths-animator/examples/convex_lens_object_to_infinity.py \
        ConvexLensObjectToInfinity --format mp4 --disable_caching

The model is a normalized, paraxial thin-lens construction. The graph uses
1/f = 1/u + 1/v and highlights the current (u, v) state during the animation.
"""
from __future__ import annotations

from manim import *
from manim_physics import Lens


class ConvexLensObjectToInfinity(Scene):
    """Show a real image moving toward the focal point as u tends to infinity."""

    FOCAL_LENGTH = 2.0
    OBJECT_HEIGHT = 1.25
    RAY_END_X = 6.6

    def construct(self):
        # Start immediately beside the lens, then move outward.  The focal
        # crossing is shown explicitly because the image changes from virtual
        # and upright to real and inverted there.
        object_distance = ValueTracker(0.72)

        title = Text("Convex lens · object → ∞", font_size=30, weight=BOLD)
        title.to_edge(UP, buff=0.28)

        axis = Line(LEFT * 6.9, RIGHT * 6.9, color=GRAY_B, stroke_width=2)

        lens = Lens(
            self.FOCAL_LENGTH,
            0.82,
            n=1.52,
            color=BLUE_C,
            fill_color=BLUE_E,
            fill_opacity=0.48,
            stroke_width=3,
        )

        near_focus = Dot([-self.FOCAL_LENGTH, 0, 0], color=YELLOW, radius=0.06)
        far_focus = Dot([self.FOCAL_LENGTH, 0, 0], color=YELLOW, radius=0.06)
        near_focus_label = Text("F", font_size=22, color=YELLOW).next_to(
            near_focus, DOWN, buff=0.12
        )
        far_focus_label = Text("F", font_size=22, color=YELLOW).next_to(
            far_focus, DOWN, buff=0.12
        )

        def image_distance() -> float:
            u = object_distance.get_value()
            return self.FOCAL_LENGTH * u / (u - self.FOCAL_LENGTH)

        def image_height() -> float:
            u = object_distance.get_value()
            return self.OBJECT_HEIGHT * self.FOCAL_LENGTH / (u - self.FOCAL_LENGTH)

        def magnification() -> float:
            u = object_distance.get_value()
            return -self.FOCAL_LENGTH / (u - self.FOCAL_LENGTH)

        def make_object() -> VGroup:
            x = -object_distance.get_value()
            arrow = Arrow(
                [x, 0, 0],
                [x, self.OBJECT_HEIGHT, 0],
                buff=0,
                color=ORANGE,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.18,
            )
            label = Text("O", color=ORANGE, font_size=30).next_to(arrow, LEFT, buff=0.12)
            return VGroup(arrow, label)

        def make_image() -> VGroup:
            x = image_distance()
            h = image_height()
            # Signed h gives an upright virtual image for u < f and an
            # inverted real image for u > f.
            arrow = Arrow(
                [x, 0, 0],
                [x, -h, 0],
                buff=0,
                color=GREEN_C,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.2,
            )
            label = Text("I", color=GREEN_C, font_size=26).next_to(
                [x, -h, 0], RIGHT if h >= 0 else LEFT, buff=0.12
            )
            return VGroup(arrow, label)

        def ray_group() -> VGroup:
            u = object_distance.get_value()
            v = image_distance()
            h = self.OBJECT_HEIGHT
            h_i = image_height()

            # A ray parallel to the axis refracts through the far focus for a
            # real image, and diverges as though it came from the virtual
            # image for u < f.
            parallel_in = Line([-u, h, 0], [0, h, 0], color=RED, stroke_width=3)
            if u > self.FOCAL_LENGTH + 0.02:
                parallel_out = Line([0, h, 0], [v, -h_i, 0], color=RED, stroke_width=3)
            else:
                virtual_h = -h_i
                slope = (h - virtual_h) / (-v)
                parallel_out = Line(
                    [0, h, 0], [self.RAY_END_X, h + slope * self.RAY_END_X, 0],
                    color=RED, stroke_width=3,
                )

            # A ray through the optical center remains undeviated.
            central = Line(
                [-u, h, 0], [self.RAY_END_X, -h / u * self.RAY_END_X, 0],
                color=TEAL, stroke_width=3,
            )

            # A second construction ray starts toward the near focal point and
            # emerges parallel to the principal axis.
            focal_in = Line([-u, h, 0], [0, 0, 0], color=PURPLE_C, stroke_width=2.5)
            focal_out = Line([0, 0, 0], [self.RAY_END_X, 0, 0], color=PURPLE_C, stroke_width=2.5)
            return VGroup(parallel_in, parallel_out, central, focal_in, focal_out)

        object_arrow = always_redraw(make_object)
        image_arrow = always_redraw(make_image)
        rays = always_redraw(ray_group)

        def status_label() -> VGroup:
            m = abs(magnification())
            if m > 1.05:
                size_word = "enlarged"
            elif m < 0.95:
                size_word = "diminished"
            else:
                size_word = "same size"
            kind = "real · inverted" if magnification() < 0 else "virtual · upright"
            return Text(
                f"{kind} · {size_word}   m = {magnification():+.2f}",
                font_size=17,
                color=GREEN_C,
            ).to_edge(DOWN, buff=0.32).to_edge(RIGHT, buff=0.35)

        distance_label = always_redraw(
            lambda: Text(
                f"u={object_distance.get_value():.2f}   v={image_distance():.2f}",
                font_size=19,
                color=WHITE,
            ).to_corner(UL, buff=0.35).shift(DOWN * 0.72)
        )

        graph = self.make_uv_graph(object_distance, image_distance)
        graph_title = Text("u–v · current", font_size=16, color=YELLOW).move_to(
            [-4.45, -1.38, 0]
        )

        status = always_redraw(status_label)

        self.play(FadeIn(title), Create(axis))
        self.play(
            Create(lens),
            FadeIn(near_focus),
            FadeIn(far_focus),
            FadeIn(near_focus_label),
            FadeIn(far_focus_label),
        )
        self.play(
            FadeIn(object_arrow),
            Create(rays),
            FadeIn(image_arrow),
            FadeIn(distance_label),
            Create(graph),
            FadeIn(graph_title),
            FadeIn(status),
        )
        self.wait(1)

        # Move from beside the lens to the focal point, pause at the optical
        # singularity, then continue through the real-image regime to infinity.
        self.play(object_distance.animate.set_value(1.85), run_time=2.2, rate_func=linear)
        focal_note = Text("u = f  ·  image at ∞", font_size=17, color=YELLOW)
        focal_note.to_corner(UR, buff=0.35)
        self.play(FadeIn(focal_note), run_time=0.4)
        self.wait(0.8)
        self.play(object_distance.animate.set_value(2.2), run_time=0.3, rate_func=linear)
        self.play(FadeOut(focal_note), run_time=0.3)
        self.play(object_distance.animate.set_value(6.2), run_time=3.2, rate_func=linear)
        self.wait(2)

    def make_uv_graph(self, object_distance: ValueTracker, image_distance) -> VGroup:
        """Create a small hand-labelled graph so no LaTeX installation is needed."""

        left = -6.15
        bottom = -3.18
        width = 3.35
        height = 1.52
        u_min, u_max = 0.7, 7.0
        v_min, v_max = -6.0, 6.0

        def point(u: float, v: float) -> np.ndarray:
            return np.array(
                [
                    left + width * (u - u_min) / (u_max - u_min),
                    bottom + height * (v - v_min) / (v_max - v_min),
                    0,
                ]
            )

        frame = Rectangle(
            width=width,
            height=height,
            stroke_color=GRAY_B,
            stroke_width=1.5,
        ).move_to([left + width / 2, bottom + height / 2, 0])
        horizontal = Line([left, bottom, 0], [left + width, bottom, 0], color=GRAY_B)
        vertical = Line([left, bottom, 0], [left, bottom + height, 0], color=GRAY_B)
        u_label = Text("u", font_size=18, color=ORANGE).next_to(horizontal, RIGHT, buff=0.08)
        v_label = Text("v", font_size=18, color=GREEN_C).next_to(vertical, UP, buff=0.08)

        tick_labels = VGroup()
        for value in (1, 4, 7):
            tick_labels.add(
                Text(str(value), font_size=13, color=GRAY_B).next_to(point(value, v_min), DOWN, buff=0.04)
            )
        for value in (-6, 0, 6):
            tick_labels.add(
                Text(str(value), font_size=13, color=GRAY_B).next_to(point(u_min, value), LEFT, buff=0.04)
            )

        curve_points = []
        for interval in (np.linspace(u_min, 1.9, 36), np.linspace(2.1, u_max, 56)):
            points = []
            for u in interval:
                v = self.FOCAL_LENGTH * u / (u - self.FOCAL_LENGTH)
                # Keep every plotted branch inside the graph rectangle.  This
                # prevents the asymptote from escaping into the scene layout.
                if v_min <= v <= v_max:
                    points.append(point(u, v))
            if len(points) > 1:
                segment = VMobject(color=YELLOW, stroke_width=2.5)
                segment.set_points_smoothly(points)
                curve_points.append(segment)

        current_point = always_redraw(
            lambda: Dot(
                point(
                    object_distance.get_value(),
                    np.clip(image_distance(), v_min, v_max),
                ),
                radius=0.075,
                color=RED,
            )
        )
        current_crosshair = always_redraw(
            lambda: VGroup(
                DashedLine(
                    point(object_distance.get_value(), v_min),
                    point(object_distance.get_value(), np.clip(image_distance(), v_min, v_max)),
                    color=RED,
                    dash_length=0.06,
                    stroke_width=1.5,
                ),
                DashedLine(
                    point(u_min, np.clip(image_distance(), v_min, v_max)),
                    point(object_distance.get_value(), np.clip(image_distance(), v_min, v_max)),
                    color=RED,
                    dash_length=0.06,
                    stroke_width=1.5,
                ),
            )
        )
        return VGroup(
            frame,
            horizontal,
            vertical,
            u_label,
            v_label,
            tick_labels,
            *curve_points,
            current_crosshair,
            current_point,
        )


__all__ = ["ConvexLensObjectToInfinity"]

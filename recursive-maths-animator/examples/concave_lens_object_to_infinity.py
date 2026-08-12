"""Concave-lens ray construction as the object recedes toward infinity.

Run from the repository root with:

    manim -ql recursive-maths-animator/examples/concave_lens_object_to_infinity.py \
        ConcaveLensObjectToInfinity --format mp4 --disable_caching

This is a thin-lens, paraxial construction. Distances are normalized scene
units, not metres. The concave lens is the manim-physics Lens primitive; the
ray construction is kept explicit so it can animate with the object distance.
"""
from __future__ import annotations

from manim import *
from manim_physics import Lens


class ConcaveLensObjectToInfinity(Scene):
    """Show a diverging lens forming a virtual, upright, smaller image."""

    LENS_X = 0.0
    FOCAL_LENGTH = -2.0  # Negative focal length denotes a concave lens.
    OBJECT_HEIGHT = 1.55
    RAY_END_X = 6.6

    def construct(self):
        object_distance = ValueTracker(3.2)

        title = Text("Concave lens: object → infinity", font_size=34, weight=BOLD)
        subtitle = Text(
            "A virtual, upright, diminished image forms on the object side",
            font_size=20,
            color=GRAY_B,
        )
        VGroup(title, subtitle).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)

        axis = Line(LEFT * 6.9, RIGHT * 6.9, color=GRAY_B, stroke_width=2)
        axis_label = Text("principal axis", font_size=16, color=GRAY_B).next_to(
            axis, DOWN, buff=0.12
        )

        lens = Lens(
            self.FOCAL_LENGTH,
            0.55,
            n=1.52,
            color=BLUE_C,
            fill_color=BLUE_E,
            fill_opacity=0.48,
            stroke_width=3,
        )
        lens.move_to([self.LENS_X, 0, 0])
        lens_label = Text("concave lens", font_size=18, color=BLUE_B).next_to(
            lens, DOWN, buff=0.22
        )

        focal_point = Dot([self.FOCAL_LENGTH, 0, 0], color=YELLOW, radius=0.06)
        focal_label = Text("F", font_size=28, color=YELLOW).next_to(
            focal_point, DOWN, buff=0.12
        )

        def image_x() -> float:
            # 1/f = 1/v + 1/u, with f < 0 for a concave lens.
            u = object_distance.get_value()
            return self.FOCAL_LENGTH * u / (u - self.FOCAL_LENGTH)

        def image_height() -> float:
            # m = -v/u; m is positive for a concave lens image.
            u = object_distance.get_value()
            return self.OBJECT_HEIGHT * (-self.FOCAL_LENGTH) / (u - self.FOCAL_LENGTH)

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
            x = image_x()
            h = image_height()
            arrow = DashedLine(
                [x, 0, 0],
                [x, h, 0],
                dash_length=0.09,
                color=YELLOW,
                stroke_width=4,
            )
            tip = Triangle(color=YELLOW, fill_opacity=1).scale(0.11)
            tip.rotate(PI)
            tip.move_to([x, h, 0])
            label = Text("Iᵥ", color=YELLOW, font_size=28).next_to(
                [x, h, 0], LEFT, buff=0.12
            )
            return VGroup(arrow, tip, label)

        def ray_group() -> VGroup:
            u = object_distance.get_value()
            x_i = image_x()
            h_i = image_height()
            h = self.OBJECT_HEIGHT
            end_x = self.RAY_END_X

            # Ray 1: parallel to the axis before the lens, then diverging as
            # though it came from the virtual image point.
            parallel_in = Line([-u, h, 0], [self.LENS_X, h, 0], color=RED, stroke_width=3)
            parallel_out_y = h + (h - h_i) / (-x_i) * end_x
            parallel_out = Line(
                [self.LENS_X, h, 0], [end_x, parallel_out_y, 0], color=RED, stroke_width=3
            )

            # Ray 2: through the optical center; in the thin-lens model it is
            # undeviated.
            central = Line(
                [-u, h, 0], [end_x, end_x * h / u, 0], color=TEAL, stroke_width=3
            )

            # Dashed extensions identify the virtual intersection behind the
            # lens. They are not physical light travelling backwards.
            virtual_parallel = DashedLine(
                [x_i, h_i, 0], [self.LENS_X, h, 0], color=RED, stroke_width=2.5, dash_length=0.08
            )
            virtual_central = DashedLine(
                [x_i, h_i, 0], [self.LENS_X, 0, 0], color=TEAL, stroke_width=2.5, dash_length=0.08
            )
            return VGroup(
                parallel_in,
                parallel_out,
                central,
                virtual_parallel,
                virtual_central,
            )

        object_arrow = always_redraw(make_object)
        image_arrow = always_redraw(make_image)
        rays = always_redraw(ray_group)

        distance_label = always_redraw(
            lambda: VGroup(
                Text("object distance", font_size=18, color=ORANGE),
                Text(
                    f"{object_distance.get_value():.1f}",
                    font_size=22,
                    color=ORANGE,
                ),
            )
            .arrange(RIGHT, buff=0.12)
            .to_corner(UL, buff=0.35)
            .shift(DOWN * 1.15)
        )

        image_formula = Text(
            "1/f = 1/v + 1/u    (f < 0)",
            color=YELLOW,
            font_size=24,
        ).to_corner(DR, buff=0.35).shift(UP * 0.65)
        behavior = Text(
            "virtual • upright • diminished",
            font_size=20,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.38)

        self.play(FadeIn(title), FadeIn(subtitle), Create(axis), FadeIn(axis_label))
        self.play(Create(lens), FadeIn(lens_label), FadeIn(focal_point), FadeIn(focal_label))
        self.play(FadeIn(object_arrow), Create(rays), FadeIn(image_arrow), FadeIn(distance_label))
        self.play(Write(image_formula), FadeIn(behavior))
        self.wait(1)

        # Move the object away from the aperture. The final finite distance is
        # an on-screen stand-in for infinity; the final card states the limit.
        self.play(object_distance.animate.set_value(6.2), run_time=5, rate_func=linear)
        infinity_label = Text("u → ∞", color=ORANGE, font_size=28)
        infinity_label.next_to(distance_label, DOWN, buff=0.14).align_to(distance_label, LEFT)
        self.play(FadeOut(distance_label), FadeIn(infinity_label), run_time=0.8)
        self.wait(2)


__all__ = ["ConcaveLensObjectToInfinity"]

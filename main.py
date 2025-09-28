from manim import *
import numpy as np

class DotExample(Scene):
    def construct(self):
        dot_center = Dot(point=ORIGIN, color=BLUE)
        dot_moving = Dot(point=ORIGIN, color=RED)
        dot_sec = Dot(point=ORIGIN, color=YELLOW)

        self.add(dot_center, dot_moving)

        vec = always_redraw(lambda: Line(ORIGIN, dot_moving.get_center()))
        vec_sec = always_redraw(lambda: Line(dot_moving.get_center(), dot_sec.get_center()))
        self.add(vec, vec_sec)

        self.play(dot_moving.animate.shift(UP * 2), dot_sec.animate.shift(UP * 3))

        trail = TracedPath(dot_sec.get_center, stroke_width=4, stroke_opacity=1.0, color=BLUE)
        self.add(trail)

        self.play(Rotating(dot_moving, about_point=[0, 0, 0]), Rotating(dot_sec, about_point=dot_moving.get_center()), run_time=3)

        self.wait(3)

        r_dot_moving = 3.0
        R_moon = 0.8
        w_earth = 1.0  # угл. скорость Земли
        w_moon = 12.0  # угл. скорость Луны относительно Земли

        t = ValueTracker(0.0)

        def d_dot_moving():
            a = t.get_value()
            return np.array([r_dot_moving*np.cos(w_earth*a), r_dot_moving*np.sin(w_earth*a), 0])

        def d_dot_sec():
            a = t.get_value()
            e = d_dot_moving()
            return e + np.array([R_moon*np.cos(w_moon*a), R_moon*np.sin(w_moon*a), 0])




class SunEarthMoon(Scene):
    def construct(self):
        R_earth = 0.97
        R_moon  = 1.49
        R_3 = 0.54
        w_earth = -5.0     # угл. скорость Земли
        w_moon  = 7.0    # угл. скорость Луны относительно Земли
        w_3 = 19.0

        t = ValueTracker(0.0)

        def earth_pos():
            a = t.get_value()
            return np.array([R_earth*np.cos(w_earth*a), R_earth*np.sin(w_earth*a), 0])

        def moon_pos():
            a = t.get_value()
            e = earth_pos()
            return e + np.array([R_moon*np.cos(w_moon*a), R_moon*np.sin(w_moon*a), 0])

        def three_pos():
            a = t.get_value()
            m = moon_pos()
            return m + np.array([R_3*np.cos(w_3*a), R_3*np.sin(w_3*a), 0])

        sun   = Dot(ORIGIN, color=YELLOW).scale(1.2)
        earth = always_redraw(lambda: Dot(point=earth_pos(), color=BLUE))
        moon  = always_redraw(lambda: Dot(point=moon_pos(),  color=GREY_B))
        three = always_redraw(lambda: Dot(point=three_pos(), color=BLUE))

        earth_orbit = Circle(radius=R_earth, color=BLUE_E)
        moon_orbit  = always_redraw(lambda: Circle(radius=R_moon, color=GREY_E).move_to(earth_pos()))


        earth_trail = TracedPath(lambda: earth.get_center(), stroke_width=2, color=BLUE_A)
        moon_trail  = TracedPath(lambda: moon.get_center(),  stroke_width=2, color=GREY_E)
        three_trail = TracedPath(lambda: three.get_center(), stroke_width=2, color=GREY_B)

        vec = always_redraw(lambda: Line(sun, earth.get_center()))
        vec_sec = always_redraw(lambda: Line(earth.get_center(), moon.get_center()))
        vec_th = always_redraw(lambda: Line(moon.get_center(), three.get_center()))
        self.add(vec, vec_sec, vec_th)


        self.add(  three_trail, sun, earth, moon, three)
        self.play(t.animate.set_value(2*PI), run_time=30, rate_func=linear)
        self.wait(4)



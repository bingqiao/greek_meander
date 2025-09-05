import drawsvg as draw
import cairosvg
import math

class GreekKeyConfig:
    PATTERN_UNIT_SIZE = 5
    def __init__(self, r_o, pattern_count, border_margin, stroke_width):
        # r_a - "frame_gap" > 0 == PATTERN_UNIT_SIZE * n > 6*math.pi, so n >= 4
        r_a, r_b, r_c, r_d, r_e, r_o, r_i = get_radii_for_outer_radius(r_o, GreekKeyConfig.PATTERN_UNIT_SIZE*pattern_count)
        self.r_a = r_a        # Circle 1
        self.r_b = r_b        # Circle 2
        self.r_c = r_c        # Circle 3 (middle)
        self.r_d = r_d        # Circle 4
        self.r_e = r_e        # Circle 5

        self.radius_outer = r_o
        self.radius_inner = r_i
        self.border_margin = border_margin
        self.pattern_count = pattern_count
        self.stroke_width = stroke_width

    def get_canvas_size(self):
        offset = 2*self.radius_outer + 2*self.border_margin + 2*self.stroke_width
        return offset, offset

    def get_centre(self):
        offset = self.border_margin + self.radius_outer + self.stroke_width
        return offset, offset

    def get_start_position(self, r):
        centre_x, centre_y = self.get_centre()
        return centre_x, centre_y - r
    
    def get_coords_for_patterns(self):
        centre_x, centre_y = self.get_centre()
        start_x, start_y = self.get_start_position(self.r_a)
        points_a = calculate_circle_points(centre_x, centre_y, self.pattern_count, start_x, start_y, self.r_a)
        start_x, start_y = self.get_start_position(self.r_b)
        points_b = calculate_circle_points(centre_x, centre_y, self.pattern_count, start_x, start_y, self.r_b)
        start_x, start_y = self.get_start_position(self.r_c)
        points_c = calculate_circle_points(centre_x, centre_y, self.pattern_count, start_x, start_y, self.r_c)
        start_x, start_y = self.get_start_position(self.r_d)
        points_d = calculate_circle_points(centre_x, centre_y, self.pattern_count, start_x, start_y, self.r_d)
        start_x, start_y = self.get_start_position(self.r_e)
        points_e = calculate_circle_points(centre_x, centre_y, self.pattern_count, start_x, start_y, self.r_e)
        return points_a, points_b, points_c, points_d, points_e
    
    def get_coords_for_patterns_by_p0(self, p_a0, p_b0, p_c0, p_d0, p_e0):
        centre_x, centre_y = self.get_centre()
        points_a = calculate_circle_points(centre_x, centre_y, self.pattern_count, p_a0[0], p_a0[1], self.r_a)
        points_b = calculate_circle_points(centre_x, centre_y, self.pattern_count, p_b0[0], p_b0[1], self.r_b)
        points_c = calculate_circle_points(centre_x, centre_y, self.pattern_count, p_c0[0], p_c0[1], self.r_c)
        points_d = calculate_circle_points(centre_x, centre_y, self.pattern_count, p_d0[0], p_d0[1], self.r_d)
        points_e = calculate_circle_points(centre_x, centre_y, self.pattern_count, p_e0[0], p_e0[1], self.r_e)
        return points_a, points_b, points_c, points_d, points_e


    def draw_greek_key_circle(self, path):
        """Draws the meander pattern."""
        points_a, points_b, points_c, points_d, points_e = self.get_coords_for_patterns()
        # m, points_a_0
        path.M(points_a[0][0], points_a[0][1])

        for i in range(0, self.pattern_count):
            # v, -points_e_0
            path.L(points_e[0][0], points_e[0][1])
            # h, points_e_4
            path.L(points_e[4][0], points_e[4][1])
            # v, points_b_4
            path.L(points_b[4][0], points_b[4][1])
            # h, -points_b_2
            path.L(points_b[2][0], points_b[2][1])
            # v, -points_c_2
            path.L(points_c[2][0], points_c[2][1])
            # h, points_c_3
            path.L(points_c[3][0], points_c[3][1])
            # v, -points_d_3
            path.L(points_d[3][0], points_d[3][1])
            # h, -points_d_1
            path.L(points_d[1][0], points_d[1][1])
            # v, points_a_1
            path.L(points_a[1][0], points_a[1][1])
            # h, points_a_5
            path.L(points_a[5][0], points_a[5][1])

            points_a, points_b, points_c, points_d, points_e = self.get_coords_for_patterns_by_p0(points_a[5], points_b[5], points_c[5], points_d[5], points_e[5])


        path.Z()

    def generate_pattern_svg(self, stroke_width=2, stroke_color='black', stroke_opacity=1.0, filename='meander'):
        """Generates the complete SVG drawing."""
        width, height = self.get_canvas_size()
        d = draw.Drawing(width, height, origin=(0, 0), displayInline=False)
        path = draw.Path(
            stroke=stroke_color,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity,
            fill='none',
            #stroke_linecap='square'
        )

        self.draw_greek_key_circle(path)

        # Draw frames
        centre_x, centre_y = self.get_centre()
        circle_outer = draw.Circle(cx=centre_x, cy=centre_y,
                            r=self.radius_outer,
                            fill='none',
                            stroke=stroke_color,
                            stroke_width=stroke_width,
                            stroke_opacity=stroke_opacity)
        circle_inner = draw.Circle(cx=centre_x, cy=centre_y,
                            r=self.radius_inner,
                            fill='none',
                            stroke=stroke_color,
                            stroke_width=stroke_width,
                            stroke_opacity=stroke_opacity)

        d.append(path)
        d.append(circle_outer)
        d.append(circle_inner)
        d.save_svg(f'{filename}.svg')

        cairosvg.svg2png(url=f'{filename}.svg', write_to=f'{filename}.png', output_width=width, output_height=height)


def get_radii_for_outer_radius(r_o, n):
    # n > 6*math.pi, so n >= 19
    if n < 19:
        raise Exception("n must be greater or equal to 19")
    r_c = r_o/(6*math.pi/n+1)
    r_a = (5*r_c-2*r_o)/3
    r_b = (4*r_c-r_o)/3
    r_d = (2*r_c+r_o)/3
    r_e = (r_c+2*r_o)/3
    r_i = (6*r_c-3*r_o)/3
    # u = 2*math.pi*r_c/n
    return r_a, r_b, r_c, r_d, r_e, r_o, r_i


def calculate_circle_points(x0, y0, n, p1_x, p1_y, r):
    """
    Calculate coordinates of 6 points on a circle centered at (x0, y0) with given radius.
    u is calculated as u = 2rπ/(PATTERN_UNIT_SIZE*n).
    """
    u = (2 * r * math.pi) / (5 * n)
    theta1 = math.atan2(p1_y - y0, p1_x - x0)
    theta = u / r
    points = [(p1_x, p1_y)]
    for i in range(1, 6):
        angle = theta1 + i * theta
        x = x0 + r * math.cos(angle)
        y = y0 + r * math.sin(angle)
        points.append((x, y))
    return points


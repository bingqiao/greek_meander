import drawsvg as draw
import cairosvg
import math

class GreekKeyConfig:
    PATTERN_UNIT_SIZE = 5
    def __init__(self, r_o, pattern_count, border_margin, stroke_width):
        # r_a - "frame_gap" > 0 == PATTERN_UNIT_SIZE * n > 6*math.pi, so n >= 4
        # The pattern is drawn between 5 concentric circles. The radii of these circles are calculated based on the outer radius and the number of patterns.
        # The radii are named radius_1 to radius_5, from the outermost to the innermost circle.
        r_a, r_b, r_c, r_d, r_e, r_o, r_i = GreekKeyConfig._get_radii_for_outer_radius(r_o, GreekKeyConfig.PATTERN_UNIT_SIZE*pattern_count)
        self.radius_1 = r_a        # Circle 1
        self.radius_2 = r_b        # Circle 2
        self.radius_3 = r_c        # Circle 3 (middle)
        self.radius_4 = r_d        # Circle 4
        self.radius_5 = r_e        # Circle 5

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
        start_x, start_y = self.get_start_position(self.radius_1)
        points_1 = GreekKeyConfig._calculate_circle_points(centre_x, centre_y, self.pattern_count, start_x, start_y, self.radius_1)
        start_x, start_y = self.get_start_position(self.radius_2)
        points_2 = GreekKeyConfig._calculate_circle_points(centre_x, centre_y, self.pattern_count, start_x, start_y, self.radius_2)
        start_x, start_y = self.get_start_position(self.radius_3)
        points_3 = GreekKeyConfig._calculate_circle_points(centre_x, centre_y, self.pattern_count, start_x, start_y, self.radius_3)
        start_x, start_y = self.get_start_position(self.radius_4)
        points_4 = GreekKeyConfig._calculate_circle_points(centre_x, centre_y, self.pattern_count, start_x, start_y, self.radius_4)
        start_x, start_y = self.get_start_position(self.radius_5)
        points_5 = GreekKeyConfig._calculate_circle_points(centre_x, centre_y, self.pattern_count, start_x, start_y, self.radius_5)
        return points_1, points_2, points_3, points_4, points_5
    
    def get_coords_for_patterns_by_p0(self, p_1_0, p_2_0, p_3_0, p_4_0, p_5_0):
        centre_x, centre_y = self.get_centre()
        points_1 = GreekKeyConfig._calculate_circle_points(centre_x, centre_y, self.pattern_count, p_1_0[0], p_1_0[1], self.radius_1)
        points_2 = GreekKeyConfig._calculate_circle_points(centre_x, centre_y, self.pattern_count, p_2_0[0], p_2_0[1], self.radius_2)
        points_3 = GreekKeyConfig._calculate_circle_points(centre_x, centre_y, self.pattern_count, p_3_0[0], p_3_0[1], self.radius_3)
        points_4 = GreekKeyConfig._calculate_circle_points(centre_x, centre_y, self.pattern_count, p_4_0[0], p_4_0[1], self.radius_4)
        points_5 = GreekKeyConfig._calculate_circle_points(centre_x, centre_y, self.pattern_count, p_5_0[0], p_5_0[1], self.radius_5)
        return points_1, points_2, points_3, points_4, points_5


    def draw_greek_key_circle(self, path):
        """Draws the meander pattern."""
        points_1, points_2, points_3, points_4, points_5 = self.get_coords_for_patterns()
        # Start at the top of the outermost circle.
        path.M(points_1[0][0], points_1[0][1])

        for i in range(0, self.pattern_count):
            # Draw a line from the outermost circle to the innermost circle.
            path.L(points_5[0][0], points_5[0][1])
            # Draw a line along the innermost circle.
            path.L(points_5[4][0], points_5[4][1])
            # Draw a line from the innermost circle to the second circle.
            path.L(points_2[4][0], points_2[4][1])
            # Draw a line along the second circle.
            path.L(points_2[2][0], points_2[2][1])
            # Draw a line from the second circle to the third circle.
            path.L(points_3[2][0], points_3[2][1])
            # Draw a line along the third circle.
            path.L(points_3[3][0], points_3[3][1])
            # Draw a line from the third circle to the fourth circle.
            path.L(points_4[3][0], points_4[3][1])
            # Draw a line along the fourth circle.
            path.L(points_4[1][0], points_4[1][1])
            # Draw a line from the fourth circle to the outermost circle.
            path.L(points_1[1][0], points_1[1][1])
            # Draw a line along the outermost circle.
            path.L(points_1[5][0], points_1[5][1])

            points_1, points_2, points_3, points_4, points_5 = self.get_coords_for_patterns_by_p0(points_1[5], points_2[5], points_3[5], points_4[5], points_5[5])


        path.Z()

    @staticmethod
    def _get_radii_for_outer_radius(r_o, n):
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

    @staticmethod
    def _calculate_circle_points(x0, y0, n, p1_x, p1_y, r):
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





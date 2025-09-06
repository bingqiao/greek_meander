import drawsvg as draw
import cairosvg

class GreekKeyConfig:
    # Constants for drawing the meander pattern
    UP = -1
    DOWN = 1
    LEFT = -1
    RIGHT = 1

    def __init__(self, key_unit_length, width_units, height_units, border_margin, stroke_width):
        # The size of greek key unit
        self.key_unit_length = key_unit_length
        # Number of greek key units horizontally
        self.width_units = width_units
        # Number of greek key units vertically
        self.height_units = height_units
        self.key_pattern_length = self.key_unit_length * 5
        self.border_margin = border_margin
        self.stroke_width = stroke_width

    def get_canvas_size(self):
        width = self.width_units * self.key_pattern_length + 2 * self.border_margin + 2 * self.key_unit_length + 2*self.stroke_width
        height = self.height_units * self.key_pattern_length + 2 * self.border_margin + + 2 * self.key_unit_length + 2*self.stroke_width
        return width, height

    def get_start_position(self):
        start_x = self.border_margin + self.key_unit_length + self.stroke_width
        start_y = self.key_pattern_length + self.border_margin + self.key_unit_length + self.stroke_width
        return start_x, start_y

    def get_outer_frame_size(self):
        outer_x = self.border_margin + self.stroke_width
        outer_y = self.border_margin + self.stroke_width
        outer_width = self.width_units * self.key_pattern_length + 2 * self.key_unit_length
        outer_height = self.height_units * self.key_pattern_length + 2 * self.key_unit_length
        return outer_x, outer_y, outer_width, outer_height

    def get_inner_frame_size(self):
        inner_x = 6 * self.key_unit_length + self.border_margin + self.stroke_width
        inner_y = 6 * self.key_unit_length + self.stroke_width
        inner_width = (self.width_units - 2) * self.key_pattern_length
        inner_height = (self.height_units - 2) * self.key_pattern_length
        return inner_x, inner_y, inner_width, inner_height


    def draw_horizontal_unit(self, path):
        """Draws a single horizontal unit of the meander pattern."""
        key_unit_length = self.key_unit_length
        path.v(-4 * key_unit_length)
        path.h(4 * key_unit_length)
        path.v(3 * key_unit_length)
        path.h(-2 * key_unit_length)
        path.v(-key_unit_length)
        path.h(key_unit_length)
        path.v(-key_unit_length)
        path.h(-2 * key_unit_length)
        path.v(3 * key_unit_length)
        path.h(4 * key_unit_length)


    def draw_vertical_unit(self, path):
        """Draws a single vertical unit of the meander pattern."""
        key_unit_length = self.key_unit_length
        path.h(4 * key_unit_length)
        path.v(4 * key_unit_length)
        path.h(-3 * key_unit_length)
        path.v(-2 * key_unit_length)
        path.h(key_unit_length)
        path.v(key_unit_length)
        path.h(key_unit_length)
        path.v(-2 * key_unit_length)
        path.h(-3 * key_unit_length)
        path.v(4 * key_unit_length)

    def draw_horizontal_unit_right_to_left(self, path):
        """Draws a single horizontal unit of the meander pattern, from right to left."""
        key_unit_length = self.key_unit_length
        path.h(-4*key_unit_length)
        path.v(-3*key_unit_length)
        path.h(2*key_unit_length)
        path.v(1*key_unit_length)
        path.h(-key_unit_length)
        path.v(1*key_unit_length)
        path.h(2*key_unit_length)
        path.v(-3*key_unit_length)
        path.h(-4*key_unit_length)
        path.v(4*key_unit_length)

    def draw_vertical_unit_bottom_up(self, path):
        """Draws a single vertical unit of the meander pattern, bottom up."""
        key_unit_length = self.key_unit_length
        path.v(-4*key_unit_length)
        path.h(3*key_unit_length)
        path.v(2*key_unit_length)
        path.h(-key_unit_length)
        path.v(-key_unit_length)
        path.h(-key_unit_length)
        path.v(2*key_unit_length)
        path.h(3*key_unit_length)
        path.v(-4*key_unit_length)
        path.h(-4*key_unit_length)
    
    def draw_greek_key_unit(self, path):
        """Draws the main meander pattern."""
        start_x, start_y = self.get_start_position()
        key_unit_length = self.key_unit_length
        key_pattern_length = self.key_pattern_length
        width_units = self.width_units
        height_units = self.height_units

        # top line
        path.M(start_x, start_y)
        path.v(-key_unit_length)
        for _ in range(width_units - 1):
            self.draw_horizontal_unit(path)
        path.v(-4 * key_unit_length)
        path.h(key_unit_length)
        # right line
        for _ in range(height_units - 1):
            self.draw_vertical_unit(path)

        path.h(4*key_unit_length)
        path.v(5*key_unit_length)

        # bottom line
        for _ in range(width_units -1):
            self.draw_horizontal_unit_right_to_left(path)

        path.h(-5*key_unit_length)

        # left line
        for _ in range(height_units - 1):
            self.draw_vertical_unit_bottom_up(path)

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

        self.draw_greek_key_unit(path)

        def draw_frame(path, x, y, w, h):
            """Draws a rectangular frame using a path."""
            path.M(x, y)
            path.h(w)
            path.v(h)
            path.h(-w)
            path.v(-h)
            path.Z()

        # Draw frames
        draw_frame(path, *self.get_outer_frame_size())
        draw_frame(path, *self.get_inner_frame_size())

        d.append(path)
        d.save_svg(f'{filename}.svg')

        cairosvg.svg2png(url=f'{filename}.svg', write_to=f'{filename}.png', output_width=width, output_height=height)




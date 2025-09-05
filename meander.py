import argparse
import meander_rectangle as rect
import meander_circle as circle


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Draw a Greek Key (Meander) SVG and PNG with customizable properties.")
    parser.add_argument('--stroke-width', type=float, default=7.0, help="Line thickness in pixels (default: 2.0)")
    parser.add_argument('--stroke-color', type=str, default='#AB8E0E', help="Line color: name (e.g., 'red'), hex (e.g., '#FF0000'), or RGB (e.g., '255,0,0') (default: '#AB8E0E')")
    parser.add_argument('--stroke-opacity', type=float, default=0.7, help="Line transparency, 0.0 (transparent) to 1.0 (opaque) (default: 0.7)")
    parser.add_argument('--border-margin', type=int, default=1, help="The margin (>1) of borders (default: 3)")
    parser.add_argument('--file', type=str, default='meander', help="File name for svg and png (default: `meander`)")

    subparsers = parser.add_subparsers(dest="type", help="Available types")

    # Subcommand: rectangle
    parser_rect = subparsers.add_parser("rect", help="A rectangle of Greek Keys")
    parser_rect.add_argument('--size', type=int, default=10, help="This defines the size of the pattern (default: 10)")
    parser_rect.add_argument('--width', type=int, default=16, help="The number of patterns horizontally (default: 16)")
    parser_rect.add_argument('--height', type=int, default=9, help="The number of patterns vertically (default: 9)")

    # Subcommand: circle
    parser_circle = subparsers.add_parser("circle", help="A circle of Greek Keys")
    parser_circle.add_argument('--pattern-count', type=int, default=30, help="This defines the number of patterns >= 4 (default: 30)")
    parser_circle.add_argument('--radius', type=int, default=300, help="The radius of the circle (default: 300)")

    # Parse arguments
    args = parser.parse_args()
    
    if args.type == 'rect':
        config = rect.GreekKeyConfig(args.size, args.width, args.height, args.border_margin, args.stroke_width)

    elif args.type == 'circle':
        config = circle.GreekKeyConfig(args.radius, args.pattern_count, args.border_margin, args.stroke_width)

    else:
        parser.print_help()
        return
    
    config.generate_pattern_svg(
        stroke_width=args.stroke_width,
        stroke_color=args.stroke_color,
        stroke_opacity=args.stroke_opacity,
        filename=args.file)

if __name__ == '__main__':
    main()

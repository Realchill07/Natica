import cairo
import os

from .base_chart import BaseChart

class BarChart(BaseChart):
    
    css_path = os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      "main.css"
    )
    
    def draw_chart(self, ctx, width, height):
        if not self.data:
            return

        max_value = max(self.data.values(), default=1)

        bar_width = 40
        spacing = 50

        left = 55
        right = width - 20
        top = 20
        bottom = height - 40

        chart_height = bottom - top

        # Calculate scale
        scale = chart_height / max_value

        # Y-axis scale intervals
        steps = 5
        interval = max_value / steps

        ctx.set_font_size(12)

        # Draw Y-axis values and gridlines
        for i in range(steps + 1):
            value = interval * i
            y = bottom - (value * scale)

            # Gridline
            ctx.set_source_rgb(0.35, 0.35, 0.35)
            ctx.set_line_width(0.5)

            ctx.move_to(left, y)
            ctx.line_to(right, y)
            ctx.stroke()

            # Axis value
            ctx.set_source_rgb(1, 1, 1)
            ctx.move_to(5, y + 4)
            ctx.show_text(f"{value:.0f}")

        # Draw axes
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(1)

        ctx.move_to(left, top)
        ctx.line_to(left, bottom)
        ctx.line_to(right, bottom)
        ctx.stroke()

        # Draw bars
        for i, (name, value) in enumerate(self.data.items()):

            x = left + 15 + i * (bar_width + spacing)
            bar_height = value * scale

            # Bar
            ctx.set_source_rgb(0.078, 0.6, 0.659)

            ctx.rectangle(
                x,
                bottom - bar_height,
                bar_width,
                bar_height
            )

            ctx.fill()

            # X-axis label
            ctx.set_source_rgb(1, 1, 1)
            ctx.set_font_size(12)
            ctx.move_to(x, bottom + 20)
            ctx.show_text(name)
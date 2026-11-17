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
        max_value = max(self.data.values(), default = 1)
        
        bar_width = 40
        spacing = 50
        bottom = height - 40
        
        scale = (height-80)/max_value
        
        left = 40

        ctx.move_to(left, 20)
        ctx.line_to(left, bottom )
        ctx.line_to(width - 400, bottom )
        ctx.stroke()
                
        
        
        for i, (name, value) in enumerate(self.data.items()):
            
            x = 40 + i * (bar_width + spacing)
            bar_height = value * scale

            ctx.set_source_rgb(1, 1, 1)

            ctx.move_to(x, bottom + 20)
            ctx.set_font_size(12)
            ctx.show_text(name)
            
            ctx.set_source_rgb(0.078, 0.6, 0.659)                           
            
            ctx.rectangle(
                x, 
                bottom - bar_height,
                bar_width,
                bar_height
            )
            
            ctx.fill()
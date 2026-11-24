import gi

gi.require_version("Gtk","4.0")
from gi.repository import Gtk


class BaseChart(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.data = {}
        
        self.set_content_width(690)
        self.set_content_height(420)
        
        self.set_draw_func(self._draw)
        
    def _draw(self, area, ctx, width, height):
        self.draw_chart(ctx, width, height)
        
    def draw_chart(self, ctx, width, height):
        pass
        
    def update_data(self, data):
        self.data = data
        self.queue_draw() 
            
            
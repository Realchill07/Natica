import gi

gi.require_version('Adw','1')
gi.require_version('Gtk','4.0')

from gi.repository import Gtk, Adw

Adw.init()

class MyApp(Adw.Application):
  def __init__(self):
    super().__init__(application_id='com.realchill.Natica')
    
  window = Adw.ApplicationWindow(application = self)
  window.set_title("Natica")
  window.set_default_size(690,690)
   
   
    
  def create_page(self, name):
    page = Gtk.Box(orientation=Gtk.orientation.VERTICAL, spacing = 10)
            
    page.set_margin_top(20)
    page.set_margin_bottom(20)
    page.set_margin_start(20)
    page.set_margin_end(20)
            
    label = Gtk.Label(label=name)
    page.append(label)
            
    return page
    
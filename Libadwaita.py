import gi

gi.require_version('Adw','1')
gi.require_version('Gtk','4.0')

from gi.repository import Adw,Gtk

Adw.init()

class MyApp(Adw.Application):
  def __init__(self):
    super().__init__(application_id='com.realchill.adw-testing')
  
  def do_activate(self):
    window = Adw.ApplicationWindow(application = self)
    window.set_title("Adw")
    window.set_default_size(690,690)
    
    header = Adw.HeaderBar()
    
    title = Gtk.Label(label = "Natica")
    header.set_title_widget(title)
    
    
    self.current = 0
    
    content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # content.set_margin_top(50)
    # content.set_margin_bottom(0)
    content.set_halign(Gtk.Align.CENTER)
    content.set_valign(Gtk.Align.CENTER)
    
    increase_button = Gtk.Button(label="Click to Increase the Count")
    increase_button.connect("clicked",self.count_increament)
    
    decrease_button = Gtk.Button(label="Click to Decrease the Count")
    decrease_button.connect("clicked",self.count_decreament)
    
    reset_button = Gtk.Button(label="CLick to Reset the Count")
    reset_button.connect("clicked",self.reset_count)
    self.label = Gtk.Label()
    self.label.set_text(str(self.current))
    
    content.append(self.label)
    content.append(increase_button)
    content.append(decrease_button)
    content.append(reset_button)
    
    toolbar = Adw.ToolbarView()
    toolbar.add_top_bar(header)
    toolbar.set_content(content)
    
    window.set_content(toolbar)
    window.present()
  
  def count_increament(self, button):
   self.current = self.current + 1 
   self.label.set_text(str(self.current))
   
  
  def count_decreament(self, button):
    self.current = self.current - 1 
    self.label.set_text(str(self.current))
    
  def reset_count(self,button):
    self.current = 0
    self.label.set_text(str(self.current))
    
test = MyApp()
test.run()
import gi

gi.require_version('Adw','1')
gi.require_version('Gtk','4.0')
from gi.repository import Gtk, Adw, Gio, Gdk  
        
class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id = 'com.horknee.testing')
    
        self.connect("activate",self.on_activate)
               
          
    def on_activate(self, app):
        win = Adw.ApplicationWindow(application = self)
        win.set_default_size(400, 300);  
        
        label = Gtk.Label(label = 'right click here')
        
        #right click detection
        gesture = Gtk.GestureClick()
        gesture.set_button(3)
        gesture.connect("pressed", self.on_right_click, label)
        
        label.add_controller(gesture)
        
        win.set_content(label)
        win.present()   
        
    
    def on_right_click(self, gesture, n_press, x, y, widget):
        
        menu = Gio.Menu()
                    
        menu.append("Delete", 'app.delete')
        menu.append("Edit", 'app.edit')
        menu.append("Edit Tag", 'app.edit_tag')
        
        popup = Gtk.PopoverMenu.new_from_model(menu)
        popup.set_parent(widget)
        
        rect = Gdk.Rectangle()
        rect.x = int(x)
        rect.y = int(y)
        rect.width = 1
        rect.height = 1
        
        popup.set_pointing_to(rect)
        popup.popup()
        
    def on_delete(self, action, param):
        print("Delete")
        
    def on_edit(self, action, param):
        print("Edit")
        
    def on_edit_tag(self, action, param):
        print("Edit Tag")
        
app = App() 

delete = Gio.SimpleAction.new('delete', None)
delete.connect("activate", app.on_delete)
app.add_action(delete)

edit = Gio.SimpleAction.new('edit', None)
edit.connect('activate', app.on_edit)
app.add_action(edit)

edit_tag = Gio.SimpleAction.new('edit_tag', None)
edit_tag.connect('activate', app.on_edit_tag)
app.add_action(edit_tag)
        
app.run(None)
    
    

 

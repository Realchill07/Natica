import gi

gi.require_version('Adw','1')
gi.require_version('Gtk','4.0')

from gi.repository import Adw,Gtk

Adw.init()

class MyApp(Adw.Application):
  def __init__(self):
    super().__init__(application_id = 'com.natic.UiTesting')
  
  def do_activate(self):
    window = Adw.ApplicationWindow(application = self)
    window.set_title('testing UI')
    window.set_default_size(500,500)
    
    header=Adw.HeaderBar()
    title = Gtk.Label(label='UI Testing')
    header.set_title_widget(title)
    
    main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

    self.stack = Gtk.Stack()
    
    sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 6)
    sidebar.set_size_request(180,-1)
    sidebar.set_margin_top(10)
    sidebar.set_margin_bottom(10)
    sidebar.set_margin_start(10)
    sidebar.set_margin_end(10)
    
    home = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=10)
    home.set_halign(Gtk.Align.CENTER)
    home.set_valign(Gtk.Align.CENTER)
    home.append(Gtk.Label(label='Home'))
       
    projects = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=10)
    projects.set_valign(Gtk.Align.CENTER)
    projects.set_halign(Gtk.Align.CENTER)
    projects.append(Gtk.Label(label='Projects'))
    
    self.stack.add_named(home,'home')
    self.stack.add_named(projects,'projects')
    
    homeButton = Gtk.Button(label='Home')
    homeButton.connect("clicked", lambda b:self.stack.set_visible_child_name('projects'))
    projects.append(homeButton)
    
    projectsButton = Gtk.Button(label='Projects')
    projectsButton.connect("clicked",lambda b: self.stack.set_visible_child_name('home'))
    home.append(projectsButton)
    
    reportsButton = Gtk.Button(label='Reports')
    # reportsButton.connect('clicked',self.)
  
    
    
    
    
    main_box.append(self.stack)
    main_box.append(sidebar)
    toolbar = Adw.ToolbarView()
    toolbar.add_top_bar(header)
    toolbar.set_content(main_box)
    
    window.set_content(toolbar)
    window.present()
    
  def goHome(self, button):
    self.stack.set_visible_child_name('home')
    
  def goProjects(self, button):
    self.stack.set_visible_child_name('projects')

test = MyApp()
test.run()
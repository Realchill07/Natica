import gi

gi.require_version('Adw','1')
gi.require_version('Gtk','4.0')

from gi.repository import Adw,Gtk

Adw.init()

class MyApp(Adw.Application):
  def __init__(self):
    super().__init__(application_id = 'com.Realchill.Natica')
  
  def do_activate(self):
    window = Adw.ApplicationWindow(application = self)
    window.set_title('testing UI')
    window.set_default_size(500,500)
    
    header=Adw.HeaderBar()
    title = Gtk.Label(label='Natica')
    header.set_title_widget(title)
    
    main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

    self.stack = Gtk.Stack()
    
    sidebar = Gtk.ListBox()
    sidebar.set_selection_mode(Gtk.SelectionMode.SINGLE)
    sidebar.add_css_class('navigation-sidebar')
    sidebar.set_size_request(220,-1)
    sidebar.set_margin_top(10)
    sidebar.set_margin_bottom(10)
    sidebar.set_margin_start(10)
    sidebar.set_margin_end(10)
    

    
    self.stack.add_named(self.create_page("Home"), "home")
    self.stack.add_named(self.create_page("Projects"), "projects")
    self.stack.add_named(self.create_page("Reports"), "reports")
    self.stack.add_named(self.create_page("Statistics"), "stats")
    self.stack.add_named(self.create_page("Settings"), "settings")
    
    self.pages = [
      ("🏠 Home",'home'),
      ("📁 Projects",'projects'),
      ('📊 Reports','reports'),
      ('📈 Statistics','stats'),
      ("⚙ Settings", "settings"),
    ]
    
    for title, page_name in self.pages:
      self.stack.add_named(self.create_page(title),page_name)
    
    for title, page_name in self.pages:
      row = Gtk.ListBoxRow()
      
      label = Gtk.Label(label=title)
      label.set_halign(Gtk.Align.START)
      
      row.set_child(label)
      
      sidebar.append(row)
    
    sidebar.select_row(sidebar.get_row_at_index(0))  
      
    sidebar.connect("row-selected",self.change_page)
    
    
    main_box.append(sidebar)
    main_box.append(self.stack)
    
    self.stack.set_hexpand(True)
    self.stack.set_vexpand(True)
    
    toolbar = Adw.ToolbarView()
    toolbar.add_top_bar(header)
    toolbar.set_content(main_box)
    
    window.set_content(toolbar)
    window.present()
    
  def create_page(self, name):
    page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 10)
                
    page.set_margin_top(20)
    page.set_margin_bottom(20)
    page.set_margin_start(20)
    page.set_margin_end(20)
                
    label = Gtk.Label(label=name)
    page.append(label)
    return page
    
  def change_page(self, listbox, row):
    if row is None:
      return
    self.stack.set_visible_child_name(self.pages[row.get_index()][1])
    
                

test = MyApp()
test.run()
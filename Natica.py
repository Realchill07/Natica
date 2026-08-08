import gi
import time
import uuid

gi.require_version('Adw','1')
gi.require_version('Gtk','4.0')

from gi.repository import Adw,Gtk, GLib

Adw.init()


class Stopwatch:
    def __init__(self, name, parent=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.accumulatedSeconds = 0
        self.startTime = None
        self.running = False
        self.children = []
        self.parent = parent

    def start(self):
        self.running = True
        self.startTime = time.time()
        

    def pause(self):
        timeAtStop = time.time()
        totalTime = timeAtStop - self.startTime
        self.accumulatedSeconds += totalTime
        self.running = False
        self.startTime = None
        
       
    def get_elapsed(self):
        if self.running:
            return self.accumulatedSeconds + (time.time()-self.startTime)
            
        else:
            return self.accumulatedSeconds
    
    def lap(self):
        for sibling in self.children:
            if sibling.running is True:
                sibling.pause()
        if not self.running:
            self.start()        
        child = Stopwatch("lap",self)
        self.children.append(child)
        child.start()
        return child
    
    def resume(self):
        daddy = self.parent
        if daddy.running:
            for baby in daddy.children:
                if baby.running:
                    baby.pause()
        else:
            daddy.start()
        self.start()
      
           
def timeformat(total_seconds):
    total_seconds = int(total_seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

class MyApp(Adw.Application):
  def __init__(self):
    super().__init__(application_id = 'com.Realchill.Natica')
    self.projects = []
    self.project_label = {}
  
  def do_activate(self):
    window = Adw.ApplicationWindow(application = self)
    window.set_title('testing UI')
    window.set_default_size(500,500)
    
    header=Adw.HeaderBar()
    title = Gtk.Label(label='Natica')
    header.set_title_widget(title)
    
    main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

    self.stack = Gtk.Stack()
    
    # making the sidebar
    sidebar = Gtk.ListBox()
    sidebar.set_selection_mode(Gtk.SelectionMode.SINGLE)
    sidebar.add_css_class('navigation-sidebar')
    sidebar.set_size_request(220,-1)
    sidebar.set_margin_top(10)
    sidebar.set_margin_bottom(10)
    sidebar.set_margin_start(10)
    sidebar.set_margin_end(10)
    

    
    self.stack.add_named(self.create_home_page(),'home')
    self.stack.add_named(self.create_projects_page(),'projects')
    self.stack.add_named(self.create_page("Reports"), "reports")
    self.stack.add_named(self.create_page("Statistics"), "stats")
    self.stack.add_named(self.create_page("Settings"), "settings")
    
    
    # This is for sidebar i.e. ("this is displayed in sidebar","kind of an id")
    self.pages = [
      ("🏠 Home",'home'),
      ("📁 Projects",'projects'),
      ('📊 Reports','reports'),
      ('📈 Statistics','stats'),
      ("⚙ Settings", "settings"),
    ]
    
  
    for title, page_name in self.pages:
      row = Gtk.ListBoxRow()
      
      label = Gtk.Label(label=title)
      label.set_halign(Gtk.Align.START)
      
      row.set_child(label)
      
      sidebar.append(row)
    
    sidebar.select_row(sidebar.get_row_at_index(0))  
      
    sidebar.connect("row-selected",self.change_page)
    
    # setting up the layout
    # this is dependent on order so if i put main_box.apped(self.stack) and then main_box.append(sidebar) then the sidebar will on right
    main_box.append(sidebar)
    main_box.append(self.stack)
    
    self.stack.set_hexpand(True)
    self.stack.set_vexpand(True)
    
    toolbar = Adw.ToolbarView()
    toolbar.add_top_bar(header)
    toolbar.set_content(main_box)
    
    window.set_content(toolbar)
    window.present()
    
    GLib.timeout_add(1000, self.on_tick)
    
  def create_home_page(self):
    page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 10)
                
    page.set_margin_top(20)
    page.set_margin_bottom(20)
    page.set_margin_start(20)
    page.set_margin_end(20)
                
    label = Gtk.Label(label='Home')
    page.append(label)
    return page
  
  def create_projects_page(self):
    page = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
    
    page.set_margin_top(20)
    page.set_margin_bottom(20)
    page.set_margin_start(20)
    page.set_margin_end(20)
    
    label = Gtk.Label(label='Projects')
    page.append(label)
    
    button = Gtk.Button(label='+ New Project')
    button.connect("clicked", self.on_click_new_project)
    page.append(button)
    
    self.projects_list = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 8)
    self.projects_list.set_vexpand(True)
    page.append(self.projects_list)
    
    return page
    
  
  def create_page(self,name):
      page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 10)
                  
      page.set_margin_top(20)
      page.set_margin_bottom(20)
      page.set_margin_start(20)
      page.set_margin_end(20)
                  
      label = Gtk.Label(label=name)
      page.append(label)
      return page
  
  def create_project_only_for_ui(self, stopwatch):
    project = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 5)
    
    label = Gtk.Label(label = stopwatch.name)
    label.set_halign(Gtk.Align.START)
    label.set_hexpand(True)
    project.append(label)
    
    time_label = Gtk.Label(label = '00:00:00')
    self.project_label[stopwatch.id] = time_label
    project.append(time_label)
    
    start = Gtk.Button(label = 'Start')
    start.connect("clicked",self.on_start_clicked,stopwatch)
    project.append(start)
    
    return project
    
  def on_click_new_project(self, button):
    stopwatch = Stopwatch("New Project")
    self.projects.append(stopwatch)
    
    project_widget = self.create_project_only_for_ui(stopwatch)
    self.projects_list.append(project_widget)
    
  def on_start_clicked(self, button, stopwatch):
    if stopwatch.running:
      stopwatch.pause()
      button.set_label("Start")
    else : 
      stopwatch.start()
      button.set_label("Pause")
    print(stopwatch.running)
    
      
  def change_page(self, listbox, row):
    if row is None:
      return
    self.stack.set_visible_child_name(self.pages[row.get_index()][1])
    
  def update_labels(self):
    for stopwatch in self.projects:
      elapsed = stopwatch.get_elapsed()
      
      label = self.project_label[stopwatch.id]
      label.set_label(timeformat(elapsed))
    
  def on_tick(self):
    self.update_labels()
    return True
                

test = MyApp()
test.run()
import gi
import time
import uuid
import os
import json
import platform

gi.require_version('Adw','1')
gi.require_version('Gtk','4.0')

from gi.repository import Adw,Gtk, GLib

Adw.init()

#Stopwatch framework and some core functions
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
        if self.running:
          return
        self.running = True
        self.startTime = time.time()
        

    def pause(self):
        if not self.running:
          return
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
      
    def to_dict(self):
      return {
        "id": self.id,
        "name": self.name,
        "accumulatedSeconds": self.accumulatedSeconds,
        "startTime": self.startTime,
        "running": self.running,
        "children": [child.to_dict() for child in self.children]
    }  
      
    @classmethod
    
    def from_dict(cls, data, parent = None):
      stopwatch = cls(
        data['name'], parent
      )
      stopwatch.id = data['id']
      stopwatch.accumulatedSeconds = data['accumulatedSeconds']
      stopwatch.startTime = data['startTime']
      stopwatch.running = data['running']
      
      for child_data in data["children"]:
        child = cls.from_dict(child_data, stopwatch)
        stopwatch.children.append(child)
      return stopwatch
           
def timeformat(total_seconds):
    total_seconds = int(total_seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

class MyApp(Adw.Application):
  def __init__(self):
    super().__init__(application_id = 'io.github.realchill07.Natica')
    self.projects = []
    self.project_label = {}
    self.project_buttons = {}
    self.storage = Storage()
    self.projects = self.storage.load()
  
  def do_activate(self):
    window = Adw.ApplicationWindow(application = self)
    window.set_title('Natica')
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
    
    
    self.pages = [
      ("🏠 Home",'home'),
    # This is for sidebar i.e. ("this is displayed in sidebar","kind of an id")
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
    
    scroll = Gtk.ScrolledWindow()
    scroll.set_hexpand(True)
    scroll.set_vexpand(True)
    scroll.set_child(self.projects_list)
    page.append(scroll)
    
    for stopwatch in self.projects:
      project_widget = self.create_project_only_for_ui(stopwatch)
      self.projects_list.append(project_widget)
    
    return page
    
  #boilerplate for upcoming pages
  def create_page(self,name):
      page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 10)
                  
      page.set_margin_top(20)
      page.set_margin_bottom(20)
      page.set_margin_start(20)
      page.set_margin_end(20)
                  
      label = Gtk.Label(label=name)
      coming_soon = Gtk.Label(label = "Coming soon...")
      page.append(label)
      page.append(coming_soon)
      return page
  
  def create_project_only_for_ui(self, stopwatch):
    project = project_row(stopwatch)
    
    project.THE_button.connect("clicked",self.on_start_clicked, stopwatch)
    
    project.child_button.connect("clicked", self.on_add_child, stopwatch, project)
    
    project.name_entry.connect("activate", self.edit_project_name, stopwatch, project)
    
    project.edit_button.connect("clicked", self.edit_project_name, stopwatch, project)
    
    self.project_buttons[stopwatch.id] = project.THE_button
    self.project_label[stopwatch.id] = project.time_label
    
    for child in stopwatch.children:
      child_widget = self.create_project_only_for_ui(child)
      project.children_box.append(child_widget)
    
    return project
    
  #Create the object from class Stopwatch
  def on_click_new_project(self, button):
    stopwatch = Stopwatch("New Project")
    self.projects.append(stopwatch)
    
    project_widget = self.create_project_only_for_ui(stopwatch)
    self.projects_list.append(project_widget)
    
    self.on_add_child(None, stopwatch, project_widget)
    
    self.storage.save(self.projects)
  
  #Decides which function runs for when THE_button is clicked
  def on_start_clicked(self, button, stopwatch):
    if stopwatch.running:
      self.pause_stopwatch(stopwatch)
    else : 
      self.start_stopwatch(stopwatch)
  
  #Switches the pages when we click on them through the sidebar     
  def change_page(self, listbox, row):
    if row is None:
      return
    self.stack.set_visible_child_name(self.pages[row.get_index()][1])
  
  #Updates time lapsed for each project
  def update_stopwatch_label(self, stopwatch):
    elapsed = stopwatch.get_elapsed()

    label = self.project_label[stopwatch.id]
    label.set_label(timeformat(elapsed))

    for child in stopwatch.children:
      self.update_stopwatch_label(child)
  
  #Helper function      
  def update_labels(self):
    for stopwatch in self.projects:
        self.update_stopwatch_label(stopwatch)

  #Helper function for the forementioned helper function
  def on_tick(self):
    self.update_labels()
    return True
  
  #Creates an object of the class stopwatch but his time as a child for an exisiting stopwatch
  def on_add_child(self, button, parent, parent_widget):
    child = Stopwatch('New Task', parent)
  
    parent.children.append(child)
    
    child_widget = self.create_project_only_for_ui(child)
    
    parent_widget.children_box.append(child_widget)  
  
    self.storage.save(self.projects)     
    
  #Changes the label of THE_button 
  def update_button_label(self, stopwatch):
    button = self.project_buttons[stopwatch.id]
    
    if stopwatch.running:
      button.set_label("Pause")
    else:
      button.set_label("Resume")

  #The class which handles when a subtask or a task is resumed or started
  def start_stopwatch(self, stopwatch):
    parent = stopwatch.parent
    
    if parent is not None:
      for sibling in parent.children:
        if sibling is not stopwatch and sibling.running:
          sibling.pause()
          self.update_button_label(sibling)
    
    while parent is not None:
      if not parent.running:
        parent.start()
        
      self.update_button_label(parent)
      parent = parent.parent
    
    stopwatch.start()
    self.update_button_label(stopwatch) 
  
  #The class which handles when a subtask or a task is paused
  def pause_stopwatch(self, stopwatch):
    parent = stopwatch.parent
    stopwatch.pause()
    self.update_button_label(stopwatch)
    
    for child in stopwatch.children:
      if child.running:
        self.pause_stopwatch(child)
    
    if parent is not None:
      any_child_running = any(child.running for child in parent.children)
      if not any_child_running:
        parent.pause()
        self.update_button_label(parent)
  
  #Function to edit a task or subtask's name
  def edit_project_name(self, button, stopwatch, project):
    if not project.editing:
      project.editing = True
      
      project.name_entry.set_text(stopwatch.name)
      project.name_entry.select_region(0,-1)
      project.name_stack.set_visible_child_name("entry")
      
      project.edit_button.set_label('Save')
      project.name_entry.grab_focus()
      
    else:
      new_name = project.name_entry.get_text().strip()
      
      if new_name:
        stopwatch.name = new_name
        project.name_label.set_label(stopwatch.name)
        
      project.name_stack.set_visible_child_name("label")
      project.edit_button.set_label("Edit")
      project.editing = False   
    
    
    self.storage.save(self.projects)
    
  # Function which activates when the window is closed, so that next time the app is opened and data is loaded the task timer doesnt include the period when the app was closed
  def interrupt_stopwatch(self, stopwatch):
    if stopwatch.running:
      stopwatch.pause()
    for child in stopwatch.children:
      self.interrupt_stopwatch(child)
  
  #Helper function for interrup_stopwatch
  def interrupt_running_timers(self):
    for project in self.projects:
      self.interrupt_stopwatch(project)
   
  #calls the helper function and saves the data in a save file
  def prepare_for_close(self):
    self.interrupt_running_timers()
    self.storage.save(self.projects)

  #Calls for the above function and then lets the application based on Adw(Libadwaita) do its normal shutdown procedure 
  def do_shutdown(self):
    self.prepare_for_close()
    Adw.Application.do_shutdown(self)

#If we consider the class Stopwatch to be the framework, this class is like how that framework is showed/displayed in the app
class project_row(Gtk.Box):
  def __init__(self, stopwatch):
    super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing = 10)
    
    self.stopwatch = stopwatch
    
    #row for parents
    self.row = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 5)
    
    self.name_stack = Gtk.Stack()
    self.row.append(self.name_stack)
    
    #entry for renaming the stopwatch
    self.name_entry = Gtk.Entry()
    self.name_entry.set_text(stopwatch.name)
    
    #Name label for the stopwatch
    self.name_label = Gtk.Label(label = stopwatch.name)
    self.name_label.set_halign(Gtk.Align.START)
    self.name_label.set_hexpand(True)
    
    self.name_stack.add_named(self.name_label,"label")
    self.name_stack.add_named(self.name_entry,"entry")
    self.name_stack.set_visible_child_name("label")
    self.name_stack.set_hexpand(True)
    
    #Timer label
    self.time_label = Gtk.Label(label = '00:00:00')
    self.row.append(self.time_label)
    
    #Edit Button
    self.editing = False
    self.edit_button = Gtk.Button(label = "Edit")
    self.row.append(self.edit_button)
    
    #Button to resume/start/pause the stopwatch
    self.THE_button = Gtk.Button(label = 'Start')
    self.row.append(self.THE_button)
      
    #Button to add a child 
    self.child_button = Gtk.Button(label = '+')
    self.row.append(self.child_button)
    
    #row for each children... duh
    self.children_box = Gtk.Box(orientation= Gtk.Orientation.VERTICAL, spacing = 7)
    self.children_box.set_margin_start(25)
    
    self.append(self.row)
    self.append(self.children_box)

#Class that handles storing the data and some of the functions relevant to it since 2 of the functions related to storage lives in the class Stopwatch
class Storage:
  def __init__(self):
    if platform.system() == "Windows":
      base_directory = os.environ.get("LOCALAPPDATA")
      self.directory = os.path.join(base_directory,"Natica")
    else:
      self.directory = os.path.expanduser("~/.local/share/natica")

    self.file_path = os.path.join(self.directory,"data.json")

    os.makedirs(self.directory,exist_ok=True)
    
  def save(self, projects):
    data = {
      "projects": [
        project.to_dict()
        for project in projects   
      ]
    }
    
    with open (self.file_path, "w") as file:
      json.dump(data, file, indent = 2)
      
  def load(self):
    if not os.path.exists(self.file_path):
      return []
    
    with open (self.file_path, "r") as file:
      data = json.load(file)
      
    projects = []
    
    for project_data in data['projects']:
      project = Stopwatch.from_dict(project_data)
      projects.append(project)
      
    return projects
  
test = MyApp()
test.run()
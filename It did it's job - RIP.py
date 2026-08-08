import gi
import time
import uuid

gi.require_version('Gtk', '4.0')
gi.require_version('Adw','1')
from gi.repository import Gtk,GLib,Adw

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
    seconds = total_seconds % 60class Stopwatch:
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.realchill07.stopwatch')

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("Stopwatch")
        window.set_default_size(500, 300)
        
        self.projects = []
        
        self.children_labels = {}
        self.parent_labels = {}
        self.button_labels = {}
        
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.set_margin_top(20)
        self.box.set_margin_bottom(20)
        self.box.set_margin_start(20)
        self.box.set_margin_end(20)

        # self.stopwatch.child = None

        self.createButton = Gtk.Button(label="New")
        self.createButton.connect("clicked",self.on_create_clicked)
        self.box.append(self.createButton)

        window.set_child(self.box)
        window.present()
        
        GLib.timeout_add(1000, self.on_tick)
         
    def on_start_clicked(self, button, sw):
        if sw.running:
            mommy = sw.parent
            if mommy is not None:
                mommy.pause()
                mommy_button = self.button_labels[mommy.id]
                mommy_button.set_label("Start")
            sw.pause()
            for child in sw.children:
                if child.running is True:
                    child.pause()
            button.set_label("Start")
        else:
            mommy = sw.parent
            if not sw.children:
                self.on_lap_clicked("clicked", sw)
            if mommy is None:
                sw.start()
            else:
                sw.resume()
            if mommy is not None:
                mommy.start()
                mommy_button = self.button_labels[mommy.id]
                mommy_button.set_label("Pause")
            
            button.set_label("Pause")
        self.update_label()
        
    def on_tick(self):
        self.update_label()
        return True
    
    def on_lap_clicked(self, button, sw):
        self.new_child = sw.lap()
        self.new_child_label = Gtk.Label(label="00:00:00")
        self.children_labels[self.new_child.id] = self.new_child_label
        
        
        self.child_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        # child_box.set_margin_top(20)
        # child_box.set_margin_bottom(20)
        # child_box.set_margin_start(20)
        # child_box.set_margin_end(20)
        
        self.start_pauseButton(self.child_box, self.new_child)
        self.child_box.append(self.new_child_label)
       
                        
        # self.lapButton = Gtk.Button(label="lap")
        # self.lapButton.connect("clicked",lambda widget, sw = self.new_child:self.on_lap_clicked(widget,sw))
        # self.child_box.append(self.lapButton)
                
        self.box.append(self.child_box)
        print("yo")
        self.update_label()
        
    def update_label(self):
        for parent in self.projects:
            time_parent = parent.get_elapsed()
            parent_id = self.parent_labels[parent.id]
            parent_id.set_text(timeformat(time_parent))
            for child in parent.children:
                time_child = child.get_elapsed()
                id_child = self.children_labels[child.id]
                id_child.set_text(timeformat(time_child))
    
    
    def on_create_clicked(self, button):
        self.created_parent = self.createParent()
        
        self.created_parent_label = Gtk.Label(label="00:00:00")
        self.parent_labels[self.created_parent.id] = self.created_parent_label
        self.projects.append(self.created_parent)
        self.parent_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 5)
        self.parent_box.append(self.created_parent_label)
        self.box.append(self.parent_box)
        
        self.start_pauseButton(self.box, self.created_parent)
        
        self.lapButton = Gtk.Button(label="Lap")
        self.lapButton.connect("clicked",lambda widget, sw = self.created_parent:self.on_lap_clicked(widget,sw))
        self.box.append(self.lapButton)
                
        self.update_label()
        print("parent")
        
        
    def createParent(self):
            stopwatch = Stopwatch("New Project")
            return stopwatch
        
    #print("button was clicked")
    
    def start_pauseButton(self,position,sw):
        if sw.parent is not None:
            label_to_put = "Pause"
        else:
            label_to_put = "Start"
        self.startButton = Gtk.Button(label=label_to_put)
        self.startButton.connect("clicked",lambda widget, sw = sw:self.on_start_clicked(widget,sw))
        self.button_labels[sw.id] = self.startButton
        position.append(self.startButton)
        
    def create_page(name):
        page = Gtk.Box(orientation=Gtk.orientation.VERTICAL, spacing = 10)
        
        page.set_margin_top(20)
        page.set_margin_bottom(20)
        page.set_margin_start(20)
        page.set_margin_end(20)
        
        label = Gtk.Label(label=name)
        page.append(label)
        
        return page
        
app = MyApp()
app.run()

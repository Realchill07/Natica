import gi
import time
import uuid

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,GLib

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
       
def timeformat(total_seconds):
    total_seconds = int(total_seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.realchill07.stopwatch')
        self.stopwatch = Stopwatch("Inital Stopwatch")

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("Stopwatch")
        window.set_default_size(300, 200)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)

        self.label = Gtk.Label(label="00:00:00")
        box.append(self.label)

        self.button = Gtk.Button(label="Start")
        self.button.connect("clicked", self.on_button_clicked)
        box.append(self.button)

        window.set_child(box)
        window.present()
        
        GLib.timeout_add(1000, self.on_tick)
         
    def on_button_clicked(self, button):
        if self.stopwatch.running:
            self.stopwatch.pause()
            self.button.set_label("start")
        else:
            self.stopwatch.start()
            self.button.set_label("pause")
        self.update_label()
        
    def on_tick(self):
        self.update_label()
        return True
        
    def update_label(self):
        elapsed = self.stopwatch.get_elapsed()
        self.label.set_text(timeformat(elapsed))
        
    #print("button was clicked")

app = MyApp()
app.run()

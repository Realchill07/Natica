
import gi

gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')

from gi.repository import Gtk, Adw, Gio, Gdk


# Simple task model
class Task:
    def __init__(self, name):
        self.name = name


class App(Adw.Application):

    def __init__(self):
        super().__init__(
            application_id='com.horknee.testing'
        )

        self.connect("activate", self.on_activate)

        self.selected_task = None

    def on_activate(self, app):
        win = Adw.ApplicationWindow(application=self)
        win.set_default_size(400, 300)

        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )

        main_box.set_margin_top(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)

        # Example tasks
        tasks = [
            Task("Study DBMS"),
            Task("Work on Natica"),
            Task("Practice DSA")
        ]

        for task in tasks:

            # Create a row for each task
            row = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL
            )

            label = Gtk.Label(label=task.name)
            label.set_xalign(0)

            row.append(label)

            # Right-click gesture
            gesture = Gtk.GestureClick()
            gesture.set_button(3)

            gesture.connect(
                "pressed",
                self.on_right_click,
                task
            )

            row.add_controller(gesture)

            main_box.append(row)

        win.set_content(main_box)
        win.present()

    def on_right_click(
        self, gesture, n_press, x, y, task
    ):
        # Remember which task was clicked
        self.selected_task = task

        print("Right clicked:", task.name)

        menu = Gio.Menu()
        menu.append("Delete", "app.delete")
        menu.append("Edit", "app.edit")
        menu.append("Edit Tag", "app.edit_tag")

        # Create the context menu
        popup = Gtk.PopoverMenu.new_from_model(menu)

        # Attach to the widget that was right-clicked
        widget = gesture.get_widget()
        popup.set_parent(widget)

        rect = Gdk.Rectangle()
        rect.x = int(x)
        rect.y = int(y)
        rect.width = 1
        rect.height = 1

        popup.set_pointing_to(rect)

        # Clean up after closing
        popup.connect(
            "closed",
            lambda p: p.unparent()
        )

        popup.popup()

    def on_delete(self, action, param):
        task = self.selected_task

        if task:
            print("Delete:", task.name)

    def on_edit(self, action, param):
        task = self.selected_task

        if task:
            print("Edit:", task.name)

    def on_edit_tag(self, action, param):
        task = self.selected_task

        if task:
            print("Edit Tag:", task.name)


app = App()

# Register menu actions
for name, callback in [
    ("delete", app.on_delete),
    ("edit", app.on_edit),
    ("edit_tag", app.on_edit_tag)
]:
    action = Gio.SimpleAction.new(name, None)
    action.connect("activate", callback)
    app.add_action(action)

app.run(None)
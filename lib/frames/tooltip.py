import tkinter as tk

class ToolTip:

    """
    Object that stores a tkinter window that displays helpful information when an info button is pressed
    """

    def __init__(self):
        self.wraplength = 200

        # "definition" : tkinter widget
        self.widgets = {}
        self.active_widget = None
        self.active_text = "$"
        self.offset = {'x': 10, 'y': 10}
        self.is_visible = False
        self.top_level = None

    def add_widget(self, widget, text):
        self.widgets[text] = widget
        widget.bind("<ButtonPress>", self.show)
        self.top_level = None

    def leave(self, event=None):
        self.hide()
        self.is_visible = False
        self.active_widget = None

    def show(self, event):
        if self.is_visible:
            self.leave()
            if event.widget == self.active_widget:
                return

        self.active_widget = event.widget
        self.is_visible = True
        x = y = 0
        x, y, cx, cy = self.active_widget.bbox("insert")
        x += self.active_widget.winfo_rootx() + self.offset['x']
        y += self.active_widget.winfo_rooty() + self.offset['y']
        self.top_level = tk.Toplevel(self.active_widget)
        self.top_level.geometry(f"+{x}+{y}")
        self.top_level.overrideredirect(True)
        self.top_level.bind('<ButtonPress>', self.leave)
        self.get_definition()
        label = tk.Label(
            self.top_level, text=self.active_text, 
            bg="#5ce681", justify='left', relief='solid', borderwidth=1,
            wraplength = self.wraplength
        )
        label.pack(ipadx=5, ipady=5)

    def hide(self):
        if self.top_level:
            self.top_level.destroy()
        self.top_level = None

    def get_definition(self):
        for key, value in self.widgets.items():
            if value == self.active_widget:
                self.active_text = key
                break
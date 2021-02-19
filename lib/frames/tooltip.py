import tkinter as tk

class ToolTip:
    
    def __init__(self, widget=None, text=None):
        self.wraplength = 200   
        self.wait_time = 100
        self.widget = widget
        self.text = text

        self.offset = {'x': 10, 'y': 10}
        self.is_visible = False

        # Configure functions
        self.widget.bind("<ButtonPress>", self.enter)
        self.widget.bind("<Configure>", self.sync_position)

        self.top_level = None
        self.after_function = None

    def enter(self, event=None):
        self.reset_after_function()
        self.after_function = self.widget.after(self.wait_time, self.show)

    def leave(self, event=None):
        self.reset_after_function()
        self.hide()
        self.is_visible = False

    def reset_after_function(self):
        if self.after_function:
            self.widget.after_cancel(self.after_function)
        self.after_function = None

    def show(self):
        if self.is_visible:
            self.leave()
            return

        self.is_visible = True
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.offset['x']
        y += self.widget.winfo_rooty() + self.offset['y']
        self.top_level = tk.Toplevel(self.widget)
        self.top_level.geometry(f"+{x}+{y}")
        self.top_level.overrideredirect(True)
        self.top_level.bind('<ButtonPress>', self.leave)
        label = tk.Label(
            self.top_level, text=self.text, 
            bg="#5ce681", justify='left', relief='solid', borderwidth=1,
            wraplength = self.wraplength
        )
        label.pack(ipadx=5, ipady=5)

    def hide(self):
        if self.top_level:
            self.top_level.destroy()
        self.top_level = None

    def sync_position(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.offset['x']
        y += self.widget.winfo_rooty() + self.offset['y']
        print('configure')
        if self.top_level != None:
            print("configure top level ain't none")
            self.top_level.geometry(f"+{x}+{y}")
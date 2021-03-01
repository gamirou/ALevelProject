from ..utils.utils import *
import tkinter as tk

class PopUpConfirm(tk.Toplevel):

    def __init__(self, master=None, state=None, yes_command=None, additional_command=None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.parent = master
        self.state = state
        self.yes_command = yes_command
        self.additional_command = additional_command
        
        x = self.parent.parent.app.root.winfo_rootx() + self.parent.parent.app.root.winfo_width() / 2
        y = self.parent.parent.app.root.winfo_rooty() + self.parent.parent.app.root.winfo_height() / 2
        self.geometry(f"+{int(x)}+{int(y)}")

        tk.Label(self, font=self.parent.file_storage.fonts["x-small"], wraplength=300, text=POPUP_MESSAGES[self.state]).pack()
        
        if self.state == TRAIN:
            tk.Label(self, text="Enter the number of epochs:").pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
            self.epoch_variable = tk.StringVar()
            vcmd = (self.register(self.callback_entry_numbers))
            epoch_entry = tk.Entry(
                self, 
                text="5", 
                textvariable=self.epoch_variable, 
                validate='key', 
                validatecommand=(vcmd, '%d', '%P', '%S')
            )
            epoch_entry.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

        if self.state == CLOSE_WINDOW:
            tk.Button(self, text='Save', command=self.execute_if_yes, fg='red').pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
            tk.Button(self, text='Don\'t save', command=self.execute_additional).pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)            
            tk.Button(self, text='No, take me back!', command=self.destroy).pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        else:
            tk.Button(self, text='Yes', command=self.execute_if_yes, fg='red').pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
            tk.Button(self, text='No', command=self.destroy).pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)

    def execute_if_yes(self):
        self.destroy()
        if self.state == TRAIN:
            self.yes_command(epochs=int(self.epoch_variable.get()))
        else:
            self.yes_command()
    
    def execute_additional(self):
        self.destroy()
        self.additional_command(False)

    def callback_entry_numbers(self, action, value_if_allowed, text):
        return value_if_allowed.isdigit() or value_if_allowed == ""
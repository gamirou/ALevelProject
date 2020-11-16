import tkinter as tk

class PopUpConfirmQuit(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)
        tk.Label(self, text="Are you sure you want to quit").pack()
        tk.Button(self, text='Yes', command=master.destroy, fg='red').pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        tk.Button(self, text='No', command=self.destroy).pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)


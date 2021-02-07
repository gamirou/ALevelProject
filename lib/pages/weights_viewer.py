import tkinter as tk
import numpy as np

class WeightsViewer(tk.Toplevel):

    def __init__(self, master=None, weights=None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)

        tk.Label(self, text=weights, wraplength=400).pack()
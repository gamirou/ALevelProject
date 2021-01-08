import tkinter as tk
from tkinter import ttk
from ..utils.log import Log
from ..utils.utils import CONVOLUTIONAL, FULLY_CONNECTED

# Graph library
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class GraphWindow(tk.Toplevel):

    TAG = "GraphWindow"

    def __init__(self, master=None, weights_callback=None, cnf={}, **kw):
        super().__init__(master=master, cnf={}, **kw)
        self.parent = master
        self.callback = weights_callback

        self.figure = plt.Figure(figsize=(6,5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        
        self.parent.parent.app.graphs["model_accuracy"] = {
            "figure": self.figure,
            "animate": self.fetch_logs
        }

        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def fetch_logs(self):
        self.ax.clear()
        self.ax.set_yscale('log')
        self.ax.plot(self.callback.epochs, self.callback.metrics["accuracy"], label="acc")
        self.ax.plot(self.callback.epochs, self.callback.metrics["val_accuracy"], label="val_acc")
        self.ax.legend()
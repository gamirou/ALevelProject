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
import matplotlib.animation as animation

class GraphWindow(tk.Toplevel):

    TAG = "GraphWindow"

    def __init__(self, master=None, weights_callback=None, cnf={}, **kw):
        super().__init__(master=master, cnf={}, **kw)
        self.parent = master
        self.callback = weights_callback

        self.figure = plt.Figure(figsize=(6,5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        
        # self.parent.parent.app.graphs["model_accuracy"] = {
        #     "figure": self.figure,
        #     "animate": self.fetch_logs
        # }

        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.callback.set_bridge_function(self.draw_logs)

    def draw_logs(self, metrics, epochs):
        self.ax.clear()
        print(metrics.keys())
        self.ax.plot(epochs, metrics["accuracy"], label="accuracy")
        self.ax.plot(epochs, metrics["val_accuracy"], label="validation dataset accuracy")
        self.ax.plot(epochs, metrics["loss"], label="loss")
        self.ax.plot(epochs, metrics["val_loss"], label="validation dataset loss")
        self.ax.legend()
        # This is the right line, this updates the graph, however it is not called from tkinter thread
        # self.canvas.draw()
import tkinter as tk
from tkinter import ttk
from ..utils.utils import CONVOLUTIONAL, FULLY_CONNECTED

# Graph library
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class GraphWindow(tk.Toplevel):

    """
    Tkinter window that displays network metrics on a graph
    """

    def __init__(self, master=None, weights_callback=None, is_accuracy=True, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.parent = master
        self.callback = weights_callback
        self.is_accuracy = is_accuracy

        self.figure = plt.Figure(figsize=(6,5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)

        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.callback.set_draw_logs_function(self.draw_logs)

    def draw_logs(self, metrics, epochs):
        self.ax.clear()
        # print(metrics.keys())
        if self.is_accuracy:
            self.ax.plot(epochs, metrics["accuracy"], label="accuracy")
            self.ax.plot(epochs, metrics["val_accuracy"], label="validation dataset accuracy")
        else:
            self.ax.plot(epochs, metrics["loss"], label="loss")
            self.ax.plot(epochs, metrics["val_loss"], label="validation dataset loss")

        self.ax.legend()
        # This is the right line, this updates the graph, however it is not called from tkinter thread
        # self.canvas.draw()
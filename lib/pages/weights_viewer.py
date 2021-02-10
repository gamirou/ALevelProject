import tkinter as tk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from ..utils.utils import WEIGHTS, BIASES

class WeightsViewer(tk.Toplevel):

    def __init__(self, master=None, weights=None, state=WEIGHTS, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        
        self.state = state
        self.weights = np.copy(weights)
        self.ax = []
        self.figure = plt.Figure(figsize=(6,5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self)

        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        print(self.weights)
        print(np.shape(self.weights))
        for i in self.weights:
            print(i)
        if self.state == WEIGHTS:
            pass
        else:
            pass
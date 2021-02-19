import tkinter as tk
from tkinter import ttk
from ..page import Page
from ..utils.utils import ARROW_WIDTH_IMAGE, ARROW_HEIGHT_IMAGE

class DictionaryPage(Page):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        
        # Main frame
        self.canvas_frame = tk.Frame(self, bg="#fff")
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Canvas
        canvas = tk.Canvas(self.canvas_frame, bg="#fff")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure scrollbar to canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        # Frame that holds everything inside canvas
        self.inside_frame = tk.Frame(canvas, bg="#fff", width=600, height=600)
        canvas.create_window((0,0), window=self.inside_frame, anchor=tk.NW)
        
        # Load the data
        self.data = self.parent.file_storage.dictionary_data
        fonts = self.parent.file_storage.fonts

        # Display the data
        for i in range(len(self.data)):
            label_term = tk.Label(
                self.inside_frame, text=self.data[i]['term'], bg='#fff', font=fonts['bold small']
            )
            text_definition = tk.Text(
                self.inside_frame, bg='#fff', font=fonts['small'], relief='flat',
                width=35, height=5, wrap=tk.WORD
            )
            text_definition.insert(tk.INSERT, self.data[i]['definition'])
            text_definition.configure(state='disabled')

            label_term.grid(row=i, column=0, padx=20, pady=20, sticky=tk.W)
            text_definition.grid(row=i, column=1, pady=5, sticky=tk.W)

        # Back page
        self.arrow_left = tk.Button(
            self.inside_frame, text="Back", image=self.parent.file_storage["arrow_left.png"], 
            width=ARROW_WIDTH_IMAGE, height=ARROW_HEIGHT_IMAGE, command=self.parent.back_page
        )
        self.arrow_left.grid(row=i+1, column=0, sticky=tk.W)

        # 1:9 term:definition
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=9)
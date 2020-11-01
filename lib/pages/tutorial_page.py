import tkinter as tk
from ..page import Page
from ..utils.log import Log
from ..utils.utils import *
import os, json

class TutorialPage(Page):

    TAG = "TutorialPage"
    tutorial_data = []
    pages = []
    current_index = 0;
    arrows = {}

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.load_tutorial_info()
        self.initialise_pages()
        self.show_page(self.current_index)

    def load_tutorial_info(self):
        # script_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) #<-- absolute dir the script is in
        # rel_path = "assets\\tutorial.json"
        # abs_file_path = os.path.join(script_dir, rel_path)
        
        abs_file_path = get_main_path("assets", "tutorial.json")

        with open(abs_file_path) as json_file:
            data = json.load(json_file)
            self.tutorial_data = data

    def initialise_pages(self):
        self.container = tk.Frame(self, bg="#ff0000", width=120, height=120)
        self.container.pack(side="top", fill="both", expand=False)

        for i in range(len(self.tutorial_data)):
            page = Page(self)
            data = self.tutorial_data[i]

            for j in range(len(data["headers"])):
                tk.Label(page, text=data["headers"][j]).grid(row=0, column=j)
                tk.Label(page, text=data["text"][j]).grid(row=1, column=j)

            # Add rest of text
            self.pages.append(page)
        
        self.arrows["left"] = tk.Button(
            self, text="Back", image=self.parent.file_storage["arrow_left.png"], width=ARROW_WIDTH_IMAGE, 
            height=ARROW_HEIGHT_IMAGE, command=lambda index=-1: self.change_page(index)
        )
        self.arrows["right"] = tk.Button(
            self, text="Create New Network", image=self.parent.file_storage["arrow_right.png"], width=ARROW_WIDTH_IMAGE, 
            height=ARROW_HEIGHT_IMAGE, command=lambda index=1: self.change_page(index)
        )

        self.arrows["left"].pack(side="bottom")
        self.arrows["right"].pack(side="bottom")
            
    def show_page(self, index):
        self.current_index = index
        self.pages[self.current_index].place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.pages[self.current_index].show()

    def change_page(self, where):
        # Where can be 1 or -1
        new_index = self.current_index + where
        if new_index == -1:
            self.parent.back_page()
        elif new_index == len(self.pages):
            self.parent.update_page("NewNeuralPage")
        else:
            # If you go back, change the button back to arrow
            if self.arrows["right"].cget('image') == '':
                self.arrows["right"].config(
                    image=self.parent.file_storage["arrow_right.png"], 
                    width=ARROW_WIDTH_IMAGE, height=ARROW_HEIGHT_IMAGE
                )
            self.show_page(new_index)

        # Get rid of arrow because we will go to neural network page
        if new_index == len(self.pages) - 1:
            self.arrows["right"].config(image='', width=ARROW_WIDTH_CHARS, height=ARROW_HEIGHT_CHARS)
        
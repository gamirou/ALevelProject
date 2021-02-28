import tkinter as tk
from tkinter import scrolledtext as st
from ..page import Page
from ..utils.log import Log
from ..utils.utils import *
import os, json

class TutorialPage(Page):

    TAG = "TutorialPage"
    tutorial_data = []
    pages = []
    current_index = 0
    arrows = {}

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.file_storage = self.parent.file_storage
        self.tutorial_data = self.file_storage.tutorial_data
        self.initialise_pages()
        self.show_page(self.current_index)

    def initialise_pages(self):
        self.container = tk.Frame(self, bg="#fff")
        self.container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        image_index = 1

        for i in range(len(self.tutorial_data)):
            page = Page(self, bg="#fff")
            data = self.tutorial_data[i]

            for j in range(len(data["headers"])):
                side = tk.LEFT if j == 0 else tk.RIGHT
                frame = tk.Frame(page, bg="#fff")
                title = tk.Label(frame, bg="#fff", text=data["headers"][j], wraplength=300, font=self.file_storage.fonts["bold medium"])
                content = st.ScrolledText(frame, bg="#fff", width=INITIAL_SCROLLED_TEXT_WIDTH, height=10, wrap=tk.WORD, font=self.file_storage.fonts["small"])
                # content.insert(tk.INSERT, data['text'][j])
                # text.image_create(tk.END, image = img) # Example 1
                
                paragraphs = data['text'][j].split('<image>')
                for k in range(len(paragraphs)):
                    content.insert(tk.END, paragraphs[k])
                    if k != len(paragraphs) - 1:
                        content.image_create(tk.END, image=self.file_storage[f'tutorial_{image_index}.jpg'])
                        image_index += 1

                content.configure(state='disabled')
                
                # print(find_all_occurences(data['text'][j], '<image>'))

                # ScrollableText(frame, bg="#ff0000", label_cnf=label_cnf)
                # self.parent.widgets_bind_stack.append(content)
        
                # pack them
                title.pack(side=tk.TOP)
                content.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True) 
                frame.pack(side=side, anchor=tk.N, fill=tk.BOTH, expand=True)

                # add to app wrapping list
                self.parent.app.wrapping_widgets.append([content, True])

            # Add rest of text
            self.pages.append(page)
        
        self.footer = tk.Frame(self, bg="#fff")
        self.arrows["left"] = tk.Button(
            self.footer, text="Back", image=self.file_storage["arrow_left.png"], 
            width=ARROW_WIDTH_IMAGE,
            height=ARROW_HEIGHT_IMAGE, command=lambda index=-1: self.change_page(index)
        )
        self.arrows["right"] = tk.Button(
            self.footer, text="Create New Network", image=self.file_storage["arrow_right.png"], 
            width=ARROW_WIDTH_IMAGE,
            height=ARROW_HEIGHT_IMAGE, command=lambda index=1: self.change_page(index)
        )

        self.footer.pack(side=tk.BOTTOM, fill=tk.BOTH, pady=(20, 0))
        self.arrows["left"].pack(side=tk.LEFT)
        self.arrows["right"].pack(side=tk.RIGHT)
            
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
        
import tkinter as tk
from ..page import Page
from .tutorial_page import TutorialPage

class MainMenu(Page):

    TAG = "MainMenu"
    # [tk.Button(), index in MainView pages list]
    buttons = {
        "How to Use": [None, "TutorialPage"],
        "New Neural Network": [None, "NewNeuralPage"],
        "Load Neural Network": [None, "LoadingPage"],
        "What do these complicated words mean?": [None, "DictionaryPage"],
        "Settings": [None, "SettingsPage"],
        "Quit": [None, 0] 
    }

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        fonts = self.parent.file_storage.fonts        
        app_title = "Image Classification for all"
        label = tk.Label(self, text=app_title, bg="#fff", font=fonts["bold large"])
        label.pack(expand=True)
        
        index = 1
        for key in self.buttons:
            # Add buttons to dictionary
            self.buttons[key][0] = tk.Button(
                self, text=key, bg='#fff', fg='#5e0800', 
                relief='flat', font=fonts["medium"]
            )
            self.buttons[key][0].configure(
                command=lambda page_name=self.buttons[key][1]: self.on_click(page_name, self.open_page)
            )
            self.buttons[key][0].pack(expand=True)
            #self.buttons[key][0].grid(row=index, column=0)
            index += 1

    def on_click(self, page_name, function):
        function(page_name)

    def open_page(self, page_name):
        self.parent.update_page(page_name)
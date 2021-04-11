import tkinter as tk
from ..page import Page
from .tutorial_page import TutorialPage

class MainMenu(Page):

    # [tk.Button(), index in MainView pages list]
    buttons = {
        "How to Use": [None, "TutorialPage"],
        "New Neural Network": [None, "NewNeuralPage"],
        "Load Neural Network": [None, "LoadingPage"],
        "What do these complicated words mean?": [None, "DictionaryPage"],
        "Quit": [None, 0] 
    }

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        fonts = self.parent.file_storage.fonts        
        app_title = self.parent.app.title
        label = tk.Label(self, text=app_title, bg="#fff", font=fonts["bold large"])
        label.pack(expand=True)
        
        index = 1
        for key in self.buttons:
            # Add buttons to dictionary
            self.buttons[key][0] = tk.Button(
                self, text=key, bg='#fff', fg='#5e0800', 
                relief='flat', font=fonts["medium"], wraplength=400,
                command=lambda page_name=self.buttons[key][1]: self.parent.update_page(page_name)
            )
            self.buttons[key][0].pack(expand=True)
            index += 1
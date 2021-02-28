import tkinter as tk
from .pages.main_menu import MainMenu
from .pages.tutorial_page import TutorialPage
from .pages.new_neural_page import NewNeuralPage
from .pages.neural_main_page import NeuralMainPage
from .pages.loading_page import LoadingPage
from .pages.neural_edit_page import NeuralEditPage
from .pages.dictionary_page import DictionaryPage

class MainView(tk.Frame):

    current_id = "MainMenu"
    page_stack = []
    pages = {}

    def __init__(self, master, app, file_storage, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.app = app
        self.parent = master
        self.file_storage = file_storage
        self.load_pages()
        self.update_page(self.current_id)

    def load_pages(self):
        self.add_page(MainMenu(self, bg="#fff"))
        self.add_page(TutorialPage(self, bg="#fff"))
        self.add_page(NewNeuralPage(self, bg="#fff"))
        self.add_page(NeuralMainPage(self, bg="#fff"))
        self.add_page(LoadingPage(self, bg="#fff"))
        self.add_page(NeuralEditPage(self, bg="#fff"))
        self.add_page(DictionaryPage(self, bg="#fff"))

    def add_page(self, instance):
        self.pages[instance.__class__.__name__] = instance

    def update_page(self, new_id=None):
        if new_id == 0:
            self.parent.destroy()
            return 
            
        if new_id != None:
            self.current_id = new_id
            self.page_stack.append(new_id)
        else:
            self.current_id = self.page_stack[-1]

        # self.pages[self.current_id].place({
        #     "in_": self,
        #     "x": 0,
        #     "y": 0,
        #     "relwidth": 1,
        #     "relheight": 1
        # })
        self.pages[self.current_id].place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        self.pages[self.current_id].show()
        if self.app.active_tooltip.active_widget != None:
            self.app.active_tooltip.leave()

    def back_page(self):
        self.page_stack.pop()
        if len(self.page_stack) == 0:
            self.app.is_running = False
            self.parent.destroy()
            return

        self.update_page()

    # Only happens when NeuralMainPage is the main page
    def go_to_neural_page(self, neural_id):
        self.page_stack = ["MainMenu", "NeuralMainPage"]
        self.update_page()

        network = self.file_storage.get_network(neural_id)
        self.pages[self.current_id].fetch_network(network)

    def add_network(self, neural_id):
        self.file_storage.add_network(neural_id)
        self.pages["LoadingPage"].add_frame(neural_id)
    
    def start_progress_bar(self, mode, text=None, is_sub_text=None, epochs=1):
        self.app.progress_footer.start(mode, text, is_sub_text, epochs)

    def stop_progress_bar(self):
        self.app.progress_footer.is_finished = True

    def send_data_to_progress_bar(self, value):
        self.app.progress_footer.update_values(value)

    def notify(self, text):
        self.app.notification_header.show(text)
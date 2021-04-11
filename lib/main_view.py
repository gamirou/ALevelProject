import tkinter as tk
from .pages.main_menu import MainMenu
from .pages.tutorial_page import TutorialPage
from .pages.new_neural_page import NewNeuralPage
from .pages.neural_main_page import NeuralMainPage
from .pages.loading_page import LoadingPage
from .pages.neural_edit_page import NeuralEditPage
from .pages.dictionary_page import DictionaryPage

class MainView(tk.Frame):

    """
    Tkinter frame that stores a list of pages (subclasses of tkinter Frames)
    It decides which page is active and hides every other page
    """

    # The id of the page shown pm the scree
    current_id = "MainMenu"

    # Stack that stores the order of the pages shown
    # current_id is the head of the stack
    page_stack = []

    # Dictionary that stores the pages
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

    # This function allows the page to be stored in the dictionary by the name of their class
    def add_page(self, instance):
        self.pages[instance.__class__.__name__] = instance

    def update_page(self, new_id=None):
        # new_id is 0 when the QUIT button is pressed
        if new_id == 0:
            self.app.close_window()
            return 
        
        # If new_id is specified, push it onto the stack
        if new_id != None:
            self.current_id = new_id
            self.page_stack.append(new_id)
        # Else the stack might have lost an id, so current_id is updated
        else:
            self.current_id = self.page_stack[-1]

        # Place the active page on the screen
        self.pages[self.current_id].place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        self.pages[self.current_id].show()

        # The page might have changed, which means the tooltip should disappear as well
        if self.app.active_tooltip.active_widget != None:
            self.app.active_tooltip.leave()

    # BACK button is pressed, pop the stack
    def back_page(self):
        self.page_stack.pop()
        if len(self.page_stack) == 0:
            self.app.is_running = False
            return

        self.update_page()

    # Only happens when NeuralMainPage is the main page
    def go_to_neural_page(self, neural_id):
        self.page_stack = ["MainMenu", "NeuralMainPage"]
        self.update_page()

        network = self.file_storage.get_network(neural_id)
        self.pages[self.current_id].fetch_network(network)

    # Intermediate function that connects FileStorage with the LoadingPage
    def add_network(self, neural_id):
        self.file_storage.add_network(neural_id)
        self.pages["LoadingPage"].add_frame(neural_id)
    
    # The rest are intermediate functions that connect the app with the respective page
    def start_progress_bar(self, mode, text=None, is_sub_text=None, epochs=1):
        self.app.progress_footer.start(mode, text, is_sub_text, epochs)

    def stop_progress_bar(self):
        self.app.progress_footer.is_finished = True

    def send_data_to_progress_bar(self, value):
        self.app.progress_footer.update_values(value)

    def notify(self, text):
        self.app.notification_header.show(text)
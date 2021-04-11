from .utils.utils import *
from .neural.network import Network
from .neural.dataset import Dataset
import os
import json
import shutil
from tkinter.font import Font
from tensorflow import get_default_graph, Session
from keras.models import model_from_json
from keras import backend as K

class FileStorage:

    """
    Object that deals with external files such as:
    * images inside images folder
    * json files that stores the widgets structure of some pages
    * json files that store a glossary and tutorial data
    * saved (networks) ->
        * uuid ->
            * model.h5 (keras model that stores the weights and architecture)
            * model_info.txt (small text file that stores the name and description)
            * model_metrics.json (stores accuracy and loss values at each epoch)
            * weights -> folder that stores numpy files of weights
    """

    cache = {}
    saved_networks = {}
    widgets = {}

    def __init__(self, app):
        self.app = app

        # Absolute path of the application
        self.path = os.path.dirname(os.path.dirname(__file__))

        # Object that loads training data
        self.dataset = Dataset(os.path.join(self.path, "dataset"))
        
        # Tensorflow specific variables
        self.graph = get_default_graph()
        self.session = Session()
        K.set_session(self.session)

        # Load all files
        self.load_all_images()
        self.load_all_widgets()
        self.load_all_networks()
        self.load_font()
        self.load_tutorial_info()
        self.load_dictionary()

    def load_all_networks(self):
        # r=root, d=directories, f = files
        for root, directory, files in os.walk(self.path + "\\saved"):
            # if directory name is not empty
            if len(directory) != 0:
                for uuid in directory:
                    # only load up folders which are not 'weights'
                    if uuid in ["weights"]:
                        continue
                    self.saved_networks[uuid] = Network(uuid, os.path.join(root, uuid), self.graph, self.session)
        
    # Add a networks to the list
    def add_network(self, neural_id):
        self.saved_networks[neural_id] = Network(neural_id, os.path.join(self.path + "\\saved", neural_id), self.graph, self.session)

    # Retrieve network so saved_networks remains private
    def get_network(self, neural_id):
        return self.saved_networks[neural_id]

    # Function that saves a network in a folder
    def save_network(self, network):
        # Path and name of folder
        neural_id = network.network_id
        neural_id_path = self.path + "\\saved\\" + neural_id
        
        # Store metrics as json
        json_data = {
            "metrics": network.callback.metrics,
            "epochs": network.callback.epochs
        }
       
        # Make each number a string
        stringified_json = json.loads(json.dumps(json_data), parse_int=str, parse_float=str)
        with open(os.path.join(neural_id_path, "model_metrics.json"), "w") as json_file:
            json.dump(stringified_json, json_file)

        # Edit text file
        txt = ""
        with open(os.path.join(neural_id_path, "model_info.txt"), "r") as txt_file:
            txt = txt_file.readlines()
        
        # Replace training flag in order to allow/block certain features to be used
        try:
            index_false = txt[1].index("False")
            substring = "False" if index_false != -1 else "True"       
        except ValueError:
            index_false = txt[1].index("True")
            substring = "True" if index_false != -1 else "False"

        txt[1] = txt[1].replace(substring, str(network.is_trained))

        # Replace date edited
        index_date = len(txt[1]) - txt[1][::-1].index('*')
        substring = txt[1][index_date:len(txt[1])]
        txt[1] = txt[1].replace(substring, today())
        with open(os.path.join(neural_id_path, "model_info.txt"), "w") as txt_file:
            txt_file.writelines(txt)

        # serialize weights to HDF5
        network.model.save(os.path.join(neural_id_path, "model.h5"))
        self.app.notification_header.show(f"The network has been saved")

    # Delete a folder
    def delete_network(self, network_id, loading_page):
        try:
            # This file deletes the whole folder
            shutil.rmtree(os.path.join(self.path, "saved", network_id))
            self.app.notification_header.show(f"The network has been deleted")
        
            # Removes network from loading page
            loading_page[network_id].grid_forget()
            loading_page.index -= 1

            # Removes network from the list
            self.saved_networks.pop(network_id)
        except OSError as err:
            self.app.notification_header.show("Network cannot be deleted. Try again!")

    # Loads images and saves them in a cache
    def load_all_images(self):
        files = []
        # Get the names of each file
        for (dirpath, dirnames, filenames) in os.walk(self.path + "\\images"):
            files.extend(filenames)
            break
        
        for file_name in files:
            # Stores the image as a PIL object to be used by tkinter
            photo = get_image_from_folder(file_name)
            self.cache[file_name] = photo

    # Loads JSON files that store widget structure
    def load_all_widgets(self):
        files = []
        widgets_path = os.path.join(self.path, "assets", "widgets")
        for (dirpath, dirnames, filenames) in os.walk(widgets_path):
            files.extend(filenames)
            break
        
        for file_name in files:
            # neural_main_page -> NeuralMainPage
            key = turn_to_camel_case(file_name.replace('.json', ''))
            with open(os.path.join(widgets_path, file_name), 'r') as json_file:
                self.widgets[key] = json.load(json_file)

    # Initialise a font dictionary
    def load_font(self):
        family = "Helvetica"
        self.fonts = {
            "x-small": Font(family=family, size=10),
            "small": Font(family=family, size=14),
            "medium": Font(family=family, size=24),    
            "large": Font(family=family, size=32),
            "x-large": Font(family=family, size=48),

            "bold x-small": Font(family=family, size=10, weight="bold"),
            "bold small": Font(family=family, size=14, weight="bold"),
            "bold medium": Font(family=family, size=24, weight="bold"),
            "bold large": Font(family=family, size=32, weight="bold"),
            "bold x-large": Font(family=family, size=48, weight="bold")
        }

    # Loads JSON file that stores all of the information in the tutorial page 
    def load_tutorial_info(self):
        abs_file_path = get_main_path("assets", "tutorial.json")

        with open(abs_file_path) as json_file:
            data = json.load(json_file)
            self.tutorial_data = data

    # Loads JSON file that stores all of the information in the dictionary page    
    def load_dictionary(self):
        abs_file_path = get_main_path("assets", "dictionary.json")

        with open(abs_file_path) as json_file:
            data = json.load(json_file)
            self.dictionary_data = data

    # Returns definition of term from dictionary json file
    def get_definition_by_term(self, term):
        for data in self.dictionary_data:
            if data['term'] == term:
                return data['definition']

    ### These functions allow the object to be used as a dictionary to access self.cache ###
    def __setitem__(self, key, item):
        self.cache[key] = item

    def __getitem__(self, key):
        return self.cache[key]

    def __repr__(self):
        return repr(self.cache)

    def __len__(self):
        return len(self.cache)

    def __delitem__(self, key):
        del self.cache[key]

    def clear(self):
        return self.cache.clear()

    def copy(self):
        return self.cache.copy()

    def has_key(self, k):
        return k in self.cache

    def update(self, *args, **kwargs):
        return self.cache.update(*args, **kwargs)

    def keys(self):
        return self.cache.keys()

    def values(self):
        return self.cache.values()

    def items(self):
        return self.cache.items()

    def pop(self, *args):
        return self.cache.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.cache, dict_)

    def __contains__(self, item):
        return item in self.cache

    def __iter__(self):
        return iter(self.cache)

    def __unicode__(self):
        return unicode(repr(self.cache))
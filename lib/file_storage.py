from .utils.utils import *
from .utils.log import Log
from .neural.network import Network
from .neural.dataset import Dataset
import os
import json
import shutil
from tkinter.font import Font

from tensorflow import get_default_graph, Session
from keras.models import model_from_json
from keras import backend as K
import warnings
warnings.filterwarnings("ignore")

class FileStorage:

    TAG = "FileStorage"
    cache = {}
    saved_networks = {}
    widgets = {}

    def __init__(self, app):
        self.app = app
        self.is_loading = True

        self.path = os.path.dirname(os.path.dirname(__file__))
        self.dataset = Dataset(self, os.path.join(self.path, "dataset"))
        
        self.graph = get_default_graph()
        self.session = Session()
        K.set_session(self.session)

        self.load_all_images()
        self.load_all_widgets()
        self.load_all_networks()
        self.load_font()

    def load_all_networks(self):
        # r=root, d=directories, f = files
        for root, directory, files in os.walk(self.path + "\\saved"):
            if len(directory) != 0:
                for uuid in directory:
                    self.saved_networks[uuid] = Network(uuid, os.path.join(root, uuid), self.graph, self.session)
        
    def add_network(self, neural_id):
        self.saved_networks[neural_id] = Network(neural_id, os.path.join(self.path + "\\saved", neural_id), self.graph, self.session)

    def get_network(self, neural_id):
        return self.saved_networks[neural_id]

    def save_network(self, network):    
        neural_id = network.network_id
        neural_id_path = self.path + "\\saved\\" + neural_id
        json_data = {
            "metrics": network.callback.metrics,
            "epochs": network.callback.epochs
        }
       
        stringified_json = json.loads(json.dumps(json_data), parse_int=str, parse_float=str)
        with open(os.path.join(neural_id_path, "model_metrics.json"), "w") as json_file:
            json.dump(stringified_json, json_file)

        txt = ""
        with open(os.path.join(neural_id_path, "model_info.txt"), "r") as txt_file:
            txt = txt_file.readlines()
        
        # TODO: Fix this
        index_false = txt[1].index("False")
        substring = "False" if index_false != -1 else "True"       
        txt[1].replace(substring, str(network.is_trained))
        with open(os.path.join(neural_id_path, "model_info.txt"), "w") as txt_file:
            txt_file.writelines(txt)

        # serialize weights to HDF5
        network.model.save(os.path.join(neural_id_path, "model.h5"))

    def delete_network(self, network_id, loading_page):
        try:
            shutil.rmtree(os.path.join(self.path, "saved", network_id))
            Log.i(self.TAG, f"Network {network_id} has been deleted")
        
            loading_page[network_id].grid_forget()
            loading_page.index -= 1
            self.saved_networks.pop(network_id)
        except OSError as err:
            Log.e(self.TAG, "Network cannot be deleted", err)

    def load_all_images(self):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(self.path + "\\images"):
            files.extend(filenames)
            break
        
        for file_name in files:
            photo = get_image_from_folder(file_name)
            self.cache[file_name] = photo

    def load_all_widgets(self):
        files = []
        widgets_path = os.path.join(self.path, "assets", "widgets")
        for (dirpath, dirnames, filenames) in os.walk(widgets_path):
            files.extend(filenames)
            break
        
        for file_name in files:
            key = turn_to_camel_case(file_name.replace('.json', ''))
            with open(os.path.join(widgets_path, file_name), 'r') as json_file:
                self.widgets[key] = json.load(json_file)

    def load_font(self):
        ### change to font inside assets later
        family = "Helvetica"
        self.fonts = {
            "small": Font(family=family, size=16),
            "medium": Font(family=family, size=32),
            "large": Font(family=family, size=48)
        }

    ### FOR IMAGES ###
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
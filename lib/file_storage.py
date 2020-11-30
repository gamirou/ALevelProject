from .utils.utils import *
from .utils.log import Log
from .neural.network import Network
from .dataset import Dataset
import os

from keras.models import model_from_json

class FileStorage:

    TAG = "FileStorage"
    cache = {}
    saved_networks = {}

    def __init__(self, app):
        self.app = app

        self.path = os.path.dirname(os.path.dirname(__file__))
        self.dataset = Dataset(self, os.path.join(self.path, "dataset"))

        self.load_all_images()
        self.load_all_networks()

    def start_progress(self):
        self.app.progress.start()

    def stop_progress(self):
        self.app.progress.stop()
        print("stop progress")
        self.app.progress.pack_forget()
        self.app.init_main_view()

    def load_all_networks(self):
        # r=root, d=directories, f = files
        for root, directory, files in os.walk(self.path + "\\saved"):
            if len(directory) != 0:
                for uuid in directory:
                    self.saved_networks[uuid] = Network(uuid, os.path.join(root, uuid))
        
    def add_network(self, neural_id):
        self.saved_networks[neural_id] = Network(neural_id, os.path.join(self.path + "\\saved", neural_id))

    def get_network(self, neural_id):
        return self.saved_networks[neural_id]

    def save_network(self, network):    
        neural_id = network.network_id
        neural_id_path = self.path + "\\saved\\" + neural_id
        model_json = network.model.to_json()
        with open(os.path.join(neural_id_path, "model_json"), "w") as json_file:
            json_file.write(model_json)

        # serialize weights to HDF5
        network.model.save(os.path.join(neural_id_path, "model.h5"))

    def load_all_images(self):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(self.path + "\\images"):
            files.extend(filenames)
            break
        
        for file_name in files:
            photo = get_image_from_folder(file_name)
            self.cache[file_name] = photo

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
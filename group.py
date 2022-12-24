import os
import os.path
from datetime import datetime
class Group:
    def __init__(self):
        self.path = os.walk("models")
        self.model_files = []
        self.init_files()
        self.limit = 50
    def init_files(self):
        for root, directories, files in self.path:
            self.model_files = files
    def file_saved(self,ticker):
        self.init_files()
        if (f"{ticker}.json" in self.model_files) and (f"{ticker}.h5" in self.model_files):
            return True
        else:
            return False
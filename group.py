import os
import os.path
from datetime import datetime
class Group:
    def __init__(self):
        self.path = os.walk("models")
        self.model_files = []
        self.init_files()
        self.limit = 50

    # Assigning values

    def init_files(self):
        for root, directories, files in self.path:
            self.model_files = files
    def file_saved(self,ticker):
        self.init_files()
        if (f"{ticker}.json" in self.model_files) and (f"{ticker}.h5" in self.model_files):
            return True
        else:
            return False

        # Saving Models

    def group(self,ticker):
            self.init_files()
            if self.file_saved(ticker):
                path = os.path.join(os.getcwd(), "models",f"{ticker}.json")
                tme = os.path.getctime(path)
                file_tm = datetime.fromtimestamp(tme)
                dt_tm = datetime.now()
                if (dt_tm - file_tm).days > 1:
                    os.remove(os.path.join(os.getcwd(), "models", f"{ticker}.json"))
                    os.remove(os.path.join(os.getcwd(), "models", f"{ticker}.h5"))
                    return False
                else:
                    return True
            else:
                if len(self.model_files) < self.limit:
                    pass
                else:
                    self.remove_files()
                return False
import json


class ConfReader:
    def __init__(self, path):
        super().__init__()
        self.path = path

    def get_conf_as_dict(self):
        path = self.path
        with open(path, 'r') as conf_file:
            conf_dict = json.loads(conf_file.read())
        return conf_dict
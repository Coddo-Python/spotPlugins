class Storage:

    def __init__(self):
        self.pl = []
        self.vars = {}

    def register_pl(self, plugin_name):
        self.pl.append(plugin_name)
        self.vars[plugin_name] = {}

    def set(self, plugin_name, **kwargs):
        for key, value in kwargs.items():
            self.vars[plugin_name][key] = value

    def get(self, plugin_name, *args):
        return [self.vars[plugin_name][key] for key in args]

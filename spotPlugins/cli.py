import argparse
import os
import sys
import importlib
import multiprocessing

sys.path.insert(0, os.path.realpath(__file__)[:-6])

import inject

from storage import Storage


class ConsoleEntryPoint:

    def __init__(self):
        parser = argparse.ArgumentParser(description='TODO: Put description')

        parser.add_argument('verbose',
                            metavar='-v',
                            type=bool,
                            default=False,
                            help='To enable Verbose (Debug)')

        self.args = parser.parse_args()


class ImportSetup:

    def __init__(self, verbose=None, pluginloader=None, dual_boot=False, plugindir=None, storage=None, **kwargs):
        self.__dict__.update(kwargs)
        self.verbose = verbose
        if storage is None:
            self.storage = Storage()
        else:
            self.storage = storage()

        # TODO: Dual booting will be when the importer uses two (more than this would be unstable) pluginloaders at once
        # The plugin loaders (default and external) will both interact and choose which function/code to follow if not
        # both at once. On each step of the load process, extra load steps will automatically be loaded.
        self.dual_boot = dual_boot

        if pluginloader is not None:
            if type(pluginloader) == str:
                importlib.import_module(pluginloader).setup()
            else:
                pluginloader.load_plugins(verbose=verbose, plugindir=plugindir)
        else:
            self.import_plugins(plugindir)

    def import_plugins(self, pldir):
        if pldir is None:
            pldir = "./plugins"
        sys.path.insert(0, pldir)
        directory = os.fsencode(pldir)
        # fancy one liner which contains a list of all imported plugins, removed due to complexity (may be hard to
        # understand)
        # self.plugins = list(filter(('').__ne__, [ importlib.import_module(os.fsdecode(file)[:-3]) if
        # os.fsdecode(file).endswith('.py') else '' for file in os.listdir(directory)]))
        self.plugins = []
        for file in os.listdir(directory):
            if os.fsdecode(file).endswith('py'):
                self.storage.register_pl(os.fsdecode(file)[:-3])
                self.plugins.append(importlib.import_module(os.fsdecode(file)[:-3]))
                self.plugins = list(filter(('').__ne__, self.plugins))
        self.process_plugins()

    def process_plugins(self):
        def sort_by_priority(elem):
            print(elem[1])
            return elem[1]

        self.startdata = []
        for plugin in self.plugins:
            data = plugin.getstartdata()
            self.startdata.append((plugin, data["priority"], data["type"], data["startmethod"]))
        self.startdata.sort(key=sort_by_priority)
        print(self.startdata)
        self.load_plugins()

    def load_plugins(self):
        self.procs = []
        for plugin in self.startdata:
            if plugin[2] == "inject":
                continue
            elif plugin[2] == "background":
                self.procs.insert(len(self.procs), multiprocessing.Process(target=plugin[3]()))
            elif plugin[2] == "events":
                continue
        print("Done!")


if __name__ == "__main__":
    pass
    # TODO: CLI
else:
    pass

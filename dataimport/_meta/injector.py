import importlib.abc
import importlib.machinery
import importlib.util
import types

import csv
def csvloader(filename):
    with open(filename, "r", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            yield row

import json
def jsonloader(filename):
    with open(filename, "r") as jsonfile:
        return json.load(jsonfile)

class DataLoader():
    '''
        Need to define a __path__ so that the following code chunk from
        cpython does not throw a keyerror in _find_and_load_unlocked

        if name in sys.modules:
            return sys.modules[name]
        parent_module = sys.modules[parent]
        try:
            path = parent_module.__path__
        except AttributeError:
            msg = (_ERR_MSG + '; {!r} is not a package').format(name, parent)
            raise ModuleNotFoundError(msg, name=name) from None
    '''
    __path__ = 'dataloader'
    data_loaders = {} # Define this so that we don't infinitely recurse on setattr/getattr

    def __init__(self, data, *args, **kwargs):
        self.data_loaders = {
            'csv': csvloader,
            'json': jsonloader,
        }
        self.data = data
        super().__init__(*args, **kwargs)

    def register(self, name, loader):
        self.data_loaders[name] = loader

    def __getattr__(self, attr_name):
        if attr_name in self.data_loaders:
            return self.data_loaders[attr_name](self.data)
        return super().__getattr__(attr_name)

    '''
    This is to allow imports like the following to work

    import dataimport.test.csv


    This is a chunk of source from cpython in _find_and_load_unlocked that would otherwise break our package

    if parent:
      # Set the module as an attribute on its parent.
      parent_module = sys.modules[parent]
      child = name.rpartition('.')[2]
      try:
          setattr(parent_module, child, module)
      except AttributeError:
          msg = f"Cannot set an attribute on {parent!r} for child module {child!r}"
          _warnings.warn(msg, ImportWarning)

    Without throwing away setattr calls to our loaders, this would attach a 'csv'
    attribute, cutting off access to the csv loader from __getattr__, which is needed
    so that the csv loader is called on import, giving the user the actual loaded data
    and not the data loader itself
    '''
    def __setattr__(self, name, value):
        if name in self.data_loaders:
            return
        super().__setattr__(name, value)


_COMMON_PREFIX = "dataimport."
class DataImportFinder(importlib.abc.MetaPathFinder):

    def __init__(self, loader, *args, **kwargs):
        self._loader = loader
        super().__init__(*args, **kwargs)

    def find_spec(self, fullname, path, target=None):
        # I would normally want to discard the common prefix
        # but that causes the following code from cypthon _find_and_load_unlocked
        # to throw an exception
        #
        # # Crazy side-effects!
        # if name in sys.modules:
        #     return sys.modules[name]
        # parent_module = sys.modules[parent] <- this right here
        # try:
        #     ...
        #
        # By mangling the name, the "parent" name that it would search for would throw a key error
        # So we don't mangle it here, and instead strip it off in the loader
        if fullname.startswith(_COMMON_PREFIX):
            return self._gen_spec(fullname)

    def _gen_spec(self, fullname):
        return importlib.machinery.ModuleSpec(fullname, self._loader)

class DataImportLoader(importlib.abc.Loader):
    def __init__(self, *args, **kwargs):
        self.module = DataLoader(None)
        super().__init__(*args, **kwargs)

    def create_module(self, spec):
        self.module.data = spec.name[len(_COMMON_PREFIX):]
        return self.module

    def exec_module(self, module):
        pass

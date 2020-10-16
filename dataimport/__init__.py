from pathlib import Path
import sys
from dataimport._meta import injector

loader = injector.DataImportLoader()
finder = injector.DataImportFinder(loader)
sys.meta_path.append(finder)

def register(name, data_loader):
    loader.module.register(name, data_loader)

def set_path(path):
    loader.module.prefix = Path(path)

from dataimport._meta import injector
import sys

loader = injector.DataImportLoader()
finder = injector.DataImportFinder(loader)
sys.meta_path.append(finder)

def register(name, data_loader):
    loader.module.register(name, data_loader)

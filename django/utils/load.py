# -*- coding: utf-8 -*-
from django.utils.importlib import import_module
import sys


def load_object(import_path, exception_handler=None):
    """
    Loads an object from an 'import_path', like in MIDDLEWARE_CLASSES and the
    likes.
    
    Import paths should be: "mypackage.mymodule.MyObject". It then imports the
    module up until the last dot and tries to get the attribute after that dot
    from the imported module.
    
    If the import path does not contain any dots, a TypeError is raised.
    
    If the module cannot be imported, an ImportError is raised.
    
    If the attribute does not exist in the module, a AttributeError is raised.
    
    You can provide custom error handling using the optional exception_handler
    argument which gets called with the exception type, the exception value and
    the traceback object if there is an error during loading.
    
    The exception_handler is not called if an invalid import_path (one without
    a dot in it) is provided.
    """
    if '.' not in import_path:
        raise TypeError(
            "'import_path' argument to 'django.utils.load.load_object' must "
            "contain at least one dot."
        )
    module_name, object_name = import_path.rsplit('.', 1)
    try:
        module = import_module(module_name)
    except:
        if callable(exception_handler):
            exctype, excvalue, tb = sys.exc_info()
            return exception_handler(import_path, exctype, excvalue, tb)
        else:
            raise
    try: 
        return getattr(module, object_name)
    except:
        if callable(exception_handler):
            exctype, excvalue, tb = sys.exc_info()
            return exception_handler(import_path, exctype, excvalue, tb)
        else:
            raise

def iterload_objects(import_paths, exception_handler=None):
    """
    Calls django.contrib.load.load_object on all items in the iterable
    import_paths and returns a generator that yields the objects to be loaded.
    
    The exception_handler is propagated to load_object.
    
    If the exception_handler does not return anything or returns None, the
    value is ignored.
    """
    for import_path in import_paths:
        next = load_object(import_path, exception_handler)
        if next:
            yield next

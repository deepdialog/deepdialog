"""Automatic load module."""

# import os
import importlib


EXISTS = {}


def load_ext(name):
    """Load an ext function."""
    global EXISTS
    if name in EXISTS:
        return EXISTS[name]
    # filename = name + '.py'
    # assert os.path.exists(filename)
    m = importlib.import_module(name)
    c = getattr(m, name)
    i = c()
    EXISTS[name] = i
    return EXISTS[name]

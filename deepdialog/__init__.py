# -*- coding: utf-8 -*-
"""DeepDialog, dialogue system build tool with deep learning."""

import os
from .train import main as train
from .serve import main as serve
from .serve import Serve

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
__VERSION__ = open(os.path.join(CURRENT_DIR, 'version.txt')).read()

__all__ = ['train', 'serve', 'Serve']

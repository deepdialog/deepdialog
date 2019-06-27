# -*- coding: utf-8 -*-
"""Train NLG."""

# import os
from ..nlg.nlg import NaturalLanguageGenerator


def train_nlg(data_path):
    """Train NLG."""
    # nlg_path = os.path.join(data_path, 'nlg')
    nlg = NaturalLanguageGenerator()
    nlg.fit(data_path)
    return nlg

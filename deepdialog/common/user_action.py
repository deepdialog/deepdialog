# -*- coding: utf-8 -*-
"""User Action Define.

系统行为模块
NLU模块的输出
"""


class UserAction(object):
    """User Action Define."""

    def __init__(self, utterance):
        """Init an User Action."""
        self.raw = {
            'text': utterance,
            'tokens': list(utterance),
            'intent': None,
            'domain': None,
            'slots': [],
        }

    def __getattr__(self, key):
        """Return certain attribute."""
        if key == 'utterance':
            return self.raw['text']
        if key == 'intent':
            return self.raw['intent']
        if key == 'domain':
            return self.raw['domain']
        if key == 'slots':
            return self.raw['slots']
        raise AttributeError(key)

    def __str__(self):
        """Return stringify."""
        return f'''domain: {self.raw.get('domain', None)}
intent: {self.raw.get('intent', None)}
slots: {self.raw.get('slots', None)}'''

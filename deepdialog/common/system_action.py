# -*- coding: utf-8 -*-
"""System Action Define."""


class SystemAction(object):
    """System Action define."""

    def __init__(self, sys_action):
        """Init system action."""
        self.intent = sys_action

    def __str__(self):
        """Return stringify System Action."""
        return f'{self.intent}'

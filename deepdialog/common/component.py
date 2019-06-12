# -*- coding: utf-8 -*-
"""Bot Component Base."""


class Component(object):
    """Bot Component Base."""

    def __call__(self, *args, **kwargs):
        """Call function."""
        return self.forward(*args, **kwargs)

    def forward(self):
        """Raise error when components not override this function."""
        raise NotImplementedError()

# -*- coding: utf-8 -*-
"""Dialog Policy Learning Module."""

from typing import List
import numpy as np
from .keras_dpl import get_model
from ..common.system_action import SystemAction
from ..common.dialog_state import DialogState
from ..common.component import Component


class DialogPolicyLearning(Component):
    """DialogPolicyLearning Module."""

    def __init__(self):
        """Init DPL variables."""
        self.clf = None

    def forward(self,
                history: List[DialogState]) -> SystemAction:
        """DPL Forward."""
        x = np.array([
            s.vec
            for s in history
        ])  # .flatten()
        pred = self.clf.predict(np.array([x])).flatten()
        pred = pred[0]
        system_action = SystemAction(history[-1].index_sys_intent[pred])
        return system_action

    def fit(self, x, y):
        """Fit the DPL."""
        clf = get_model(int(y.shape[-1]))
        clf.fit(x, y)
        print(f'DPL FIT {clf.score(x, y)}')
        self.clf = clf

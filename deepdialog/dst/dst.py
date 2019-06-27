# -*- coding: utf-8 -*-
"""DST Module."""

from typing import List
import numpy as np
from .keras_dst import get_model
from ..common.dialog_state import DialogState
from ..common.user_action import UserAction
from ..common.build_dialog_train_data import make_new_state
from ..common.component import Component


class DialogStateTracker(Component):
    """DST Module."""

    def __init__(self):
        """Init DST."""
        self.clf = None

    def forward(self,
                init_state: DialogState,
                history: List[DialogState],
                user_action: UserAction) -> DialogState:
        """DST Forward.

        input:
            state: current state
            user_action: action from this turn
        return: new_state DialogState
        """
        state = history[-1].clone()
        new_state = make_new_state(
            init_state.clone(),
            # state,
            user_action.domain,
            user_action.intent,
            user_action.slots,
            user_action.utterance
        )

        if self.clf is not None:
            x = np.array([history[-1].vec] + [new_state.vec])

            # import pdb; pdb.set_trace()

            pred = self.clf.predict_proba(np.array([x])).flatten()
            print('pred', pred)
            for i, slot in enumerate(new_state.slots):
                if pred[i] > 0.5:
                    print(f'change slot {i}')
                    state.slots[i] = slot
            print('new state after fill', str(state))

        state.user_intent = new_state.user_intent
        state.user_domain = new_state.user_domain
        state.utterance = new_state.utterance
        return state

    def fit(self, x, y):
        """Fit DST Model."""
        if y.shape[1] > 0:
            clf = get_model(int(y.shape[-1]))
            clf.fit(x, y)
            print(f'DST FIT {clf.score(x, y)}')
            self.clf = clf

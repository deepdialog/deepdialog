# -*- coding: utf-8 -*-
"""Serve bot."""

# import os
import pickle
from ..common import FAQ_INTENT
from ..common.component import Component


class Serve(Component):
    """Serve bot."""

    def __init__(self, model_path):
        """Load trained modules."""
        data = pickle.load(open(model_path, 'rb'))

        faq = data.get('faq')
        nlg = data.get('nlg')
        nlu = data.get('nlu')
        dst = data.get('dst')
        dpl = data.get('dpl')
        state = data.get('init_state')

        self.state = self.init_state = state
        self.nlu = nlu
        self.dst = dst
        self.dpl = dpl
        self.nlg = nlg
        self.faq = faq
        self.history = [
            state.clone()
            for _ in range(3)
        ]

    def forward(self, utterance):
        """Bot pipeline forward."""
        init_state, nlu, dst, dpl, nlg, faq = (
            self.state,
            self.nlu,
            self.dst,
            self.dpl,
            self.nlg,
            self.faq
        )
        history = self.history
        user_action = nlu(utterance)
        if utterance == 'state':
            return str(history[-2]) + str(history[-1])
        if user_action.intent == FAQ_INTENT:
            sys_response = faq(utterance)
        else:
            new_state = dst(init_state, history, user_action)
            history = history[1:] + [new_state]
            sys_action = dpl(history)
            sys_response = nlg(new_state, sys_action)
            history[-1].sys_intent = sys_action.intent
        self.history = history
        return sys_response

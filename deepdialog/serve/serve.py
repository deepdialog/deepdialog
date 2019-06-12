# -*- coding: utf-8 -*-
"""Serve bot."""

import os
import pickle
from ..common import FAQ_INTENT
from ..common.component import Component


class Serve(Component):
    """Serve bot."""

    def __init__(self, model_path, outside_function={}):
        """Load trained modules."""
        faq_output = os.path.join(model_path, 'faq.model')
        nlu_output = os.path.join(model_path, 'nlu.model')
        nlg_output = os.path.join(model_path, 'nlg.model')
        dst_output = os.path.join(model_path, 'dst.model')
        dpl_output = os.path.join(model_path, 'dpl.model')
        state_path = os.path.join(model_path, 'init_state.model')

        faq = pickle.load(open(faq_output, 'rb'))
        nlu = pickle.load(open(nlu_output, 'rb'))
        nlg = pickle.load(open(nlg_output, 'rb'))
        nlg.outside_function = outside_function
        dst = pickle.load(open(dst_output, 'rb'))
        dpl = pickle.load(open(dpl_output, 'rb'))
        state = pickle.load(open(state_path, 'rb'))

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
